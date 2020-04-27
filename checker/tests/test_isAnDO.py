import unittest
import AnDOChecker as ANDO
import json
import os
PATH=os.getcwd()


class test_AnDO(unittest.TestCase):

    
    def setUp(self):
        pass
    
    
    '''testing ds001 folder'''
    def test_bids_dataset_1(self):
        names=list()
        test1=PATH+"/tests/ds001/Data/Landing"
        dic_data = json.loads(
        json.dumps(ANDO.path_hierarchy(test1), indent=2, sort_keys=True))
        names = ANDO.get_name_in_dir([dic_data], names)
        self.assertEqual(ANDO.is_AnDO(names), False)
    '''testing ds002 folder'''
    def test_bids_dataset_2(self):
        names=list()
        test1=PATH+"/tests/ds002/data/Landing"
        dic_data = json.loads(
        json.dumps(ANDO.path_hierarchy(test1), indent=2, sort_keys=True))
        names = ANDO.get_name_in_dir([dic_data], names)
        self.assertEqual(ANDO.is_AnDO(names), True)
    '''testing ds003 folder'''
    def test_bids_dataset_3(self):
        names=list()
        test1=PATH+"/tests/ds003/data/my_experiment"
        dic_data = json.loads(
        json.dumps(ANDO.path_hierarchy(test1), indent=2, sort_keys=True))
        names = ANDO.get_name_in_dir([dic_data], names)
        self.assertEqual(ANDO.is_AnDO(names), False)
    '''testing ds004 folder'''
    def test_bids_dataset_4(self):
        names=list()
        test1=PATH+"/tests/ds004/data/newexp_vision"
        dic_data = json.loads(
        json.dumps(ANDO.path_hierarchy(test1), indent=2, sort_keys=True))
        names = ANDO.get_name_in_dir([dic_data], names)
        self.assertEqual(ANDO.is_AnDO(names), False)
    '''testing ds005 folder'''
    def test_bids_dataset_5(self):
        names=list()
        test1=PATH+"/tests/ds005/data/my_experiment"
        dic_data = json.loads(
        json.dumps(ANDO.path_hierarchy(test1), indent=2, sort_keys=True))
        names = ANDO.get_name_in_dir([dic_data], names)
        self.assertEqual(ANDO.is_AnDO(names), False)
    

if __name__ == '__main__':
    unittest.main()
 
