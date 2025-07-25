import asyncio
import nest_asyncio
from pyrogram import idle
from app import app, init_handlers
from database import init_db

nest_asyncio.apply()  


async def startup():
    await init_db()        
    init_handlers(app)     
    await app.start()     
    print("🤖 Bot is running...")
    await idle()            
    await app.stop()        


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
