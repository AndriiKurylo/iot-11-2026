class Fish:
    def __init__(self, name, age, species, size, preferred_food,
                 is_aggressive, needed_space):
        self._name = name
        self._age = age
        self._species = species
        self._size = size                    # см
        self._preferred_food = preferred_food
        self._is_aggressive = is_aggressive
        self._needed_space = needed_space    # м³
        print(f"[Створено] Риба: {self._name}")

    def __del__(self):
        print(f"[Видалено] Риба: {self._name}")

    # --- функції доступу ---
    def get_name(self): return self._name
    def get_age(self): return self._age
    def get_species(self): return self._species
    def get_size(self): return self._size
    def get_preferred_food(self): return self._preferred_food
    def is_aggressive(self): return self._is_aggressive
    def get_needed_space(self): return self._needed_space

    def set_name(self, name): self._name = name
    def set_age(self, age): self._age = age
    def set_size(self, size): self._size = size
    def set_preferred_food(self, food): self._preferred_food = food

    # --- виведення ---
    def print_info(self):
        print(f"  {self._name} | вид: {self._species} | вік: {self._age} | "
              f"розмір: {self._size} см | їжа: {self._preferred_food} | "
              f"агресивна: {'так' if self._is_aggressive else 'ні'} | "
              f"потрібен об'єм: {self._needed_space} м³")


class Aquarium:
    def __init__(self, name, total_volume):
        self._name = name
        self._total_volume = total_volume
        self._free_space = total_volume
        self._fishes = []
        print(f"[Створено] Акваріум: {self._name}")

    def __del__(self):
        print(f"[Видалено] Акваріум: {self._name}")

    # --- функції доступу ---
    def get_name(self): return self._name
    def get_total_volume(self): return self._total_volume
    def get_free_space(self): return self._free_space
    def get_fishes(self): return list(self._fishes)

    # --- логіка ---
    def is_aggressive_aquarium(self):
        """True/False, якщо в акваріумі є риби; None, якщо він порожній."""
        if not self._fishes:
            return None
        return self._fishes[0].is_aggressive()

    def can_add(self, fish):
        if fish.get_needed_space() > self._free_space:
            return False, "недостатньо вільного місця"
        kind = self.is_aggressive_aquarium()
        if kind is not None and kind != fish.is_aggressive():
            return False, "агресивних і неагресивних не можна тримати разом"
        return True, ""

    def add_fish(self, fish):
        ok, reason = self.can_add(fish)
        if not ok:
            print(f"  ✗ Не вдалося додати «{fish.get_name()}» "
                  f"до «{self._name}»: {reason}")
            return False
        self._fishes.append(fish)
        self._free_space -= fish.get_needed_space()
        print(f"  ✓ «{fish.get_name()}» додано до «{self._name}»")
        return True

    def remove_fish(self, fish):
        if fish in self._fishes:
            self._fishes.remove(fish)
            self._free_space += fish.get_needed_space()

    def get_top_largest(self, n=3):
        return sorted(self._fishes, key=lambda f: f.get_size(), reverse=True)[:n]

    # --- виведення ---
    def print_top_largest(self, n=3):
        print(f"Топ-{n} найбільших риб в акваріумі «{self._name}»:")
        top = self.get_top_largest(n)
        if not top:
            print("  (акваріум порожній)")
        for i, fish in enumerate(top, 1):
            print(f" {i}.", end="")
            fish.print_info()

    def print_info(self):
        print(f"\n=== Акваріум «{self._name}» ===")
        print(f"Загальний об'єм: {self._total_volume} м³, "
              f"вільно: {self._free_space:.2f} м³, риб: {len(self._fishes)}")
        for fish in self._fishes:
            fish.print_info()


def main():
    # Риби
    shark = Fish("Біллі", 5, "Червонохвостий шарк", 15, "м'ясо", True, 0.30)
    piranha = Fish("Піра", 3, "Піранья", 20, "м'ясо", True, 0.25)
    cichlid = Fish("Цик", 2, "Цихліда", 12, "креветки", True, 0.15)
    guppy = Fish("Гуппі", 1, "Гуппі", 4, "пластівці", False, 0.05)
    neon = Fish("Неон", 1, "Неон", 3, "пластівці", False, 0.03)
    goldfish = Fish("Золотко", 4, "Золота рибка", 18, "водорості", False, 0.20)
    angel = Fish("Ангел", 2, "Скалярія", 14, "пластівці", False, 0.10)
    big_one = Fish("Гігант", 7, "Арапайма", 150, "риба", True, 5.0)

    # Акваріуми
    aq1 = Aquarium("Хижак", 0.8)
    aq2 = Aquarium("Мирний", 0.4)
    aq3 = Aquarium("Малюк", 0.1)

    print("\n--- Додавання риб ---")
    for f in (shark, piranha, cichlid):
        aq1.add_fish(f)
    aq1.add_fish(guppy)       # неагресивна в агресивний -> відмова
    aq1.add_fish(big_one)     # не вистачає місця -> відмова

    for f in (guppy, neon, goldfish, angel):
        aq2.add_fish(f)
    aq2.add_fish(shark)       # агресивна в мирний -> відмова

    aq3.add_fish(neon)        # neon уже в aq2, але демонструємо ліміт об'єму
    aq3.add_fish(goldfish)    # 0.03 + 0.20 > 0.1 -> відмова

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
