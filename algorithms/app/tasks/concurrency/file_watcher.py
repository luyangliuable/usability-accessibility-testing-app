from tasks.enums.status_enum import StatusEnum
from resources.resource import *
from threading import Thread
from time import sleep
from tasks.task import Task
import typing as t
import requests
import os
import json
from models.screenshot import Screenshot

class FileWatcher():
    """
    This class is responsible for checking an **output directory** every 3 seconds for new file of **file_type**
    """

    _status_controller = os.environ['STATUS_CONTROLLER']

    def __init__(self, uuid: str, file_type: str, output_directory: str, task: Task, callback: t.Callable) -> None:
        """
        This class is responsible for checking an **output directory** every 3 seconds for new file of **file_type**.

        It then publishes the new files as new **resource_type**.

        It will continue until **task** status is no long RUNNING.

        Parameters:
            uuid - (str) The job uuid.
            file_type - ( str ) The suffix of the file (e.g. jpg, png, dl and apk)
            output_directory - (str) The path to check for new files every 3 seconds
            resource_type - (ResourceType) The type of resource the file corresponds to
            task - (Task) The parent task that uses this.
            callback - (Callable) After file watcher detects a new file, callback will be called.
        """
        self.source_task = task
        self.callback = callback
        self.algorithm_name = self._lower_first_char_of_str(task.get_name())
        self._thread = Thread(target = self.watch_for_new_files)
        self.task_output_directory = output_directory
        self.uuid = uuid
        self.file_type = file_type
        self.files = ()


    def start(self):
        """
        Signal start to the file watcher.

        Checking an **output directory** every 3 seconds for new file of **file_type**.
        """
        self._thread.start()


    def _log_new_files(self, new_files) -> None:
        """
        Log the new files onto **mongodb** as status to display to **front-end** and inside the **console** as well.
        """
        if len(new_files) > 0:

            update_status_url = os.path.join(self._status_controller, self.uuid, self.algorithm_name)

            for file in new_files:
                logs = f'{self.algorithm_name}: New file {file} generated.'
                data = {
                    "logs": logs
                }
                requests.post(update_status_url, headers={"Content-Type": "application/json"}, json=data)


    def _lower_first_char_of_str(self, string: str):
        """
        Utility reasons lower the first character of string for the task name.
        """
        return string[0].lower() + string[1:]


    def watch_for_new_files(self):
        """
        Every 3 seconds check for new files then it log and publishes those files
        """
        check_path = self.task_output_directory

        while(True):
            if self.source_task.get_status() != StatusEnum.running:
                print("Exiting file watcher.")
                break

            if os.path.exists(check_path):
                new_files = []
                old = self.files
                self.files += self._list_image_files_in_dir(check_path)
                new_files = list( set( self.files ).difference( set( old ) ) )
                self._log_new_files(new_files)

                ###############################################################################
                #                      Callback if a new file is detected                     #
                ###############################################################################
                self.callback(new_files)
            else:
                print(f'{check_path} does not exist yet.')

            sleep(5)


    def _callback_on_new_files(self, new_files: t.List[str]) -> bool:
        """
        Calls a callback function determined by the task classes after a new file is detected.

        new_files - (List) List of new files.
        """
        for each_file in new_files:
            """
            For each new file call the callback function
            """
            self.callback(each_file)

        return True

    # def _publish_all_new_files(self, files: t.List[str], check_path: str, origin: str) -> bool:
    #     """
    #     Publish new detected/created files from the path being checked.

    #     Parameters:
    #         files - (List[str]) List of files newly detected or generated.
    #         check - (str) The path these files are detected from
    #         origin - (str) The task origin.
    #     """
    #     for each_image in files:
    #         resource_path = os.path.join(check_path, each_image)
    #         self._create_new_resource_group()
    #         # json_path = self.get_json(resource_path)

    #         # with open(json_path) as f:
    #         #     data = json.loads(f.read())
    #         #     ui_screen = data['foreground_activity']
    #         # screenshot = Screenshot(ui_screen, resource_path, json_path)
    #         img = ResourceWrapper(resource_path, origin)
    #         complete = self.task.status != StatusEnum.running
    #         self.task.resource_dict[self.resource_type].publish(img, complete)

    #     return True


    def _create_new_resource_group(self) -> bool:
        """
        If the resource group is not yet inside, created it.

        Parameters:
            resource_wrapper - (ResourceWrapper) The wrapper for the new file detected by this watcher.

        Returns: (bool) If the method was successful
        """
        if self.resource_type not in self.source_task.resource_dict:
            self.source_task.resource_dict[self.resource_type] = ResourceGroup(self.resource_type)

        return True


    def _list_image_files_in_dir(self, check_path: str) -> t.Tuple:
        """
        Show all current files in directory

        Parameters:
            check_path - (str) The path to check from

        Returns: (Tuple) Set of all files
        """
        files = ()
        for file in os.listdir(check_path):
            fullpath=os.path.join(check_path, file)
            if os.path.isfile(fullpath) and self._check_file_is_correct_type(file, self.file_type):
                files += (file,)

        return files


    # def get_json(self, path: str) -> str:
    #     return 'states'+path.removeprefix('screen')[-4:]+'json'


    def join(self):
        self._thread.join()


    def _check_file_is_correct_type(self, file: str, type: str) -> bool:
        type_length = len(type)
        file_type = file[len(file)-type_length:len(file)]
        if file_type == type:
            return True

        return False
