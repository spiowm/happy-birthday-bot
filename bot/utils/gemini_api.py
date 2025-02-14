from typing import List

# from bot.sections.questionnaire.handlers import Question
from config import Config
from google import genai


async def generate_wish(questions) -> str:
    prompt = """На основі відповідей:  



Створи персоналізоване привітання-програмістську історію. Історія має бути веселою, креативною та містити жартівливі відсилки до програмування, технологій і навіть штучного інтелекту. Завершення має бути надихаючим і щирим.  

Приклад фрази-закінчення: "Нехай твій код завжди буде без багів, а життя — з нескінченними циклами щастя! 🎂💻"  

Зроби два варіанти історії: фентезі та кіберпанк.  

    
    """
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    response = client.models.generate_content(model=Config.MODEL, contents=prompt)
    return response.text
