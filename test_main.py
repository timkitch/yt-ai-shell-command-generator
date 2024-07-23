import unittest
from unittest.mock import patch
from main import select_shell

class TestSelectShell(unittest.TestCase):
    @patch('click.echo')
    def test_select_shell_valid_input(self, mock_echo):
        with patch('builtins.input', return_value='2'):
            result = select_shell(input_func=input)
            self.assertEqual(result, 'powershell')

    @patch('click.echo')
    def test_select_shell_invalid_then_valid_input(self, mock_echo):
        with patch('builtins.input', side_effect=['4', '1']):
            result = select_shell(input_func=input)
            self.assertEqual(result, 'cmd')

    @patch('click.echo')
    def test_select_shell_custom_shells(self, mock_echo):
        with patch('builtins.input', return_value='1'):
            result = select_shell(shells=['zsh', 'fish'], input_func=input)
            self.assertEqual(result, 'zsh')

    @patch('click.echo')
    def test_select_shell_non_numeric_input(self, mock_echo):
        with patch('builtins.input', side_effect=['abc', '2']):
            result = select_shell(input_func=input)
            self.assertEqual(result, 'powershell')

if __name__ == '__main__':
    unittest.main()
