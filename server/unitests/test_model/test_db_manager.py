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

# relative import ends ########################################################

from models.DBManager import DBManager

class Test_Db_Manager(unittest.TestCase):
    def setUp(self):
        self.db = DBManager.instance()

        # Test collection
        self.tcn = "test"
        self.tc = self.db.create_collection(self.tcn)

        # Test document
        self.uuid = unique_id_generator()
        format = DBManager.get_format(self.uuid)

        self.td = self.db.insert_document(format, self.tc)


    def test_get_d(self):
        """
            Test that getting document works
        """
        res = self.db.get_document(self.uuid, self.tc)

        ###############################################################################
        #                            Pop dynamic attributes                           #
        ###############################################################################
        res.pop('_id')
        res.pop('date')

        format = DBManager.get_format(self.uuid)
        format.pop('date')

        write_to_view("view.txt", res)

        self.assertEqual(str( res ), str( format ))


    # def test_get_format(self):
    #     val = DBManager.get_format(self.uuid)

    #     val.pop('date')
    #     val.pop('uuid')

    #     with open("../../models/document_format.json", "w") as f:
    #         expected = json.load(f)

    #     expected.pop('date')
    #     expected.pop('uuid')

    #     self.assertEqual(expected, val) 


    def test_update_d(self):
        """
            Test that update document works
        """

        val = {"test": { "status": "pending", "message": "works"}}

        self.db.update_document(self.uuid, self.tc, "algorithm_status",  val)

        res = self.db.get_document(self.uuid, self.tc)

        ###############################################################################
        #                            Pop dynamic attributes                           #
        ###############################################################################
        res.pop('_id')
        res.pop('date')

        write_to_view("view.txt", res)
        write_to_view("view2.txt", val)

        self.assertEqual(val, res["algorithm_status"])

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
    suit = unittest.TestLoader().loadTestsFromTestCase(Test_Db_Manager)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()
