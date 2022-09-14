from resources.resource import *
from tasks.storydistiller import *
from tasks.xbot import *

from resources.emulator import *


if __name__ == '__main__':
    #TODO
    # create apk resource
    # create emulator resource
    # create storydistiller object
    # add apk
    
    
    # make resource groups
    apk_resources = ResourceGroup(ResourceType.APK_FILE)
    emulator_resources = ResourceGroup[Emulator](ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = apk_resources
    resource_dict[ResourceType.EMULATOR] = emulator_resources

    storydistiller = Storydistiller('/home/data/test_apks/a2dp.Vol_133/storydistiller/', resource_dict)
    xbot = Xbot('/home/data/test_apks/a2dp.Vol_133/xbot/', resource_dict)
    
    apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
    emulator = ResourceWrapper('', 'upload', Emulator('host.docker.internal:5555'))
    
    apk_resources.publish(apk, True)
    emulator_resources.publish(emulator, True)