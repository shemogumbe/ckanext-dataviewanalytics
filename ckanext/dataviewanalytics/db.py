'''Models definition for database tables creation
'''

from ckan.common import config
from sqlalchemy import (Column, Integer, String, ForeignKey, create_engine, types)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ckan import model
from ckan.model import user_table

Base = declarative_base()
DB_LOCATION = config.get('sqlalchemy.url')
engine = create_engine(DB_LOCATION)
Session = sessionmaker(bind=engine)


def create_tables():
    '''Create the tables on the database
    '''
    Base.metadata.create_all(engine)


class UserAnalytics(Base):
    ''' Model to create database table for extra user details
    '''

    __tablename__ = 'user_analytics'

    id = Column(Integer, primary_key=True)
    user_id = Column(types.UnicodeText, primary_key=False)
    country = Column(String(256))
    occupation = Column(String(256))

    def __repr__(self):
        return '<User_ID: {}, Occupation: {}, Country: {}>'.format(
            self.user_id, self.occupation, self.country)


class DataAnalytics(Base):
    '''Model to create database table for data analytics information
    '''

    __tablename__ = 'data_analytics'

    id = Column(Integer, primary_key=True)
    resource_id = Column(types.UnicodeText, primary_key=False)
    user_id = Column(types.UnicodeText, primary_key=False)
    occupation = Column(String(256))
    country = Column(String(256))

    def __repr__(self):
        return '<Resource_ID: {}, User_ID: {}>'.format(self.resource_id, self.user_id)
