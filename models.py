import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publishers'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)


class Book(Base):
    __tablename__ = 'books'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publishers.id'))
    publisher = relationship('Publisher')


class Sale(Base):
    __tablename__ = 'sales'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    stock = relationship('Stock')
    sale_date = sq.Column(sq.DateTime)
    count = sq.Column(sq.Integer)


class Shop(Base):
    __tablename__ = 'shops'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    stock = relationship('Stock', back_populates='shop', overlaps='shop')


class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('books.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shops.id'))
    count = sq.Column(sq.Integer)
    book = relationship(Book, backref='books')
    shop = relationship(Shop, back_populates='stock')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
