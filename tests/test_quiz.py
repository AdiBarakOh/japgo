from pathlib import Path
import time

from config import (
    LONG_QUIZ_QUESTIONS,
    LONG_QUIZ_REACTION,
    MEDIUM_QUIZ_QUESTIONS,
    MEDIUM_QUIZ_REACTION,
    SHORT_QUIZ_QUESTIONS,
    SHORT_QUIZ_REACTION,
)
from services.database import add_word_to_db, create_db
from services.quiz import Quiz


def test_calc_how_many_questions():
    assert (
        Quiz.calc_how_many_questions(Quiz, SHORT_QUIZ_REACTION) == SHORT_QUIZ_QUESTIONS
    )
    assert (
        Quiz.calc_how_many_questions(Quiz, MEDIUM_QUIZ_REACTION) == MEDIUM_QUIZ_QUESTIONS
    )
    assert (
        Quiz.calc_how_many_questions(Quiz, LONG_QUIZ_REACTION) == LONG_QUIZ_QUESTIONS
    )


def test_quiz_info_collecting(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    word = "test word"
    add_word_to_db(word, TEMP_DB_PATH)
    assert (time.strftime('%Y-%m-%d')) in Quiz.pull_dates_for_quiz(Quiz, TEMP_DB_PATH)
    assert word in Quiz.pull_info_for_quiz(Quiz, [time.strftime('%Y-%m-%d')], TEMP_DB_PATH)









