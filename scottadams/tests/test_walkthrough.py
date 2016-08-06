'''
    test_walkthrough - Validate that a play through the game works as expected

'''

from testtools import TestCase

import os

from game.data import Data
from game.state import StateFromGameData
from game.engine import Engine

DATAFILE = os.path.join(os.path.dirname(__file__), '..', 'assets', 'adv01.dat')


class TestWalkthrough(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DATAFILE) as datafile:
            cls._data = Data(datafile)

        cls._initial_state = StateFromGameData(cls._data)
        cls._engine = Engine(cls._data)

    def test_start(self):
        ''' Validate that start of game is ok '''
        new_state = self._engine.start_game(self._initial_state)
        self.assertIn('ADVENTURELAND', new_state.last_message)

    def test_walkthrough(self):
        command_list = (('go east', 'sunny meadow'),  # to meadow
                        ('go east', 'on the shore of a lake'),  # to shore
                        ('get axe', ''),
                        )
        new_state = self._engine.start_game(self._initial_state)
        print '[start] %s' % new_state.last_message
        for item in command_list:
            command, check = item
            new_state = self._engine.process(new_state, command)
            print '[%s] %s' % (command, new_state.last_message)
            self.assertIn(check, new_state.last_message)
        print '[done]'
