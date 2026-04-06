from sqlalchemy import *
from sqlalchemy.orm import *
import sys
from configuration import *

Base = declarative_base()
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

# classes tables in database
class Users(Base):
    __tablename__ = 'users'
    id_users = Column(Integer, primary_key=True)
    name = Column(String)
    sure_name = Column(String)
    phone = Column(String)
    login = Column(String)
    password = Column(String)
    reader_tickets = relationship('Reader_Ticket', back_populates='user')
    user_roles = relationship('User_roles', back_populates='user')
 
class Roles(Base):#+
    __tablename__ = "role"
    id_role = Column(Integer, primary_key=True)
    role_title = Column(String)
    user_roles = relationship('User_roles', back_populates='roles')

class User_roles(Base):#+
    __tablename__ = 'user_roles'
    id_user_roles = Column(Integer, primary_key=True)
    Users_id_users = Column(Integer, ForeignKey('users.id_users'))
    role_id_role = Column(Integer, ForeignKey('role.id_role'))
    user = relationship('Users', back_populates='user_roles')
    roles = relationship('Roles', back_populates='user_roles')

class Author(Base):#+
    __tablename__ = 'author'
    id_author = Column(Integer, primary_key=True)
    name = Column(String)
    sure_name = Column(String)
    authors_book = relationship('Authors_book', back_populates='author')

class Reader_Ticket(Base):#+
    __tablename__ = 'reader_ticket'
    id_ticket = Column(Integer, primary_key=True)
    data_create = Column(Date)
    is_active = Column(String)
    name_reader = Column(String)
    sure_name_reader = Column(String)
    user_id_user = Column(Integer, ForeignKey("users.id_users"))
    user = relationship('Users', back_populates='reader_tickets')
    books_reader = relationship('Books_Reader', back_populates='reader_tickets')
    

class Type_book(Base):#+
    __tablename__ = 'type_book'
    id_type_book = Column(Integer, primary_key=True)
    book_type = Column(String)
    book_types = relationship('Book_types', back_populates='type_book')

class Book(Base):#+
    __tablename__ = 'book'
    id_book = Column(Integer, primary_key=True)
    book_title = Column(String)
    publication_date = Column(Date)
    in_stock = Column(Integer)
    pictcher = Column(String)
    book_types = relationship('Book_types', back_populates='book')
    authors_book = relationship('Authors_book', back_populates='book')
    books_reader = relationship('Books_Reader', back_populates='book')

class Books_Reader(Base):#+
    __tablename__ = 'books_reader'
    id_Books_Reader = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id_book'))
    id_ticket = Column(Integer,ForeignKey("reader_ticket.id_ticket"))
    book = relationship('Book', back_populates='books_reader')
    reader_tickets = relationship('Reader_Ticket', back_populates='books_reader')
    

class Book_types(Base):#+
    __tablename__ = 'book_types'
    id_book_types = Column(Integer, primary_key=True)
    book_id_book = Column(Integer, ForeignKey('book.id_book'))
    type_book_id_type_book = Column(Integer, ForeignKey('type_book.id_type_book'))
    type_book = relationship('Type_book', back_populates='book_types')
    book = relationship('Book', back_populates='book_types')

class Authors_book(Base):#+
    __tablename__ = 'authors_book'
    id_authors_book = Column(Integer, primary_key=True)
    author_id_author = Column(Integer, ForeignKey('author.id_author'))
    book_id_book = Column(Integer, ForeignKey('book.id_book'))
    author = relationship('Author', back_populates='authors_book')
    book = relationship('Book', back_populates='authors_book')

# books = session.query(Reader_Ticket).all()

# for b in books:
#     print(f"Читатель {b.name_reader} {b.sure_name_reader}")
#     print(f"Читает ")
#     for i in b.books_reader:
#         print(i.book.book_title)

print('connect as databese sucsecful')
