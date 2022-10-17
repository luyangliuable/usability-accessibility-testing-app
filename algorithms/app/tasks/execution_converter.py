import json
import re

class ExecutionConverter:
    """Converts utg file to json of screen details
    
    Example json output of execution details format per screen pair:
        '035f856b24b8a4b8a096689a18b5fac4-->68c735fb28d32928959bd9e42323ea44': 
        {
            'from': '035f856b24b8a4b8a096689a18b5fac4', 	
            'from_path': 'states/screen_2022-09-09_002450.jpg', 
            'to': '68c735fb28d32928959bd9e42323ea44', 
            'to_path': 'states/screen_2022-09-09_002458.jpg', 
            'events': 
            [
                {
                'event_str': 'TouchEvent(state=035f856b24b8a4b8a096689a18b5fac4, 
                view=f50134ebaa21cd73a93a106e7b3ad676(EditDevice/CheckBox-Capture lo))', 		
                'event_id': 53, 
                'event_type': 'touch', 
                'view_images': ['views/view_f50134ebaa21cd73a93a106e7b3ad676.jpg']
                }
            ]
        }
    
    """
    
    def __init__(self, utg_js):
        self.utg = self._convert_utg(utg_js)
        self.image_id = {}
        self.execution_details = {}
        self.execution_graph = {}
        self.all_path = {}
       
    def _convert_utg(self, utg_js: str) -> json:
        """Convert utg.js to readable json"""
        file_js = open(utg_js).read()
        re_text = r'var utg = ([\S\s]*)'
        text = re.findall(re_text, file_js)[0]
        return json.loads(text)
    
    def _store_id(self) -> None:
        """Store screen id and image path in dictionary"""
        if len(self.image_id) == 0:
            for node in self.utg['nodes']:
                self.image_id[node['id']] = node['image']
            
    def store_all_execution_details(self):
        """Store execution details for all edge pairings"""
        self._store_id()
        for edge in self.utg['edges']:
            self.execution_details[edge['id']] = {
                "from": edge['from'],
                "from_path": self.image_id[edge['from']],
                "to": edge['to'],
                "to_path":self.image_id[edge['to']],
                "events": edge['events']
            }
    
    def get_all_execution_details(self) -> dict:
        return self.execution_details
    
    def get_select_execution_details(self, path) -> dict:
        """Return execution details for specific path"""
        if len(self.execution_details) == 0:
            self.store_all_execution_details()
        execution_out = {}
        for p in range(len(path)-1):
            for edge in self.execution_details.values():
                print(edge)
                if edge['from'] == path[p] and edge['to'] == path[p+1]:
                    execution_out[p] = {
                        "from": edge['from'],
                        "from_path": edge['from_path'],
                        "to": edge['to'],
                        "to_path": edge['to_path'],
                        "events": edge['events']
                    }
                    break
        return execution_out
    
    def create_execution_graph(self):
        """Creates execution graph for entire utg"""
        for edge in self.utg['edges']:
            source = edge['from']
            dest = edge['to']
            if source in self.execution_graph:
                curr_source = self.execution_graph[source]
                new_out = []
                new_out = curr_source + new_out
                new_out.append(dest)
                self.execution_graph[source] = new_out
            else:
                self.execution_graph[source] = [dest]
                
    def get_execution_graph(self) -> dict:
        return self.execution_graph
                
    def construct_all_paths(self, source, dest) -> dict:
        """Constructs all paths of screens between source and destination"""
        self._store_id()
        visited = {}
        for key in self.image_id.keys():
            visited[key] = False
        self.all_path[source + '_' + dest] = []
        self._each_path(source, dest, visited, [], source + '_' + dest)
        return self.all_path[source + '_' + dest]

    def _each_path(self, source, dest,visited, path, name):
        """Helper function to traverse graph"""
        visited[source]= True
        path.append(source)
        if source == dest:
            self.all_path[name].append(path.copy())
        else:
            for i in self.execution_graph[source]:
                if visited[i]== False:
                    self._each_path(i, dest, visited, path, name)
        path.pop()
        visited[source]= False


if __name__ == '__main__':
    ec = ExecutionConverter('utg.js')  
    # ec.store_execution_paths()
    ec.create_execution_graph()
    path = ec.construct_all_paths('86e0aef82d06bb185fd9710cc942f09e', '3397632e4bd06925af687e601461e5d8')
    print(ec.get_select_execution_details(path[0]))
