# Configuration Example

This is an example of how to configure the Angular Tester application.

## Configuration File Formats

The Angular Tester supports multiple configuration file formats:

1. `.angulartesterrc` (JSON format)
2. `.angulartesterrc.json` (JSON format)
3. `angular-tester.config.js` (JavaScript format - coming soon)

## Example Configuration

```json
{
  "coverage_threshold": 85,
  "llm_timeout": 45,
  "max_tokens": 2500,
  "temperature": 0.2,
  "test_file_suffix": ".spec.ts",
  "custom_templates": {
    "UserCardComponent": "import { ComponentFixture, TestBed } from '@angular/core/testing';\n{{imports}}\n\ndescribe('{{component_name}}', () => {\n  let component: {{component_name}};\n  let fixture: ComponentFixture<{{component_name}}>;\n\n  beforeEach(async () => {\n    await TestBed.configureTestingModule({\n      imports: [{{component_name}}]\n    })\n    .compileComponents();\n    \n    fixture = TestBed.createComponent({{component_name}});\n    component = fixture.componentInstance;\n    fixture.detectChanges();\n  });\n\n  it('should create', () => {\n    expect(component).toBeTruthy();\n  });\n\n  // Custom template for UserCardComponent - add specific tests here\n  it('should display user information', () => {\n    // Add your custom test logic here\n    expect(component).toBeTruthy();\n  });\n});",
    "service": "import { TestBed } from '@angular/core/testing';\n{{imports}}\n\ndescribe('{{component_name}}', () => {\n  let service: {{component_name}};\n\n  beforeEach(() => {\n    TestBed.configureTestingModule({});\n    service = TestBed.inject({{component_name}});\n  });\n\n  it('should be created', () => {\n    expect(service).toBeTruthy();\n  });\n\n  // Custom template for services - add specific tests here\n});"
  },
  "excluded_files": [
    "node_modules/**",
    "dist/**",
    "*.d.ts"
  ],
  "included_files": [
    "*.component.ts",
    "*.service.ts"
  ]
}
```

## Configuration Options

### Core Options
- `coverage_threshold`: Minimum code coverage percentage (default: 80)
- `llm_timeout`: Timeout for LLM API requests in seconds (default: 30)
- `max_tokens`: Maximum tokens for LLM responses (default: 2000)
- `temperature`: LLM temperature setting (default: 0.3)
- `test_file_suffix`: Suffix for generated test files (default: ".spec.ts")

### Custom Templates
- `custom_templates`: Object mapping component/service types to custom template strings
  - Use `{{component_name}}` as a placeholder for the component name
  - Use `{{file_name}}` as a placeholder for the file name
  - Use `{{imports}}` as a placeholder for the import statements

### File Inclusion/Exclusion
- `excluded_files`: Array of glob patterns to exclude from processing
- `included_files`: Array of glob patterns to include for processing

## Environment Variables

You can also override configuration with environment variables:

```bash
export LLM_API_URL="http://your-llm-endpoint.com"
export COVERAGE_THRESHOLD=90
```

Environment variables take precedence over configuration file values.