import random
from itertools import product

COINS = [2, 5]
P_LOSS = [0.5, 0.2]
LIMIT = 3

print("1. Перебор всех исходов")
print(f"   {'2 руб.':<10}{'5 руб.':<10}{'потеря':>7}{'P':>7}  мачеха")
p_ok = 0.0
for lost in product([False, True], repeat=len(COINS)):
    p = 1.0
    for flag, q in zip(lost, P_LOSS):
        p *= q if flag else 1 - q
    total = sum(c for c, flag in zip(COINS, lost) if flag)
    angry = total > LIMIT
    if not angry:
        p_ok += p
    yn = ["потеряна" if f else "цела" for f in lost]
    print(f"   {yn[0]:<10}{yn[1]:<10}{total:>7}{p:>7.2f}  "
          f"{'разозлится' if angry else 'махнёт рукой'}")
print(f"   P(подзатыльника не будет) = {p_ok:.2f}")
print(f"   P(подзатыльник)           = {1 - p_ok:.2f}")

random.seed(42)
print("\n2. Метод Монте-Карло")
for n in (100, 1_000, 10_000, 100_000, 1_000_000):
    ok = 0
    for _ in range(n):
        total = sum(c for c, q in zip(COINS, P_LOSS) if random.random() < q)
        if total <= LIMIT:
            ok += 1
    est = ok / n
    print(f"   N = {n:>9}: P = {est:.4f}, отклонение от точного {abs(est - p_ok):.4f}")
