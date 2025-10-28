import os
from pathlib import Path
import sqlite3
import time

from config import GRAMMER_TABLE_NAME, QUESTIONS_TABLE_NAME, WORDS_TABLE_NAME
from services.database import (
    add_grammer_to_db,
    add_question_to_db,
    add_word_to_db,
    create_db,
    delete_question,
    delete_user_text_in_word_or_grammer,
    get_all_info_dates,
    pull_added_today,
)
from services.quiz import Quiz


def test_create_db(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    assert os.path.exists(TEMP_DB_PATH)
    
def test_adding_word_to_db(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    word = "this is adding_word_to_db test word"
    add_word_to_db(word, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {WORDS_TABLE_NAME} WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_user_text_in_word_or_grammer('word', word, TEMP_DB_PATH)
    assert added_result is not None

def test_delete_user_text_in_word_or_grammer(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    word = "this is adding_word_to_db test word"
    add_word_to_db(word, TEMP_DB_PATH)
    delete_user_text_in_word_or_grammer(WORDS_TABLE_NAME, word, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {WORDS_TABLE_NAME} WHERE user_text=?", (word,)) 
    result = cursor.fetchone()
    cursor.close()
    assert result is None
    
def test_adding_grammer_to_db(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    grammer = "this is adding_grammer_to_db grammer"
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {GRAMMER_TABLE_NAME} WHERE user_text=?", (grammer,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is not None

def test_pull_info_for_quiz(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    grammer = "this is pull_info_for_test word"
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    dates = Quiz.pull_dates_for_quiz(Quiz, TEMP_DB_PATH)
    info_to_test = Quiz.pull_info_for_quiz(Quiz, dates, TEMP_DB_PATH)
    assert grammer in info_to_test
    
def test_pull_added_today(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    grammer = "this is pull_added_today test"
    word = "this is pull_added_today test"
    add_word_to_db(word, TEMP_DB_PATH)
    add_grammer_to_db(grammer, TEMP_DB_PATH)
    grammers = pull_added_today(GRAMMER_TABLE_NAME, TEMP_DB_PATH)
    words = pull_added_today(WORDS_TABLE_NAME, TEMP_DB_PATH)
    clean_words = [word for words, _ in words]
    clean_grammer = [grammer for grammer, _ in grammers]
    assert word in clean_words
    assert grammer in clean_grammer
    
def test_add_question_to_db(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    question = ("this is a question?")
    add_question_to_db(question, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {QUESTIONS_TABLE_NAME} WHERE question=?", (question,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is not None
    
def test_delete_question(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    question = ("this is a question?")
    add_question_to_db(question, TEMP_DB_PATH)
    delete_question(question, TEMP_DB_PATH)
    connection = sqlite3.connect(TEMP_DB_PATH)  
    cursor = connection.cursor()  
    cursor.execute(f"SELECT * FROM {QUESTIONS_TABLE_NAME} WHERE question=?", (question,)) 
    added_result = cursor.fetchone()
    cursor.close()
    assert added_result is None
    
def test_get_all_info_dates(tmp_path):
    TEMP_DB_PATH = Path(str(tmp_path)) / "test_db.sqlite"
    create_db(TEMP_DB_PATH)
    word = "get_all_info_dates"
    add_word_to_db(word, TEMP_DB_PATH)
    dates = get_all_info_dates(WORDS_TABLE_NAME, TEMP_DB_PATH)
    assert (time.strftime('%Y-%m-%d'),) in dates


