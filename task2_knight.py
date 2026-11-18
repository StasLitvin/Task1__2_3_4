import math
import time
from decimal import Decimal, getcontext, ROUND_HALF_UP

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

B = 1_000_000.0
RATE = 0.07
DT = 2
YEAR = 365 * 24 * 3600
STEPS_YEAR = YEAR // DT

getcontext().prec = 50


def exact(t):
    """Эталон: B * 1.07^(t/YEAR), вычисленный в Decimal с 50 знаками."""
    return Decimal(B) * (Decimal(1) + Decimal("0.07")) ** (Decimal(t) / Decimal(YEAR))


A32 = np.float32(1.07) ** np.float32(DT / YEAR)
print("1. Алгоритм New = A*Old в float32")
print(f"   A - 1 (точно)   = {1.07 ** (DT / YEAR) - 1:.3e}")
print(f"   A в float32     = {A32!r}, A == 1: {A32 == np.float32(1.0)}")
print(f"   машинный эпсилон float32 = {np.finfo(np.float32).eps:.3e}")
old = np.float32(B)
for _ in range(24 * 3600 // DT):
    old = A32 * old
print(f"   через сутки: {float(old):.2f} руб., должно быть {float(exact(24*3600)):.2f} руб.")

A = 1.07 ** (DT / YEAR)
print("\n2. Алгоритм New = A*Old в float64 (1 год, "
      f"{STEPS_YEAR} шагов)")
checkpoints = {3600 // DT: "1 час", 24 * 3600 // DT: "1 сутки",
               7 * 24 * 3600 // DT: "1 неделя", 30 * 24 * 3600 // DT: "30 суток",
               182 * 24 * 3600 // DT: "182 суток", STEPS_YEAR: "1 год"}
hist_t, hist_err = [], []
old = B
t0 = time.perf_counter()
for k in range(1, STEPS_YEAR + 1):
    old = A * old
    if k % 50_000 == 0 or k in checkpoints:
        ref = exact(k * DT)
        err = abs(Decimal(old) - ref) / ref
        hist_t.append(k * DT / 86400)
        hist_err.append(float(err))
        if k in checkpoints:
            print(f"   {checkpoints[k]:<10} рыцарь: {old:16.6f}  эталон: {float(ref):16.6f}"
                  f"  отн. ошибка: {float(err):.2e}")
print(f"   время счёта: {time.perf_counter() - t0:.2f} с")

C = math.log(1 + RATE) / YEAR
print("\n3. Расчёт по формуле y = B*exp(C*t), C = ln(1.07)/T")
print(f"   C = {C:.6e} 1/с")
for t, name in [(24 * 3600, "1 сутки"), (YEAR, "1 год"), (10 * YEAR, "10 лет")]:
    y = B * math.exp(C * t)
    ref = exact(t)
    print(f"   {name:<8} y = {y:18.6f}  эталон: {float(ref):18.6f}"
          f"  отн. ошибка: {float(abs(Decimal(y) - ref) / ref):.2e}")

print("\n4. По договору: проценты раз в месяц (7 %/12), округление до копеек")
bal = Decimal("1000000.00")
month_rate = Decimal("0.07") / 12
for month in range(1, 13):
    bal = (bal * (1 + month_rate)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    if month in (1, 6, 12):
        print(f"   месяц {month:>2}: {bal} руб.")
print("   Между датами начисления сумма не меняется, пересчитывать каждые 2 с не нужно.")

plt.figure(figsize=(8, 4.5))
plt.plot(hist_t, hist_err)
plt.xlabel("Время хранения вклада, сутки")
plt.ylabel("Относительная ошибка")
plt.title("Накопление ошибки в алгоритме New = A*Old (float64)")
plt.grid(True)
plt.tight_layout()
plt.savefig("knight_error.png", dpi=150)
print("\nГрафик сохранён в knight_error.png")
