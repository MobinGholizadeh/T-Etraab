import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.config.settings import settings
from src.presentation.bot.handlers import common, manager

logger = logging.getLogger(__name__)

def create_bot() -> tuple[Bot, Dispatcher]:
    """Initialize bot and dispatcher with all routers"""
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

                         
    dp.include_router(common.router)
    dp.include_router(manager.router)
    
    return bot, dp

async def start_polling():
    """Start polling for Telegram updates"""
    logger.info("Starting Telegram Bot in polling mode...")
    bot, dp = create_bot()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_polling())
