from datetime import datetime

from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base, Book
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import yaml

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_yaml():
    with session_scope() as s:
        print('ok')
        ## LOAD THE YAML WHEN RECREATING DATABASE
        ## TODO: GET MORE SOPHISTICATED HERE W DEPLOY STEP...
        for data in yaml.load_all(open('books.yaml')):
            book = Book(**data)
            # print(book)
            s.add(book)
            s.commit()

if __name__ == '__main__':
    recreate_database()
    book = Book(
            title='Deep Learning',
            author='Ian Goodfellow',
            id=0,
            published=datetime(2016, 11, 18),
            title_url="https://en.wikipedia.org/wiki/Deep_learning",
            origin="none"
    )
    with session_scope() as s:
        ## SEE NOTE ABOVE REGARDING DEPLOY & FUTURE STEPS
        s.add(book)
        s.query(Book).filter_by(title="Deep Learning").delete()
        load_yaml()


