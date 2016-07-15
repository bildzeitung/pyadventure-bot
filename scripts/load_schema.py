#!/usr/bin/env python
"""
  load_schema.py - database models

    Use SQLAlchemy to create a representation of the schema for the database

"""

import click
import os

from sqlalchemy import create_engine

from game.model import Base


@click.command()
def main():
    ''' Database schema loader CLI

    '''
    click.echo('Connecting to DB')
    engine = create_engine(os.environ['DATABASE_URL'], echo=True)

    click.echo('Create schema')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
