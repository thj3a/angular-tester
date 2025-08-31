import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.main import AngularTester


class TestCoverageFunctionality:
    """Tests for coverage checking functionality"""
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_check_coverage_with_high_coverage(self):
        """Test coverage check with high coverage percentage"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        
        # Mock the get_coverage_report method to return high coverage
        tester.get_coverage_report = MagicMock(return_value=95.5)
        
        result = tester.check_coverage()
        assert result == True
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_check_coverage_below_threshold(self):
        """Test coverage check with coverage below threshold"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 90
        
        # Mock the get_coverage_report method to return low coverage
        tester.get_coverage_report = MagicMock(return_value=85.0)
        
        result = tester.check_coverage()
        assert result == False
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_check_coverage_no_coverage_data(self):
        """Test coverage check when no coverage data is available"""
        tester = AngularTester.__new__(AngularTester)
        tester.coverage_threshold = 80
        
        # Mock the get_coverage_report method to return None
        tester.get_coverage_report = MagicMock(return_value=None)
        
        result = tester.check_coverage()
        assert result == False
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com", "COVERAGE_THRESHOLD": "75"})
    def test_coverage_threshold_from_env(self):
        """Test that coverage threshold is correctly loaded from environment"""
        tester = AngularTester()
        assert tester.coverage_threshold == 75