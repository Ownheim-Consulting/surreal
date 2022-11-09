import os
import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

engine = create_engine('sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'surreal.db'))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# Declare a Base that extends ABCMeta so that @abc.abstractmethod can be used
class DeclarativeBaseABCMeta(DeclarativeMeta, abc.ABCMeta):
    pass
class Base(declarative_base(metaclass=DeclarativeBaseABCMeta)):
    __abstract__ = True

Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models.chart import Chart
    from models.map_chart import MapChart
    from models.choropleth_map import ChoroplethMap
    Base.metadata.create_all(bind=engine)
