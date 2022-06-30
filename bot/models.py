
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Text, Date

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    nickname = Column(String)
    max_to_book = Column(Integer, default=8)
    sweet = Column(Integer, default=0)
    salty = Column(Integer, default=0)
    order_date = Column(Date)

    def __repr__(self):
        return "<User(id='%s' name='%s', nickname='%s', sweet='%s', salty='%s', max_to_book='%s')>" \
               % (self.id, self.name, self.nickname, self.sweet, self.salty, self.max_to_book)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    is_coffee = Column(Boolean, nullable=False)
    is_milk = Column(Boolean, nullable=False)
    is_lact_free_milk = Column(Boolean, nullable=False)
    is_vegan_milk = Column(Boolean, nullable=False)
    is_tea = Column(Boolean, nullable=False)
    is_matcha = Column(Boolean, nullable=False)
    is_cold = Column(Boolean, nullable=False)
    is_black_coffee = Column(Boolean, nullable=False)
    is_fresh = Column(Boolean, nullable=False)
    is_other = Column(Boolean, nullable=False)
    is_deserts = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)
    volume = Column(String, nullable=False)
