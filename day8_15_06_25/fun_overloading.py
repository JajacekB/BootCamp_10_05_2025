from functools import singledispatch

@singledispatch
def process(x):
    print("Defoult:", x)

@process.register(int)
def _(x):
    print("Int:", x)

@process.register(str)
def _(x):
    print("Str:", x)

process(42)
process("Hello")