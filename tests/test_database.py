import sqlite3
import os
import time

from config import GRAMMER_TABLE_NAME, QUESTIONS_TABLE_NAME, WORDS_TABLE_NAME
from services.database import (
    add_grammer_to_db,
    add_question_to_db,
    add_word_to_db,
    create_db,
    delete_user_text_in_word_or_grammer,
    delete_question,
    get_all_info_dates,
    pull_added_today,
    
)
from services.quiz import Quiz

TEMP_DB_PATH = str(lambda tmp_path: tmp_path)

def test_create_db():
    create_db(TEMP_DB_PATH)
    assert os.path.exists(TEMP_DB_PATH)
    
def test_adding_word_to_db():
    word = "this is adding_word_to_db test word"
    add_word_to_db(word, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {WORDS_TABLE_NAME} WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_user_text_in_word_or_grammer('word', word, TEMP_DB_PATH)
    assert added_result is not None

def test_delete_user_text_in_word_or_grammer():
    word = "this is adding_word_to_db test word"
    add_word_to_db(word, TEMP_DB_PATH)
    delete_user_text_in_word_or_grammer(WORDS_TABLE_NAME, word, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {WORDS_TABLE_NAME} WHERE user_text=?", (word,)) 
    result = cursor.fetchone()
    cursor.close()
    assert result is None
    
def test_adding_grammer_to_db():
    grammer = "this is adding_grammer_to_db grammer"
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {GRAMMER_TABLE_NAME} WHERE user_text=?", (grammer,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is not None

def test_pull_info_for_quiz():
    grammer = "this is pull_info_for_test word"
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    info_to_test = Quiz.pull_info_for_quiz(Quiz, dates=[time.strftime('%Y-%m-%d')])
    assert grammer in info_to_test
    
def test_pull_added_today():
    grammer = "this is pull_added_today test"
    word = "this is pull_added_today test"
    add_word_to_db(word, TEMP_DB_PATH)
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    grammers = pull_added_today(GRAMMER_TABLE_NAME, TEMP_DB_PATH)
    words = pull_added_today(WORDS_TABLE_NAME, TEMP_DB_PATH)
    assert word in words
    assert grammer in grammers
    
def test_add_question_to_db():
    question = ("this is a question?")
    add_question_to_db(question, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {QUESTIONS_TABLE_NAME} WHERE user_text=?", (question,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is not None
    
def test_delete_question():
    question = ("this is a question?")
    add_question_to_db(question, TEMP_DB_PATH)
    delete_question(question, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {QUESTIONS_TABLE_NAME} WHERE user_text=?", (question,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is None
    
def test_get_all_info_dates():
    word = "get_all_info_dates"
    add_word_to_db(word, TEMP_DB_PATH)
    dates = get_all_info_dates(WORDS_TABLE_NAME, TEMP_DB_PATH)
    assert time.strftime('%Y-%m-%d') in dates
    
    
    