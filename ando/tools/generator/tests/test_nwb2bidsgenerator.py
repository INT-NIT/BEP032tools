import tempfile
import unittest
from pathlib import Path

from datalad.api import install, Dataset

from ando.tools.generator.nwb2bidsgenerator import bep_organize, is_valid


class TestNwbBIDSGenerator(unittest.TestCase):

    def setUp(self):
        pt = Path.cwd()/"BEP032-examples"
        if pt.exists():
            self.dataset = Dataset(pt)
            self.dataset.update(merge=True)
            self.dataset.get()
        else:
            self.dataset = install(
                source="https://gin.g-node.org/NeuralEnsemble/BEP032-examples",
                get_data=True,
            )
        self.datadir = str(pt)
        self.savedir = tempfile.mkdtemp()

    def test_nwb_to_bids(self):
        bep_organize(self.datadir, output_path=self.savedir, move_nwb=True, validate=False)
        try:
            is_valid(self.savedir)
        except:
            raise Exception('Validation Error')
