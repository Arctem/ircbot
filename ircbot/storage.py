from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import object_mapper
from sqlalchemy.orm.exc import UnmappedInstanceError

Base = declarative_base()

engine = None
session = None


def initialize(dbname='sqlite:///:memory:'):
    global engine, session
    engine = create_engine(dbname, echo=True)
    session = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)


def is_mapped(obj):
    try:
        object_mapper(obj)
    except UnmappedInstanceError:
        return False
    return True


##################
# Decorators
##################

# loads a session if needed
def needs_session(func):
    def needs_session_wrapper(*args, s=None, **kwargs):
        if not s:
            s = session()
            s._irc_atomic = False

            retval = func(*args, s=s, **kwargs)
            if retval and is_mapped(retval) and retval in s:  # and retval.id?
                s.expunge(retval)
            s.close()
            return retval
        else:
            return func(*args, s=s, **kwargs)
    return needs_session_wrapper

# make sure we commit at the end of this function


def atomic(func):
    @needs_session
    def atomic_wrapper(*args, s=None, **kwargs):
        if s._irc_atomic:
            return func(*args, s=s, **kwargs)

        try:
            s._irc_atomic = True
            retval = func(*args, s=s, **kwargs)
            s.commit()
            return retval
        except:
            s.rollback()
            raise
        finally:
            s._irc_atomic = False
    return atomic_wrapper
