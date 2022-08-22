from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import MONEY

 
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    title_url = Column(String)
    author = Column(String)
    origin=Column(String)
    # pages = Column(Integer)
    published = Column(Date)
    # price = Column(MONEY)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Book(title='{}', title_url='{}', author='{}', published={})>" \
            .format(self.title, self.title_url, self.author, self.published )