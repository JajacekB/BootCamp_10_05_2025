def allparams(a, b, /, c, **kwargs):
    print(a, b, c)
    print(kwargs)


allparams(1, 2, 3)
allparams(1, 2, c=9)
# allparams(a=1, b=2, c=8)
allparams(1, 2, c=9)
allparams(1, 2, c=9, a=8)
allparams(1, 2, 3, a=8, name="Radek")


print(111 * "+")


def allparams_all(a,b, /, c=43, *args, d=256, **kwargs):
    print(f"{a=}, {b=}")
    print(f" {c=}, {d=}")
    print(f' {args=}')
    print(f" {kwargs=}")


allparams_all(3, 4, )
allparams_all(1, 2, 3)
allparams_all(1, 2, c=90)
allparams_all(1, 2, 3, 2,4,5,6)
allparams_all(1, 2, 3, 2,3,4,5,6,7,8,9,10, d=100)
allparams_all(1, 2, 3, 2,3,4,5,6,7,8,9,10, d=100, name="Radek")
allparams_all(1, 2, 3, 2,3,4,5,6,7,8,9,10, d=100, name="Radek", a=89)

