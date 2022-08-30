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

from controllers.algorithm_status_controller import AlgorithmStatusController as asc
from models.Apk import *

class TestDbManager(unittest.TestCase):
    def setUp(self):
        self.tcn = "apk"
        self.db = ApkManager.instance()

        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()

        format = ApkManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)


    def test_get_file(self):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        data = requests.get("http://localhost:5005/file/get", data=json.dumps( {"uuid": self.uuid} ), headers=headers).json()
        write_to_view("view.txt", data)

        data.pop('date')

        expected = ApkManager.get_format(self.uuid)
        expected.pop('date')

        # Get file route
        print(data)


        self.assertEqual(expected, data)


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
    suit = unittest.TestLoader().loadTestsFromTestCase(TestDbManager)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
