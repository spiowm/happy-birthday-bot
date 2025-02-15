from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)



again = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Спробувати ще раз 🔄", callback_data="questionnaire__start")],
    ],
)

