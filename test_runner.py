"""runner"""
import unittest

from tests import test_class_AB
from tests import test_class_Email
from tests import test_class_NB
from tests import test_class_Note
from tests import test_class_Phone
from tests import test_class_RecordContact
from tests import test_class_RecordNote
from tests import test_class_User
from tests import test_utils
from tests import test_validation

ABTestSuite = unittest.TestSuite()
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_AB.TestAddressBook))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Email.TestEmail))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Phone.TestPhone))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_RecordContact.TestRecordContact))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_User.TestUser))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_validation.TestValidation))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_utils.TestPrintContacts))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Note.TestNote))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_RecordNote.TestRecordNote))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_NB.TestNotesBook))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(ABTestSuite)
