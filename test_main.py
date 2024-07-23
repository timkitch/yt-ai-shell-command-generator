import unittest
from unittest.mock import patch
from main import select_shell

class TestSelectShell(unittest.TestCase):
    @patch('builtins.input')
    def test_select_shell_valid_input(self, mock_input):
        mock_input.return_value = '2'
        result = select_shell(input_func=input)
        self.assertEqual(result, 'powershell')

    @patch('builtins.input')
    def test_select_shell_invalid_then_valid_input(self, mock_input):
        mock_input.side_effect = ['4', '1']
        result = select_shell(input_func=input)
        self.assertEqual(result, 'cmd')

    @patch('builtins.input')
    def test_select_shell_custom_shells(self, mock_input):
        mock_input.return_value = '1'
        result = select_shell(shells=['zsh', 'fish'], input_func=input)
        self.assertEqual(result, 'zsh')

if __name__ == '__main__':
    unittest.main()
