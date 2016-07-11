'''
    state.py - Internal representation of game state

    (c) 2016 bildzeitung@gmail.com

'''

from collections import defaultdict

from data import Item


class State(object):
    def __init__(self):
        self._last_message = []

        self.current_location = None
        self.redraw = False
        self.items = None
        self.bitflags = defaultdict(bool)

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

        new_state.bitflags = defaultdict(bool)
        for key, val in self.bitflags.iteritems():
            new_state[key] = val

        return new_state

    def save(self):
        pass


class StateFromGameData(State):
    ''' Initial game state
    '''
    def __init__(self, data):
        super(StateFromGameData, self).__init__()
        self.current_location = data.starting_room
        self.items = data.items


class StateFromDatabase(State):
    ''' Game state from DB
    '''
    def __init__(self, data):
        super(StateFromDatabase, self).__init__()
