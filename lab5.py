import weakref
from decimal import Decimal


def _to_decimal(value):
    """Точне десяткове представлення числа (без накопичення похибки float)."""
    return Decimal(str(value))


class Fish:
    def __init__(self, name, age, species, size, preferred_food,
                 is_aggressive, needed_space):
        self._check_name(name)
        self._check_positive("вік", age)
        self._check_positive("розмір", size)
        self._check_positive("потрібний об'єм", needed_space)
        self._name = name
        self._age = age
        self._species = species
        self._size = size
        self._preferred_food = preferred_food
        self._is_aggressive = is_aggressive
        self._needed_space = needed_space
        self._aquarium = None
        print(f"[Створено] Риба: {self._name}")

    def __del__(self):
        if hasattr(self, "_name"):
            print(f"[Видалено] Риба: {self._name}")

    @staticmethod
    def _check_name(name):
        if not isinstance(name, str):
            raise TypeError(
                f"ім'я має бути рядком, отримано {type(name).__name__}")
        if not name.strip():
            raise ValueError("ім'я не може бути порожнім")

    @staticmethod
    def _check_positive(label, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"{label} має бути числом, отримано {type(value).__name__}")
        if not value > 0:
            raise ValueError(
                f"{label} має бути додатним числом, отримано {value!r}")

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_species(self):
        return self._species

    def get_size(self):
        return self._size

    def get_preferred_food(self):
        return self._preferred_food

    def is_aggressive(self):
        return self._is_aggressive

    def get_needed_space(self):
        return self._needed_space

    def get_aquarium(self):
        return self._aquarium() if self._aquarium is not None else None

    def set_name(self, name):
        self._check_name(name)
        self._name = name

    def set_age(self, age):
        self._check_positive("вік", age)
        self._age = age

    def set_size(self, size):
        self._check_positive("розмір", size)
        self._size = size

    def set_preferred_food(self, food):
        self._preferred_food = food

    def set_aquarium(self, aquarium):
        self._aquarium = None if aquarium is None else weakref.ref(aquarium)

    def print_info(self):
        print(f" {self._name} | вид: {self._species} | вік: {self._age} | "
              f"розмір: {self._size} см | їжа: {self._preferred_food} | "
              f"агресивна: {'так' if self._is_aggressive else 'ні'} | "
              f"потрібен об'єм: {self._needed_space} м³")


class Aquarium:
    def __init__(self, name, total_volume):
        self._name = name
        self._total_volume = total_volume
        self._free_space = _to_decimal(total_volume)
        self._fishes = []
        print(f"[Створено] Акваріум: {self._name}")

    def __del__(self):
        print(f"[Видалено] Акваріум: {self._name}")

    def get_name(self): return self._name
    def get_total_volume(self): return self._total_volume
    def get_free_space(self): return float(self._free_space)
    def get_fishes(self): return list(self._fishes)

    def is_aggressive_aquarium(self):
        """True/False, якщо в акваріумі є риби; None, якщо він порожній."""
        if not self._fishes:
            return None
        return self._fishes[0].is_aggressive()

    def can_add(self, fish):
        current = fish.get_aquarium()
        if fish in self._fishes or current is self:
            return False, "риба вже є в цьому акваріумі"
        if current is not None:
            return False, f"риба вже в акваріумі «{current.get_name()}»"
        if _to_decimal(fish.get_needed_space()) > self._free_space:
            return False, "недостатньо вільного місця"
        kind = self.is_aggressive_aquarium()
        if kind is not None and kind != fish.is_aggressive():
            return False, "агресивних і неагресивних не можна тримати разом"
        return True, ""

    def add_fish(self, fish):
        ok, _ = self.can_add(fish)
        if not ok:
            return False
        self._fishes.append(fish)
        self._free_space -= _to_decimal(fish.get_needed_space())
        fish.set_aquarium(self)
        return True

    def remove_fish(self, fish):
        if fish not in self._fishes:
            return False
        self._fishes.remove(fish)
        self._free_space += _to_decimal(fish.get_needed_space())
        fish.set_aquarium(None)
        return True

    def get_top_largest(self, n=3):
        if n < 1:
            raise ValueError(f"n має бути не менше 1, отримано {n}")
        return sorted(
            self._fishes, key=lambda f: f.get_size(), reverse=True
        )[:n]

    def print_top_largest(self, n=3):
        print(f"Топ-{n} найбільших риб в акваріумі «{self._name}»:")
        top = self.get_top_largest(n)
        if not top:
            print(" (акваріум порожній)")
        for i, fish in enumerate(top, 1):
            print(f" {i}.", end="")
            fish.print_info()

    def print_info(self):
        print(f"\n=== Акваріум «{self._name}» ===")
        print(f"Загальний об'єм: {self._total_volume} м³, "
              f"вільно: {self._free_space:.2f} м³, риб: {len(self._fishes)}")
        for fish in self._fishes:
            fish.print_info()


def report_add(aquarium, fish):
    """Додає рибу і виводить результат (виведення тут, а не в add_fish)."""
    if aquarium.add_fish(fish):
        print(f" ✓ «{fish.get_name()}» додано до «{aquarium.get_name()}»")
    else:
        _, reason = aquarium.can_add(fish)
        print(f" ✗ Не вдалося додати «{fish.get_name()}» "
              f"до «{aquarium.get_name()}»: {reason}")


def main():
    shark = Fish("Біллі", 5, "Червонохвостий шарк", 15, "м'ясо", True, 0.30)
    piranha = Fish("Піра", 3, "Піранья", 20, "м'ясо", True, 0.25)
    cichlid = Fish("Цик", 2, "Цихліда", 12, "креветки", True, 0.15)
    guppy = Fish("Гуппі", 1, "Гуппі", 4, "пластівці", False, 0.05)
    neon = Fish("Неон", 1, "Неон", 3, "пластівці", False, 0.03)
    goldfish = Fish("Золотко", 4, "Золота рибка", 18, "водорості", False, 0.20)
    angel = Fish("Ангел", 2, "Скалярія", 14, "пластівці", False, 0.10)
    big_one = Fish("Гігант", 7, "Арапайма", 150, "риба", True, 5.0)

    aq1 = Aquarium("Хижак", 0.8)
    aq2 = Aquarium("Мирний", 0.4)
    aq3 = Aquarium("Малюк", 0.1)

    print("\n--- Додавання риб ---")
    for f in (shark, piranha, cichlid):
        report_add(aq1, f)
    report_add(aq1, guppy)
    report_add(aq1, big_one)

    for f in (guppy, neon, goldfish, angel):
        report_add(aq2, f)
    report_add(aq2, shark)

    report_add(aq3, neon)
    report_add(aq3, goldfish)

    print("\n--- Інформація про акваріуми ---")
    for aq in (aq1, aq2, aq3):
        aq.print_info()

    print("\n--- Три найбільші риби ---")
    aq1.print_top_largest()
    aq2.print_top_largest()

    print("\n--- Демонстрація set/get ---")
    guppy.set_name("Гуппі-2")
    print("Нове ім'я:", guppy.get_name())

    print("\n--- Завершення програми ---")


if __name__ == "__main__":
    main()
