#! /usr/bin/python
import sys
import unittest

if ('--help') in sys.argv:
    print('BBot Unit Tester')
    print('Usage:')
    print('  --test <list of options>')
    print('    Test only the code listed after test (seperate by commas')
    print('    ex: ./unittests.py --test api,BBot')

# Tests to Run
if ('--test' in sys.argv):
    tests=sys.argv[sys.argv.find('--test')+1].split(',')
else:
    tests=['api']

# Import test classes
if ('api' in tests):
    from unittests.test_api import TestAPI


# Run the loaded tests
if (__name__ == '__main__'):
    unittest.main()
