#! /usr/bin/python
'''Run unittests on BBot and some of its modules.'''
import sys
import unittest

if ('--help') in sys.argv:
    print('BBot Unit Tester')
    print('Usage:')
    print('  --test <list of options>')
    print('    Test only the code listed after test (seperate by commas')
    print('    ex: ./unittests.py --test api, BBot')

# Tests to Run
if ('--test' in sys.argv):
    tests = sys.argv[sys.argv.find('--test') + 1].split(', ')
else:
    tests = ['api', 'backends_async']

# Import test classes
if ('api' in tests):
    from unittests.test_api import TestAPI
if ('backends_async' in tests):
    # from unittests.test_backends_async import TestAsync
    print('tests for backends_async do not exist yet')

# Run the loaded tests
if (__name__ == '__main__'):
    unittest.main()
