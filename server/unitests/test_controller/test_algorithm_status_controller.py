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
from controllers.algorithm_status_controller import AlgorithmStatusController
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from enums.status_enum import StatusEnum as Status
from utility.uuid_generator import unique_id_generator
from models.DBManager import *

class TestDbManager(unittest.TestCase):
    def setUp(self):
        self._parser = gifdroidJsonParser
        self.tcn = "test"
        self.db = DBManager.instance()

        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()
        format = DBManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)

        self.asc = AlgorithmStatusController(self.tcn)


    def test_get_status_of_specific_algorithm(self):
        new_status = Status.running

        self.asc.update_algorithm_status(self.uuid, 'xbot', new_status)
        r = self.asc.get_specific_algorithm_status(self.uuid, 'xbot')

        self.assertEqual(r['status'], new_status)


    def test_same_collection(self):
        self.assertEqual(self.asc.get_collection(), self.tc)


    def test_update_algorithm_status(self):

        self.asc.update_algorithm_status(self.uuid, 'gifdroid', Status.running)

        expected = {
            'gifdroid': {
                'status': 'RUNNING',
                'notes': '',
                'start_time': '',
                'end_time': '',
                'apk': '',
            }
        }

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']

        expected = expected['gifdroid']

        # write_to_view("view.txt", r)
        # write_to_view("view2.txt", expected)
        self.assertEqual(r, expected)


    def test_update_apk_in_status(self):
        expected = 'netflix.apk'

        self.asc.update_algorthm_status_apk_file_name(self.uuid, 'owleye', expected)

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['owleye']['apk']

        self.assertEqual(r, expected)


    def test_update_algorithm_attribute(self):
        self.asc.update_algorithm_status_attribute(self.uuid, 'gifdroid', 'notes', 'random_notes for testing')

        expected = {
            'gifdroid': {
                'status': '',
                'notes': 'random_notes for testing',
                'start_time': '',
                'end_time': '',
                'apk': ''
            }
        }

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']

        expected = expected['gifdroid']

        self.assertEqual(r, expected)


    def test_declare_apk_name_in_status(self):
       expected = 'netflix_no_chill.apk'
       t = self.asc.decalare_apk_name_in_status(self.uuid, expected)
       write_to_view("view.txt", t)
       r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']['apk']

       self.assertEqual(expected, r)


    def test_get_all_algorithm_status(self):
       r = self.asc.get_all_algorithm_status(self.uuid)
       expected = {'storydistiller': {'status': '', 'notes': '', 'start_time': '', 'end_time': '', 'apk': ''}, 'owleye': {'status': '', 'notes': '', 'start_time': '', 'end_time': '', 'apk': ''}, 'xbot': {'status': '', 'notes': '', 'start_time': '', 'end_time': '', 'apk': ''}, 'gifdroid': {'status': '', 'notes': '', 'start_time': '', 'end_time': '', 'apk': ''}, 'ui_checker': {'status': '', 'notes': '', 'start_time': '', 'end_time': '', 'apk': ''}}

       self.assertEqual(expected, r)


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
    suit = unittest.TestLoader().loadTestsFromTestCase(TestDbManager)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
