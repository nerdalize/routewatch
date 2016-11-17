from sqlalchemy.orm import sessionmaker

from RouteWatch.DB.declarative import *

engine = create_engine('sqlite:///core.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class DB(object):

    tables = dict(Prefix=Prefix, Recipient=Recipient, Settings=Settings)

    def create(self, table, **kwargs):
        new = self.tables[table](**kwargs)
        session.add(new)
        session.commit()

    def get(self, table, **kwargs):
        objs = session.query(self.tables[table])
        for key, value in kwargs.items():
            objs = objs.filter(getattr(self.tables[table], key) == value)
        objs = objs.all()
        return objs

    def delete(self, table, **kwargs):
        objs = session.query(self.tables[table])
        for key, value in kwargs.items():
            objs = objs.filter(getattr(self.tables[table], key) == value)
        objs = objs.all()
        for obj in objs:
            session.delete(obj)

    def commit(self):
        session.commit()