#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages storage of hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session """
        if cls:
            obj = self.__session.query(cls)
        else:
            obj = self.__session.query(State).all()
            obj.extend(self.__session.query(City).all())
            obj.extend(self.__session.query(User).all())
            obj.extend(self.__session.query(Place).all())
            obj.extend(self.__session.query(Review).all())
            obj.extend(self.__session.query(Amenity).all())

        new_dict = {}
        for item in obj:
            key = type(item).__name__ + '.' + item.id
            new_dict[key] = item
        return new_dict

    def new(self, obj):
        """add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session)
        self.__session = Session()

    def close(self):
        """close working sqlalchemy session"""
        self.__session.close()
