from TestUtils import *
import unittest


def testSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCharacteristic))
    suite.addTest(unittest.makeSuite(TestPoint))
    suite.addTest(unittest.makeSuite(TestVelocity))
    suite.addTest(unittest.makeSuite(TestAcceleration))
    return suite


if __name__ in "__main__":
    tests = testSuite()
    runner = unittest.TextTestRunner()
    runner.run(tests)
