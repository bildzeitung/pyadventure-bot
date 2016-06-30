'''
    state.py - Internal representation of game state

    (c) 2016 bildzeitung@gmail.com

'''


class State(object):
    def __init__(self):
        self._current_location = None

    @property
    def current_location(self):
        return self._current_location


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
        super(StateFromGameData, self).__init__()
