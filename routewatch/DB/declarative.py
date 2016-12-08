from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prefix(Base):
    __tablename__ = 'prefix'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    prefix = Column(String(1024), nullable=False)
    protocol = Column(Integer, nullable=False)


class Recipient(Base):
    __tablename__ = 'recipient'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    email = Column(String(1024), nullable=False)


class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    data = Column(String(1000000), nullable=False)
    name = Column(String(1024), nullable=False)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///core.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
