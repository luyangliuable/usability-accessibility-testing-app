from resources.resource import *
from tasks.task import *
from tasks.xbot import *
from tasks.owleye import *
from tasks.tappability import *
from models.emulator import *


def test():
    # make resource groups
    resource_dict = {} # make resource dict
    resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
    resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)
    resource_dict[ResourceType.ACCESSIBILITY_ISSUE] = ResourceGroup(ResourceType.ACCESSIBILITY_ISSUE)


    tasks = ["Xbot"]

    base_dir = "/home/data/test/a2dp.Vol_133/xbot/"

    TaskFactory.create_tasks(tasks, base_dir, resource_dict, None)

    emulator = Emulator("emulator-5556", "host.docker.internal:5557", (1920, 1080))
    emulator_rw = ResourceWrapper('', '', metadata=emulator)
    apk_rw = ResourceWrapper('/home/data/test/a2dp.Vol_133/a2dp.Vol_133.apk', 'upload')

    # resource_dict[ResourceType.APK_FILE].publish(apk, True)
    resource_dict[ResourceType.APK_FILE].publish(apk_rw, True)
    resource_dict[ResourceType.EMULATOR].publish(emulator_rw, True)

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
    # xbot = Xbot("/home/data/test_apks/a2dp.Vol_133/xbot/", resource_dict, None)
    # tap = Tappability("/home/data/test_apks/a2dp.Vol_133/tappability/", resource_dict, None)
    xbot = Xbot("/home/data/test_apks/a2dp.Vol_133/xbot/", resource_dict, None)
    tap = Tappability("/home/data/test_apks/a2dp.Vol_133/tappability/", resource_dict, None)
    
    # publish xbot outputs
    xbot._publish_outputs()
    
    # print resource groups
    for r_group in resource_dict.values():
        print('\n' + str(r_group._type))
        for rsrc in r_group._resources:
            print(rsrc.get_metadata())

def test_tappability_results():
    """Tests if tapability is producing correct result resource format"""
    tap = Tappability("/home/data/test/a2dp.Vol_133/tappability/", {}, None)
    screenshot = Screenshot(
        ui_screen='a2dp.Vol.main', 
        image_path='/home/data/test/a2dp.Vol_133/xbot/screenshot/a2dp.Vol.main/a2dp.Vol.main.png', 
        layout_path='/home/data/test/a2dp.Vol_133/xbot/layouts/a2dp.Vol.main.xml'
        )
    print(tap._get_results([screenshot]))
    
if __name__ == '__main__':
    test_tappability()
    
