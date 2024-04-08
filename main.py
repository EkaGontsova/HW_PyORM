import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Sale, Book, Shop, Publisher, Stock


DSN = 'postgresql://postgres:postgres@localhost:5432/HW_PySQL'

engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as f:
    data = json.load(f)
    for item in data:
        model = item.get('model')
        pk = item.get('pk')
        fields = item.get('fields')

        if model == 'publisher':
            publisher = Publisher(id=pk, name=fields.get('name'))
            session.add(publisher)
        elif model == 'book':
            book = Book(id=pk, title=fields.get('title'), id_publisher=fields.get('id_publisher'))
            session.add(book)
        elif model == 'shop':
            shop = Shop(id=pk, name=fields.get('name'))
            session.add(shop)
        elif model == 'stock':
            stock = Stock(id=pk, id_shop=fields.get('id_shop'), id_book=fields.get('id_book'),
                          count=fields.get('count'))
            session.add(stock)
        elif model == 'sale':
            price = float(fields.get('price'))
            sale = Sale(price=price, id_stock=fields.get('id_stock'), sale_date=fields.get('date_sale'),
                        count=fields.get('count'))
            session.add(sale)

session.commit()

# Вывод данных о продажах книг заданного издателя

publisher_input = input("Enter publisher's name or ID: ")
if publisher_input.isdigit():
    publisher = session.query(Publisher).filter(Publisher.id == int(publisher_input)).first()
else:
    publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()

if publisher:
    sales = (session.query(Sale).join(Stock).join(Book).join(Publisher).join(Shop).
             filter(Book.id_publisher == publisher.id).all())
    for sale in sales:
        print(f'{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | '
              f'{sale.sale_date.strftime("%d-%m-%Y")}')
else:
    print('Publisher not found')

session.close()

session.close()
