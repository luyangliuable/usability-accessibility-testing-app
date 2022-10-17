from screenshot import Screenshot
from typing import List, Callable

class UIInfo():
    
    def __init__(self, application: str):
        self.application = application
        self.states = []
        self.states_names = []
        self.sequence_files = []
        self.subsribers = []
        

    def add_screenshot(self, screenshot: Screenshot):
        activity_name = screenshot.get_view_name()
        add = False
        if self.states_names == []:
            self.states.append(screenshot)
            self.states_names.append(activity_name)
            add = True
        else:
            if activity_name not in self.states_name:
                self.states.append(screenshot)
                self.states_names.append(activity_name)
                add = True
        if add:
            #NOTIFY SUBSCRIBERS
            pass
                         

    def subscribe(self, subscriber : Callable[[str],None]) -> None:
        """Subscriber for new screenshot"""
        self.subscribers.append(subscriber) # add subscriber to queue
    
        
