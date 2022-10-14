import os
import sys
import uuid
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
print(parentdir)
sys.path.insert(0, parentdir)

from tasks.task import *
from resources.resource import *

class Test_Droidbot(unittest.TestCase):
    def setUp(self):
        self.resource_dict = {} # make resource dict
        self.resource_dict[ResourceType.APK_FILE] = ResourceGroup(ResourceType.APK_FILE)
        self.resource_dict[ResourceType.EMULATOR] = ResourceGroup(ResourceType.EMULATOR, usage=ResourceUsage.SEQUENTIAL)

        self.tasks = ["Droidbot"]
        self.base_dir = "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/"

    def test_download_summary_works(self):
        TaskFactory.create_tasks(self.tasks, self.base_dir, self.resource_dict)

        test = TaskFactory._tasks["Droidbot"]

        exit(0)


###############################################################################
#                              Utility functions                             #
###############################################################################

def write_to_view(filename: str, content):
    """
    Useful for debuging
    """
    with open(filename, "w") as f:
        f.write(str(content))


def unique_id_generator() -> str:
    res = str( uuid.uuid4() )
    return res


def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(Test_Droidbot)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
