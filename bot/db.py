from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import config
from models import User, Booking
from bot.navigation import get_next_saturday

engine = create_async_engine(config.DB_URI)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def getting_users_from_session(search):
    async with async_session() as session:
        result = await session.execute(select(User).where(search))
        print(result)

        users = result.fetchall()

    return users


async def get_booking_for_user(user_id):
    next_saturday = get_next_saturday()
    async with async_session() as session:
        result = await session.execute(
            select(Booking).where(Booking.user_id == user_id, Booking.order_date == next_saturday)
        )
        print("result", result)

        booking = result.fetchall()
        booking_result = {}
        for row in booking:
            booking_result[row.Booking.product_type] = row.Booking

    return booking_result


async def get_user_by_id(user_id):
    return (await getting_users_from_session(User.id == user_id))[0]


async def get_verified_user(status):
    return await getting_users_from_session(User.is_verified == status)


async def query_menu_items(sql_query):
    async with async_session() as session:
        r = await session.execute(sql_query)
        results_as_dict = r.mappings().all()

    return results_as_dict


async def get_user(update):
    async with async_session() as session:
        user = await session.get(User, update.effective_user.id)
        if not user:
            user = User(
                id=update.effective_user.id,
                name=update.effective_user.first_name,
                nickname=update.effective_user.username,
            )
            session.add(user)
            await session.commit()
    return user


async def update_booking_qty(user_id, product_type, math):
    async with async_session() as session:
        booking = await get_booking_for_user(user_id)
        user = await get_user_by_id(user_id)
        diff = -1 if math == '-' else 1

        print("booking", booking)
        print("user", user)
        if product_type in booking:
            booking[product_type].qty = max(0, min(booking[product_type].qty + diff, user[0].max_to_order))
        else:
            booking[product_type] = Booking(qty=1, user_id=user_id,
                                            order_date=get_next_saturday(),
                                            product_type=product_type)
        session.add(booking[product_type])
        await session.commit()


async def verify_user(user_id):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user:
            user.is_verified = True
        session.add(user)
        await session.commit()
