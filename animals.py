import random
import places
import transfer
import abilities


class Animal:
    def __init__(self, name='', sex='non-binary', age=0, stamina=0, level=0, equip=[]):
        self.name = name
        self.sex = sex
        self.age = age
        self.stamina = stamina
        self.level = level
        self.equip = equip

    def get_self(self):
        return self

    def get_stamina(self):
        return self.stamina

    def get_name(self):
        return self.name

    def get_equip(self):
        return self.equip

    def remove_equip(self, item):
        self.equip.remove(item)

    def get_info(self):
        return f'{self.name} is {self.level} level {self.age} years old {self.sex} {type(self).__name__}'


class Pet(Animal):
    def __init__(self, name='', sex='non-binary', age=0, stamina=0,
                 level=0, owner='none', voice='', equip=[]):
        super().__init__(name, sex, age, stamina, level, equip)
        self.owner = owner
        self.voice = voice

    def voice(self):
        print(f'{self.name} says: {self.voice}')

    def get_owner(self):
        return self.owner

    def get_tamed(self, new_owner):
        self.owner = new_owner

    def add_equip(self, item):
        self.equip.append(item)

    def buff_stam(self):
        buff = 0
        for i in self.equip:
            if type(i) == 'Suit':
                buff += i.get_stam()
        return buff

    def buff_damage(self):
        buff = 0
        for i in self.equip:
            if type(i) == 'Toy':
                buff += i.get_damage()
        return buff


class Cat(Pet):
    def __init__(self, name='', sex='non-binary', age=0, stamina=0,
                 level=0, owner='none', voice='', equip=[], life=1):
        super().__init__(name, sex, age, stamina, level, owner, voice, equip)
        self.life = life
        self.luck = random.randint(-10, 10)
        self.skills = [abilities.Skill('Bite', self.level, abs(self.level - self.life)),
                       abilities.Skill('Claws', self.level, abs(self.level + self.luck)),
                       abilities.Skill('Ultimate', self.level, abs(self.luck * 10))]

    def happy_birthday(self):
        if self.luck < -4:
            print(f'Oh, no! {self.name} die...')
            self.age = 0
            self.life += 1
        else:
            self.age += 1
            print(f'Happy birthday, {self.name}! She turns {self.age}')

    def ascension(self):
        self.level += 1
        self.stamina += 10
        self.skills = [abilities.Skill('Bite', self.level, abs(self.level - self.life)),
                       abilities.Skill('Claws', self.level, abs(self.level + self.luck)),
                       abilities.Skill('Ultimate', self.level, abs(self.luck * 100))]

    def rebirth(self):
        if self.life == 9:
            print(f"{self.name} can't rebirth.\n",
                  f"{self.name}lived a good life and died a brave death")
            return
        print(f'{self.name} rebirth!!!')
        self.life += 1
        self.age = 1
        self.stamina = 10
        self.equip = []
        self.level = 1
        self.luck = random.randint(-10, 10)
        self.skills = [abilities.Skill('Bite', self.level, abs(self.level - self.life)),
                       abilities.Skill('Claws', self.level, abs(self.level + self.luck)),
                       abilities.Skill('Ultimate', self.level, abs(self.luck * 100))]

    def get_skills(self):
        return self.skills

    def get_info_skills(self):
        print(f'{self.name} skills:')
        for i, sk in enumerate(self.skills):
            print('\t', i + 1, sk.get_info())


class Dog(Pet):
    def __init__(self, name='', sex='non-binary', age=0, stamina=0,
                 level=0, owner='none', voice='', equip=[], loyalty=0):
        super().__init__(name, sex, age, stamina, level, owner, voice, equip)
        self.loyalty = loyalty
        self.dist = 0

    def get_loyalty(self, human, old_place, new_place):
        trace = new_place.dist(old_place.get_point())
        quantity = (trace + self.dist % 200) // 200
        if quantity > 1:
            self.loyalty += quantity
            self.dist += trace
            print(f"\nCongratulations! {self.name}'s loyalty raised to {self.loyalty}!")
        for i in range(quantity):
            human.add_equip()


class Human(Animal):
    def __init__(self, name='', sex='non-binary', age=0, stamina=0,
                 level=0, equip=[], pets=[], place=places.Place()):
        super().__init__(name, sex, age, stamina, level, equip)
        self.pets = pets
        self.place = place

    def tame(self, new_pet):
        if self.level >= new_pet.level and new_pet.owner == 'none':
            print(f'Congrats! Your new friend - {new_pet.get_name()}!')
            self.pets.append(new_pet)
            new_pet.get_tamed(self.name)
            self.place.update_frees()
        elif new_pet.owner != 'none':
            print("This pet already has an owner!")
        else:
            print("Sorry, you're too weak...")

    def get_human(self):
        return Human(self.name, self.sex, self.age, self.stamina, self.level,
                     self.equip, self.pets, self.place)

    def go_to(self, new_place):
        cond = transfer.Conductor()
        for i in self.pets:
            if type(i).__name__ == 'Dog':
                i.get_loyalty()
        self.get_place().get_out(self.get_self())
        new_place.get_in(self.get_self())
        self.place = new_place
        cond.update()

    def random_pet(self):
        a = random.choice(self.pets)
        while type(a).__name__ != 'Cat':
            a = random.choice(self.pets)
        return a

    def show_pets(self):
        print(f"{self.name}'s collection:")
        for i, val in self.pets:
            print(i + 1, val.get_name())

    def get_place(self) -> places.Place:
        return self.place

    def add_equip(self):
        new_item = random.choice(
            [abilities.Toy(random.choice(['bunny', 'kitty']), 1, random.randint(1, 10)),
             abilities.Suit(random.choice(['cosplay', 'black-suit']), 1, random.randint(1, 10))])
        self.equip.append(new_item)
        print(f"You received {new_item.get_info()}\n")

    def reequip(self):
        self.show_pets()
        if len(self.equip) == 0:
            print("There is no equipment.")
            return
        print("Choose equipment.")
        print(f"{self.name}'s equipment:")
        for i, val in enumerate(self.equip):
            print(i + 1, val.get_info())
        item = int(input())
        while True:
            if item < 1 or item > len(self.equip):
                print("Please, input valid value")
                item = int(input())
                continue
            break
        print("\nChoose Pet to equip him an item.")
        equip_pet = int(input())
        while True:
            if equip_pet < 1 or equip_pet > len(self.pets):
                print("Please, input valid value")
                equip_pet = int(input())
                continue
            if self.pets[equip_pet - 1].equip.empty():
                print("This Pet doesn't have any equipment. Please, try again.")
                equip_pet = int(input())
                continue
            break
        self.pets[equip_pet].add_equip(item)
