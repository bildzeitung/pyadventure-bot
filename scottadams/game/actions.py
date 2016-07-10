'''
    actions.py - Routines for actions

    (c) 2016 bildzeitung@gmail.com

'''


def set_bitflag(state, params):
    state.bitflags[params[0]] = True
    params.pop(0)


# ordered set of action handlers
actions = {
        58: set_bitflag
        }
