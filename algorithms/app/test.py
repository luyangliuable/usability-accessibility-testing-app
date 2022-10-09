from resources.resource import *
from tasks.task import *
from tasks.xbot import *
from tasks.owleye import *
from tasks.tappability import *
# from tasks.droidbot import *
# from tasks.gifdroid import *
# from tasks.image_converter import *
# from tasks.layout_converter import *
# from tasks.storydistiller import *
# from tasks.unique_screenshots import *

def test_xbot():
    # make resource groups
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
    resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)


    tasks = ["Xbot"]

    base_dir = "/home/data/test_apks/a2dp.Vol_133/xbot/"

    execution_data={}
    TaskFactory.create_tasks(tasks, base_dir, resource_dict)


    apk = ResourceWrapper('/home/data/test_apks/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')
    emulator = ResourceWrapper('', 'host.docker.internal:5555')

    # resource_dict[ResourceType.APK_FILE].publish(apk, True)
    resource_dict[ResourceType.EMULATOR].publish(emulator, True)

def test_xbot_outputs():
    """Test Xbot generates correct outputs before publishing"""
    xbot = Xbot("/home/data/test_apks/a2dp.Vol_133/xbot/", {}, None)
    
    print(xbot._get_screenshots())            # screenshot xbot publishes
    print(xbot._get_accessibility_issues())   # accessibility issues xbot publishes

def test_owleye():
    """Tests complete Owleye functionality using Xbot to publish screenshots.
    \n Requires Owleye algorithm container to be running
    """
    # resources to be used in test
    resource_types = [ResourceType.SCREENSHOT, ResourceType.ACCESSIBILITY_ISSUE, ResourceType.DISPLAY_ISSUE]
    resource_dict = {resource_type:ResourceGroup(resource_type) for resource_type in resource_types}
    
    # algorithms
    xbot = Xbot("/home/data/test_apks/a2dp.Vol_133/xbot/", resource_dict, None)
    owleye = Owleye("/home/data/test_apks/a2dp.Vol_133/owleye/", resource_dict, None)
    
    # publish xbot outputs
    xbot._publish_outputs()
    
    # print resource groups
    for r_group in resource_dict.values():
        print('\n' + str(r_group._type))
        for rsrc in r_group._resources:
            print(rsrc.get_metadata())

def test_tappability():
    """Tests complete Tappability functionality using Xbot to publish screenshots.
    \n Requires Tappability algorithm container to be running
    """
    # resources to be used in test
    resource_types = [ResourceType.SCREENSHOT, ResourceType.ACCESSIBILITY_ISSUE, ResourceType.TAPPABILITY_PREDICTION]
    resource_dict = {resource_type:ResourceGroup(resource_type) for resource_type in resource_types}
    
    # algorithms
    xbot = Xbot("/home/data/test_apks/a2dp.Vol_133/xbot/", resource_dict, None)
    tap = Tappability("/home/data/test_apks/a2dp.Vol_133/tappability/", resource_dict, None)
    
    # publish xbot outputs
    xbot._publish_outputs()
    
    # print resource groups
    for r_group in resource_dict.values():
        print('\n' + str(r_group._type))
        for rsrc in r_group._resources:
            print(rsrc.get_metadata())
    
if __name__ == '__main__':
    test_tappability()
    
