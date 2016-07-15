'''
    actions.py - Routines for actions

    (c) 2016 bildzeitung@gmail.com

'''

import logging

LOG = logging.getLogger('scottadams')


def set_bitflag(state, params):
    LOG.debug('[action] [set_bitflag] %s', params[0])
    state.bitflags[params[0]] = True
    params.pop(0)


# ordered set of action handlers
actions = {
        58: set_bitflag
        }
