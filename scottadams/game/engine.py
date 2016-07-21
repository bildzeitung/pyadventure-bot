'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''

import logging

from actions import actions
from conditions import conditions
from constants import EXITNAMES

LOG = logging.getLogger('scottadams')


class Engine(object):
    NOTFOUND = -1

    def __init__(self, data):
        self.data = data

    def start_game(self, state):
        ''' Process start of game loop & look()
        '''
        new_state = state.clone()

        self.look(new_state)
        self.perform_actions(new_state, 0, 0)

        return new_state

    def parse(self, line):
        ''' Munge line into verb, noun integer pairs

            Divide line into two parts; if there are more, fail
            Take only the first 3 chars of each part, locate index in array
        '''
        parts = line.split(' ')

        if not parts:
            return 0, 0  # main loop

        if len(parts) == 1:
            verb = parts[0].upper()
            noun = ''

            # expand short direction names
            remap = {'N': 'NORTH', 'S': 'SOUTH',
                     'E': 'EAST', 'W': 'WEST',
                     'U': 'UP', 'D': 'DOWN',
                     'I': 'INVENTORY'}
            if len(verb) == 1 and verb in remap:
                noun = remap[verb]
                verb = 'GO'

        else:  # at least two parts
            verb, noun = [x.upper() for x in parts[:2]]

        # truncate to word length
        verb = verb[:self.data.headers['word_length']]
        noun = noun[:self.data.headers['word_length']]

        if verb in self.data.verbs:
            verb = self.data.verbs[verb]
        else:
            LOG.debug('Could not find verb part of line: %s (%s)', line, verb)
            verb = self.NOTFOUND

        if noun in self.data.nouns:
            noun = self.data.nouns[noun]
        else:
            LOG.debug('Could not find noun part of line: %s (%s)', line, noun)
            noun = self.NOTFOUND

        return verb, noun

    def process(self, state, line):
        ''' Process one game loop, returning a new state
        '''
        new_state = state.clone()

        self.perform_actions(new_state, 0, 0)  # event loop

        verb, noun = self.parse(line)

        self.perform_actions(new_state, verb, noun)  # command

        # TODO: deal with lights

        return new_state

    def look(self, state):
        ''' Display room description
        '''
        msg_list = []

        # TODO: sort out lighting situation

        room = self.data.rooms[state.current_location]

        # TODO: sort out * in text

        msg_list.append("I'm in a %s" % room['desc'])

        msg_list.append('')
        msg = 'Obvious exits: '
        msg += ', '.join([EXITNAMES[idx] for idx, val in enumerate(room['exits'])
                         if val != 0]) or 'none'
        msg_list.append(msg)

        if state.colocated_items:
            msg_list.append('')
            msg = 'You can also see: '
            msg += ' - '.join([item.desc for item in state.colocated_items])
            msg_list.append(msg)

        state.last_message = '\n'.join(msg_list)

    def perform_actions(self, state, verb, noun):
        ''' Main game logic
        '''
        LOG.debug('Processing verb, noun: %s %s', verb, noun)

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
                state.last_message = self.data.messages[act]
                continue
            if act > 101:
                LOG.debug('[action] [message (>101)] %s', act)
                act -= 50  # adjustment
                state.last_message = self.data.messages[act]
                continue

            # TODO: process regular actions
            actions[act](state, params)
