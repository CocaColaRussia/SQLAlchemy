from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Integer, String, BINARY, DATETIME, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, backref

# Enterprise DB to be used
USERNAME = "sa"
PSSWD = "sa"
SERVERNAME = "DESKTOP-0FB8G64"
DB = "vd-main"
DRIVER = "ODBC Driver 17 for SQL Server"

engine = create_engine(f"mssql+pyodbc://{USERNAME}:{PSSWD}@{SERVERNAME}/{DB}?driver={DRIVER}", echo=False)

Base = declarative_base()

# Документ_ЗаказКлиента_Товары = Table(
#     't_Документ_ЗаказКлиента_Товары', Base.metadata,
#     Column('t_Документ_ЗаказКлиента_Товары.ссылка', BINARY, ForeignKey('t_Документ_ЗаказКлиента.ссылка')),
#     Column('t_Документ_ЗаказКлиента_Товары.номенклатура', BINARY, ForeignKey('t_Справочник_Номенклатура.ссылка'))
# )

# class Документ_ЗаказКлиента(Base):
#     __tablename__ = 't_Документ_ЗаказКлиента'
#     ссылка = Column(BINARY, primary_key=True)
#     Номер = Column(String(max))
#     Номенклатура = relationship(
#                                 'Cправочник_Номенклатура',
#                                 secondary='t_Документ_ЗаказКлиента_Товары',
#                                 back_populates='ЗаказСсылка',
#                                 lazy=True
#                                 )
# readers = relationship(     #MTM
#         'User', secondary=association,
#         back_populates='books', lazy=True
#     )


# class Справочник_Номенклатура(Base):
#     __tablename__ = 't_Справочник_Номенклатура'
#     ссылка = Column(BINARY,  primary_key=True)
#     наименование = Column(String(max))
#     ЗаказСсылка = relationship(
#                                          'Документ_ЗаказКлиента',
#                                          secondary='t_Документ_ЗаказКлиента_Товары',
#                                          back_populates='Номенклатура',
#                                          lazy=True
#                                          )
# books = relationship(
#             'Book', secondary=association,
#             back_populates='readers', lazy=True
#         )









# Документ_ЗаказКлиента_Товары = Table(
#     't_Документ_ЗаказКлиента_Товары', Base.metadata,
#     Column('ссылка', BINARY, ForeignKey('t_Документ_ЗаказКлиента.ссылка')),
#     Column('номенклатура', BINARY, ForeignKey('t_Справочник_Номенклатура.ссылка')),
#     Column('Цена', Numeric(15,2))
# )
#
#
# class Док_ЗаказКлиента(Base):
#     __tablename__ = 't_Документ_ЗаказКлиента'
#     ссылка = Column(BINARY, primary_key=True)
#     Номер = Column(String(250))
#     Номенклатура = relationship(     #MTM
#         'Спр_Номенклатура', secondary=Документ_ЗаказКлиента_Товары,
#         back_populates='ЗаказКлиента', lazy=True
#     )
#     def __repr__(self):
#         return f'{self.Номер}'
#
#
#     class Спр_Номенклатура(Base):
#         __tablename__ = 't_Справочник_Номенклатура'
#         ссылка = Column(BINARY, primary_key=True)
#         наименование = Column(String(250))
#         ЗаказКлиента = relationship(
#             'Док_ЗаказКлиента', secondary=Документ_ЗаказКлиента_Товары,
#             back_populates='Номенклатура', lazy=True
#         )
#         def __repr__(self):
#             return f'{self.наименование}'
#
#
# session = sessionmaker(bind=engine)
# s = session()
#
#
# bok = s.query(Док_ЗаказКлиента).all()
# for el in bok:
#     print( el.Номенклатура )



class Order(Base):
    __tablename__ = "t_Документ_ЗаказКлиента"
    ссылка = Column(BINARY, primary_key=True)
    order_items = relationship(
        "OrderItem", cascade="all, delete-orphan", backref="t_Документ_ЗаказКлиента"
    )

    # def __init__(self, customer_name):
    #     self.customer_name = customer_name


class Item(Base):
    __tablename__ = "t_Справочник_Номенклатура"
    ссылка = Column(BINARY, primary_key=True)
    наименование = Column(String(250), nullable=False)

    # def __init__(self, description, price):
    #     self.description = description
    #     self.price = price
    #
    # def __repr__(self):
    #     return "Item(%r, %r)" % (self.description, self.price)


class OrderItem(Base):
    __tablename__ = "t_Документ_ЗаказКлиента_Товары"
    ссылка = Column(BINARY, ForeignKey("t_Документ_ЗаказКлиента.ссылка"), primary_key=True)
    номенклатура = Column(Integer, ForeignKey("t_Справочник_Номенклатура.ссылка"), primary_key=True)
    цена = Column(Float, nullable=False)

    # def __init__(self, item, price=None):
    #     self.item = item
    #     self.price = price or item.price
# f
    item = relationship(Item, lazy="joined")


session = sessionmaker(bind=engine)
s = session()

# query the order, print items
# order = s.query(Order).first()
# print( order
#     # [
#     #     (order_item.item.наименование, order_item.цена)
#     #     for order_item in order.order_items
#     # ]
# )

order = s.query(Order).all()
for element in order:
    print(element.order_items[0].item.наименование, element.order_items[0].цена)
