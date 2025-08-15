import asyncio
import logging
from config import config

async def fetch_gifts(session):
    for attempt in range(1, config.API_MAX_RETRIES + 1):
        try:
            async with session.get(config.API_URL) as resp:
                if resp.status != 200:
                    logging.warning(f"[Attempt {attempt}] Got status {resp.status} from {config.API_URL}")
                    raise Exception(f"Unexpected status: {resp.status}")

                data = await resp.json(content_type=None)
                gifts = data.get("available gifts")

                if gifts is None:
                    logging.error(f"No 'available gifts' key in response: {data}")
                    return []

                return gifts

        except Exception as e:
            logging.error(f"[Attempt {attempt}] Error fetching gifts: {e}")

            if attempt < config.API_MAX_RETRIES:
                delay = config.API_RETRY_DELAY * (2 ** (attempt - 1))
                logging.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                logging.critical(f"All {config.API_MAX_RETRIES} attempts to fetch gifts failed.")
                return []
