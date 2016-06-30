'''
    state.py - Internal representation of game state

    (c) 2016 bildzeitung@gmail.com

'''


class State(object):
    def __init__(self):
        self._current_location = None
        self._last_message = ''

    @property
    def current_location(self):
        return self._current_location

    @property
    def last_message(self):
        return self._last_message

    @last_message.setter
    def last_message(self, message):
        self._last_message = message

    def clone(self):
        new_state = State()
        new_state._current_location = self._current_location

        return new_state

    def save(self):
        pass


class StateFromGameData(State):
    ''' Initial game state
    '''
    def __init__(self, data):
        super(StateFromGameData, self).__init__()
        self._current_location = data.starting_room


class StateFromDatabase(State):
    ''' Game state from DB
    '''
    def __init__(self, data):
        super(StateFromDatabase, self).__init__()
