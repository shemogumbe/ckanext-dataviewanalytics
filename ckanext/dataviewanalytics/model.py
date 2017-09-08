"""Models for dataviewanalytics extension"""
from sqlalchemy import (Column, Integer, String,
                        create_engine)
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from ckan import model

Base = declarative_base()
engine = create_engine('postgresql://ckan_default:ckan@localhost/ckan_default')


Session = sessionmaker(expire_on_commit=False)
Session.configure(bind=engine)

def create_tables(engine):
    Base.metadata.create_all(engine)

class UserAnalytics(Base):

     __tablename__ = 'user_analytics'
     id = Column(Integer, primary_key=True)
     country = Column(String(256))
     occupation = Column(String(256))
     
     def __init__(self, country, occupation):
        self.country = country
        self.occupation = occupation

class DataAnalytics(Base):

    __tablename__ = "data_analytics"
    id = Column(Integer, primary_key=True)
    journalists = Column(String(256))
    students = Column(String(256))
    researchers = Column(String(256))
    scientists = Column(String(256))
    countrys = Column(String(256))

    def __init__(self, journalists, students, researchers, scientists, countrys:
        self.journalists = journalists
        self.students = students
        self.researchers = researchers
        self.scientists = scientists
        self.countrys = countrys
