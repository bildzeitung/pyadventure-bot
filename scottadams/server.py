'''
    server.py - Server for the text adventure game

    (c) 2016 bildzeitung@gmail.com

'''
from game.data import Data
from game.engine import Engine
from game.state import StateFromGameData


class Server(object):
    def __init__(self, datafile):
        with open(datafile, 'rb') as src:
            self.data = Data(src)

        self.engine = Engine(self.data)

    def play(self, player, command):
        state = StateFromGameData(self.data)

        new_state = self.engine.process(state, command)
        new_state.save()

        return new_state.last_message
