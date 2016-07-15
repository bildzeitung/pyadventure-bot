'''
    conditions.py - Routines for conditionals

    (c) 2016 bildzeitung@gmail.com

'''

import logging

from constants import CARRIED

LOG = logging.getLogger('scottadams')


def parameter(value, state, params):
    LOG.debug('[cond] [push parameter] %s', value)
    params.append(value)
    return True


def item_carried(value, state, params):
    LOG.debug('[cond] [item_carried] %s', state.items[value])
    return state.items[value].location == CARRIED


def item_colocated(value, state, params):
    LOG.debug('[cond] [item_colocated] %s', state.items[value])
    return state.items[value].location == state.current_location


def item_carried_or_colocated(value, state, params):
    LOG.debug('[cond] [item_carried_or_colocated] %s', state.items[value])
    return item_carried(value, state, params) or item_colocated(value, state, params)


def in_room(value, state, params):
    LOG.debug('[cond] [in_room] %s %s', state.current_location, value)
    return state.current_location == value


def item_not_colocated(value, state, params):
    raise NotImplemented()


def item_not_carried(value, state, params):
    LOG.debug('[cond] [item_not_carried] %s', state.items[value])
    return not item_carried(value, state, params)


def not_in_room(value, state, params):
    raise NotImplemented()


def bitflag_arg_is_set(value, state, params):
    LOG.debug('[cond] [bitflag_arg_is_set] %s %s', value, state.bitflags[value])
    return state.bitflags[value]


def bitflag_arg_is_cleared(value, state, params):
    LOG.debug('[cond] [bitflag_arg_is_cleared] %s %s', value, state.bitflags[value])
    return not state.bitflags[value]


def something_carried(value, state, params):
    raise NotImplemented()


def nothing_carried(value, state, params):
    raise NotImplemented()


def item_not_carried_or_colocated(value, state, params):
    raise NotImplemented()


def item_arg_in_game(value, state, params):
    raise NotImplemented()


def item_arg_not_in_game(value, state, params):
    raise NotImplemented()


def current_counter_leq_arg(value, state, params):
    raise NotImplemented()


def current_counter_geq_arg(value, state, params):
    raise NotImplemented()


def object_in_initial_room(value, state, params):
    raise NotImplemented()


def object_not_in_initial_room(value, state, params):
    raise NotImplemented()


def current_counter_eq_arg(value, state, params):
    raise NotImplemented()


# ordered set of conditional actions
conditions = [
        parameter,  # 0
        item_carried,  # 1
        item_colocated,  # 2
        item_carried_or_colocated,  # 3
        in_room,  # 4
        item_not_colocated,  # 5
        item_not_carried,  # 6
        not_in_room,  # 7
        bitflag_arg_is_set,  # 8
        bitflag_arg_is_cleared,  # 9
        something_carried,  # 10
        nothing_carried,  # 11
        item_not_carried_or_colocated,  # 12
        item_arg_in_game,  # 13 (i.e. not in room 0)
        item_arg_not_in_game,  # 14 (i.e. in room 0)
        current_counter_leq_arg,  # 15
        current_counter_geq_arg,  # 16
        object_in_initial_room,  # 17
        object_not_in_initial_room,  # 18
        current_counter_eq_arg,  # 19
        ]
