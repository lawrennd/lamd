import os
import subprocess

def test_documentation_build():
    # Check if the Sphinx configuration file exists
    assert os.path.exists('conf.py'), "The 'conf.py' file does not exist."

    # Check if the index.rst file exists
    assert os.path.exists('index.rst'), "The 'index.rst' file does not exist."

    # Attempt to build the documentation
    result = subprocess.run(['sphinx-build', '-b', 'html', '.', '_build/html'], capture_output=True, text=True)
    assert result.returncode == 0, f"Documentation build failed with error: {result.stderr}"

if __name__ == '__main__':
    test_documentation_build() 