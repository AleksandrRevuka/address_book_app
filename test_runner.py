"""runner"""
import unittest

from tests import test_class_AB
from tests import test_class_Email
from tests import test_class_Phone
from tests import test_class_Record
from tests import test_class_User
from tests import test_utils
from tests import test_validation

ABTestSuite = unittest.TestSuite()
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_AB.TestAddressBook))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Email.TestEmail))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Phone.TestPhone))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_Record.TestRecord))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class_User.TestUser))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_validation.TestValidation))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_utils.TestPrintContacts))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(ABTestSuite)
