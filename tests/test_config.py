import pytest
import os
import sys
import json
import tempfile
from unittest.mock import patch

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from angular_tester.config import ConfigManager


class TestConfigManager:
    """Tests for the ConfigManager class"""
    
    def setup_method(self):
        """Create a temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
    
    def test_load_default_config(self):
        """Test that default configuration is loaded when no config file exists"""
        config_manager = ConfigManager()
        config = config_manager.load_config(self.test_dir)
        
        # Check default values
        assert config['coverage_threshold'] == 80
        assert config['llm_timeout'] == 30
        assert config['max_tokens'] == 2000
        assert config['temperature'] == 0.3
        assert config['test_file_suffix'] == '.spec.ts'
    
    def test_load_json_config(self):
        """Test loading configuration from JSON file"""
        # Create a config file
        config_data = {
            "coverage_threshold": 90,
            "llm_timeout": 60,
            "max_tokens": 3000,
            "temperature": 0.5,
            "test_file_suffix": ".test.ts"
        }
        
        config_file = os.path.join(self.test_dir, ".angulartesterrc")
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config_manager = ConfigManager()
        config = config_manager.load_config(self.test_dir)
        
        # Check loaded values
        assert config['coverage_threshold'] == 90
        assert config['llm_timeout'] == 60
        assert config['max_tokens'] == 3000
        assert config['temperature'] == 0.5
        assert config['test_file_suffix'] == '.test.ts'
    
    def test_get_custom_template(self):
        """Test getting custom templates from configuration"""
        # Create a config file with custom templates
        config_data = {
            "custom_templates": {
                "UserCardComponent": "custom template content",
                "service": "service template content"
            }
        }
        
        config_file = os.path.join(self.test_dir, ".angulartesterrc")
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config_manager = ConfigManager()
        config_manager.load_config(self.test_dir)
        
        # Test getting custom templates
        user_card_template = config_manager.get_custom_template("UserCardComponent")
        service_template = config_manager.get_custom_template("service")
        unknown_template = config_manager.get_custom_template("UnknownComponent")
        
        assert user_card_template == "custom template content"
        assert service_template == "service template content"
        assert unknown_template is None
    
    def test_get_with_default(self):
        """Test getting configuration values with defaults"""
        config_manager = ConfigManager()
        config_manager.load_config(self.test_dir)
        
        # Test existing value
        coverage = config_manager.get('coverage_threshold', 75)
        assert coverage == 80  # Default from default_config
        
        # Test non-existing value with default
        unknown = config_manager.get('unknown_key', 'default_value')
        assert unknown == 'default_value'