from aiogram import Router, F, types
from aiogram.filters import CommandStart

from . import keyboards

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    text = f'''Привіт, {message.from_user.first_name}! 🧑‍💻 Сьогодні я твій персональний AI-напарник із святкування Дня Народження! 🥳 Хочу створити для тебе особливе привітання, яке залишить яскравий слід у твоїй пам'яті ❤️💾 Але мені потрібна трішки інформації від тебе. Готовий? 🚀'''
    await message.answer(text, reply_markup=keyboards.start)


