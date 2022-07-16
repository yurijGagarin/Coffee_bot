import asyncio
from functools import wraps

import click

import data.menu_items as menu_items
from db import async_session
from models import MenuItem


@click.group()
def cli():
    pass


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@cli.command()
@coro
async def load_data():
    click.echo("Load data into database")
    data = menu_items.data

    async with async_session() as session:
        await session.execute(MenuItem.__table__.delete())
        for datum in data:
            model = MenuItem()
            for k, v in datum.items():
                setattr(model, k, v)
            session.add(model)

        await session.commit()


if __name__ == "__main__":
    cli()
