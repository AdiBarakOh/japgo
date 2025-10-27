import discord
import os
import logging

logging.basicConfig(filename='main_log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger("config")

# --- discord ---
DISCORD_INTENTS:discord.Intents = discord.Intents.default()
DISCORD_INTENTS.message_content = True
DISCORD_CLIENT: discord.Client = discord.Client(intents=DISCORD_INTENTS)

# --- tokens ---
DISCORD_TOKEN: str | None = os.getenv("JAPGO_DISCORD_TOKEN")
OPENAI_API_KEY: str | None = os.getenv('open_ai_token')

# --- bot settings ---
BOT_PREFIX: str = "!japgo" # Small caps
if BOT_PREFIX != BOT_PREFIX.lower():
    logger.warning("BOT_PREFIX includes capital letters.")
GENERAL_REACTION_SECONDS: int = 100
DAYS_HOMEWORK_REMINDER: int = 4

# --- channels ---
QUIZ_CHANNEL_NAME: str = "quiz"
HOME_WORK_CHANNEL_NAME: str = "homework-help"
GRAMMER_CHANNEL_NAME: str = "grammer"
WORDS_CHANNEL_NAME: str = "words-kanji"

# --- paths ---
DATA_BASE_PATH: str = "data/japgo_db"

# --- quiz settings ---
SHORT_QUIZ_QUESTIONS: int = 1
MEDIUM_QUIZ_QUESTIONS: int = 2
LONG_QUIZ_QUESTIONS: int = 3
SHORT_QUIZ_REACTION: str = "👍"
MEDIUM_QUIZ_REACTION: str = "😆",
LONG_QUIZ_REACTION: str =  "🙏"
QUESTION_SEPERATION: str = "q:"
ANSWER_SEPARATION: str = "a:"
LONGEST_INPUT_OF_DATA_TO_QUIZ: int = 500
SECONDS_FOR_ANSWER_QUIZ: int = 60 * 3
MAX_DATES_TO_QUIZ: int = 3

# --- data base settings ---
WORDS_TABLE_NAME: str = "word"
GRAMMER_TABLE_NAME: str = "grammer"
QUESTIONS_TABLE_NAME: str = "questions"

# --- ai responses ---
OPENAI_MODEL_NAME: str = "gpt-4.1-nano"
MAX_OUTPUT_TOKENS: int = 1000
AI_INSTRUCTIONS: str = (
                "return only questions(no numbering) and answers with:" +
                f"{QUESTION_SEPERATION}, {ANSWER_SEPARATION}."
            )
def clean_user_input_for_ai(
    how_many_questions: int, info_to_test: list, more_instructions=''
    ) -> str:
    combined: str = (
        f"this is what I learned at japanease class: {info_to_test}. " +
        f"create ONLY {how_many_questions} questions to help me practice" +
        "(translate, fill the word, verb formations) and more." +
        more_instructions
    )
    return combined

if DISCORD_TOKEN is None: 
    logging.warning("DISCORD_TOKEN was not found as environment variable.")
if OPENAI_API_KEY is None:
    logging.warning("OPENAI_API_KEY was not found as environment variable.")

logger.debug("Configuration loaded.")