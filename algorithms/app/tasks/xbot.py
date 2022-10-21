from models.screenshot import Screenshot
from models.emulator import Emulator
from tasks.task import *
from resources.resource import *
from typing import List, Dict, Tuple
import os


class Xbot(Task):
    """Class for managing Xbot algorithm"""

    _input_types = [ResourceType.APK_FILE, ResourceType.EMULATOR]
    # _output_types = [ResourceType.ACCESSIBILITY_ISSUE]
    _output_types = [ResourceType.SCREENSHOT, ResourceType.ACCESSIBILITY_ISSUE]
    _url = 'http://host.docker.internal:3003/execute'

    def __init__(self, output_dir, resource_dict : Dict[ResourceType, ResourceGroup], uuid: str) -> None:
        super().__init__(output_dir, resource_dict, uuid)
        self.apk_queue = []
        self._sub_to_apks()
        self.running = False

    @classmethod
    def get_name(cls) -> str:
        """Name of the task"""
        return Xbot.__name__

    @classmethod
    def get_input_types(cls) -> List[ResourceType]:
        """Input resource types of the task"""
        return Xbot._input_types

    @classmethod
    def get_output_types(cls) -> List[ResourceType]:
        """Output resource types of the task"""
        return Xbot._output_types


    @classmethod
    def start(cls, apk_path: str, output_dir: str, emulator: str):
        """
        Signal start thread to the xbot.
        """

        # TODO may not work
        task = Thread(target=cls.run, args=(apk_path, output_dir, emulator));
        task.start()

    @classmethod
    def run(cls, apk_path: str, output_dir: str, emulator: str) -> None:
        """Runs Xbot"""
        data = {
            "apk_path": apk_path,
            "output_dir": output_dir,
            "emulator": emulator
        }

        Xbot.http_request(Xbot._url, data)


    def _sub_to_apks(self) -> None:
        """Get notified when a new APK is available"""
        if ResourceType.APK_FILE in self.resource_dict:
            self.resource_dict[ResourceType.APK_FILE].subscribe(self.apk_callback) # calls add_apk() when new apk is available


    def _sub_to_emulators(self) -> None:
        """Get notified when an emulator is available"""
        if ResourceType.EMULATOR in self.resource_dict:
            self.resource_dict[ResourceType.EMULATOR].subscribe(self.emulator_callback)


    def _process_apks(self, emulator: Emulator) -> None:
        """Process apks"""
        if self.running:
            return
        
        self.running = True
        print("XBOT RUNNING, EMULATOR= " + str(emulator))
        

        if len(self.apk_queue) > 0:                              # get next apk
            apk = self.apk_queue.pop(0)

            apk_path = apk.get_path()
            Xbot.run(apk_path, self.output_dir, emulator.connection_str)      # run algorithm
            self._publish_outputs()                                # dispatch results

        print("XBOT COMPLETED")
        self.running = False


    def apk_callback(self, new_apk : ResourceWrapper) -> None:
        """callback method to add apk and run algorithm"""
        if new_apk not in self.apk_queue:
            self.apk_queue.append(new_apk)
            self._sub_to_emulators()


    def emulator_callback(self, emulator : ResourceWrapper) -> None:
        """callback method for using emulator"""
        device: Emulator = emulator.get_metadata()
        if device.can_use('Xbot') and len(self.apk_queue) > 0:
            self._process_apks(emulator.get_metadata())
        emulator.release()


    def is_complete(self) -> bool:
        if len(self.apk_queue) > 0:
            return False

        return not self.resource_dict[ResourceType.APK_FILE].is_active()


    def _publish_outputs(self) -> None:
        """Dispatch all outputs for processed apk"""
        screenshots = self._get_screenshots()
        issues = self._get_accessibility_issues()

        complete = False
        for screenshot in screenshots:
            if screenshot == screenshots[-1]:
                complete = self.is_complete()
            rw = ResourceWrapper(None, 'Xbot', screenshot)
            self.resource_dict[ResourceType.SCREENSHOT].publish(rw, complete)

        if not ResourceType.ACCESSIBILITY_ISSUE in self.resource_dict:
            return

        complete = False
        for issue in issues:
            if issue == issues[-1]:
                complete = self.is_complete()
            rw = ResourceWrapper(None, 'Xbot', issue)
            self.resource_dict[ResourceType.ACCESSIBILITY_ISSUE].publish(rw, complete)



    def _get_accessibility_issues(self) -> List[dict]:
        """ Gets list of accessibility issues from xbot output directory.
            Returns list containing {original screenshot, image path, description path}
        """
        screenshots = self._get_screenshots()
        issues = []
        issues_dir = os.path.join(self.output_dir, "issues")

        # folder name = activity name
        for screenshot in screenshots:
            activity = screenshot.ui_screen
            image_path = os.path.join(issues_dir, activity, activity + ".png")
            desc_path = os.path.join(issues_dir, activity, activity + ".txt")
            issue_list = self._get_issue_list(desc_path)
            # if no issues found, create empty issue
            if issue_list is None:
                image_path = screenshot.image_path
                os.makedirs(os.path.dirname(desc_path))
                issue_list = [{
                    'issue_type': " ",
                    'component_type': "No accessibility issues were suggested.",
                    'issue_desc': " "
                }]
                with open(desc_path, 'w') as desc_file:
                    desc_file.writelines(issue_list[0].values())
                    
            issues.append({
                "activity_name": screenshot.ui_screen,      # activity name 
                "screenshot_id": screenshot.screenshot_id,  
                "state_id": screenshot.state_id,
                "structure_id": screenshot.structure_id,    
                "image": image_path,                        # annotated screenshot file
                "description": issue_list                   # list of issues from text file
                })
        return issues
    
    def _get_issue_list(self, desc_path: str) -> list[str]:
        """Reads issue text file and produces list of issues"""
        issue_list = []
        if not os.path.exists(desc_path):
            return None  
        with open(desc_path) as f:
            desc = f.read()
        # list of each issue description
        desc = desc.split('\n\n')
        for i in range(1, len(desc)):
            issue = desc[i].split('\n')
            if len(issue) != 3:
                continue
            element = issue[1]
            if element[0] == '[':
                element = f'Element at bounds {issue[1]}'
            issue_list.append({
                "issue_type": issue[0],
                "component_type": element,
                "issue_desc": issue[2]
                    })
        return issue_list

    def _get_screenshots(self) -> List[Screenshot]:
        """ Gets list of screenshot images and layouts from xbot output directory.
            Returns list of tuples containing (activity name, image path, layout path)
        """
        screenshots = []
        images_dir = os.path.join(self.output_dir, "screenshot")
        layouts_dir = os.path.join(self.output_dir, "layouts")

        if not (os.path.exists(images_dir) or os.path.exists(layouts_dir)):
            return screenshots

        for activity in os.listdir(images_dir):
            layout_path = os.path.join(layouts_dir, activity + ".xml")
            # select image file which is not the thumbnail
            for filename in os.listdir(os.path.join(images_dir, activity)):
                if len(filename) > 14 and filename[-14:-5] != "_thumbnail":
                    image_path = os.path.join(images_dir, activity, activity+'.png')
                    os.rename(os.path.join(images_dir, activity, filename), image_path) # rename screenshot to same name as layout file
                    screenshots.append(Screenshot(activity, image_path, layout_path))
                    break
        return screenshots
