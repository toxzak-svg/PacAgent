# Test Suite Documentation

## Overview

The Backpack test suite provides comprehensive coverage of all modules using pytest. The tests are organized by module and include unit tests, integration tests, and error handling tests.

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_crypto.py

# Run specific test class
pytest tests/test_crypto.py::TestEncryptData

# Run specific test function
pytest tests/test_crypto.py::TestEncryptData::test_encrypt_data_basic
```

### With Coverage

```bash
# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Then open htmlcov/index.html in your browser

# Generate XML coverage report (for CI/CD)
pytest --cov=src --cov-report=xml
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run slow tests
pytest -m slow
```

## Test Structure

### test_crypto.py
Tests for encryption and decryption functionality:
- Key derivation (PBKDF2)
- Data encryption
- Data decryption
- Error handling (wrong passwords, corrupted data)
- Input validation
- Edge cases (empty strings, unicode, special characters)

**Test Classes:**
- `TestDeriveKey`: Key derivation tests
- `TestEncryptData`: Encryption tests
- `TestDecryptData`: Decryption tests
- `TestCryptoValidation`: Input validation tests

### test_keychain.py
Tests for OS keychain integration:
- Storing keys
- Retrieving keys
- Listing keys
- Deleting keys
- Registry management
- Integration workflows

**Test Classes:**
- `TestStoreKey`: Key storage tests
- `TestGetKey`: Key retrieval tests
- `TestListKeys`: Key listing tests
- `TestRegisterKey`: Registry management tests
- `TestDeleteKey`: Key deletion tests
- `TestKeychainIntegration`: Integration tests

### test_agent_lock.py
Tests for agent.lock file management:
- File creation
- File reading
- Memory updates
- Required keys extraction
- Error handling (missing files, wrong keys)
- Multiple agent management

**Test Classes:**
- `TestAgentLockInit`: Initialization tests
- `TestAgentLockCreate`: File creation tests
- `TestAgentLockRead`: File reading tests
- `TestAgentLockUpdateMemory`: Memory update tests
- `TestAgentLockGetRequiredKeys`: Key extraction tests
- `TestAgentLockIntegration`: Integration tests

### test_cli.py
Tests for CLI command execution:
- Init command
- Run command
- Key management commands
- Help commands
- Full workflow integration

**Test Classes:**
- `TestCLIInit`: Init command tests
- `TestCLIRun`: Run command tests
- `TestCLIKey`: Key management tests
- `TestCLIHelp`: Help command tests
- `TestCLIIntegration`: Integration tests

### test_exceptions.py
Tests for custom exception classes:
- Exception inheritance
- Error messages
- Exception properties

**Test Classes:**
- `TestBackpackError`: Base exception tests
- `TestCryptoErrors`: Cryptographic exception tests
- `TestKeychainErrors`: Keychain exception tests
- `TestAgentLockErrors`: Agent lock exception tests
- `TestValidationErrors`: Validation exception tests

## Test Fixtures

Fixtures are defined in `conftest.py`:

- `temp_dir`: Creates temporary directory for test files
- `test_agent_lock_path`: Path to test agent.lock file
- `test_master_key`: Test master key for encryption
- `sample_credentials`: Sample credentials dictionary
- `sample_personality`: Sample personality dictionary
- `sample_memory`: Sample memory dictionary
- `mock_keyring`: Mocks OS keyring for testing
- `clean_env`: Cleans environment variables

## Mocking

The test suite uses `pytest-mock` for mocking:

- **OS Keychain**: Mocked to avoid requiring actual keychain access
- **File System**: Uses temporary directories
- **Environment Variables**: Cleaned between tests

## Coverage Goals

Current coverage targets:
- **Overall**: > 80%
- **Core modules**: > 90% (crypto, keychain, agent_lock)
- **CLI**: > 70% (some interactive parts are harder to test)

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=src --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Writing New Tests

When adding new functionality:

1. **Add tests in appropriate file** or create new test file
2. **Follow naming convention**: `test_<module_name>.py`
3. **Use descriptive test names**: `test_<functionality>_<scenario>`
4. **Use fixtures** from `conftest.py` when possible
5. **Test both success and failure cases**
6. **Update this README** if adding new test categories

### Example Test

```python
def test_new_feature_basic(fixture_name):
    """Test basic functionality of new feature."""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

## Troubleshooting

### Import Errors
If you see import errors, ensure:
- Dependencies are installed: `pip install -r requirements.txt`
- Python path includes project root
- Virtual environment is activated

### Keychain Errors
Keychain tests use mocks, so they should work without actual keychain access. If you see keychain errors:
- Check that `mock_keyring` fixture is being used
- Verify keyring mocking in `conftest.py`

### File Permission Errors
Tests use temporary directories that are cleaned up automatically. If you see permission errors:
- Check that temp directory cleanup is working
- Verify no files are locked by other processes

## Test Statistics

Run `pytest --co -q` to see all collected tests without running them.

Run `pytest --cov=src --cov-report=term-missing` to see coverage statistics.
