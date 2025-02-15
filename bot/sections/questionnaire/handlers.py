from aiogram import Router, F, types, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
# from bot.utils.gemini_api import generate_wish
from typing import List, Optional
from . import keyboards

router = Router()

from config import Config
from google import genai


class Question:
    def __init__(self, question_id: str, question: str, answer: str = None):
        self.question_id = question_id
        self.question_text = question
        self.answer_text = answer


async def generate_wish(questions: List[Question]) -> (str, str):
    """Generate personalized greeting using Gemini API."""
    questions_text = "\n".join(
        f"Питання: {q.question_text}\nВідповідь: {q.answer_text}"
        for q in questions
    )

    prompt = f"""Ти - креативний письменник, який створює персоналізовані програмістські історії-привітання. 
Використовуй інформацію нижче, щоб створити унікальне, веселе та надихаюче привітання:
Питання: Як звати?
Відповідь: Денис
{questions_text}

Вказівки для створення історії:
1. Створи захоплюючу історію (довжиною 1500-2000 символів), яка переплітає всі деталі з відповідей.
2. Додай технічний гумор та програмістські жарти, пов'язані з наданою інформацією.
3. Використовуй сучасні емодзі доречно (3-5 емодзі на абзац).
4. Зроби історію динамічною - з несподіваними поворотами, можливо, з елементами обраного стилю розповіді.
5. Включи відсилки до сучасних технологій, ШІ та програмування.
6. Заверши історію потужним побажанням, яке поєднує особисті деталі з програмістською тематикою.

Стиль написання:
- Дружній та енергійний тон
- Короткі, динамічні речення
- Використовуй деталі з відповідей для створення персоналізованих метафор
- Додавай трохи самоіронії та добрих жартів про програмістське життя

Приклад фрази-закінчення: "Нехай твій код завжди буде без багів, а життя — з нескінченними циклами щастя! 🎂💻"  
"""
    # Створи персоналізоване привітання-програмістську історію. Історія має бути веселою, креативною та містити
    # жартівливі відсилки до програмування, технологій і навіть штучного інтелекту. Також додавай трохи влучних смайликів.
    # Завершення має бути надихаючим і щирим.

    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=Config.MODEL,
            contents=prompt
        )
        return prompt, response.text
    except Exception as e:
        return prompt, f"На жаль, сталася помилка при генерації привітання. Спробуйте ще раз пізніше. Помилка: {str(e)}"


# Визначаємо стани як клас
class QuestionnaireStates(StatesGroup):
    favorite_language = State()
    dream_location = State()
    favorite_movie = State()
    favorite_game = State()
    coding_place = State()
    genre = State()


QUESTIONS = [
    Question('favorite_language', '🛠 Яка мова програмування приносить тобі найбільше задоволення?'),
    Question('dream_location', '🌍 Назви місце, де ти хотів би прокинутися завтра вранці?'),
    Question('favorite_movie', '🎥 З яким героєм фільму ти себе найбільше асоціюєш?'),
    Question('favorite_game', '🎮 Чим ти любиш займатися, коли хочеш відпочити від усього?'),
    Question('coding_place', '🌈 Де ти найбільше любиш кодити? \n(Затишна кав\'ярня, офіс з командою, домашній setup з котом на колінах, чи може космічна станція?)'),
    Question('genre', '🎬 В якому стилі ти хочеш отримати своє привітання? \n(Епічне фентезі, кіберпанк, комедія, надихаюча історія успіху чи, може, романтична драма з багами в головній ролі?)')
]


@router.callback_query(F.data == "questionnaire__start")
async def start_questionnaire(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    # Встановлюємо перший стан
    await state.set_state(QuestionnaireStates.favorite_language)

    # Відправляємо перше питання
    await callback_query.message.answer(text=QUESTIONS[0].question_text)
    await callback_query.answer()


@router.message(QuestionnaireStates.favorite_language)
async def process_favorite_language(message: types.Message, state: FSMContext):
    await state.update_data(favorite_language=message.text)
    await state.set_state(QuestionnaireStates.dream_location)
    await message.answer(QUESTIONS[1].question_text)


@router.message(QuestionnaireStates.dream_location)
async def process_dream_location(message: types.Message, state: FSMContext):
    await state.update_data(dream_location=message.text)
    await state.set_state(QuestionnaireStates.favorite_movie)
    await message.answer(QUESTIONS[2].question_text)


@router.message(QuestionnaireStates.favorite_movie)
async def process_favorite_movie(message: types.Message, state: FSMContext):
    await state.update_data(favorite_movie=message.text)
    await state.set_state(QuestionnaireStates.favorite_game)
    await message.answer(QUESTIONS[3].question_text)


@router.message(QuestionnaireStates.favorite_game)
async def process_favorite_food(message: types.Message, state: FSMContext):
    await state.update_data(favorite_game=message.text)
    await state.set_state(QuestionnaireStates.coding_place)
    await message.answer(QUESTIONS[4].question_text)


@router.message(QuestionnaireStates.coding_place)
async def process_last_task(message: types.Message, state: FSMContext):
    await state.update_data(coding_place=message.text)
    await state.set_state(QuestionnaireStates.genre)
    await message.answer(QUESTIONS[5].question_text)


@router.message(QuestionnaireStates.genre)
async def process_genre(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    await state.clear()
    # Update questions with answers
    questions = list(QUESTIONS)  # Create a copy to modify
    for question in questions:
        question.answer_text = data.get(question.question_id, "Немає відповіді")

    # Generate and send the wish
    await message.answer("🎨 Генерую ваше персоналізоване привітання...")
    prompt, wish_text = await generate_wish(questions)

    await message.answer(
        text=wish_text,
        parse_mode="Markdown",
        reply_markup=keyboards.again
    )

    try:
        await bot.send_message(
            chat_id=str(Config.ADMIN_TG_ID),
            text=prompt,
            parse_mode="Markdown",

        )
    except Exception as e:
        print(e)

    try:
        await bot.send_message(
            chat_id=str(Config.ADMIN_TG_ID),
            text=wish_text,
            parse_mode="Markdown",

        )
    except Exception as e:
        print(e)
