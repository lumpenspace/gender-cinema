import unittest

if __name__ == '__main__':
    # Define the test directory
    test_dir = 'test'
    # Create a test suite combining all the test cases
    suite = unittest.TestLoader().discover(test_dir)
    # Run the test suite
    unittest.TextTestRunner(verbosity=2).run(suite)
