import unittest
import AnDO_engine as andoE
import json
import os
path=os.getcwd()


class test_AnDO(unittest.TestCase):

    
    def setUp(self):
        pass
    
    '''testing ds001 folder'''
    def test_AnDO_dataset_1(self):
        names=list()
        directory=path+"/tests/ds001/Data/Landing"
        self.assertEqual(andoE.is_AnDO(directory), False)
        
  
    '''testing ds002 folder'''
    def test_AnDO_dataset_2(self):
        names=list()
        directory=path+"/tests/ds002/data/exp-Landing"
        self.assertEqual(andoE.is_AnDO(directory),True)
        
    '''testing ds003 folder'''
    def test_AnDO_dataset_3(self):
        names=list()
        directory=path+"/tests/ds003/data/my_experiment"
        self.assertEqual(andoE.is_AnDO(directory),False)
        
    '''testing ds004 folder'''
    def test_AnDO_dataset_4(self):
        names=list()
        directory=path+"/tests/ds004/data/newexp_vision"
        self.assertEqual(andoE.is_AnDO(directory),False)
        
    '''testing ds005 folder'''
    def test_AnDO_dataset_5(self):
        names=list()
        directory=path+"/tests/ds005/data/my_experiment"
        self.assertEqual(andoE.is_AnDO(directory),False)
    
    '''testing ds006 folder'''
    def test_AnDO_dataset_6(self):
        names=list()
        directory=path+"/tests/ds006/data/Landing"
        self.assertEqual(andoE.is_AnDO(directory),False)
        
    '''testing ds007 folder'''
    def test_AnDO_dataset_7(self):
        names=list()
        directory=path+"/tests/ds007/data/exp-Landing/"
        self.assertEqual(andoE.is_AnDO(directory),False)
    
    
 
if __name__ == '__main__':
    unittest.main()
 
