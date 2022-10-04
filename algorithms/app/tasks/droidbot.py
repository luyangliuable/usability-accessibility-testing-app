from resources.resource import *
from threading import Thread
from tasks.task import Task
from typing import List
from time import sleep
import typing as t
import requests
import os
import json

from resources.resource import *

class Droidbot(Task):
    """Class for managing droidbot algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    _output_types = [ResourceType.JSON_LAYOUT, ResourceType.UTG]
    _execute_url = "http://localhost:3008/new_job"
    name = "Droidbot"
    _shared_volume = "/home/tasks"


    def __init__(self, output_dir: str, resource_dict: Dict[ResourceType, ResourceGroup], dependant_algorithms: t.List=[]) -> None:
        """
        Droidbot class manages a single droidbot task. It subscribes to utg and gif resources. Whenever both a new utg and gif are added it starts running.


        Parameters:
            output_dir - (str) The output directory for the gifdroid result
            resource_dict - (str) Dictionary of resource groups required by this algorithm # TODO try combine utg and gif into single resource group

        Returns: Nothing
        """
        super().__init__(output_dir, resource_dict)
        self.emulator = resource_dict[ResourceType.EMULATOR]
        self._sub_to_apks()
        self._sub_to_emulators()
        self.apk_queue = []
        self.images = ()
        self._watcher = Thread(target = self.watch_for_new_files_aux)
        self.dependent_algorithms = []


    def _list_image_files_in_dir(self, check_path: str) -> t.Tuple:
        images = ()
        for file in os.listdir(check_path):
            fullpath=os.path.join(check_path, file)
            if os.path.isfile(fullpath) and self._check_file_is_image(file):
                images += (file,)

        return images


    def _create_new_resource_group(self, resource_wrapper: ResourceWrapper, resource_type: ResourceType) -> bool:

        print(resource_wrapper)
        self.resource_dict[resource_type] = ResourceGroup(resource_type)
        self.resource_dict[ResourceType.SCREENSHOT_JPEG].publish(resource_wrapper, True)

        return True


    def _publish_all_new_images(self, images: t.List[str], check_path: str) -> bool:
        for each_image in images:
            resource_path = os.path.join(check_path, each_image)
            img = ResourceWrapper(resource_path, self.name)
            self._create_new_resource_group(img, ResourceType.SCREENSHOT_JPEG)

        return True


    def _log_new_images(self, new_images) -> None:
        if len(new_images) > 0:
            print(f'{len(new_images)} new images detected {new_images}.')


    def watch_for_new_files_aux(self):
        droidbot_screenshots_folder = 'states'
        check_path = os.path.join(self.output_dir, droidbot_screenshots_folder)

        # TODO remove this line for testing
        check_path = "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/droidbot/states/"

        while(True):
            if self.status != "RUNNING":
                break

            if os.path.exists(check_path):
                new_images = []
                old = self.images
                self.images += self._list_image_files_in_dir(check_path)
                new_images = list( set( self.images ).difference( set( old ) ) )
                self._log_new_images(new_images)
                self._publish_all_new_images(new_images, check_path)

            sleep(3)


    def watch_for_new_files(self):
        # self._watcher = Thread(target = self.watch_for_new_files_aux, args =(lambda : exit_flag, ))
        self._watcher.start()


    def mark_algorithm_completed(self):
        self.status = "DONE"
        self._watcher.join()


    def terminate_watch_for_new_files(self):
        self.watch_for_new_files.terminate()


    def run(self, apk_path: str) -> t.Dict[str, str]:
        """
        Execute gifdroid algorithm by http request and passing in necessary data for gifdroid to figure out stuff.

        Parameters:
            apk_path - (str) The string path for the apk for to run droidbot.
        """
        self.status = "RUNNING"
        self.watch_for_new_files()
        requests.post(str( self._execute_url ), data=json.dumps(self._get_execution_data(apk_path)), headers={"Content-Type": "application/json"})
        self.mark_algorithm_completed()

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

        return data


    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available


    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk not in self.apk_queue:
            self.apk_queue.append(new_apk)


    def emulator_callback(self, emulator : ResourceWrapper) -> None:
        """callback method for using emulator"""
        self._process_apks()
        emulator.release()


    def _process_apks(self) -> None:
        while len(self.apk_queue) > 0:                                      # get next apk
            apk = self.apk_queue.pop(0)
            apk_path = apk.get_path()
            self.run(apk_path)
            apk.release()


    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            self.resource_dict[ResourceType.EMULATOR].subscribe(self.emulator_callback)


    def _check_file_is_image(self, file: str) -> bool:
        file_type = file[len(file)-3:len(file)]
        if file_type == "png" or file_type == "jpg":
            return True

        return False


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


