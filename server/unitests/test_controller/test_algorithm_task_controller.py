import os
import sys
import uuid
import inspect
import unittest

###############################################################################
#                              relative importing                             #
###############################################################################

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)

# relative import ends ########################################################
from controllers.algorithm_task_controller import *
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from enums.status_enum import StatusEnum as Status
from utility.uuid_generator import unique_id_generator
from models.DBManager import *

class TestAlgorithmTaskController(unittest.TestCase):
    def setUp(self):
        self._parser = gifdroidJsonParser
        self.tcn = "test"
        self.db = DBManager.instance()

        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()
        format = DBManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)

        self.algorithm_task_controller = AlgorithmTaskController(self.tcn)


    def test_get_apk_file(self):
        apk_directory = "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/server/unitests/test_folder"

        result = self.algorithm_task_controller._get_apk_file(apk_directory, 'uuid')
        expected = os.path.join(apk_directory, result)

        self.assertEqual(result, expected)


    def test_get_additional_file(self):
        shared_volume = "/Users/blackfish/Documents/FIT3170_Usability_Accessibility_Testing_App/algorithms/app/.data/"
        uuid = "1b5ec9eb-d0c3-4f3e-b0b9-0227a90440e8"
        algorithms = ['gifdroid']
        result = str(self.algorithm_task_controller._get_additional_files(shared_volume, uuid, algorithms))
        expected = str({'gifdroid': {'gif': ['/users/blackfish/documents/fit3170_usability_accessibility_testing_app/algorithms/app/.data/1b5ec9eb-d0c3-4f3e-b0b9-0227a90440e8/gifdroid/sample.gif']}})

        self.assertEqual(result, expected)

    # def test_signal_analysis(self):
    #     result = self.algorithm_task_controller.post('uuid', [{'uuid': 'gifdroid'}])


###############################################################################
#                              Untility functions                             #
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
    suit = unittest.TestLoader().loadTestsFromTestCase(TestAlgorithmTaskController)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
