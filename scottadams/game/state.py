'''
    state.py - Internal representation of game state

    (c) 2016 bildzeitung@gmail.com

'''

from collections import defaultdict
from copy import copy

from data import Item


class State(object):
    ''' Representation of all Scott Adams game engine state

        The entire game state can be recorded as:
        - the room the player is in
        - the value of the bitflags
        - the locations of all of the items
        - TODO: game counters
        - TODO: lighting flag ??

    '''

    def __init__(self):
        self._last_message = []

        self.current_location = None
        self.redraw = False
        self.items = None
        self.bitflags = defaultdict(bool)
        self.is_playing = True

    @property
    def colocated_items(self):
        ''' Return a list of Items that are at the current player location
        '''
        return [item for item in self.items if item.location == self.current_location]

    def stored_treasures(self, treasure_room):
        ''' Return a list of Items that are in the treasure room
        '''
        return sum(1 for item in self.items
                   if item.desc.startswith('*') and item.location == treasure_room)

    @property
    def last_message(self):
        return '\n'.join(self._last_message)

    @last_message.setter
    def last_message(self, message):
        self._last_message.append(message)

    def clone(self):
        new_state = State()
        new_state.current_location = self.current_location

        new_state.items = []
        for item in self.items:
            new_state.items.append(Item(item.desc, item.location))

        new_state.bitflags = copy(self.bitflags)

        return new_state

    def serialise_bitflags(self):
        ''' The bitflags are less than 32-bit, so translate the dict into a
            single 4-byte value
        '''
        total = 0
        for flag in [key for key, val in self.bitflags.iteritems() if val]:
            total += 2 ** flag

        return total

    @staticmethod
    def deserialise_bitflags(bitflags):
        ''' The dict is easier to handle in the code, so decompose the integer
            back into a dict for the engine
        '''
        out = defaultdict(bool)
        count = 0
        while (bitflags):
            if bitflags % 2:
                out[count] = True

            count += 1
            bitflags = bitflags >> 1

        return out


class StateFromGameData(State):
    ''' Initial game state taken from the game data itself
    '''
    def __init__(self, data):
        super(StateFromGameData, self).__init__()
        self.current_location = data.starting_room
        self.items = data.items


class StateFromDatabase(State):
    ''' Given a SQLAlchemy model, create the game state
    '''
    def __init__(self, game, data):
        super(StateFromDatabase, self).__init__()
        self.current_location = data.current_location
        self.is_playing = data.is_playing

        item_locations = [int(x) for x in data.items.split(',')]
        self.items = [Item(x.desc, 0) for x in game.items]
        for item in self.items:
            item.location = item_locations.pop(0)
        self.bitflags = self.deserialise_bitflags(data.bitflags)
