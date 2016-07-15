"""
  model.py - database models

"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ Serialise game state on a per-user level
    """
    __tablename__ = 'users'

    sender_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, primary_key=True)
    bitflags = Column(Integer, default=0)
    current_location = Column(Integer)
    items = Column(String(256))
