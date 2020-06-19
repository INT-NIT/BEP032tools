import unittest
import engine as andoE
class Test_Rules(unittest.TestCase):

    def setUp(self):
        pass

    '''testing session rules'''
    def test_session_rules(self):
        list=["sess-180116_001_m_enya_land-001"]
        self.assertEqual(andoE.is_session(list), True)
    def test_session_rules_1(self):
        list=["180116_m_enya_land-001"]
        self.assertEqual(andoE.is_session(list), False)
    def test_session_rules_2(self):
        list=["180116_001_m_land-001"]
        self.assertEqual(andoE.is_session(list), False)


    '''testing source rules'''
    def test_source_rules(self):
        list=["source"]
        self.assertEqual(andoE.is_source(list), True)
    def test_source_rules_1(self):
        list=["Source"]
        self.assertEqual(andoE.is_source(list), False)
    def test_source_rules_2(self):
        list=["sources"]
        self.assertEqual(andoE.is_source(list), False)

    '''testing subject rules'''
    def test_subject_rules(self):
        list=["sub-001"]
        self.assertEqual(andoE.is_subject(list), True)
    def test_subject_rules_1(self):
        list=["sub_001"]
        self.assertEqual(andoE.is_subject(list), False)
    def test_subject_rules_2(self):
        list=["Sub_001"]
        self.assertEqual(andoE.is_subject(list), False)

if __name__ == '__main__':
    unittest.main()
