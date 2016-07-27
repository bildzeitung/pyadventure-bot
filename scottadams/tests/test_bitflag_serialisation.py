'''
    test_bitflag_serialisation - Validate that bitflag state can be saved/loaded

'''

from testtools import TestCase

from game.state import State


class TestBitflagSerialisation(TestCase):
    ''' Validate correctness of serialising the bitflags dict
    '''

    def test_serialise_no_flags(self):
        ''' Serialise with no bitflags set '''
        state = State()
        self.assertEqual(state.serialise_bitflags(), 0)

    def test_serialise_1(self):
        ''' Serialise with bitflag 1 set '''
        state = State()
        state.bitflags[1] = True
        self.assertEqual(state.serialise_bitflags(), 2)

    def test_serialise_1_and_10(self):
        ''' Serialise with bitflags 1 and 10 set '''
        state = State()
        state.bitflags[1] = True
        state.bitflags[10] = True
        self.assertEqual(state.serialise_bitflags(), 2**1 + 2**10)


class TestBitflagsDeserialisation(TestCase):
    ''' Validate correctness of deserialising the storage bitflag value
    '''

    def test_deserialise_0(self):
        ''' Deserialise with no bitflags
        '''
        bitflags = State.deserialise_bitflags(0)
        self.assertEqual(bitflags, {})

    def test_deserialise_1(self):
        ''' Deserialise expecting 1 bitflag set '''
        bitflags = State.deserialise_bitflags(2)
        self.assertEqual(bitflags, {1: True})

    def test_deserialise_1026(self):
        ''' Deserialise expecting 1 and 10 bitflags set '''
        bitflags = State.deserialise_bitflags(2**1 + 2**10)
        self.assertEqual(bitflags, {1: True, 10: True})
