import sqlite3
import string
import random
import time

from ai_responses import create_quiz
from data_bases import (
    add_grammer_to_db,
    add_word_to_db,
    create_db,
    delete_user_text_in_word_or_grammer,
)
from quizes import Quiz

create_db()

def create_random_text(lengh: int):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_characters = ''.join([random.choice(characters) for i in range(lengh)])
    return random_characters

def test_adding_word_to_db() -> bool:
    word = "this is adding_word_to_db test word"
    add_word_to_db(word)
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM word WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_user_text_in_word_or_grammer('word', word)
    return added_result is not None

def test_adding_grammer_to_db() -> bool:
    word = "this is adding_grammer_to_db grammer"
    add_grammer_to_db(word)
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM grammer WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_user_text_in_word_or_grammer('grammer', word)
    return added_result is not None

def test_create_quiz() -> bool:
    ai_quiz = create_quiz(1, ["よる　よります", "ことにする　i have decided to do"])
    for ai_output in ai_quiz.split("\n"):
        if len(ai_output) == 0:
            return False
    return True

def test_pull_info_for_quiz() -> bool:
    word = "this is pull_info_for_test word"
    add_grammer_to_db(word)
    info_to_test = Quiz.pull_info_for_quiz(Quiz, dates=[time.strftime('%Y-%m-%d')])
    delete_user_text_in_word_or_grammer('grammer', word)
    return word in info_to_test


    




