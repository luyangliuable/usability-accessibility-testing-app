from resources.resource import *
import typing as t

from tasks.task import *
from tasks.droidbot import *
from tasks.gifdroid import *
from tasks.image_converter import *
from tasks.layout_converter import *
from tasks.owleye import *
from tasks.storydistiller import *
from tasks.tappability import *
from tasks.unique_screenshots import *
from tasks.xbot import *

import threading



class droidbot(threading.Thread):
    def __init__(self, resource_dict: t.Dict[ResourceType, ResourceGroup], thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.resource_dict = resource_dict

    def run(self):
        # resource_dict = {} # make resource dict
        # resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
        # resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)


        tasks = ["Droidbot"]

        base_dir = "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/"

        execution_data={}
        TaskFactory.create_tasks(tasks, base_dir, self.resource_dict, "213123123")


        apk = ResourceWrapper('/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/f5fe1d2c-865d-4bf7-a8f6-caf5458c83ca/a2dp.Vol_133.apk', 'upload')
        emulator = ResourceWrapper('', 'host.docker.internal:5555')

        self.resource_dict[ResourceType.APK_FILE].publish(apk, True)
        self.resource_dict[ResourceType.EMULATOR].publish(emulator, True)

        print(f'Finished running {self.thread_name}.')


    def get_resource_dict(self):
        return self.resource_dict


class gifdroid(threading.Thread):
    def __init__(self, resource_dict: t.Dict[ResourceType, ResourceGroup], thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.resource_dict = resource_dict

    def run(self):
        tasks = ["Gifdroid"]

        base_dir = "/home/data/"

        execution_data={}
        TaskFactory.create_tasks(tasks, base_dir, resource_dict, "asdasdasd")

        utg = ResourceWrapper('/home/data/droidbot', 'droidbot result')
        gif = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/sample.gif', '')

        # resource_dict[ResourceType.UTG].publish(utg, True)
        resource_dict[ResourceType.GIF].publish(gif, True)

        print(f'Finished running {self.thread_name}.')

if __name__ == '__main__':
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
    resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)
    resource_dict[ResourceType.GIF] = ResourceGroup(ResourceType.GIF)
    resource_dict[ResourceType.UTG] = ResourceGroup(ResourceType.UTG)

    first_droidbot = droidbot(resource_dict, "test1", 1)
    first_gifdroid = gifdroid(resource_dict, "test1", 1) # second_gifdroid = gifdroid("test2", 2)
    first_droidbot.start()
    # first_gifdroid.start()
    # print(first_droidbot.get_resource_dict())
    # second_droidbot = thread("test2", 2)
    # third_droidbot = thread("test3", 3)
    # first_droidbot.start()
    # second_droidbot.start()
    # third_droidbot.start()

    # first_gifdroid = gifdroid("test1", 1) # second_gifdroid = gifdroid("test2", 2)
    # second_gifdroid.start()

    # a = Droidbot("/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/droidbot_result", resource_dict)
    # a.get_new_files()
    # a.watch_for_new_files()
