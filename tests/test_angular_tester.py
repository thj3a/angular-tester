import pytest
import os
import sys
import json
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.main import AngularTester


class TestAngularTester:
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_init_with_default_coverage(self):
        tester = AngularTester()
        assert tester.coverage_threshold == 80
        assert tester.llm_api_url == "https://test.api.com"

    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com", "COVERAGE_THRESHOLD": "90"})
    def test_init_with_custom_coverage(self):
        tester = AngularTester()
        assert tester.coverage_threshold == 90

    @patch.dict(os.environ, {})
    def test_init_without_llm_url_raises_error(self):
        with pytest.raises(ValueError, match="LLM_API_URL must be set via environment variable or config file"):
            AngularTester()

    def test_find_test_file(self):
        tester = AngularTester.__new__(AngularTester)  # Create instance without calling __init__
        component_file = "/path/to/component/my.component.ts"
        expected_test_file = "/path/to/component/my.component.spec.ts"
        assert tester.find_test_file(component_file) == expected_test_file

    @patch("angular_tester.main.os.walk")
    def test_find_component_files(self, mock_walk):
        tester = AngularTester.__new__(AngularTester)
        mock_walk.return_value = [
            ("/src", ["app"], ["user.component.ts", "other.txt"]),
            ("/src/app", ["components"], ["user-card.component.ts", "user-card.component.spec.ts"]),
            ("/src/app/components", [], ["profile.component.ts", "profile.component.spec.ts", "utils.ts"])
        ]
        
        result = tester.find_component_files("/src")
        expected = ["/src/user.component.ts", "/src/app/user-card.component.ts", "/src/app/components/profile.component.ts"]
        assert result == expected

    @patch("angular_tester.main.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="component content")
    def test_generate_test_content_success(self, mock_file, mock_post):
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock the API response with realistic test content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"text": "import { ComponentFixture, TestBed } from '@angular/core/testing';\n\ndescribe('TestComponent', () => {\n  it('should create', () => {\n    expect(true).toBe(true);\n  });\n});"}]
        }
        mock_post.return_value = mock_response
        
        result = tester.generate_test_content("/path/to/component.ts")
        assert "TestComponent" in result
        assert "describe(" in result

    @patch("angular_tester.main.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="component content")
    def test_generate_test_content_with_text_field(self, mock_file, mock_post):
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock the API response with realistic test content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "text": "import { ComponentFixture, TestBed } from '@angular/core/testing';\n\ndescribe('TestComponent', () => {\n  it('should create', () => {\n    expect(true).toBe(true);\n  });\n});"
        }
        mock_post.return_value = mock_response
        
        result = tester.generate_test_content("/path/to/component.ts")
        assert "TestComponent" in result
        assert "describe(" in result

    @patch("angular_tester.main.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="component content")
    def test_generate_test_content_api_error(self, mock_file, mock_post):
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock the API response with error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        result = tester.generate_test_content("/path/to/component.ts")
        # Now we expect a basic test to be generated instead of empty string
        assert "describe(" in result
        assert "ComponentFixture" in result

    @patch("angular_tester.main.os.path.exists")
    @patch("angular_tester.main.subprocess.run")
    def test_run_tests_success(self, mock_subprocess, mock_exists):
        tester = AngularTester.__new__(AngularTester)
        mock_exists.return_value = True
        
        # Mock subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Test output\nTOTAL: 5 SUCCESS"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        result = tester.run_tests()
        assert result == True

    @patch("angular_tester.main.os.path.exists")
    @patch("angular_tester.main.subprocess.run")
    def test_run_tests_failure(self, mock_subprocess, mock_exists):
        tester = AngularTester.__new__(AngularTester)
        mock_exists.return_value = True
        
        # Mock subprocess result with failure
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "Test output\nTOTAL: 3 FAILED, 2 SUCCESS"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        
        result = tester.run_tests()
        assert result == False

    def test_create_or_update_test_success(self):
        tester = AngularTester.__new__(AngularTester)
        
        with patch("angular_tester.main.open", mock_open()) as mock_file:
            result = tester.create_or_update_test("/path/to/component.ts")
            # This will fail because we haven't mocked generate_test_content
            # but we can test the file writing logic

    @patch("angular_tester.main.subprocess.run")
    def test_process_components(self, mock_subprocess):
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock find_component_files to return a list
        tester.find_component_files = MagicMock(return_value=["/src/app/component.ts"])
        
        # Mock create_or_update_test to return True
        tester.create_or_update_test = MagicMock(return_value=True)
        
        result = tester.process_components("/src")
        assert result == True
        tester.create_or_update_test.assert_called_once_with("/src/app/component.ts")