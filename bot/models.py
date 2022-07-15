from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Text, Date, func, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    nickname = Column(String)
    max_to_order = Column(Integer, default=8)

    def __repr__(self):
        return "<User(id='%s' name='%s', nickname='%s', max_to_order='%s')>" \
               % (self.id, self.name, self.nickname, self.max_to_order)


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
    is_season = Column(Boolean, nullable=False)
    available = Column(Boolean, nullable=False)
    is_black_coffee = Column(Boolean, nullable=False)
    is_fresh = Column(Boolean, nullable=False)
    is_other = Column(Boolean, nullable=False)
    is_deserts = Column(Boolean, nullable=False)
    description = Column(Text, nullable=False)
    volume = Column(String, nullable=False)


class Booking(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    order_date = Column(Date)
    product_type = Column(Text)
    qty = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return "<Booking(id='%s' user_id='%s', order_date='%s', product_type='%s', qty='%s')>" \
               % (self.id, self.user_id, self.order_date, self.product_type, self.qty)
