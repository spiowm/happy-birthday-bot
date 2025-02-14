import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import Config
from bot.sections.start.handlers import router as start_router
from bot.sections.questionnaire.handlers import router as questionnaire_router


async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        bot = Bot(token=Config.BOT_TOKEN)
        dp = Dispatcher()
        dp.include_routers(
            start_router,
            questionnaire_router,

        )
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")


if __name__ == '__main__':
    asyncio.run(main())


# потім ще добавити вірш або текст
# кнопки перегенерувати та почати знову