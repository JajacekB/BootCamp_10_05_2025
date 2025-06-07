def allparams(a, b, /, c, **kwargs):
    print(a, b, c)
    print(kwargs)


allparams(1, 2, 3)
allparams(1, 2, c=9)
# allparams(a=1, b=2, c=8)
allparams(1, 2, c=9)
allparams(1, 2, c=9, a=8)
allparams(1, 2, 3, a=8, name="Radek")