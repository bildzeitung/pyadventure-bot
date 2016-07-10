'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''

import logging

from actions import actions
from conditions import conditions

LOG = logging.getLogger('scottadams')


class Engine(object):
    def __init__(self, data):
        self.data = data

    def redraw(self, state):
        if state.redraw:
            state.last_message = self.look(state)
            state.redraw = False

    def process(self, state, line):
        ''' Process one game loop, returning a new state
        '''
        new_state = state.clone()

        self.redraw(new_state)

        self.perform_actions(new_state, 0, 0)  # main loop

        self.redraw(new_state)

        # TODO: parse input
        # TODO: process action
        # TODO: deal with lights

        return new_state

    def look(self, state):
        ''' Display room description
        '''
        # TODO: sort out lighting situation

        room = state.current_location

        # TODO: sort out * in text

        msg = "I'm in a %s" % room['desc']

        # TODO: add exits

        # TODO: add items

        return msg

    def perform_actions(self, state, verb, noun):
        ''' Main game logic
        '''
        # TODO: some validation on verb / noun pairs

        # TODO: basic move
        for action in self.data.actions_by_verb(verb):
            # TODO: sort out random percent (always 100% right now)
            if (action.verb == 0) or (action.verb != 0 and
                                      (action.noun == noun or action.noun == 0)):
                result = self.perform_line(state, action)

    def perform_line(self, state, action):
        # TODO: sort out conditionals
        LOG.debug('[perform line]')

        params = []
        for condition in action.conditions:
            if not conditions[condition['type']](condition['value'], state, params):
                return 0

        # TODO: perform actions if conditionals pass
        for act in action.actions:
            # process messages
            if act > 0 and act < 52:
                LOG.debug('[action] [message] %s', act)
                state.last_message += self.data.messages[act]
                continue
            if act > 101:
                LOG.debug('[action] [message (>101)] %s', act)
                act -= 50  # adjustment
                state.last_message += self.data.messages[act]
                continue

            # TODO: process regular actions
            actions[act](state, params)
