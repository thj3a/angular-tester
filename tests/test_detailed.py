import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.main import AngularTester


class TestAngularTesterDetailed:
    """Detailed tests for AngularTester methods"""
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_run_method_success(self):
        """Test the run method with successful execution"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        tester.llm_api_url = "https://test.api.com"
        
        # Mock all the methods that would actually run
        tester.process_components = MagicMock(return_value=True)
        tester.run_tests = MagicMock(return_value=True)
        tester.check_coverage = MagicMock(return_value=True)
        
        # Test the run method
        result = tester.run("./test")
        assert result == True
        
        # Verify that the methods were called
        tester.process_components.assert_called_once_with("./test")
        tester.run_tests.assert_called_once()
        tester.check_coverage.assert_called_once()
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_run_method_process_components_failure(self):
        """Test the run method when process_components fails"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        tester.llm_api_url = "https://test.api.com"
        
        # Mock process_components to return False
        tester.process_components = MagicMock(return_value=False)
        tester.run_tests = MagicMock(return_value=True)
        tester.check_coverage = MagicMock(return_value=True)
        
        # Test the run method
        result = tester.run("./test")
        assert result == False
        
        # Verify that only process_components was called
        tester.process_components.assert_called_once_with("./test")
        tester.run_tests.assert_not_called()
        tester.check_coverage.assert_not_called()
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_run_method_run_tests_failure(self):
        """Test the run method when run_tests fails"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        tester.llm_api_url = "https://test.api.com"
        
        # Mock run_tests to return False
        tester.process_components = MagicMock(return_value=True)
        tester.run_tests = MagicMock(return_value=False)
        tester.check_coverage = MagicMock(return_value=True)
        
        # Test the run method
        result = tester.run("./test")
        assert result == False
        
        # Verify that the methods were called
        tester.process_components.assert_called_once_with("./test")
        tester.run_tests.assert_called_once()
        tester.check_coverage.assert_not_called()
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_run_method_check_coverage_failure(self):
        """Test the run method when check_coverage fails"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        tester.llm_api_url = "https://test.api.com"
        
        # Mock check_coverage to return False
        tester.process_components = MagicMock(return_value=True)
        tester.run_tests = MagicMock(return_value=True)
        tester.check_coverage = MagicMock(return_value=False)
        
        # Test the run method
        result = tester.run("./test")
        assert result == False
        
        # Verify that the methods were called
        tester.process_components.assert_called_once_with("./test")
        tester.run_tests.assert_called_once()
        tester.check_coverage.assert_called_once()