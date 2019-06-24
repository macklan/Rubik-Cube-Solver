'''
rubik_cube_180.py

Macklan Badger
macklanb
CSE 415
Project: Option 3

Usage: python3 rubik_cube_180.py

The Rubik Cube is stored as a array
The index in the cube array determines the tile on the cube
Goes as the following

FRONT
0   1
2   3

DOWN
4   5
6   7

BACK
8   9
10  11

TOP
12  13
14  15

LEFT
16  17
18  19

RIGHT
20  21
22  23

Will use the command line as the menu, mimicking the A6 menu

'''


from random import randint, choice


class State:
    directions = ['f', 'd', 'b', 'u', 'l', 'r']
    move_directions = ["f - cl", "f - cc", "d - cl", "d - cc", "b - cl", "b - cc",
                       "u - cl", "u - cc", "l - cl", "l - cc", "r - cl", "r - cc"]
    sides = {
        'f': 3,
        'd': 7,
        'b': 11,
        'u': 15,
        'r': 19,
        'l': 23
    }
    total_cubes = 24

    def __init__(self, cube=None):
        if cube is None:
            cube = [] * self.total_cubes

            cube[0:3] = [0] * 4
            cube[4:7] = [1] * 4
            cube[8:11] = [2] * 4
            cube[12:15] = [3] * 4
            cube[16:19] = [4] * 4
            cube[20:23] = [5] * 4

        self.cube = cube

    def __str__(self):
        txt = "\n"
        for i in range(len(self.directions)):
            txt += self.directions[i] + "\n"

            for j in range(4):
                index = i * 4 + j
                txt += str(self.cube[index])
                if j is 1:
                    txt += "\n"
            txt += "\n\n"
        return txt

    def __eq__(self, other):
        for i in range(self.total_cubes):
            if self.cube[i] is not other.cube[i]:
                return False
        return True

    def __hash__(self):
        return (self.__str__()).__hash__()

    def print_index(self):
        txt = "\n"
        for i in range(len(self.directions)):
            txt += self.directions[i] + "\n"

            for j in range(4):
                index = i * 4 + j
                txt += str(index) + " "
                if j is 1:
                    txt += "\n"
            txt += "\n\n"
        return txt

    def copy(self):
        news = State()
        for i in range(self.total_cubes):
            news.cube[i] = self.cube[i]
        return news

    def can_move(self, move):
        return True

    # Rotate the side 180 degrees clockwise
    def move(self, move):
        news = self.copy()
        cube = news.cube

        if move is "f - cl":
            temp = cube[0]
            cube[0] = cube[2]
            cube[2] = cube[3]
            cube[3] = cube[1]
            cube[1] = temp

            temp1 = cube[14]
            temp2 = cube[15]
            cube[14] = cube[17]
            cube[15] = cube[19]

            cube[17] = cube[4]
            cube[19] = cube[5]

            cube[4] = cube[22]
            cube[5] = cube[20]

            cube[22] = temp2
            cube[20] = temp1

        if move is "b - cl":
            temp = cube[8]
            cube[8] = cube[10]
            cube[10] = cube[11]
            cube[11] = cube[9]
            cube[9] = temp

            temp1 = cube[6]
            temp2 = cube[7]
            cube[6] = cube[16]
            cube[7] = cube[18]

            cube[16] = cube[13]
            cube[18] = cube[12]

            cube[13] = cube[23]
            cube[12] = cube[21]

            cube[21] = temp2
            cube[23] = temp1

        if move is "u - cl":
            temp = cube[12]
            cube[12] = cube[14]
            cube[14] = cube[15]
            cube[15] = cube[13]
            cube[13] = temp

            temp1 = cube[10]
            temp2 = cube[11]
            cube[10] = cube[17]
            cube[11] = cube[16]

            cube[17] = cube[1]
            cube[16] = cube[0]

            cube[0] = cube[20]
            cube[1] = cube[21]

            cube[20] = temp1
            cube[21] = temp2

        if move is "d - cl":
            temp = cube[4]
            cube[4] = cube[6]
            cube[6] = cube[7]
            cube[7] = cube[5]
            cube[5] = temp

            temp1 = cube[2]
            temp2 = cube[3]
            cube[2] = cube[18]
            cube[3] = cube[19]

            cube[18] = cube[9]
            cube[19] = cube[8]

            cube[9] = cube[22]
            cube[8] = cube[23]

            cube[22] = temp1
            cube[23] = temp2

        if move is "l - cl":
            temp = cube[16]
            cube[16] = cube[18]
            cube[18] = cube[19]
            cube[19] = cube[17]
            cube[17] = temp

            temp1 = cube[12]
            temp2 = cube[14]
            cube[12] = cube[8]
            cube[14] = cube[10]

            cube[8] = cube[4]
            cube[10] = cube[6]

            cube[4] = cube[0]
            cube[6] = cube[2]

            cube[0] = temp1
            cube[2] = temp2

        if move is"r - cl":
            temp = cube[20]
            cube[20] = cube[22]
            cube[22] = cube[23]
            cube[23] = cube[21]
            cube[21] = temp

            temp1 = cube[15]
            temp2 = cube[13]
            cube[15] = cube[3]
            cube[13] = cube[1]

            cube[3] = cube[7]
            cube[1] = cube[5]

            cube[7] = cube[11]
            cube[5] = cube[9]

            cube[11] = temp1
            cube[9] = temp2

        news.cube = cube
        return news

    def mix_up(self, num_shuffles):
        news = self.copy()
        for i in range(num_shuffles):
            news = news.move(choice(self.move_directions))
        return news


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# Checks the 6 sides, making sure that each side only contains
# One 'color' or value
def goal_test(s):
    for i in range(6):
        if not check_side(s.cube, i * 4):
            return False
    return True


def goal_message(s):
    return "Congrats! You solved the Rubik Cube!"


def check_side(cube, index):
    return cube[index] == cube[index + 1] and \
           cube[index] == cube[index + 2] and \
           cube[index] == cube[index + 3]


# state = State()
# print(state)
# print(state.move("f"))
# print(state.move("d"))
# print(state.move("b"))
# print(state.move("u"))
# print(state.move("l"))
# print(state.move("r"))

# state = State([8, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST FRONT")
# for i in range(4):
#     state = state.move("f")
#     print(state)
#
# state = State([0, 0, 0, 0, 8, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST DOWN")
# for i in range(4):
#     state = state.move("d")
#     print(state)
#
# state = State([0, 0, 0, 0, 1, 1, 1, 1, 8, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST BACK")
# for i in range(4):
#     state = state.move("b")
#     print(state)
#
#
# state = State([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 8, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST UP")
# for i in range(4):
#     state = state.move("u")
#     print(state)
#
#
# state = State([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 8, 4, 4, 4, 5, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST LEFT")
# for i in range(4):
#     state = state.move("l")
#     print(state)
#
# state = State([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 8, 5, 5, 5])
# print(state)
# print("**************")
# print("TEST RIGHT")
# for i in range(4):
#     state = state.move("r")
#     print(state)

