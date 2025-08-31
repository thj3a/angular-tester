# Angular Tester

A Python application that uses LLMs to automatically generate and run unit tests for Angular applications.

## Features

- Automatically finds Angular component files (.component.ts)
- Generates comprehensive unit tests using an LLM via API
- Runs the generated tests using Angular CLI
- Checks code coverage against a configurable threshold
- Updates existing test files or creates new ones

## Requirements

- Python 3.8+
- Angular CLI
- Access to an LLM API (via URL)

## Installation

You can install the package in one of the following ways:

### Option 1: Install from PyPI (when published)
```bash
pip install angular-tester
```

### Option 2: Install from source
```bash
git clone <repository-url>
cd angular-tester
pip install .
```

### Option 3: Install in development mode
```bash
git clone <repository-url>
cd angular-tester
pip install -e .
```

### Option 4: Install dependencies manually
```bash
pip install -r requirements.txt
```

## Configuration

The application requires the following environment variables:

- `LLM_API_URL` - The URL to the LLM API endpoint
- `COVERAGE_THRESHOLD` - Minimum coverage percentage (default: 80)

## Usage

After installation, you can use the `angular-tester` command:

1. Set the required environment variables:
   ```bash
   export LLM_API_URL="https://your-llm-api.com/generate"
   export COVERAGE_THRESHOLD=80
   ```

2. Run the tester:
   ```bash
   angular-tester [directory]
   ```

   If no directory is specified, it will default to `./src`

## How It Works

1. The application scans the specified directory for Angular component files (.component.ts)
2. For each component file, it:
   - Calls the LLM API to generate appropriate unit tests
   - Creates or updates the corresponding .component.spec.ts file
3. Runs all tests using Angular CLI
4. Checks code coverage against the specified threshold
5. Reports results

## Example

```bash
# Set environment variables
export LLM_API_URL="https://api.openai.com/v1/completions"
export COVERAGE_THRESHOLD=85

# Run the tester on the src/app directory
angular-tester src/app
```

## Development

To run tests:
```bash
python -m pytest tests/
```

To build the package:
```bash
python -m build
```