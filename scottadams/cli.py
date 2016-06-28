'''
    cli.py - Commandline interface to text adventure engine

    (c) 2016 bildzeitung@gmail.com

'''

import click


@click.command()
@click.argument('datafile', type=click.File('rb'))
def main(datafile):
    ''' Text Adventure CLI

        DATAFILE - Path to ScottFree data file
    '''
    pass
