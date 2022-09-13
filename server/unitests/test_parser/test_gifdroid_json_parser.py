import os
import sys
import json
import uuid
import inspect
import unittest


###############################################################################
#                              relative importing                             #
###############################################################################

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)

from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from models.DBManager import DBManager

# relative import ends ########################################################

class Test_GifDDroid_Parser(unittest.TestCase):
    def setUp(self):
        self.db = DBManager.instance()
        # Test collection
        self.tcn = "test"
        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()
        format = DBManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)


    def test_gifdroid_parser(self):
        p = gifdroidJsonParser
        uuid = self.uuid

        expected = [{'name': 'fa', 'link': 'a', 'type': 'None', 's3_bucket': 'apk', 's3_key': uuid + '/report' + '/fa'}, {'name': 'fb', 'link': 'b', 'type': 'None', 's3_bucket': 'apk', 's3_key': uuid + '/report' + '/fb'}, {'name': 'fc', 'link': 'c', 'type': 'None', 's3_bucket': 'apk', 's3_key': uuid + '/report' + '/fc'}]

        res = p.do_algorithm(self.uuid, ['a', 'b', 'c'], ['fa', 'fb', 'fc'])

        write_to_view("view.txt", res)

        self.assertEqual(res, expected)

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
    suit = unittest.TestLoader().loadTestsFromTestCase(Test_GifDDroid_Parser)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
