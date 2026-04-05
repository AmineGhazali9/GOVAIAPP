import py_compile
import sys

files = [
    r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP\app\api\schemas.py',
    r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP\app\api\routes.py',
    r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP\app\api\main.py',
    r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP\app\rag\retriever.py',
    r'C:\Users\User\Documents\Repositories\Dev Dev GitHub Copilot\GOVAIAPP\app\agents\orchestrator.py'
]

for file in files:
    filename = file.split('\\')[-1]
    try:
        py_compile.compile(file, doraise=True)
        print(f'{filename}: OK')
    except py_compile.PyCompileError as e:
        print(f'{filename}: ERROR')
        print(str(e))
