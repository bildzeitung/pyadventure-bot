'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''


class Engine(object):
    def __init__(self, data):
        self.data = data

    def process(self, state, line):
        new_state = state.clone()

        if line is None:
            new_state.last_message = self.look(state)

        return new_state

    def look(self, state):
        # TODO: sort out lighting situation

        room = state.current_location

        # TODO: sort out * in text

        msg = "I'm in a %s" % room['desc']

        # TODO: add exits

        # TODO: add items

        return msg
