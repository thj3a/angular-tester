import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.main import AngularTester, main


class TestMainFunction:
    """Tests for the main function"""
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    @patch("angular_tester.main.AngularTester")
    def test_main_function_success(self, mock_tester_class):
        """Test main function with successful execution"""
        # Mock the tester instance
        mock_tester_instance = MagicMock()
        mock_tester_instance.run.return_value = True
        mock_tester_class.return_value = mock_tester_instance
        
        # Test main function
        with patch("sys.argv", ["angular-tester", "/test/path"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(0)
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    @patch("angular_tester.main.AngularTester")
    def test_main_function_failure(self, mock_tester_class):
        """Test main function with failed execution"""
        # Mock the tester instance
        mock_tester_instance = MagicMock()
        mock_tester_instance.run.return_value = False
        mock_tester_class.return_value = mock_tester_instance
        
        # Test main function
        with patch("sys.argv", ["angular-tester", "/test/path"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(1)
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    @patch("angular_tester.main.AngularTester")
    def test_main_function_exception(self, mock_tester_class):
        """Test main function with exception"""
        # Mock the tester instance to raise an exception
        mock_tester_class.side_effect = Exception("Test error")
        
        # Test main function
        with patch("sys.argv", ["angular-tester", "/test/path"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(1)
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    @patch("angular_tester.main.AngularTester")
    def test_main_function_no_args(self, mock_tester_class):
        """Test main function with no arguments"""
        # Mock the tester instance
        mock_tester_instance = MagicMock()
        mock_tester_instance.run.return_value = True
        mock_tester_class.return_value = mock_tester_instance
        
        # Test main function with no args (should default to './src')
        with patch("sys.argv", ["angular-tester"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(0)
                mock_tester_instance.run.assert_called_once_with('./src')