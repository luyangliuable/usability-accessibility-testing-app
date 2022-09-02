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
# from controllers.algorithm_status_controller import algorithm_status_controller as asc
from controllers.download_controller import DownloadController
from models.DBManager import *

class TestDownloadCtrl(unittest.TestCase):
    def setUp(self):
        self.d_ctrl = DownloadController()
        self.uuid = "57730388-de61-45c1-8098-d449491004ec"
        self.algorithm = "gifdroid"


    def test_file_downloaded(self):
        res = self.d_ctrl.download(self.uuid, self.algorithm)

        write_to_view("view.txt", res)


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
    suit = unittest.TestLoader().loadTestsFromTestCase(TestDownloadCtrl)
    # Run the test suit
    unittest.TextTestRunner(verbosity=2).run(suit)

main()