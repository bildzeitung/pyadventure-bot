'''
    actions.py - Routines for actions

    (c) 2016 bildzeitung@gmail.com

'''

import logging

from constants import EXITNAMES

LOG = logging.getLogger('scottadams')


def nop(data, state, params):
    pass


def move_to_room(data, state, params):
    LOG.debug('[action] [move_to_room] %s', params[0])
    state.current_location = params.pop(0)


def set_bitflag(data, state, params):
    LOG.debug('[action] [set_bitflag] %s', params[0])
    state.bitflags[params[0]] = True
    params.pop(0)


def game_over(data, state, params):
    LOG.debug('[action] [game over]')
    state.last_message = 'The game is now over'
    state.is_playing = False


def describe_room(data, state, params):
    look(data, state, params)


def score(data, state, params):
    count = state.stored_treasures(data.headers['treasure_room'])
    percent = count * 100 / data.headers['treasure_count']
    state.last_message = 'You have stored %s treasures. ' \
                         'On a scale of 0 to 100 that rates %s.' % (count, percent)

    if count == data.headers['treasure_count']:
        state.last_message = 'Well done.'
        game_over(data, state, params)


def clear_screen(data, state, params):
    state.last_message = '\n'


def look(data, state, params):
    ''' Display room description
    '''
    msg_list = []

    # TODO: sort out lighting situation

    room = data.rooms[state.current_location]

    prefix = "I'm in a "
    if room.noprefix:
        prefix = ''

    msg_list.append("%s%s" % (prefix, room.desc))

    msg_list.append('')
    msg = 'Obvious exits: '
    msg += ', '.join([EXITNAMES[idx] for idx, val in enumerate(room.exits)
                     if val != 0]) or 'none'
    msg_list.append(msg)

    if state.colocated_items:
        msg_list.append('')
        msg = 'You can also see: '
        msg += ' - '.join([item.desc for item in state.colocated_items])
        msg_list.append(msg)

    state.last_message = '\n'.join(msg_list)


# ordered set of action handlers
actions = {
        0: nop,
        54: move_to_room,
        58: set_bitflag,
        63: game_over,
        64: describe_room,
        65: score,
        70: clear_screen,
        76: look,
        }
