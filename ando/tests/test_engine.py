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
currpath = os.path.dirname(os.path.abspath(__file__))


class test_AnDO(unittest.TestCase):
    def setUp(self):
        pass

    def test_mainEngine1(self):
        directory = os.path.join(currpath, "dataset001", "Landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)
    def test_mainEngine2(self):
        directory = os.path.join(currpath, "dataset002", "exp-Landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)
    def test_mainEngine3(self):
        directory = os.path.join(currpath, "dataset003", "exp-landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)
    def test_mainEngine4(self):
        directory = os.path.join(currpath, "dataset004", "exp-Landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)
    def test_mainEngine5(self):
        directory = os.path.join(currpath, "dataset005", "exp-Landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)
    def test_mainEngine6(self):
        directory = os.path.join(currpath, "dataset006", "exp-Landing")
        self.assertEqual(andoE.mainEngine(directory,True), False)

    def test_mainEngine1(self):
        directory = os.path.join(currpath, "dataset007", "exp-Landing")
        self.assertEqual(andoE.mainEngine(directory,True), True)



if __name__ == '__main__':
    unittest.main()
