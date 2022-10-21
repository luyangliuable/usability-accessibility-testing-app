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

        self.asc.post(self.uuid, 'xbot', status=new_status)
        r = self.asc.get(self.uuid, 'xbot')

        self.assertEqual(r['status'], new_status)


    def test_same_collection(self):
        self.assertEqual(self.asc.get_collection(), self.tc)


    def test_update_algorithm_status(self):

        self.asc.post(self.uuid, 'gifdroid', status=Status.running)

        expected = {'status': 'RUNNING', 'notes': '', 'start_time': '', 'end_time': '', 'apk': '', 'progress': 0, 'logs': [], 'ert': 0}

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']

        self.assertEqual(r, expected)


    def test_update_apk_in_status(self):
        expected = 'netflix.apk'

        self.asc.update_apk_filename(self.uuid, 'owleye', expected)

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['owleye']['apk']

        self.assertEqual(r, expected)


    def test_update_algorithm_attribute(self):
        self.asc.update_status_attribute(self.uuid, 'gifdroid', 'notes', 'random_notes for testing')

        expected = {'status': '', 'notes': 'random_notes for testing', 'start_time': '', 'end_time': '', 'apk': '', 'progress': 0, 'logs': [], 'ert': 0}

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']

        self.assertEqual(r, expected)


    def test_declare_apk_name_in_status(self):
        expected = 'netflix_no_chill.apk'
        t = self.asc.declare_apk_name_in_status(self.uuid, expected)

        r = self.db.get_document(self.uuid, self.tc)['algorithm_status']['gifdroid']['apk']

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
