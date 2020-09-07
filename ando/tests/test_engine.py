# File: test_engine.py
# Project: tests
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:33:13 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


import unittest
import ando.engine as andoE
import os
path = os.getcwd()


class test_AnDO(unittest.TestCase):
    """Overall check of the rules given in the rules directory

    Args:
        unittest ([unittest]): [check every level of a given list of path ]
    """

    def setUp(self):
        pass

    def test_AnDO_Func_experiment_level(self):
        """
        Check if the experiment level follow the rules given in
        rules/experiment_rules.json
        """
        names = list()
        names = ['Landing', 'sub-anye', '180116_001_m_anye_land-001',
                 'source']
        validate = list()
        self.assertEqual(all(andoE.is_AnDO_R(names, 0, validate)), False)

    def test_AnDO_Func_subject_level(self):
        """
        Check if the subject level follow the rules given in
        rules/subject_rules.json
        """
        names = list()
        names = ['exp-Landing', 'anye', 'sess-180116_001_m_anye_land-001',
                 'source']
        validate = list()
        self.assertEqual(all(andoE.is_AnDO_R(names, 0, validate)), False)

    def test_AnDO_Func_session_level(self):
        """
        Check if the session level follow the rules given in
        rules/session_rules.json
        """
        names = list()
        names = ['exp-Landing', 'sub-anye', '180116_001_m_anye_land-001',
                 'source']
        validate = list()
        self.assertEqual(all(andoE.is_AnDO_R(names, 0, validate)), False)

    def test_AnDO_Func_sources_level(self):
        """
        Check if the sources level follow the rules given in
        rules/sources_rules.json
        """
        names = list()
        names = ['exp-Landing', 'sub-anye', 'sess-180116_001_m_anye_land-001',
                 'sources']
        validate = list()
        self.assertEqual(all(andoE.is_AnDO_R(names, 0, validate)), False)


if __name__ == '__main__':
    unittest.main()
