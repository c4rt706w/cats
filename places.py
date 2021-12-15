from math import sqrt
import names
import random
import animals


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def dist(self, p_p):
        return sqrt((self.x - p_p.x) ** 2 + (self.y - p_p.y) ** 2)

    def get_point(self):
        return Point(self.x, self.y)


class City(Point):
    def __init__(self, name='', locate=Point(0.0, 0.0)):
        self.name = name
        super().__init__(locate.x, locate.y)

    def get_name(self):
        return self.name


class Place(City):
    def __init__(self, name='', locate=Point(0.0, 0.0), humans=[]):
        super().__init__(name, locate)
        self.humans = humans
        self.free_animals = []
        c = random.randint(0, 1000)
        f1 = open('C:/Users/ar961/PycharmProjects/cats/meow', 'rt')
        f2 = open('C:/Users/ar961/PycharmProjects/cats/bark', 'rt')
        for i in range(c):
            self.free_animals.append(
                random.choice([animals.Cat(names.get_first_name(), random.choice(['male', 'female']),
                                           random.randint(1, 20), random.randint(1, 100), random.randint(1, 100),
                                           'none', 'miau', [], random.randint(1, 9)),
                               animals.Dog(names.get_first_name(), random.choice(['male', 'female']),
                                           random.randint(1, 20), random.randint(1, 100), random.randint(1, 100),
                                           'none', 'woof', [])]))

    def get_out(self, human):
        self.humans.remove(human)

    def get_in(self, human):
        self.humans.append(human)

    def random_human(self):
        return random.choice(self.humans)

    def get_free_pets(self):
        return self.free_animals

    def get_humans(self):
        return self.humans

    def update_frees(self):
        for i in self.free_animals:
            if i.get_owner() != 'none':
                self.free_animals.remove(i)


class Arena(Place):
    def __init__(self, name='', locate=Point(0.0, 0.0), humans=[], allow=0):
        super().__init__(name, locate, humans)
        self.allow = allow

    def update_humans(self, new_humans):
        self.humans = new_humans

    def fight(self, part1):
        if self.allow == 1:
            print("It's not allowed to fight there.")
            return

        if len(self.humans) < 2:
            print(f'This Arena {self.name} is too small')
            return
        print(f'On the Arena {self.name} the battle begins...')

        part2 = self.random_human()
        while part1 == part2:
            part2 = self.random_human()

        print(f'On the blue corner of the {self.get_name()} - {part1.get_name()}')
        print(f'On the red corner of the {self.get_name()} - {part2[0].get_name()}')

        player1 = part1.random_pet()
        player2 = part2[0].random_pet()

        print('\nFighter 1:', player1.get_info())
        print('Fighter 2:', player2.get_info())

        print('\nPress F to start the fight...')
        user_reply = input()
        if user_reply.lower() != 'f':
            print(f'{part1.get_name()} runs away from the fight!')
            return

        sp = '\t\t\t\t\t\t\t'

        buff_stam1 = player1.buff_stam()
        buff_stam2 = player2.buff_stam()

        buff_damage1 = player1.buff_damage()
        buff_damage2 = player2.buff_damage()

        lunar1 = 0
        lunar2 = 0

        stam1 = player1.get_stamina() + buff_stam1
        stam2 = player2.get_stamina() + buff_stam2

        print(f"\nDuring your turn choose {player1.get_name()}'s skill from the list below")
        player1.get_info_skills()

        while stam1 > 0 and stam2 > 0:
            print('_' * 100, f'\n{player1.get_name()}: {sp} \t {player2.get_name()}:',
                  f'\nStamina: {stam1} hp {sp} {stam2} hp',
                  f'\nLunar drops: {lunar1} {sp} {lunar2}',
                  f'\n{player1.get_name()} turn:')

            damage1 = buff_damage1
            damage2 = buff_damage2

            while True:
                user_try = int(input())
                if 0 < user_try < 3 or user_try == 3 and lunar1 > 9:
                    damage1 += player1.get_skills()[user_try - 1].get_damage()
                    break
                print('Enter right value')
            print(f'{player1.get_name()} deals damage - {damage1} hp')
            stam2 -= damage1
            if stam2 <= 0:
                break

            print(f'{player2.name} turn:')
            if lunar2 < 10:
                damage2 += max(player2.get_skills()[0].get_damage(),
                               player2.get_skills()[1].get_damage())
            else:
                damage2 += player2.get_skills()[2].get_damage()
            print(f'{player2.get_name()} deals damage - {damage2} hp')
            stam1 -= damage2

            lunar1 += 1
            lunar2 += 1
            print('_' * 100, '\n')

        print(f'\nThe sun rises over the {self.name}...',
              f'\n{player1.get_name()} and {player2.get_name()} swear to fight to death...',
              'may cat_God judge them!!!')
        if stam2 <= 0:
            print(f'{player1.get_name()} defeat {player2.get_name()} in the fight!!!')
        else:
            print(f'{player1.get_name()} die a heroic death in the battle with {player2.get_name()}...',
                  '\nPlease, improve your characteristics...')
            player1.rebirth()
