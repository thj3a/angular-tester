import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.main import AngularTester


class TestAngularTesterIntegration:
    """Integration tests using real Angular component examples"""
    
    def setup_method(self):
        """Create a temporary directory with test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.component_file = os.path.join(self.test_dir, "user-card.component.ts")
        self.test_file = os.path.join(self.test_dir, "user-card.component.spec.ts")
        
        # Copy our fixture files
        shutil.copy(
            os.path.join(os.path.dirname(__file__), "fixtures/sample.component.ts"),
            self.component_file
        )
        
    def teardown_method(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    @patch.dict(os.environ, {"LLM_API_URL": "https://test.api.com"})
    def test_find_component_files_with_real_structure(self):
        """Test finding component files in a real directory structure"""
        tester = AngularTester()
        
        # Test that our component file is found
        components = tester.find_component_files(self.test_dir)
        assert len(components) == 1
        assert components[0] == self.component_file
    
    def test_find_test_file_conversion(self):
        """Test converting component file path to test file path"""
        tester = AngularTester.__new__(AngularTester)
        test_file = tester.find_test_file(self.component_file)
        assert test_file == self.test_file
    
    @patch("angular_tester.main.requests.post")
    def test_generate_test_content_with_real_component(self, mock_post):
        """Test generating test content for a real Angular component"""
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock the API response with realistic test content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "text": "import { ComponentFixture, TestBed } from '@angular/core/testing';\n\ndescribe('UserCardComponent', () => {\n  let component: UserCardComponent;\n  let fixture: ComponentFixture<UserCardComponent>;\n\n  beforeEach(async () => {\n    await TestBed.configureTestingModule({\n      imports: [UserCardComponent]\n    }).compileComponents();\n  });\n\n  it('should create', () => {\n    expect(component).toBeTruthy();\n  });\n});"
            }]
        }
        mock_post.return_value = mock_response
        
        # Read the actual component content
        with open(self.component_file, 'r') as f:
            component_content = f.read()
        
        result = tester.generate_test_content(self.component_file)
        assert "UserCardComponent" in result
        assert "should create" in result
        assert "TestBed.configureTestingModule" in result
    
    @patch("angular_tester.main.requests.post")
    def test_create_or_update_test_with_cleanup(self, mock_post):
        """Test creating test file with content cleanup"""
        tester = AngularTester.__new__(AngularTester)
        tester.llm_api_url = "https://test.api.com"
        
        # Mock the API response with content that has artifacts
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "text": "*/\nimport { ComponentFixture, TestBed } from '@angular/core/testing';\ndescribe('UserCardComponent', () => {\n  it('should create', () => {\n    expect(true).toBe(true);\n  });\n});"
            }]
        }
        mock_post.return_value = mock_response
        
        # Test that the file is created and cleaned up
        with patch("builtins.open", mock_open()) as mock_file:
            result = tester.create_or_update_test(self.component_file)
            assert result == True
            
            # Check that open was called to write the file
            mock_file.assert_called()
            
            # Get the written content
            handle = mock_file()
            written_content = ''.join(call.args[0] for call in handle.write.call_args_list)
            
            # Verify cleanup removed the stray characters
            assert not written_content.startswith("*/")
            assert "UserCardComponent" in written_content

    def test_find_component_files_excludes_spec_files(self):
        """Test that spec files are excluded from component search"""
        tester = AngularTester.__new__(AngularTester)
        
        # Create a mock directory structure
        with patch("angular_tester.main.os.walk") as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], [
                    "user-card.component.ts",
                    "user-card.component.spec.ts",
                    "other.component.ts",
                    "utils.ts"
                ])
            ]
            
            components = tester.find_component_files(self.test_dir)
            assert len(components) == 2
            assert any("user-card.component.ts" in path for path in components)
            assert any("other.component.ts" in path for path in components)
            assert not any("spec.ts" in path for path in components)