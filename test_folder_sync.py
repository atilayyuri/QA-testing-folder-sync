import unittest
import os
from folder_sync import InputTest

class TestInputTest(unittest.TestCase):

    def setUp(self):
        self.input_test = InputTest()

    def test_capitalize_string(self):
        self.assertEqual(self.input_test.capitalize_string('hello'), 'Hello')
        self.assertEqual(self.input_test.capitalize_string('World'), 'World')

    # def test_check_path_directory(self):
    #     path = os.path.dirname(os.path.abspath(__file__))
    #     path_source = self.input_test.check_path_directory(path, 'source')
    #     self.assertIsInstance(path_source, str)
    #     self.assertEqual(path_source, path)
    #
    # def test_check_path_file(self):
    #     file_path, file_mode = self.input_test.check_path_file('test.log')
    #     self.assertIsInstance(file_path, str)
    #     self.assertEqual(file_path, os.path.join(os.getcwd(), 'test.log'))
    #     self.assertEqual(file_mode, 'w')

    def test_get_user_input(self):
        source_path = os.path.dirname(os.path.abspath(__file__))
        replica_path = os.path.join(os.getcwd(), 'test_replica')
        log_path = os.path.join(os.getcwd(), 'test.log')

        user_input = ['\n'.join([source_path, replica_path, 'n', log_path, 'a', '5'])]

        with unittest.mock.patch('builtins.input', side_effect=user_input):
            self.input_test.get_user_input()

        self.assertEqual(self.input_test.path_source, source_path)
        self.assertEqual(self.input_test.path_replica, replica_path)
        self.assertEqual(self.input_test.sync_interval, 5)
        self.assertEqual(self.input_test.log_file_path, log_path)
        self.assertEqual(self.input_test.log_file_mode, 'a')

if __name__ == '__main__':
    unittest.main()