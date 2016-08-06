'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''

import logging

from actions import actions, look
from conditions import conditions

LOG = logging.getLogger('scottadams')


class Engine(object):
    NOTFOUND = -1

    def __init__(self, data, log=None):
        self.data = data

        if log:
            self.log = log
        else:
            self.log = LOG

    def start_game(self, state):
        ''' Process start of game loop & look()
        '''
        new_state = state.clone()

        look(self.data, new_state, None)
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
                     'U': 'UP', 'D': 'DOWN'}
            if len(verb) == 1 and verb in remap:
                noun = remap[verb]
                verb = 'GO'

            if len(verb) == 1 and verb == 'I':
                verb = 'INVENTORY'

        else:  # at least two parts
            verb, noun = [x.upper() for x in parts[:2]]

        # truncate to word length
        verb = verb[:self.data.headers['word_length']]
        noun = noun[:self.data.headers['word_length']]

        if verb in self.data.verbs:
            verb = self.data.verbs[verb]
        else:
            self.log.debug('Could not find verb part of line: %s (%s)', line, verb)
            verb = self.NOTFOUND

        if noun in self.data.nouns:
            noun = self.data.nouns[noun]
        else:
            self.log.debug('Could not find noun part of line: %s (%s)', line, noun)
            noun = self.NOTFOUND

        return verb, noun

    def process(self, state, line):
        ''' Process one game loop, returning a new state
        '''
        if not state.is_playing:
            return state

        new_state = state.clone()

        self.perform_actions(new_state, 0, 0)  # event loop

        verb, noun = self.parse(line)

        self.perform_actions(new_state, verb, noun)  # command

        # TODO: deal with lights

        return new_state

    def perform_actions(self, state, verb, noun):
        ''' Main game logic
        '''
        self.log.debug('Processing verb, noun: %s %s', verb, noun)

        # error if no direction specified with GO <x>
        if verb == 1 and noun == self.NOTFOUND:
            state.last_message = 'Give me a direction too.'
            return

        # basic move
        if verb == 1 and (0 < noun < 7):
            # TODO: deal with the lighting situation

            # check exits
            self.log.debug('Room has exits: %s',
                           self.data.rooms[state.current_location].exits)
            destination = self.data.rooms[state.current_location].exits[noun-1]
            if destination:
                self.log.debug('Moving to %s', destination)
                state.current_location = destination
                look(self.data, state, None)
            else:
                state.last_message = "You can't go in that direction."

            return

        # TODO: basic move
        result = True
        for action in self.data.actions_by_verb(verb):
            self.log.debug('[action] action (%s / %s | %s) by verb (%s)',
                           action, action.verb, action.noun, verb)
            # TODO: sort out random percent (always 100% right now)
            if (action.verb == 0) or (action.verb != 0 and
                                      (action.noun == noun or action.noun == 0)):
                result = self.perform_line(state, action)

        self.log.debug('RESULT: %s', result)

    def perform_line(self, state, action):
        # TODO: sort out conditionals
        self.log.debug('[perform line]')

        params = []
        for condition in action.conditions:
            if not conditions[condition['type']](condition['value'], state, params):
                return False

        # TODO: perform actions if conditionals pass
        self.log.debug('conditions ok; %s actions', len(action.actions))
        for act in action.actions:
            # process messages
            if act > 0 and act < 52:
                self.log.debug('[action] [message] [%s] %s', act, self.data.messages[act])
                state.last_message = self.data.messages[act]
                continue
            if act > 101:
                self.log.debug('[action] [message (>101)] [%s] %s', act, self.data.messages[act-50])
                act -= 50  # adjustment
                state.last_message = self.data.messages[act]
                continue

            # TODO: process regular actions
            actions[act](self.data, state, params)

        self.log.debug('[completed line]')
        return True
