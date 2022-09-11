from algorithm_controllers import *
import os


class ApkDetails:
    
    def __init__(self, apk_path, output_dir) -> None:
        self.apk_path = apk_path
        self.output_dir = output_dir
    
    def _init_output_dir(self) -> None:
        """Initialises ouput directory and creates temp directory for processing"""
        # TODO create output dir if it doesn't exist and create temp directory
        pass
    
    def execute_task(Self, task: Task) -> None:
        """Executes task"""
        pass
    
    def get_screenshots(self) -> str:
        # TODO run xbot and droidbot and copy screenshots into activity folders
        pass
    
    def get_accessibility_issues(self) -> str:
        # TODO 
        # run xbot and droidbot if not already run
        # copy screenshots into temp folder convert PNGs to JPEG
        # run owleye
        # copy results into activity folders
        pass
    
    def get_display_issues(self) -> str:
        # TODO 
        # run xbot and droidbot if not already run
        # copy screenshots into temp folder convert PNGs to JPEG
        # run owleye
        # copy results into activity folders
        pass
    
    def get_tappability_predictions(self) -> str:
        # TODO 
        # run xbot and droidbot if not already run
        # copy screenshots into temp folder convert PNGs to JPEG
        # get annotations
        # run tappability
        # copy results into activity folders
        pass
    
    def get_execution_trace(self) -> str:
        # TODO 
        # run droidbot
        # copy utg into gifdroid input folder
        # run gifdroid
        pass
   

if __name__=='__main__':
    pass