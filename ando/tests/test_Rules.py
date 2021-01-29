# File: test_Rules.py
# Project: tests
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:35:37 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


import unittest
import ando.engine as andoE


class Test_Rules(unittest.TestCase):

    def setUp(self):
        pass

# ---------------------------------- FOLDER ---------------------------------- #

    def test_session_folder_rules(self):
        list = ["ses-18000116001land001"]
        self.assertEqual(andoE.is_session_folder(list), True)

    def test_session_folder_rules_1(self):
        list = ["180116_m_enya_land-001"]
        self.assertEqual(andoE.is_session_folder(list), False)

    def test_session_folder_rules_2(self):
        list = ["180116_001_m_land-001"]
        self.assertEqual(andoE.is_session_folder(list), False)

    def test_session_folder_rules_3(self):
        list = ["ses-180116_001_m_land_001"]
        self.assertEqual(andoE.is_session_folder(list), False)

    def test_subject_folder_rules(self):
        list = ["sub-001"]
        self.assertEqual(andoE.is_subject_folder(list), True)

    def test_subject_folder_rules_1(self):
        list = ["sub_001"]
        self.assertEqual(andoE.is_subject_folder(list), False)
    def test_subject_folder_rules_2(self):
        list = ["Sub_001"]
        self.assertEqual(andoE.is_subject_folder(list), False)

    '''testing ephys rules'''
    def test_ephys_rules(self):
        list = ["ephys"]
        self.assertEqual(andoE.is_ephys_folder(list), True)
    def test_ephys_rules1(self):
        list = ["Ephys"]
        self.assertEqual(andoE.is_ephys_folder(list), False)
    def test_ephys_rules3(self):
        list = ["NotEphysAtAll"]
        self.assertEqual(andoE.is_ephys_folder(list), False)






# ----------------------------------- FILE ----------------------------------- #

    
    '''top level rules'''
    def test_top_level_rules(self):
        list = ["exp-test/dataset_description.tsv"]
        self.assertEqual(andoE.is_DataSetDescription_file(list), True)
    def test_top_level_rules4(self):
        list = ["exp-test/Not_dataset_description.tsv"]
        self.assertEqual(andoE.is_DataSetDescription_file(list), False)
    def test_top_level_rules1(self):
        list = ["exp-test/subjects.tsv"]
        self.assertEqual(andoE.is_subject_file(list), True)
    def test_top_level_rules3(self):
        list = ["exp-test/subjects.json"]
        self.assertEqual(andoE.is_subject_file(list), True)
   
    def test_top_level_rules5(self):
        list = ["exp-test/not_subject.tsv"]
        self.assertEqual(andoE.is_subject_file(list), False)
    def test_top_level_rules6(self):
        list = ["exp-test/not_subject.json"]
        self.assertEqual(andoE.is_subject_file(list), False)
  


if __name__ == '__main__':
    unittest.main()
