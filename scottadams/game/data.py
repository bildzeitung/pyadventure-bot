'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''

import logging
import re

LOG = logging.getLogger('scottadams')


class ActionGlob(object):
    ''' Internal representation of an action

        150*verb+noun
        5 repeats of condition+20*value
        150*action1+action2
        150*action3+action4
    '''
    def __init__(self, data):
        self.vocab = data[0]
        self.conditions = [{'type': x % 20, 'value': x / 20} for x in data[1:5]]
        self.actions = [data[6] / 150, data[6] % 150,
                        data[7] / 150, data[7] % 150]

        self.noun = self.vocab % 150
        self.verb = self.vocab / 150

    def __str__(self):
        return '%s %s' % (self.conditions, self.actions)


class Item(object):
    ''' Internal representation of an item

        Items are given in the format item text then location. Item text may
        end with /TEXT/. This text is not printed but means that an automatic
        get/drop will be done for 'GET/DROP TEXT' on this item. Item names beginning
        with '*' are treasures. The '*' is printed. If you put all treasures in the
        treasure room (in the header) and 'SCORE' the game finishes with a well done
        message. Item location -1 is the inventory (255 on C64 and Spectrum tape
                games) and 0 means not in play in every game I've looked at. The lamp (always
        object 9) behaviour supports this belief.

    '''
    def __init__(self, desc, location):
        self.desc = desc
        self.location = location

    def __str__(self):
        return ' '.join([self.desc, str(self.location)])


class Data(object):
    ''' Internal representation of game data

        Data file structure:

        <header>
        <actions>
        <verbs and nouns>
        <rooms>
        <messages>
        <items>

    '''

    def __init__(self, fileobj):
        self.src_lines = [x.strip() for x in fileobj.readlines()]
        self._offset = 0

        self.headers = None
        self.rooms = None
        self.actions = None
        self.items = None
        self.nouns = None
        self.verbs = None
        self.messages = None

        # load game data, in order
        self._load_header()
        self._load_actions()
        self._load_nouns_and_verbs()
        self._load_rooms()
        self._load_messages()
        self._load_items()

    def _load_header(self):
        headers = [int(x) for x in self.src_lines[0:12]]
        self.headers = {'item_count': headers[1],
                        'action_count': headers[2],
                        'noun_and_verb_count': headers[3],
                        'room_count': headers[4],
                        'max_carry': headers[5],
                        'starting_room': headers[6],
                        'treasure_count': headers[7],
                        'word_length': headers[8],
                        'light_duration': headers[9],
                        'message_count': headers[10],
                        'treasure_room': headers[11],
                        }

        self._offset = 12

    def _load_rooms(self):
        # due to line continuations, a state machine is necessary to read the room data
        self.rooms = []

        for _ in xrange(self.headers['room_count'] + 1):
            exits = self.src_lines[self._offset:self._offset+6]
            desc = self.src_lines[self._offset+6]
            self._offset += 7
            final_desc = desc
            while desc[-1] != '"':
                desc = self.src_lines[self._offset]
                self._offset += 1
                final_desc += ' ' + desc
            self.rooms.append({'exits': exits, 'desc': final_desc[1:-1]})

    def _load_actions(self):
        self.actions = []
        for _ in xrange(self.headers['action_count'] + 1):
            items = [int(x) for x in self.src_lines[self._offset:self._offset+8]]
            self.actions.append(ActionGlob(items))
            self._offset += 8

    def actions_by_verb(self, verb):
        return [x for x in self.actions if x.verb == verb]

    @property
    def starting_room(self):
        return self.headers['starting_room']

    def _load_items(self):
        regex = r'"([^"]*)" (\d+)'

        self.items = []
        for _ in xrange(self.headers['item_count'] + 1):
            data = self.src_lines[self._offset]
            solution = re.search(regex, data)
            self._offset += 1
            while not solution:
                self._offset += 1
                data = '\n'.join([data, self.src_lines[self._offset]])
                solution = re.search(regex, data)

            desc, location = solution.groups()
            location = int(location)

            self.items.append(Item(desc, location))

    def _load_nouns_and_verbs(self):
        self.nouns = []
        self.verbs = []
        for _ in xrange(self.headers['noun_and_verb_count'] + 1):
            self.nouns.append(self.src_lines[self._offset])
            self.verbs.append(self.src_lines[self._offset + 1])
            self._offset += 2

    def _load_messages(self):
        self.messages = []
        for _ in xrange(self.headers['message_count'] + 1):
            desc = self.src_lines[self._offset]
            final_desc = desc
            self._offset += 1
            while desc == '' or final_desc == '"' or desc[-1] != '"':
                desc = self.src_lines[self._offset]
                self._offset += 1
                final_desc += '\n' + desc
            self.messages.append(final_desc[1:-1])  # strip double quotes
