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

    '''testing dataset001 folder'''
    def test_AnDO_dataset_1(self):
        directory = currpath+"/dataset001/Landing"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset002 folder'''
    def test_AnDO_dataset_2(self):
        directory = currpath+"/dataset002/exp-Landing"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset003 folder'''
    def test_AnDO_dataset_3(self):
        directory = currpath+"/dataset003/exp-landing"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset004 folder'''
    def test_AnDO_dataset_4(self):
        directory = currpath+"/dataset004/exp_vision"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset005 folder'''
    def test_AnDO_dataset_5(self):
        directory = currpath+"/dataset005/exp-myexperiment"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset006 folder'''
    def test_AnDO_dataset_6(self):
        directory = currpath+"/dataset006/exp-Landing"
        self.assertEqual(andoE.is_AnDO(directory, False), True)

    '''testing dataset007 folder'''
    def test_AnDO_dataset_7(self):
        directory = currpath+"/dataset007/exp-Landing/"
        self.assertEqual(andoE.is_AnDO(directory, False), False)


if __name__ == '__main__':
    unittest.main()
