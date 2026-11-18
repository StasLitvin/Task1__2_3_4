import sys

def shaves(who, whom):
    """«Брадобрей бреет тех и только тех, кто не бреется сам»."""
    if who == "брадобрей":
        return not shaves(whom, whom)
    return False


sys.setrecursionlimit(200)
print("1. Наивная модель: бреет ли брадобрей сам себя?")
try:
    print(shaves("брадобрей", "брадобрей"))
except RecursionError:
    print("   RecursionError: ответ зависит сам от себя, решения нет (противоречие)")

CLASS_NAMES = {
    1: "брадобрей, нужно бритьё",
    2: "брадобрей, бритьё не нужно",
    3: "житель, нужно бритьё, сам не бреется",
    4: "житель, нужно бритьё, бреется сам",
    5: "житель, бритьё не нужно",
    6: "нелегал",
}


class Resident:
    def __init__(self, name, shave_class, beard_time=None):
        self.name = name
        self.shave_class = shave_class
        self.current_class = shave_class
        self.beard_time = beard_time
        self.last_shave = None
        self.unshaven = shave_class in (1, 3, 4)

    def increase_time(self, now):
        """Обновить свойства, зависящие от времени."""
        if self.last_shave is None or self.unshaven:
            return
        if now - self.last_shave >= self.beard_time:
            self.unshaven = True
            self.current_class = self.shave_class

    def mark_shaved(self, now, new_class):
        self.last_shave = now
        self.unshaven = False
        self.current_class = new_class

    def shave_self(self, now):
        """Житель 4-го класса бреется сам, номер класса не меняется."""
        if self.current_class == 4 and self.unshaven:
            self.mark_shaved(now, 4)
            return True
        return False


class Barber(Resident):
    def shave(self, village):
        """Метод «брею»: бреет жителей текущих классов 1 и 3."""
        done = []
        for r in village.residents:
            if r.current_class == 1:
                r.mark_shaved(village.time, 2)
                done.append(r.name)
            elif r.current_class == 3:
                r.mark_shaved(village.time, 5)
                done.append(r.name)
        return done


class Village:
    def __init__(self, time=0):
        self.time = time
        self.residents = []

    def register(self, resident):
        """«Зарегистрировать жителя»."""
        self.residents.append(resident)
        return resident

    def increase_time(self, dt=1):
        """«Увеличить текущее время» для деревни и всех жителей."""
        self.time += dt
        for r in self.residents:
            r.increase_time(self.time)

    def shaving(self):
        """«Бреемся»: брадобреи бреют, жители 4-го класса бреются сами."""
        log = []
        for r in self.residents:
            if r.shave_class in (1, 2):
                shaved = r.shave(self)
                if shaved:
                    log.append(f"{r.name} побрил(а): {', '.join(shaved)}")
        for r in self.residents:
            if r.shave_self(self.time):
                log.append(f"{r.name} побрился сам")
        return log

    def check(self):
        """Проверка на противоречие: брадобрей не бреет тех, кто бреется сам."""
        for r in self.residents:
            assert not (r.shave_class == 4 and r.current_class in (2, 5)), r.name
            assert r.current_class in CLASS_NAMES

    def show(self):
        return "  ".join(f"{r.name}={r.current_class}" for r in self.residents)

    def unshaven_names(self):
        return ", ".join(r.name for r in self.residents if r.unshaven) or "нет"


village = Village()
village.register(Barber("Иван", 1, beard_time=2))
village.register(Barber("Марья", 2))
village.register(Resident("Пётр", 3, beard_time=3))
village.register(Resident("Семён", 3, beard_time=2))
village.register(Resident("Алексей", 4, beard_time=1))
village.register(Resident("Анна", 5))
village.register(Resident("Ваня", 5))
village.register(Resident("Гость", 6))

print("\n2. Модель с классами, моделирование 6 суток")
print("   Классы бритья: " + "  ".join(f"{r.name}={r.shave_class}" for r in village.residents))
for day in range(1, 7):
    village.increase_time()
    print(f"\n   Сутки {day}. Небриты утром: {village.unshaven_names()}")
    for line in village.shaving():
        print("     " + line)
    village.check()
    print("     Текущие классы: " + village.show())
print("\n   Противоречий не обнаружено: бреет ли брадобрей себя, "
      "определяется его текущим классом.")
