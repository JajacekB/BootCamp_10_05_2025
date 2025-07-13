from decimal import localcontext, getcontext, Decimal, ROUND_DOWN

print(getcontext().rounding)

with localcontext() as ctx:
    ctx.rounding = ROUND_DOWN
    value = Decimal('2.3456').quantize('0.01')
    print("W lokalnym kontekście:", value)


print()