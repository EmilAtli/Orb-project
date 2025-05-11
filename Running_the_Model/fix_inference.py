import fileinput
# Inserts a dummy compiler, since torch v2.0.1 doesn't have a compiler.

# block to insert.
block = '''if not hasattr(torch, "compiler"):
    class DummyCompiler:
        @staticmethod
        def disable(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
    torch.compiler = DummyCompiler()
'''

# Open inference.py for in-place editing.
with fileinput.input('./inference.py', inplace=True) as file:
    for line_number, line in enumerate(file, 1):
        print(line, end='')
        # After line 8 (which is "import torch"), block is inserted.
        if line_number == 8:
            print(block, end='')
