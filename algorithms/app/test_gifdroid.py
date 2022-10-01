from resources.resource import *
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
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    def run(self):
        resource_dict = {} # make resource dict
        resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
        resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)


        tasks = ["Droidbot"]

        base_dir = "/home/data/droidbot_result"

        execution_data={}
        TaskFactory.create_tasks(tasks, base_dir, resource_dict)


        apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
        emulator = ResourceWrapper('', 'host.docker.internal:5555')

        resource_dict[ResourceType.APK_FILE].publish(apk, True)
        resource_dict[ResourceType.EMULATOR].publish(emulator, True)

        print(f'Finished running {self.thread_name}.')


class gifdroid(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    def run(self):
        resource_dict = {} # make resource dict
        resource_dict[ResourceType.UTG] = ResourceGroup(ResourceType.UTG)
        resource_dict[ResourceType.GIF] = ResourceGroup(ResourceType.GIF)
        tasks = ["Gifdroid"]

        base_dir = "/home/data/"

        execution_data={}
        TaskFactory.create_tasks(tasks, base_dir, resource_dict)

        utg = ResourceWrapper('/home/data/droidbot_result/', 'droidbot result')
        gif = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/sample.gif', '')

        resource_dict[ResourceType.UTG].publish(utg, True)
        resource_dict[ResourceType.GIF].publish(gif, True)

        print(f'Finished running {self.thread_name}.')

if __name__ == '__main__':
    # first_droidbot = droidbot("test1", 1)
    # second_droidbot = thread("test2", 2)
    # third_droidbot = thread("test3", 3)
    # first_droidbot.start()
    # second_droidbot.start()
    # third_droidbot.start()

    first_gifdroid = gifdroid("test1", 1)
    second_gifdroid = gifdroid("test2", 2)
    first_gifdroid.start()
    # second_gifdroid.start()
