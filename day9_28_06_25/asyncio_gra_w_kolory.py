import asyncio
import random
from colorama import Fore, Style, init

init(autoreset=True)

#c = (
#    "\033[0m,"
#    "\033[36m,"
#    "\033[31m,"
#    "\033[35m,"
#    "\033[33m,"
#    "\033[32m,"
#)

c= (
    Style.RESET_ALL,
    Fore.CYAN,
    Fore.RED,
    Fore.MAGENTA,
    Fore.YELLOW,
    Fore.GREEN,
)

async def makerandom(idx: int, threshold: int =6) -> int:
    print(f"{c[idx +1]} inicjalizacja makerandom({idx})")

    i = random.randint(0, 10)
    while i <= threshold:
        print(f"{c[idx + 1]} makerandom({idx}) <= {i} -> zbyt niska wartość> Powtórzenie")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)

    print(f"{c[idx + 1]} zakończono makerandom({idx}) == {i} -> {c[0]}")

    return i

async def main():
    res = await asyncio.gather(*(makerandom(i, 9 - 1) for i in range(5)))
    return res

if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3, r4, r5 = asyncio.run(main())
    print(f"\nWynik: {r1=}, {r2=}, {r3=}, {r4=}, {r5=}")