def count_down(min):
    count = min
    while count > 0:
        yield count
        count -= 1

def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1


c_u = count_up_to(7)
c_d = count_down(5)

# for n in c_u:
#     print(n)
#
# for n in c_d:
#     print(n)

def combine(gen1, gen2):
    yield from gen1
    yield from gen2

c = combine(c_u, c_d)

for x in range(12):
    print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))
# print(next(c))