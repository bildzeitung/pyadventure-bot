'''
    cli.py - Commandline interface to text adventure engine

    (c) 2016 bildzeitung@gmail.com

'''

import click
import cmd
import logging
import sys

from game.data import Data
from game.engine import Engine
from game.state import StateFromGameData

LOG = logging.getLogger('scottadams')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOG.addHandler(ch)
LOG.setLevel(logging.DEBUG)


class REPL(cmd.Cmd):
    ''' Facilitate running an adventure game via Python cmd
    '''
    prompt = '> '

    def __init__(self, engine):
        cmd.Cmd.__init__(self)
        self.engine = engine

    def do_EOF(self, line):
        ''' Simply exit on EOF
        '''
        return True

    def default(self, line):
        click.echo(self.engine.process(line))


@click.command()
@click.argument('datafile', type=click.File('rb'))
def main(datafile):
    ''' Text Adventure CLI

        DATAFILE - Path to ScottFree data file
    '''
    data = Data(datafile)
    state = StateFromGameData(data)
    engine = Engine(data, state)

    click.echo(engine.process(None))

    repl = REPL(engine)
    repl.cmdloop()
