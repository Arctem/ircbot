from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = None
session = None

def initialize(dbname='sqlite:///:memory:'):
    global engine, session
    engine = create_engine(dbname, echo=True)
    session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

##################
# Decorators
##################

#loads a session if needed
def needs_session(func):
    def needs_session_wrapper(*args, s=None, **kwargs):
        if not s:
            s = session()
            s._irc_atomic = False

            retval = func(*args, s=s, **kwargs)
            if retval and retval.id:
                s.expunge(retval)
            # s.expunge_all()
            s.close()
            return retval
        else:
            return func(*args, s=s, **kwargs)
    return needs_session_wrapper

#make sure we commit at the end of this function
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
