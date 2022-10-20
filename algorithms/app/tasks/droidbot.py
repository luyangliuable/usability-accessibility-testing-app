from tasks.concurrency.file_watcher import FileWatcher
from tasks.enums.status_enum import StatusEnum
from resources.resource import *
from threading import Thread
from tasks.task import Task
from typing import List
from time import sleep
import typing as t
import requests
import logging
import os
import json
from models.screenshot import Screenshot


class Droidbot(Task, Thread):
    """Class for managing droidbot algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.UTG, ResourceType.SCREENSHOT]
    # _output_types = [ResourceType.UTG]
    _execute_url = os.environ['DROIDBOT']
    name = "Droidbot"

    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        """
        Droidbot class manages a single droidbot task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.


        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (dict) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group
            apk_queue - (list) List of apks yet to be processed, which have been published to resource group
            _screenshot_dict - (list) List of states in output_dir which have not been published

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict, uuid)
        self._sub_to_apks()
        self._sub_to_emulators()
        self._apk_queue = []
        self._states = []    # unpublished states
        self.check_new_state_directory = os.path.join(output_dir, 'states')
        self.resource_type = ResourceType.SCREENSHOT
        self._image_file_watcher = FileWatcher(uuid, 'json', self.check_new_state_directory, self, self._publish_all_new_files)


    def _publish_all_new_files(self, files: t.List[str]) -> None:
        """ Publish new detected/created files from the path being checked.

        Parameters:
            files - (List[str]) List of files newly detected or generated.
        """
        for each_state in files:
            print("New file in Droidbot detected " + str(each_state))
            self._states.append(each_state)
            # resource_path = os.path.join(check_path, each_image)
            # self._create_new_resource_group()
            # # json_path = self.get_json(resource_path)

            # # with open(json_path) as f:
            # #     data = json.loads(f.read())
            # #     ui_screen = data['foreground_activity']
            # # screenshot = Screenshot(ui_screen, resource_path, json_path)
            # img = ResourceWrapper(resource_path, origin)
            # complete = self.status != StatusEnum.running
            # self.resource_dict[self.resource_type].publish(img, complete)
        
        self._publish_new_screenshots() # publish screenshots
        self._publish_utg()             # publish events
        
    
    def _publish_new_screenshots(self) -> None:
        """Publishes new screenshots from states folder if the image and json files both exist"""
        published_items = []
        for state_file in self._states:
            file_key = state_file.removeprefix('state_').removesuffix('.json')  # common key in jpeg and json
            json_path = os.path.join(self.check_new_state_directory, state_file)
            
            # check both png and jpeg 
            img_path = os.path.join(self.check_new_state_directory, f'screen_{file_key}.jpg')
            if not os.path.exists(img_path):
                img_path = os.path.join(self.check_new_state_directory, f'screen_{file_key}.png')
            
            # don't publish if image file not available
            if not os.path.exists(img_path):
                continue
            
            with open(json_path) as f:
                data = json.loads(f.read())
            ui_screen = data['foreground_activity']
            screenshot = Screenshot(ui_screen, img_path, json_path)
            published_items.append(state_file)
            
            is_complete = self.status not in [StatusEnum.running, StatusEnum.none]
            rw = ResourceWrapper('', 'Droidbot', screenshot)
            if ResourceType.SCREENSHOT in self.resource_dict:
                self.resource_dict[ResourceType.SCREENSHOT].publish(rw, is_complete)
        
        # removed published states from states list
        for item in published_items:
            self._states.remove(item)
    
    def _publish_utg(self) -> None:
        utg_path = os.path.join(self.output_dir, 'utg.js')
        if not os.path.exists(utg_path):
            return
        
        with open(utg_path) as utg_file:
            new_utg = json.loads(utg_file.read().removeprefix('var utg = \n'))

        for node in new_utg['nodes']:
            if 'image' in node:
                node['image'] = os.path.join(self.output_dir, node['image'])
        
        for edge in new_utg['edges']:
            if 'events' in edge:
                for event in edge['events']:
                    if 'view_images' in event:
                        for i in range(len(event['view_images'])):
                            event['view_images'][i] = os.path.join(self.output_dir, event['view_images'][i])
        
        complete = self.status not in [StatusEnum.running, StatusEnum.none]
        rw = ResourceWrapper(utg_path, 'Droidbot', new_utg)
        self.resource_dict[ResourceType.UTG].publish(rw, complete)

    def _create_new_resource_group(self) -> bool:
        """
        If the resource group is not yet inside, created it.

        Parameters:
            resource_wrapper - (ResourceWrapper) The wrapper for the new file detected by this watcher.

        Returns: (bool) If the method was successful
        """
        if self.resource_type not in self.resource_dict:
            self.resource_dict[self.resource_type] = ResourceGroup(self.resource_type)

        return True


    def _check_input_resources_available(self) -> bool:
        """
        Check if all resources are avalaible ( apk and emulator ).
        TODO maybe combine both into one resource group?

        Returns: (Boolean) Whether or not the resources are avalaible.
        """
        flag = True

        for resource in self._input_types:
            if not self.resource_dict[resource].is_active:
                flag = False
                break

        return flag


    def update_algorithm_status(self, status: StatusEnum):
        if not self.uuid:
            return
        
        self.status = status

        data = {
            "status": self.status,
            "logs": f'{ self.name } is {self.status.value.lower()}.'
        }

        algorithm_name = self.name[0].lower() + self.name[1:]
        url = os.path.join(self._status_controller, self.uuid, algorithm_name)
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
        print(f'Updated {algorithm_name} status on url {url} to {self.status}. {response}.')


    # def _publish_utg(self) -> bool:
    #     utg = ResourceWrapper(self.output_dir, self.name)
    #     self.resource_dict[ResourceType.UTG].publish(utg, True)

    #     print(f'Published { utg } at {self.output_dir}.')
    #     return True

    def start(self):
        """
        Signal start thread to the droidbot.
        """
        self._thread.start()


    def run(self, apk_path: str) -> t.Dict[str, str]:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.

        Parameters:
            apk_path - (str) The string path for the apk for to run droidbot.

        # TODO make this a staticmethod
        """
        self.update_algorithm_status(StatusEnum.running)
        self._image_file_watcher.start()
        print(self._execute_url)
        response = requests.post(str( self._execute_url ), data=json.dumps(self._get_execution_data(apk_path)), headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            self.update_algorithm_status(StatusEnum.successful)
        else:
            self.update_algorithm_status(StatusEnum.failed)

        self._image_file_watcher.join()
        self._publish_utg()

        return { "message": "Execute started." }


    def _get_execution_data(self, apk_path: str):

        """
        Get the execution data necessary to execute droidbot

        Parameters:
            apk_path - (str) The string path for the apk for to run droibot.
        """
        data = {
            "apk_path": apk_path,
            "output_dir": self.output_dir,
        }
        print(data)

        return data


    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available


    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk not in self._apk_queue:
            self._apk_queue.append(new_apk)


    def emulator_callback(self, emulator : ResourceWrapper) -> None:
        """callback method for using emulator"""
        self._process_apks()
        emulator.release()


    def _process_apks(self) -> None:
        while len(self._apk_queue) > 0:
            apk = self._apk_queue.pop(0)
            apk_path = apk.get_path()
            self.run(apk_path)
            apk.release()


    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            self.resource_dict[ResourceType.EMULATOR].subscribe(self.emulator_callback)


    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return cls.name


    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return cls._input_types


    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return cls._output_types
