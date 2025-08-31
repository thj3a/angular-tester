import os
import json
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration for the Angular Tester application"""
    
    def __init__(self):
        self.default_config = {
            "coverage_threshold": 80,
            "llm_timeout": 30,
            "max_tokens": 2000,
            "temperature": 0.3,
            "custom_templates": {},
            "excluded_files": [],
            "included_files": ["*.component.ts"],
            "test_file_suffix": ".spec.ts"
        }
        self.config = self.default_config.copy()
    
    def load_config(self, directory: str = ".") -> Dict[str, Any]:
        """Load configuration from supported config files"""
        # Look for config files in order of preference
        config_files = [
            os.path.join(directory, "angular-tester.config.js"),
            os.path.join(directory, ".angulartesterrc"),
            os.path.join(directory, ".angulartesterrc.json"),
            os.path.join(directory, ".angulartesterrc.yaml"),
            os.path.join(directory, ".angulartesterrc.yml")
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    if config_file.endswith(".js"):
                        # For JavaScript config files, we'll need a different approach
                        # For now, we'll skip JS files and focus on JSON/YAML
                        continue
                    elif config_file.endswith((".json", ".yaml", ".yml")) or ".angulartesterrc" in config_file:
                        config = self._load_json_config(config_file)
                        if config:
                            self.config.update(config)
                            break
                except Exception as e:
                    print(f"Warning: Could not load config file {config_file}: {str(e)}")
        
        return self.config
    
    def _load_json_config(self, config_file: str) -> Optional[Dict[str, Any]]:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in config file {config_file}: {str(e)}")
            return None
        except Exception as e:
            print(f"Warning: Could not read config file {config_file}: {str(e)}")
            return None
    
    def get(self, key: str, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def get_custom_template(self, component_type: str) -> Optional[str]:
        """Get a custom template for a specific component type"""
        return self.config.get("custom_templates", {}).get(component_type)