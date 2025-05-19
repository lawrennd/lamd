# Integration Tests for LAMD

This directory will contain integration tests for the LAMD project. Integration tests verify that different components of the system work together correctly.

## Future Test Ideas

Future integration tests could include:

1. *End-to-end tests* that process a markdown file through the entire pipeline
2. *GPP integration* tests that verify correct interaction with the actual GPP preprocessor
3. *Configuration loading* tests that verify the correct loading of configuration files
4. *Command-line tool tests* that verify the CLI works as expected

## Example Integration Test Structure

Integration tests should follow this pattern:

```python
"""Integration test example for the LAMD pipeline."""

import os
import tempfile
import pytest
import subprocess

class TestIntegration:
    """Integration tests for the LAMD pipeline."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        # Create test files and directories here
        
    def teardown_method(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
    
    def test_end_to_end_pipeline(self):
        """Test the entire processing pipeline."""
        # 1. Create a test markdown file
        # 2. Run the mdpp command on it
        # 3. Verify the output matches expectations
        pass
```

## Running Integration Tests

To run integration tests:

```bash
# Run all integration tests
pytest tests/integration/

# Run specific integration test
pytest tests/integration/test_specific.py
``` 