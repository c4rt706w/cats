import msvcrt
import animals
import places


class Conductor:
    def __init__(self):
        self.all_places = [places.Place('Cat_island', places.Point(-100.0, 50.0), []),
                           places.Place('Dog_tower', places.Point(-20.0, -40.0), []),
                           places.Place('Human_domain', places.Point(100.0, 100.0), []),
                           places.Place('Battlefield', places.Point(-100.0, 50.0), [])]

        self.all_humans = [[animals.Human('Kate', 'female', 20, 50, 100,
                                          [animals.Cat('Myaukalka', 'female', 8, 100, 50, 'Kate', 'Myauk', [], 5)],
                                          self.all_places[0])],
                           [animals.Human('Luc', 'male', 40, 40, 150,
                                          [animals.Dog('Chase', 'male', 11, 90, 30, 'Luc', 'Bark', [], 5)],
                                          self.all_places[1])],
                           [animals.Human('Frank', 'male', 15, 10, 10,
                                          [animals.Cat('Pushok', 'male', 1, 20, 1, 'Frank', 'Murr', [], 2)],
                                          self.all_places[2])],
                           [animals.Human('Marie', 'female', 50, 90, 200,
                                          [animals.Cat('Barsik', 'male', 10, 80, 70, 'Marie', 'Purr', [], 4)],
                                          self.all_places[3])]]

        self.all_arenas = [places.Arena('Cat_coliseum', self.all_places[0].get_point(), self.all_humans[0], 0),
                           places.Arena('Dog_combat', self.all_places[1].get_point(), self.all_humans[1], 1),
                           places.Arena('Human_stadium', self.all_places[2].get_point(), self.all_humans[2], 0),
                           places.Arena('Bloodbath', self.all_places[3].get_point(), self.all_humans[3], 0), ]

        for i in range(4):
            self.all_places[i].get_in(self.all_humans[i])

    def get_self(self):
        return self

    def update(self):
        for i in range(len(self.all_places)):
            self.all_arenas[i].update_humans(self.all_places[i].get_humans())

    def get_arena(self, point):
        for i in self.all_arenas:
            if i.get_point().x == point.x and i.get_point().y == point.y:
                return i
        print("Wrong point location: there is no Arena!")

    def start_world(self):
        print("Would you like to play a game?",
              "input <yes> and <no>...")

        # mne len'
        user_reply = 'yes'
        a_name = 'Vasya'
        a_sex = 'male'
        a_age = 11
        # mne len'

        # user_reply = input()
        if user_reply.lower() == 'yes':
            print("\nYOOOOOOOOOOOOOOOOOO!!!\n\nLet's make your avatar:\n")
            print("Input your name:")
            # a_name = input()
            print("Input your sex: ")
            # a_sex = input()
            print("Input your age:")
            # a_age = int(input())

            avatar = animals.Human(a_name, a_sex, a_age, 10, 1, [], [], self.all_places[2])
            self.all_places[2].get_in(avatar)
            self.update()
            print(type(avatar.pets))

            print(f"\nWelcome to Human_domain, {avatar.get_name()}!\n")

            print("Would you want to pass the tutorial?")
            user_reply = input()
            if user_reply.lower() == 'yes':
                # start education
                education = True

                print("\nWow! Look, there are little Cat and Dog. Try to tame them!")
                first_pets = [animals.Cat('Sopelka', 'female', 2, 20, 1, 'none', 'miau', [], 1),
                              animals.Dog('Shnurok', 'male', 1, 15, 1, 'none', 'gav', [])]
                while first_pets[0].get_owner() == 'none' or first_pets[1].get_owner() == 'none':
                    print("[Tip: choose the animal and press <t> to tame]")
                    Controller(avatar, self.get_self(), education).tame_sth(first_pets)

                print("\nThere is Arena in every Place, except Dog_tower. Let's fight with somebody!\n")
                print("[Tip: press <f> to fight on the Arena]")
                Controller(avatar, self.get_self(), education).start()
                print("\nCongratulations with your first battle!!!")

                print("\nYou can find free pets in the Place")
                print("[Tip: press <s> to search free pets in the Place]")
                Controller(avatar, self.get_self(), education).start()

                print("\nLet's move to another Place!")
                print("[Tip: press <g> to go to another Place]")
                Controller(avatar, self.get_self(), education).start()

                # finish education
            education = False

            Controller(avatar, self.get_self(), education).start()

        print("\nGame over!")


class Controller:
    def __init__(self, avatar=animals.Human(), conductor=Conductor(), education=False):
        self.avatar = avatar
        self.conductor = conductor
        self.education = education

        self.menu = f"Press <e> to equip your Pet.\n" + \
                    f"Press <f> to find pets in {self.avatar.get_place().get_name()}.\n" + \
                    f"Press <g> to go to another Place.\n" + \
                    f"Press <s> to search free animals in {self.avatar.get_place().get_name()}.\n" + \
                    f"Press <d> to end game.\n"

    def get_menu(self):
        print(self.menu)

    def tame_sth(self, sth):
        print("Choose the pet you'd like to tame")
        for i, th in enumerate(sth):
            print(i + 1, th.get_info())
        user_reply = int(input())
        while user_reply > len(sth) or user_reply < 1:
            print("Please, input valid choice")
            user_reply = int(input())
        while True:
            x = msvcrt.kbhit()
            if x:
                k = ord(msvcrt.getch())
                if k == 116:  # <t>
                    if self.education:
                        print(type(self.avatar.pets), self.avatar.get_name())
                        # .append(sth[user_reply - 1])
                        sth[user_reply - 1].get_tamed(self.avatar.get_name())
                    else:
                        self.avatar.tame(sth[user_reply - 1])
                    break

    def start_fight(self):
        arena_a = self.conductor.get_arena(self.avatar.get_place().get_point())
        arena_a.fight(self.avatar)

    def search_pets(self):
        free_pets_a = self.avatar.get_place().get_free_pets()
        for i in free_pets_a:
            print(i.get_info())
        while True:
            print("Would you like to tame anyone of these free_pets?\n"
                  "Input <yes> or <no>:")
            user_reply = input()
            if user_reply.lower() == 'yes':
                self.tame_sth(free_pets_a)
            else:
                break

    def go_travel(self):
        print("What Place do you want to explore?")
        for i, val in enumerate(self.conductor.all_places):
            print(i + 1, val.get_name())
        ans_place = int(input())
        while ans_place < 1 or ans_place > len(self.conductor.all_places):
            print("Invalid answer. Please, try again.")
            ans_place = int(input())
        self.avatar.go_to(self.conductor.all_places[ans_place - 1])

    def start(self):
        end_game = False
        if not self.education:
            self.get_menu()
        while not end_game:
            x = msvcrt.kbhit()
            if x:
                k = ord(msvcrt.getch())
                if k == 101:  # <e>
                    self.avatar.reequip()
                if k == 102:  # <f>
                    self.start_fight()
                if k == 103:  # <g>
                    self.go_travel()
                if k == 115:  # <s>
                    self.search_pets()
                if k == 100:  # <d>
                    end_game = True
                    break
            else:
                pass
