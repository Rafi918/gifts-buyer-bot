from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://data/orders.db',
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas()
