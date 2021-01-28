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
        self.assertEqual(andoE.check_Path(names, False)[0], True)


if __name__ == '__main__':
    unittest.main()
