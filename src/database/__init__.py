from tortoise import Tortoise
from config import Config

TORTOISE_ORM = {
    "connections": {"default": "sqlite://data/app.db"},
    "apps": {
        "models": {
            "models": ["database.models"],
            "default_connection": "default",
        }
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
