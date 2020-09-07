# File: test_isAnDO.py
# Project: tests
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:33:43 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


import unittest
import ando.engine as andoE
import os
currpath = os.path.dirname(os.path.abspath(__file__))


class test_AnDO(unittest.TestCase):

    def setUp(self):
        pass

    '''testing ds001 folder'''
    def test_AnDO_dataset_1(self):
        directory = currpath+"/ds001/Data/Landing"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds002 folder'''
    def test_AnDO_dataset_2(self):
        directory = currpath+"/ds002/data/exp-Landing"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds003 folder'''
    def test_AnDO_dataset_3(self):
        directory = currpath+"/ds003/data/my_experiment"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds004 folder'''
    def test_AnDO_dataset_4(self):
        directory = currpath+"/ds004/data/newexp_vision"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds005 folder'''
    def test_AnDO_dataset_5(self):
        directory = currpath+"/ds005/data/my_experiment"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds006 folder'''
    def test_AnDO_dataset_6(self):
        directory = currpath+"/ds006/data/Landing"
        self.assertEqual(andoE.is_AnDO(directory), False)

    '''testing ds007 folder'''
    def test_AnDO_dataset_7(self):
        directory = currpath+"/ds007/data/exp-Landing/"
        self.assertEqual(andoE.is_AnDO(directory), False)


if __name__ == '__main__':
    unittest.main()
