import math
import random

alf1 = 15.0
m1 = 9.0
g1 = 9.81

D_ALF = 0.5
D_M = 0.5
D_G = 0.02


def force(m1, g1, alf1):
    """Сила в ньютонах; масса в граммах, угол в градусах."""
    alf = math.pi * alf1 / 180
    return m1 * g1 * math.cos(alf) / 1000


F = force(m1, g1, alf1)
alf = math.pi * alf1 / 180
print("1. Расчёт силы")
print(f"   F = m*g*cos(alf) = {F:.6f} Н")

dalf = D_ALF / alf1
dm = D_M / m1
dg = D_G / g1
dF_hint = dm + dg + math.tan(alf) * dalf
print("\n2. Оценка по формуле из указаний")
print(f"   dm = {dm:.5f}, dg = {dg:.5f}, dalf = {dalf:.5f}")
print(f"   dF = dm + dg + tg(alf)*dalf = {dF_hint:.5f} ({dF_hint*100:.2f} %)")
print(f"   Абсолютная ошибка = {F*dF_hint:.6f} Н")

d_cos = math.tan(alf) * math.radians(D_ALF)
dF_diff = dm + dg + d_cos
print("\n3. Оценка через полный дифференциал ln F")
print(f"   вклад угла = tg(alf)*D_alf[рад] = {d_cos:.5f}")
print(f"   dF = {dF_diff:.5f} ({dF_diff*100:.2f} %)")
print(f"   Абсолютная ошибка = {F*dF_diff:.6f} Н")

print("\n4. Вклад каждой переменной (варьирование F1)")
print(f"   {'переменная':<12}{'F(-)':>12}{'F(+)':>12}{'отн. вклад, %':>16}")
rows = [
    ("m", force(m1 - D_M, g1, alf1), force(m1 + D_M, g1, alf1)),
    ("g", force(m1, g1 - D_G, alf1), force(m1, g1 + D_G, alf1)),
    ("alf", force(m1, g1, alf1 + D_ALF), force(m1, g1, alf1 - D_ALF)),
]
for name, f_lo, f_hi in rows:
    contrib = (f_hi - f_lo) / 2 / F * 100
    print(f"   {name:<12}{f_lo:>12.6f}{f_hi:>12.6f}{contrib:>16.3f}")

F_min = force(m1 - D_M, g1 - D_G, alf1 + D_ALF)
F_max = force(m1 + D_M, g1 + D_G, alf1 - D_ALF)
print("\n5. Граничные значения (все погрешности в одну сторону)")
print(f"   F_min = {F_min:.6f} Н, F_max = {F_max:.6f} Н")
print(f"   F = {F:.5f} (-{(F-F_min)/F*100:.2f} % / +{(F_max-F)/F*100:.2f} %)")

random.seed(1)
N = 200_000
vals = [force(random.uniform(m1 - D_M, m1 + D_M),
              random.uniform(g1 - D_G, g1 + D_G),
              random.uniform(alf1 - D_ALF, alf1 + D_ALF)) for _ in range(N)]
mean = sum(vals) / N
std = math.sqrt(sum((v - mean) ** 2 for v in vals) / (N - 1))
print(f"\n6. Метод Монте-Карло, N = {N}")
print(f"   среднее F = {mean:.6f} Н, СКО = {std:.6f} Н ({std/mean*100:.2f} %)")
print(f"   min = {min(vals):.6f} Н, max = {max(vals):.6f} Н")

print("\n7. Сила для разных значений g")
for city, g in [("Алма-Ата", 9.78), ("Рим", 9.80), ("Москва", 9.81), ("Осло", 9.819)]:
    print(f"   {city:<10} g = {g:<6} F = {force(m1, g, alf1):.6f} Н")

print(f"\nОтвет: F = {F:.4f} ± {F*dF_hint:.4f} Н (оценка по указаниям, {dF_hint*100:.1f} %)")
