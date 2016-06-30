'''
    server.py - Server for the text adventure game

    (c) 2016 bildzeitung@gmail.com

'''
from game.data import Data
from game.engine import Engine
from game.state import StateFromDatabase


class Server(object):
    def __init__(self, datafile):
        self.data = Data(datafile)

    def play(self, player, command):
        state = StateFromDatabase(player)
        engine = Engine(self.data, state)

        new_state = engine.process()
        new_state.save()

        return new_state.last_message
