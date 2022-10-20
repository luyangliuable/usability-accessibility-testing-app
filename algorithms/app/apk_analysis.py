from importlib import resources
from resources.resource import *
from resources.resource_types import ResourceType
from models.emulator import Emulator
from models.screenshot import Screenshot
from typing import Dict, List
import os
from tasks.task import *
from tasks.xbot import *
from tasks.owleye import *
from tasks.tappability import Tappability
from tasks.droidbot import *
from tasks.gifdroid import *
import re

EMULATOR = Emulator("emulator-5558", "host.docker.internal:5559", (1920, 1080))

DIFF_NAMES = {'Tappability': 'Tappable', 'UiChecker': 'Venus'}

for name in DIFF_NAMES:
    if name in TaskFactory._tasks:
        TaskFactory._tasks[DIFF_NAMES[name]] = TaskFactory._tasks[name]
        del TaskFactory._tasks[name]

class ApkAnalysis:
    """This class runs all algorithms and generates the combined results"""
    _result_types = {
        'Xbot': ResourceType.ACCESSIBILITY_ISSUE,
        'Owleye': ResourceType.DISPLAY_ISSUE,
        'Tappable': ResourceType.TAPPABILITY_PREDICTION,
        'Tappability': ResourceType.TAPPABILITY_PREDICTION
    }

    def __init__(self, output_dir: str, apk_path: str, req_tasks: list[str], additional_files: Dict[str, Dict[str, str]]={}) -> None:
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.apk_resource = ResourceWrapper(apk_path, 'upload')
        self.upload_additional_files = additional_files
        self.req_tasks = req_tasks
        self.resources = {}
        self._init_resource_groups()
        self._init_results()
        print(f'New APK Analysis.\nAPK file is {apk_path} \Req Results are {self.req_tasks}')


    def _init_resource_groups(self) -> None:
        # create apk, screenshot and emulator resources for every instance
        self.resources[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
        self.resources[ResourceType.SCREENSHOT] = ResourceGroup(ResourceType.SCREENSHOT)
        self.resources[ResourceType.UTG] = ResourceGroup(ResourceType.UTG)
        self.resources[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL) #TODO: implement singleton for emulator

        for name in self.req_tasks:
            for resource_type in TaskFactory._tasks[name].get_output_types():
                if resource_type not in self.resources:
                    self.resources[resource_type] = ResourceGroup(resource_type)

        # create optional resources
        for algorithm, algorithm_additional_files in self.upload_additional_files.items():
            for resource_type_name, _ in algorithm_additional_files.items():
                resource_type = ResourceType[resource_type_name.upper()]
                if resource_type not in self.resources:
                    self.resources[resource_type] = ResourceGroup(resource_type)
                print(f'Initialised resource type {resource_type} for {algorithm}.')
        print(f"Initialised resource groups: {self.resources.keys()}")
    
    
    def _init_results(self) -> None:
        """Subscribe to results resource events."""
        # sub to utg
        self.utg = {'nodes': [], 'edges': []}
        self.utg_nodes = set()
        self.utg_edges = set()
        self.resources[ResourceType.UTG].subscribe(self._new_utg_callback)
        
        # sub to results
        self.results = {}
        for task in self.req_tasks:
            self.results[task] = []
            if task in ApkAnalysis._result_types:
                self.resources[ApkAnalysis._result_types[task]].subscribe(self._new_result_callback)


    def _new_utg_callback(self, resource: ResourceWrapper) -> None:
        new_utg = resource.get_metadata()
        self._update_utg(new_utg)
        print("Updated UTG in APK Analysis")
    
    
    def _new_result_callback(self, resource: ResourceWrapper) -> None:
        origin = resource.get_origin()
        result = self._repl_filepaths(resource.get_metadata())
        self._add_result(result, origin)
        print(f"New result detected in APK Analysis from {resource.get_origin()}")
    
    
    def start_processing(self, uuid=None) -> None:
        """Creates required tasks and starts them"""
        self._create_tasks(uuid)
        # publish provided files to start processing
        self._publish_provided_files()
    
    
    def _create_tasks(self, uuid) -> None:
        # create tasks
        print(f'Creating tasks {self.req_tasks} with output dir {self.output_dir} and res {self.resources}')
        TaskFactory.create_tasks(self.req_tasks, self.output_dir, self.resources, uuid)


    def _publish_provided_files(self):
        # publish apk
        self.resources[ResourceType.APK_FILE].publish(self.apk_resource, True)
        # publish emulator
        self.resources[ResourceType.EMULATOR].publish(ResourceWrapper('', '', EMULATOR), True) #TODO: move this to singleton
        # publish additional_files
        print(self.upload_additional_files)
        for algorithm in self.upload_additional_files.keys():
            for resource_type_name, files in self.upload_additional_files[algorithm].items():
                resource_type = ResourceType[resource_type_name.upper()]
                file = files[0] # Assume is the first file.
                rw = ResourceWrapper(file, 'upload')
                self.resources[resource_type].publish(rw, True)


    def _publish_additional_files(self):
        """
        Re-publish all files because algorithm won't run unless trigger publish again.
        """
        for algorithm, algorithm_additional_files in self.upload_additional_files.items():
            for resource_type_name, files in algorithm_additional_files.items():
                file = files[0] # Assume each algorithm has 1 additional file
                resource_type = ResourceType[resource_type_name.upper()]
                resource_wrapper = ResourceWrapper(file, 'initialization')
                self.resources[resource_type].publish(resource_wrapper, True)
                print(f'Published resource type {resource_type} for {algorithm} with {file}.')
    
    
    def _update_utg(self, new_utg: dict) -> None:
        for node in new_utg['nodes']:
            node_id = node['id']
            if node_id not in self.utg_nodes:
                self.utg_nodes.add(node_id)
                self.utg['nodes'].append(self._repl_filepaths(node))
                
        for edge in new_utg['edges']:
            edge_id = edge['id']
            if edge_id not in self.utg_edges:
                self.utg_edges.add(edge_id)
                self.utg['edges'].append(self._repl_filepaths(edge))
        
        for key, val in new_utg.items():
            if key not in ['nodes', 'edges']:
                self.utg[key] = val

        with open(os.path.join(self.output_dir, 'utg.json'), "w+") as f:
            f.write(json.dumps(self.utg, indent=2))
            f.truncate()
    
    
    def _add_result(self, result: dict, origin: str) -> None:
        self.results[origin].append(result)
        with open(os.path.join(self.output_dir, 'results.json'), "w+") as f:
            f.write(json.dumps(self.results, indent=2))
            f.truncate()
        
        
    def _repl_filepaths(self, item: dict, _new_path: Callable[[str], str]=None) -> dict:
        text = json.dumps(item)
        output_dir = self.output_dir.rstrip('/')+'/'
        re_text =  fr'(?<=")({output_dir}.*?)(?=")'
        def _sub(match):
            if _new_path:
                return _new_path(match.group(1))
            return match.group(1).removeprefix(output_dir)
        new_item = re.sub(re_text, _sub , text)
        return json.loads(new_item)
        

if __name__ == '__main__':
    a = ApkAnalysis('/home/data/test/a2dp.Vol_133/', '/home/data/test/a2dp.Vol_133/a2dp.Vol_133.apk', ["Owleye"])
    a.start_processing()
