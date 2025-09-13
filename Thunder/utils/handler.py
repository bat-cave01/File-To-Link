# Thunder/utils/handler.py

import asyncio
from typing import Callable, Any
from pyrogram.errors import FloodWait, MessageNotModified
from Thunder.utils.logger import logger


async def handle_flood_wait(
    func: Callable, *args, retries: int = 3, delay: int = 3, **kwargs
) -> Any:
    """
    Wrapper to safely call Pyrogram functions with:
      - Automatic retry on FloodWait
      - Ignore MessageNotModified
      - Logging of all retries/errors

    Args:
        func (Callable): Async Pyrogram function to call
        retries (int): Number of retries for recoverable errors
        delay (int): Delay (in seconds) between retries for non-flood errors

    Returns:
        Any: The result of the function call, or None if suppressed
    """
    for i in range(retries):
        try:
            return await func(*args, **kwargs)

        # --- Handle FloodWait ---
        except FloodWait as e:
            wait_time = e.value
            logger.debug(
                f"[FloodWait] '{func.__name__}' → waiting {wait_time}s "
                f"(retry {i + 1}/{retries})"
            )
            await asyncio.sleep(wait_time)

        # --- Handle MessageNotModified (ignore safely) ---
        except MessageNotModified:
            logger.debug(
                f"[MessageNotModified] '{func.__name__}' → ignored (retry {i + 1}/{retries})"
            )
            return None

        # --- Handle Other Exceptions ---
        except Exception:
            logger.error(
                f"[Exception] in '{func.__name__}' on retry {i + 1}/{retries}",
                exc_info=True,
            )
            if i < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise

    return None
