import unittest
from tools.generator.AnDOGenerator import *


class Test_AnDOSesID(unittest.TestCase):

    def setUp(self):
        self.date = '20000101'
        self.sesNumber = '100'
        self.customField = 'test'
        self.sesID = f'{self.date}_{self.sesNumber}_{self.customField}'

    def test_user_input_warning(self):
        with self.assertWarns(Warning):
            AnDOSesID(sesID=self.sesID, date=self.date, sesNumber=self.sesNumber)

    def test_insufficient_input_error(self):
        with self.assertRaises(ValueError):
            AnDOSesID()

    def test_datetime(self):
        date_obj = datetime.datetime.strptime(self.date, '%Y%m%d')
        sesID = AnDOSesID(date=date_obj, sesNumber=self.sesNumber)
        self.assertEqual(self.date, sesID.date)

    def test_only_sesID(self):
        sesID = AnDOSesID(sesID=self.sesID)

        self.assertEqual(self.sesID, str(sesID))
        self.assertEqual(self.date, sesID.date)
        self.assertEqual(self.sesNumber, sesID.sesNumber)
        self.assertEqual(self.customField, sesID.customSesField)

    def test_no_sesID(self):
        sesID = AnDOSesID(date=self.date, sesNumber=self.sesNumber, customSesField=self.customField)

        self.assertEqual(self.sesID, str(sesID))
        self.assertEqual(self.date, sesID.date)
        self.assertEqual(self.sesNumber, sesID.sesNumber)
        self.assertEqual(self.customField, sesID.customSesField)


class Test_AnDOSession(unittest.TestCase):

    def setUp(self):
        self.expName = 'exp23'
        self.guid = '1234'
        self.date = '20000101'
        self.sesNumber = '100'
        self.customField = 'test'
        self.sesID = f'{self.date}_{self.sesNumber}_{self.customField}'


    def test_insufficient_input(self):
        with self.assertRaises(ValueError):
            AnDOSession(None, self.guid)

        with self.assertRaises(ValueError):
            AnDOSession(self.expName, None)

    def test_simple_parameters(self):
        ses = AnDOSession(self.expName, self.guid, self.sesID)

        self.assertEqual(self.expName, ses.expName)
        self.assertEqual(self.guid, ses.guid)
        self.assertEqual(self.sesID, str(ses.sesID))

    def test_complex_parameters(self):
        ses = AnDOSession(self.expName,
                          self.guid,
                          sesNumber=self.sesNumber,
                          date=self.date,
                          customSesField=self.customField)

        self.assertEqual(self.expName, ses.expName)
        self.assertEqual(self.guid, ses.guid)
        self.assertEqual(self.sesID, str(ses.sesID))

    # TODO: This check is still failing, review engine/check_Path for consistency
    def test_paths(self):
        ses = AnDOSession(self.expName, self.guid, self.sesID)

        expected = os.path.join(f'exp-{self.expName}', f'sub-{self.guid}', f'ses-{self.sesID}')
        self.assertEqual(expected, ses.get_session_path())

        self.assertEqual(3, len(ses.get_all_folder_paths()))

