import os
import sys
import uuid
import inspect
import unittest

import datetime

###############################################################################
#                              relative importing                             #
###############################################################################

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)

# relative import ends ########################################################
from controllers.job_status_controller import JobStatusController
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

        self.asc = JobStatusController(self.tcn)


    def test_get_job_status(self):
        new_status = Status.successful

        self.db.update_document(self.uuid, self.tc, 'status', new_status)

        # r = self.db.get_document(self.uuid, self.tc)['status']
        r = self.asc.get(self.uuid)

        expected = {'end_time': '', 'progress': 0, 'start_time': '', 'status': 'NOT_STARTED'}

        self.assertEqual(r, expected)


    def test_get_update_start_time_status(self):
        new_status = datetime.datetime(2018,1,1)

        self.asc.update(self.uuid, start_time=new_status)

        r = self.db.get_document(self.uuid, self.tc)['overall-status']

        expected = {'status': 'NOT_STARTED', 'start_time': new_status, 'end_time': '', 'progress': 0}

        write_to_view("view1.txt", r)

        self.assertEqual(r, expected)


    def test_get_update_job_status(self):
        new_status = Status.successful

        self.asc.update(self.uuid, status=new_status)

        r = self.db.get_document(self.uuid, self.tc)['overall-status']

        expected = {'status': 'SUCCESSFUL', 'start_time': '', 'end_time': '', 'progress': 0}

        self.assertEqual(r, expected)


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
