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
from controllers.algorithm_status_controller import algorithm_status_controller as asc
from models.DBManager import *

class TestDbManager(unittest.TestCase):
    def setUp(self):
        self.tcn = "apk"
        self.db = DBManager.instance()

        self.tc = self.db.create_collection(self.tcn)
        self.asc = asc(self.tcn)

        # Test document
        self.uuid = unique_id_generator()
        format = DBManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)


    def test_same_collection(self):
        self.assertEqual(self.asc.get_colletion(), self.tc)


    def test_update_status(self):
        expected = {'gifdroid': {'status': 'random_status', 'notes': 'random_notes', 'estimate_remaining_time': 100, 'result_link': ''}}

        self.asc.update_algorithm_status(self.uuid, expected)

        r = self.db.get_document(self.uuid, self.tc)[0]
        r = r['algorithm_status']

        self.assertEqual(r, expected)


    def test_update_algorithm_status_attribute(self):
        expected = {
            'gifdroid': {
                'status': 'PENDING',
                'notes': 'random_notes',
                'estimate_remaining_time': 100,
                'result_link': ''
            }
        }
        self.asc.update_algorithm_status(self.uuid, expected)
        self.asc.update_algorithm_status_attribute(self.uuid, 'gifdroid', 'status', "done")

        r = self.db.get_document(self.uuid, self.tc)[0]['algorithm_status']

        expected['gifdroid']['status'] = 'done'

        write_to_view("view.txt", r)
        write_to_view("view2.txt", expected)


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
