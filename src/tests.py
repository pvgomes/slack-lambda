import commands
import unittest


# Here's our "unit".
def IsOdd(n):
    return n % 2 == 1

# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))


class HelpTests(unittest.TestCase):

    def testHelper(self):
        helpCommand = commands.Help()
        expected = 'This is the help with argument query'
        self.assertEqual(expected, helpCommand.execute('query'), "help msg is not the same")

def main():
    unittest.main()

if __name__ == '__main__':
    main()