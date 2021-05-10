import tempfile
import unittest
from pathlib import Path
import re
from datalad.api import install, Dataset

from ando.tools.generator.nwb2bidsgenerator import NwbToBIDS, is_valid


@unittest.skip
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

        # invalidating structure: removing json file
        svpt = Path(self.savedir)
        for sub_file in svpt.iterdir():
            if sub_file.suffix == '.json':
                json_file = sub_file
                break
        json_file.unlink()

        # invalidating structure: use custom filename for nwb file
        nwbfile = list(svpt.glob('**/*.nwb'))[0]
        new_nwbfile = nwbfile.with_name('newname.nwb')
        # `replace` only provide return value for python >= 3.8
        nwbfile.replace(new_nwbfile)

        validation_output = is_valid(self.savedir)

        assert validation_output[0] == False, 'validating incorrectly'

        # validate that incorrect json file name is detected
        pattern = 'naming.+not.+' + new_nwbfile.name
        search_results = [re.search(pattern, i, flags=re.I) for i in
                          validation_output[1]]
        matching_error = [e for e in search_results if e is not None]
        assert matching_error, 'naming rule validation error'

        # validate that incorrect nwb file name is detected
        pattern = f'mandatory.+not.+{json_file.stem}.*'
        search_results = [re.search(pattern, i, flags=re.I) for i in
                          validation_output[1]]
        matching_error = [e for e in search_results if e is not None]
        assert matching_error, 'mandatory file rule validation error'

