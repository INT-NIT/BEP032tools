import unittest

import AnDO_engine as andoE
import json
import os
path=os.getcwd()


class test_AnDO(unittest.TestCase):

    
    def setUp(self):
        pass
    
    def test_AnDO_Func_level_1(self):
        names=list()
        names=['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source']
        validate=list()
        self.assertEqual(all(andoE.is_AnDO_R(names,0,validate)), False)
        
    def test_AnDO_Func_level_2(self):
        names=list()
        names=['exp-Landing', 'anye', 'sess-180116_001_m_anye_land-001', 'source']
        validate=list()
        self.assertEqual(all(andoE.is_AnDO_R(names,0,validate)), False)
        
    def test_AnDO_Func_level_3(self):
        names=list()
        names=['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source']
        validate=list()
        self.assertEqual(all(andoE.is_AnDO_R(names,0,validate)), False)
    
    def test_AnDO_Func_level_4(self):
        names=list()
        names=['exp-Landing', 'sub-anye', 'sess-180116_001_m_anye_land-001', 'sources']
        validate=list()
        self.assertEqual(all(andoE.is_AnDO_R(names,0,validate)), False)
    
if __name__ == '__main__':
    unittest.main()
 
