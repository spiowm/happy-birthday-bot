from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL = os.getenv('MODEL')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_TG_ID = os.getenv('ADMIN_TG_ID')