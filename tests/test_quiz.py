import time

from config import (
    SHORT_QUIZ_REACTION,
    SHORT_QUIZ_QUESTIONS,
    MEDIUM_QUIZ_REACTION,
    MEDIUM_QUIZ_QUESTIONS,
    LONG_QUIZ_QUESTIONS,
    LONG_QUIZ_REACTION,
)
from services.quiz import Quiz
from services.database import add_word_to_db, create_db



def test_Quiz ():
    assert isinstance(Quiz(), Quiz)

def test_calc_how_many_questions():
    assert (
        Quiz.calc_how_many_questions(SHORT_QUIZ_REACTION) == SHORT_QUIZ_QUESTIONS
    )
    assert (
        Quiz.calc_how_many_questions(MEDIUM_QUIZ_REACTION) == MEDIUM_QUIZ_QUESTIONS
    )
    assert (
        Quiz.calc_how_many_questions(LONG_QUIZ_REACTION) == LONG_QUIZ_QUESTIONS
    )


def test_quiz_info_collecting(tmp_path):
    create_db(tmp_path)
    word = "test word"
    add_word_to_db(word, tmp_path)
    assert (time.strftime('%Y-%m-%d')) in Quiz.pull_dates_for_quiz(Quiz, tmp_path)
    assert word in Quiz.pull_info_for_quiz(time.strftime('%Y-%m-%d'))
    

    

    




