'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''


class Engine(object):
    def __init__(self, data, state):
        self.data = data
        self.state = state

    def process(self, line):
        if line is None:
            return self.look()

    def look(self):
        # TODO: sort out lighting situation

        room = self.state.current_location

        # TODO: sort out * in text

        msg = "I'm in a %s" % room['desc']

        # TODO: add exits

        # TODO: add items

        return msg
