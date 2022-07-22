from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Boolean,
    Text,
    Date,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    nickname = Column(String)
    max_to_order = Column(Integer, default=8)

    def __repr__(self):
        return "<User(id='%s' name='%s', nickname='%s', max_to_order='%s')>" % (
            self.id,
            self.name,
            self.nickname,
            self.max_to_order,
        )


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    alt_prices = Column(JSON, nullable=True, server_default="{}")
    is_coffee = Column(Boolean, nullable=True, default=False)
    is_milk = Column(Boolean, nullable=True, default=False)
    is_lact_free_milk = Column(Boolean, nullable=True, default=False)
    is_vegan_milk = Column(Boolean, nullable=True, default=False)
    is_tea = Column(Boolean, nullable=True, default=False)
    is_matcha = Column(Boolean, nullable=True, default=False)
    is_season = Column(Boolean, nullable=True, default=False)
    available = Column(Boolean, nullable=True, default=True)
    is_black_coffee = Column(Boolean, nullable=True, default=False)
    is_fresh = Column(Boolean, nullable=True, default=False)
    is_other = Column(Boolean, nullable=True, default=False)
    is_deserts = Column(Boolean, nullable=True, default=False)
    description = Column(Text, nullable=True, default="")
    volume = Column(String, nullable=True, default="")

    def __repr__(self):
        return "<MenuItem(id='%s' name='%s',  price='%s')>" % (
            self.id,
            self.name,
            self.price,
        )


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    order_date = Column(Date)
    product_type = Column(Text)
    qty = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return (
                "<Booking(id='%s' user_id='%s', order_date='%s', product_type='%s', qty='%s')>"
                % (self.id, self.user_id, self.order_date, self.product_type, self.qty)
        )
