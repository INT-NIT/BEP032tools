import tempfile
import unittest
from pathlib import Path
import re
from datalad.api import install, Dataset

from ando.tools.generator.nwb2bidsgenerator import NwbToBIDS, is_valid

class TestNwbBIDSGenerator(unittest.TestCase):

    def setUp(self):
        pt = Path.cwd()/"BEP032-examples"
        if pt.exists():
            self.dataset = Dataset(pt)
            self.dataset.clean()
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
        n2b = NwbToBIDS(self.datadir)
        n2b.organize(output_path=self.savedir, move_nwb=False, validate=False)
        validation_output = is_valid(self.savedir)
        if not validation_output[0]:
            raise Exception(','.join(validation_output[1]))

    def test_validation(self):
        n2b = NwbToBIDS(self.datadir)
        n2b.organize(output_path=self.savedir, move_nwb=False, validate=False)
        svpt = Path(self.savedir)
        for sub_files in svpt.iterdir():
            if sub_files.suffix=='.json':
                json_file = sub_files
                break
        nwbfile = list(svpt.glob('**/*.nwb'))[0]
        nwbfile.unlink()
        json_file.unlink()
        validation_output = is_valid(self.savedir)
        assert validation_output[0]==False, 'validating incorrectly'
        assert(any([True if re.search(f'naming.+not.+{nwbfile.name}',i, flags=re.I) is not None
                    else False
                    for i in validation_output[1]
                    ])), \
            'naming rule validation error'
        assert (any([True if re.search(f'mandatory.+not.+{json_file.stem}.*', i, flags=re.I) is not None
                     else False
                     for i in validation_output[1]
                     ])), \
            'mandatory file rule validation error'
