# ToyBot
import os
from pprint import pprint

import regex


class BColours:
    HEADER = '\033[95m'
    BLUE_OK = '\033[94m'
    CYAN_OK = '\033[96m'
    GREEN_OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


actions = ["move", "left", "right", "report"]
cardinals = ["NORTH", "EAST", "SOUTH", "WEST"]
current_bot = None


class ToyBot:
    def __init__(self, current_x=0, current_y=0, current_direction=0):
        self.current_x = int(current_x)
        self.current_y = int(current_y)
        self.current_direction = int(current_direction)

    def left(self):
        if (self.current_direction - 1) < 0:
            self.current_direction = 3
        else:
            self.current_direction -= 1

    def right(self):
        if (self.current_direction + 1) > 3:
            self.current_direction = 0
        else:
            self.current_direction += 1

    def report(self):
        print("Output: " + str(self.current_x) + "," + str(self.current_y) + "," + cardinals[self.current_direction])

    def move(self):
        valid_move = True
        if (self.current_direction % 2) > 0:
            if self.current_direction == 1:
                if self.current_x < 5:
                    self.current_x += 1
                else:
                    valid_move = False
            else:
                if self.current_x > 0:
                    self.current_x -= 1
                else:
                    valid_move = False
        elif self.current_direction == 0:
            if self.current_y < 5:
                self.current_y += 1
            else:
                valid_move = False
        else:
            if self.current_y > 0:
                self.current_y -= 1
            else:
                valid_move = False
        return valid_move


def display_bot() -> None:
    print(BColours.HEADER + " \n"
                            "       ┌───────┐\n"
                            "      ┌┤  • •  ├┐\n"
                            "      └┤   L   ├┘\n"
                            "       │   ~~  │\n"
                            "       └──┬─┬──┘\n"
                            "      ┌───┴─┴───┐  ┌──{\n"
                            " }─┐  ├──┼──────┤  │\n"
                            "   └══┤  │      ├══x\n"
                            "      │  ├──────┤\n"
                            "      └─┬┴───┼──┘\n"
                            "       <║    ║\n"
                            "        │    │\n"
                            "     d══┘    └═b\n" + BColours.ENDC)


def clear_console() -> None:
    os.system('clear')


def place_bot(incoming):
    global cardinals, current_bot
    new_x = 0
    new_y = 0
    incoming_groups = incoming.groups()[1]
    incoming_groups = incoming_groups.split(",")

    if len(incoming_groups) > 1:
        new_x = int(incoming_groups[0])
        new_y = int(incoming_groups[1])
        if new_x < 0:
            print("Invalid X")
            return False
        if new_x > 5:
            print("Invalid X")
            return False
        if new_y < 0:
            print("Invalid Y")
            return False
        if new_y > 5:
            print("Invalid Y")
            return False

        if incoming.groups()[2].upper() not in cardinals:
            if current_bot is None:
                print("Invalid facing direction.")
                return False
    if current_bot is None:
        current_bot = ToyBot()

    current_bot.current_x = new_x
    current_bot.current_y = new_y

    if len(incoming.groups()[2]) > 0:
        current_bot.current_direction = cardinals.index(incoming.groups()[2].upper())
    return True


def validate_input(users_input) -> bool:
    incoming = regex.match(r"(\w+\b)\s?([0-5\,]*)?(\w*)?", users_input)
    global actions, cardinals, current_bot

    if incoming is None:
        # not a valid entry
        print("That didn't work. Please try again.")
        return False
    # Check if bot hasn't been placed yet
    elif current_bot is None:
        # Bot hasn't been placed yet. Check if user wants to place a bot.
        if incoming.groups()[0].lower() != "place":
            print("You haven't placed the bot yet!")
            return False
        # User wants to place a bot. Check if valid coordinates been given.
        else:
            return place_bot(incoming)

    else:
        if incoming.groups()[0].lower() == "place":
            return place_bot(incoming)
        for action in incoming.groups():
            if action.lower() in actions:
                method_to_call = getattr(current_bot, action)
                method_to_call()
        return True


def draw_board():
    global current_bot
    arrows = ['▲', '►', '▼', '◄']
    board = [['| |' for i in range(6)] for j in range(6)]

    board[abs(current_bot.current_y - 5)][current_bot.current_x] = "|" + arrows[
        current_bot.current_direction] + "|"

    pprint(board, indent=2)


def next_input():
    global current_bot
    if current_bot is not None:
        draw_board()
    prompt_for_input()


def prompt_for_input():
    print("Valid inputs: PLACE int 0 - 5,int 0 - 5,[NORTH, EAST,SOUTH, WEST], MOVE, REPORT, LEFT and RIGHT")
    print("To exit: x")
    users_input = input("Your input: ")
    while users_input.lower() != "x":
        while validate_input(users_input) is False:
            users_input = input("Your input: ")

        next_input()

    if users_input == "x":
        exit("Exiting...")


if __name__ == '__main__':
    display_bot()
    prompt_for_input()
