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

        self.asc = AlgorithmStatusController(self.tcn, self._parser)


    def test_same_collection(self):
        self.assertEqual(self.asc.get_colletion(), self.tc)


    def test_update_status_gifdroid(self):
        expected = {'gifdroid': {'status': 'DONE', 'notes': '', 'start_time': '', 'end_time': ''}}

        self.asc.update_algorithm_status(self.uuid, 'gifdroid', "DONE")

        r = self.db.get_document(self.uuid, self.tc)
        r = r['algorithm_status']

        # write_to_view("view.txt", r)
        # write_to_view("view2.txt", expected)

        self.assertEqual(r['gifdroid'], expected['gifdroid'])

    def test_insert_result_into_algorithm_result(self):
        result = ["google.com.aubdasdas", "finally_got_something.org.au"]

        expected = {'images': [{'name': 'finally_got_something.org.au', 'type': 'audio/basic', 's3_bucket': 'apk', 's3_key': os.path.join(self.uuid, 'finally_got_something.org.au' )}, {'name': 'finally_got_something.org.au', 'type': 'audio/basic', 's3_bucket': 'apk', 's3_key': os.path.join(self.uuid, "finally_got_something.org.au" )}], 'json': {'name': '', 'data': '', 's3_bucket': '', 's3_key': ''}}

        self.asc.insert_algorithm_result(self.uuid, 'gifdroid', result, 'images')

        r = self.db.get_document(self.uuid, self.tc)

        write_to_view("view.txt", r['results']['gifdroid'])
        write_to_view("view1.txt", result)

        self.assertEqual(r['results']['gifdroid']['images'], expected['images'])

    # def test_update_algorithm_status_attribute(self):
    #     expected = {
    #         'gifdroid': {
    #             'status': 'PENDING',
    #             'notes': 'random_notes',
    #             'estimate_remaining_time': 100,
    #             'result_link': ''
    #         }
    #     }
    #     self.asc.update_algorithm_status(self.uuid, expected, "PENDING")
    #     self.asc.update_algorithm_status_attribute(self.uuid, 'gifdroid', 'status', "DONE")

    #     r = self.db.get_document(self.uuid, self.tc)['algorithm_status']

    #     expected['gifdroid']['status'] = 'DONE'

    #     write_to_view("view.txt", r)
    #     write_to_view("view2.txt", expected)


    #     self.assertEqual(r, expected)


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
