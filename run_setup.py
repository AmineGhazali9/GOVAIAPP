#!/usr/bin/env python3
"""Execute setup_structure.py to create app/core directory and files."""

import subprocess
import sys
import os

# Change to project directory
os.chdir(r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP')

# Run the setup_structure.py script
try:
    result = subprocess.run([sys.executable, 'setup_structure.py'], 
                          capture_output=True, 
                          text=True,
                          check=False)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
except Exception as e:
    print(f"Error running setup_structure.py: {e}", file=sys.stderr)
    sys.exit(1)
