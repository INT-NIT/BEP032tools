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
        print('svpt: ', svpt)
        print('all 1st level subfolders of svpt: ', [g for g in svpt.glob('*')])

        nwbfile = list(svpt.glob('**/*.nwb'))[0]
        print('nwbffile: ', nwbfile)
        print(f'nwbfile.name: {nwbfile.name}')
        nwbfile = nwbfile.replace(nwbfile.with_name('newname.nwb'))
        json_file.unlink()
        validation_output = is_valid(self.savedir)

        print(f'validation_output: {validation_output}')
        # for x, i in enumerate(validation_output[1]):
        #     try:
        #         if re.search(f'naming.+not.+{nwbfile.name}', i, flags=re.I) is not None:
        #             print(f'x={x}: True\t(naming.+not.+{nwbfile.name}, i={i})')
        #         else:
        #             print(f'x={x}: False\t(naming.+not.+{nwbfile.name}, i={i})')
        #     except:
        #         print(f'Error in validation output number {x}: {i}')

        assert validation_output[0]==False, 'validating incorrectly'



        print(f'validation_output[1]: {validation_output[1]}')
        search_results = [re.search(f'naming.+not.+{nwbfile.name}',i, flags=re.I) for i in validation_output[1]]
        print(f'search_results: {search_results}')
        matching_error = [e for e in search_results if e is not None]
        print(f'matching_error: {matching_error}')
        assert matching_error, 'naming rule validation error'

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
