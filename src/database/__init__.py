from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url='sqlite://data/app.db',
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas()
    print("✅ Registered models:", Tortoise.apps)
