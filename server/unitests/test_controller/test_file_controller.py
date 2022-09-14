import os
from pickle import bytes_types
import sys
import json
import uuid
import requests
import inspect
import unittest

###############################################################################
#                              relative importing                             #
###############################################################################

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)

# relative import ends ########################################################

from controllers.update_document_controller import *
from download_parsers.gifdroid_json_parser import gifdroidJsonParser
from models.DBManager import *

class TestFileCtr(unittest.TestCase):
    def setUp(self):
        self.tcn = "apk"
        self.db = DBManager.instance()

        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()

        format = DBManager.get_format(self.uuid)
        self.fc = UpdateDocumentController(self.tcn, gifdroidJsonParser)

        self.td = self.db.insert_document(format, self.tc)


    def test_get_file(self):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        data = self.fc.get_document(self.uuid)
        write_to_view("view.txt", data)

        data.pop('date')
        data.pop('_id')

        expected = DBManager.get_format(self.uuid)
        expected.pop('date')

        # Get file route
        print(data)


        self.assertEqual(expected, data)


    def test_insert_result_into_algorithm_result(self):
        result = ["google.com.aubdasdas", "finally_got_something.org.au"]
        names = ["google", "finally_got_something"]

        expected = {'images': [{'name': 'google', 'link': 'google.com.aubdasdas', 'type': 'None', 's3_bucket': 'apk', 's3_key': os.path.join(self.uuid, 'report', 'google')}, {'name': 'finally_got_something', 'link': 'finally_got_something.org.au', 'type': 'None', 's3_bucket': 'apk', 's3_key': os.path.join(self.uuid, 'report', 'finally_got_something')}], 'json': []}

        self.fc.insert_algorithm_result(self.uuid, 'gifdroid', result, 'images', names)

        r = self.db.get_document(self.uuid, self.tc)

        write_to_view("view.txt", r['results']['gifdroid'])
        write_to_view("view1.txt", expected)

        self.assertEqual(r['results']['gifdroid'], expected)


###############################################################################
#                              Untility functions                             #
###############################################################################
def safe_serialize(obj):
    default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
    return json.dumps(obj, default=default)

def write_to_view(filename: str, content):
    """
    Useful for debuging
    """
    with open(filename, "w") as f:
        f.write(str(content))


def unique_id_generator() -> str:
    res = str( uuid.uuid4() )
    return res


def bytes_to_json(byte_str: bytes):
    data = byte_str.decode('utf8').replace("'", '"')
    data = json.loads(data)

    return data


def main():
    # Create a test suit
    suit = unittest.TestLoader().loadTestsFromTestCase(TestFileCtr)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
