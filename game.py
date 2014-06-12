import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 5
GAME_HEIGHT = 5

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y - 1)
        elif direction == "down":
            return (self.x, self.y + 1)
        elif direction == "left":
            return (self.x - 1, self.y)
        elif direction == "right":
            return (self.x + 1, self.y)
        return None

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))


class OpenDoor(GameElement):
    IMAGE = "DoorOpen"
    DOOR = "Open"

class CloseDoor(GameElement):
    IMAGE = "DoorClosed"
    DOOR = "Closed"

    def interact(self, player):
        GAME_BOARD.draw_msg("Player meets a closed door")
        open_door = OpenDoor()
        print "Open door is created"
        GAME_BOARD.register(open_door)
        GAME_BOARD.set_el(player.x - 1, player.y -1, open_door)

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    rock_positions = [(2,1), (1,2), (3,2), (2,3)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    rocks[-1].SOLID = False

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This game sucks.")
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    close_door = CloseDoor()
    GAME_BOARD.register(close_door)
    GAME_BOARD.set_el(0,4, close_door)

    open_door = OpenDoor()
    GAME_BOARD.register(open_door)
    GAME_BOARD.set_el(0,1, open_door)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"
    elif KEYBOARD[key.SPACE]:
        GAME_BOARD.erase_msg()
  
    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x == GAME_WIDTH or next_x < 0 or next_y == GAME_HEIGHT or next_y < 0:
                GAME_BOARD.draw_msg( " Cannot move outside the boundary ")
        else:
                GAME_BOARD.draw_msg("next_x: %r and next_y: %r" % (next_x, next_y) )        
                existing_el = GAME_BOARD.get_el(next_x, next_y)
                if existing_el:
                    existing_el.interact(PLAYER)

                if existing_el is None or not existing_el.SOLID:
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)