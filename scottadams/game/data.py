'''
    data.py - Internal representation of game data

    (c) 2016 bildzeitung@gmail.com

'''

import logging

LOG = logging.getLogger('scottadams')


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
        self._headers = None
        self._rooms = None

    @property
    def headers(self):
        if not self._headers:
            headers = [int(x) for x in self.src_lines[0:12]]
            self._headers = {'item_count': headers[1],
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

        return self._headers

    @property
    def rooms(self):
        if not self._rooms:
            pass

        offset = 12 + 8*(self.headers['action_count']+1) + 2*(self.headers['noun_and_verb_count']+1)

        # due to line continuations, a state machine is necessary to read the room data
        self._rooms = []

        for _ in xrange(self.headers['room_count'] + 1):
            exits = self.src_lines[offset:offset+6]
            desc = self.src_lines[offset+6]
            offset += 7
            final_desc = desc
            while desc[-1] != '"':
                desc = self.src_lines[offset]
                offset += 1
                final_desc += ' ' + desc
            self._rooms.append({'exits': exits, 'desc': final_desc[1:-1]})

        return self._rooms

    @property
    def starting_room(self):
        return self.rooms[self.headers['starting_room']]
