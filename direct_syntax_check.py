#!/usr/bin/env python
import py_compile
import sys
import os

# Change to project directory
os.chdir(r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP')

files = [
    r'app\api\schemas.py',
    r'app\api\routes.py',
    r'app\api\main.py',
    r'app\rag\retriever.py',
    r'app\agents\orchestrator.py'
]

results = []
for file in files:
    filename = file.split('\\')[-1]
    try:
        py_compile.compile(file, doraise=True)
        results.append(f'{filename}: OK')
    except py_compile.PyCompileError as e:
        results.append(f'{filename}: ERROR\n{str(e)}')
    except Exception as e:
        results.append(f'{filename}: ERROR\n{str(e)}')

for result in results:
    print(result)
    print()
