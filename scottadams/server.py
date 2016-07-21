'''
    server.py - Server for the text adventure game

    (c) 2016 bildzeitung@gmail.com

'''

from game.data import Data
from game.engine import Engine
from game.model import User
from game.state import StateFromGameData, StateFromDatabase


class Server(object):
    def __init__(self, datafile, db, log):
        with open(datafile, 'rb') as src:
            self.data = Data(src)

        self.engine = Engine(self.data, log=log)
        self.db = db
        self.log = log

    def play(self, player, command):
        self.log.debug('Searching for player %s in DB', player)
        db_player = self.db.session.query(User).filter_by(sender_id=player).all()

        if db_player:
            self.log.debug('Found player; loading state')
            state = StateFromDatabase(db_player[0])
            self.log.debug('Location: %s', state.current_location)
            self.log.debug('Flags: %s', state.bitflags)
        else:
            self.log.debug('New player; take initial state from game data')
            state = StateFromGameData(self.data)

        self.log.debug('Command: %s', command)
        new_state = self.engine.process(state, command)

        self._save_to_db(player, new_state)

        return new_state.last_message

    def _save_to_db(self, player, state):
        self.log.debug('Bitflags: %s', state.bitflags)

        item_string = ','.join(str(item.location) for item in state.items)

        db_state = User(sender_id=player,
                        game_id=self.data.version['game_id'],
                        bitflags=state.serialise_bitflags(),
                        items=item_string,
                        current_location=state.current_location,
                        )
        self.db.session.merge(db_state)
        self.db.session.commit()
