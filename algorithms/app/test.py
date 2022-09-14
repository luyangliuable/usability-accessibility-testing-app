from resources.resource import *
from tasks.storydistiller import *
from tasks.xbot import *



if __name__ == '__main__':
    
    # make resource groups
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
    resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)


    storydistiller = Storydistiller('/home/data/test_apks/a2dp.Vol_133/storydistiller/', resource_dict)
    xbot = Xbot('/home/data/test_apks/a2dp.Vol_133/xbot/', resource_dict)
    

    
    apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
    emulator = ResourceWrapper('', 'host.docker.internal:5555')

    
    resource_dict[ResourceType.APK_FILE].publish(apk, True)
    resource_dict[ResourceType.EMULATOR].publish(emulator, True)