import unittest

import ando.engine as andoE

import os
path=os.getcwd()


class test_parse_all_path(unittest.TestCase):
    """Test the function parse_all_path

    Args:
        unittest (unittest): [parse_all_path should  Transform this
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
        ['Landing', 'sub-enyo'],
        ['Landing', 'sub-enyo', '180116_001_m_enyo_land-001']
    ]
    to
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
    ]
    Checking for the longest chain with the same sub chain]
    """
    def setUp(self):
        pass

    def test_parse_all_path(self):
        result=[['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001'],['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'],['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source']]
        list1=[['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'], ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'], ['exp-Landing', 'sub-enyo'], ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001']]
        e=andoE.parse_all_path(list1)

        self.assertEqual(e.sort(),result.sort())
    
    def test_parse_all_path_1(self):
        result=[['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'], ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'], ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001'], ['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'], ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001'], ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'], ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001']]
        list1=[['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'], ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'], ['exp-Landing', 'sub-enyo'], ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001']]
        e=andoE.parse_all_path(list1)

        self.assertEqual(e.sort(),result.sort())

    def test_parse_all_path_2(self):
        list1=[['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'],
            ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
            ['exp-Landing', 'sub-enyo'],
            ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001'],
            ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-002'],
            ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'derivatives'],
            ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'metadata'],
            ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'rawdata'] ]

        result=[['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-001'],
                ['exp-Landing', 'sub-enyo', '180116_001_m_enyo_land-002'],
                ['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001'],
                ['exp-Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source', 'rawdata', 'derivatives', 'metadata']]

        e=andoE.parse_all_path(list1)
        self.assertEqual(e.sort(),result.sort())
       
if __name__ == '__main__':
    unittest.main()

