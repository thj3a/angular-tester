# Usage Example

This document shows how to use the Angular Tester with a real Angular application.

## Prerequisites

1. Set up the environment variables:
   ```bash
   export LLM_API_URL="https://your-llm-api-endpoint.com/generate"
   export COVERAGE_THRESHOLD=80
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Running the Tester

To run the tester on an Angular application:

```bash
python angular_tester.py example-angular-app/src
```

This will:
1. Find all component files in the specified directory
2. Generate tests for each component using the LLM API
3. Run the tests with coverage checking
4. Report results

## How It Works

For each component file found (e.g., `user-card.component.ts`), the tester will:

1. Call your LLM API with the component code to generate appropriate unit tests
2. Create or update the corresponding spec file (`user-card.component.spec.ts`)
3. Run `ng test` to execute the tests
4. Check that code coverage meets the specified threshold

## Integration with CI/CD

You can integrate this tool into your CI/CD pipeline:

```bash
# In your CI script
export LLM_API_URL="${{ secrets.LLM_API_URL }}"
export COVERAGE_THRESHOLD=85
python angular_tester.py src/
```

## Customization

You can customize the behavior by modifying environment variables:

- `COVERAGE_THRESHOLD`: Minimum code coverage percentage (default: 80)
- `LLM_API_URL`: The endpoint for your LLM API

## API Requirements

Your LLM API should accept POST requests with JSON payload:
```json
{
  "prompt": "string",
  "max_tokens": 2000,
  "temperature": 0.3
}
```

And return JSON with either:
- A `choices` array with a `text` field, or
- A `text` field directly

Example response formats:
```json
{
  "choices": [
    {
      "text": "generated test code here"
    }
  ]
}
```

or

```json
{
  "text": "generated test code here"
}
```