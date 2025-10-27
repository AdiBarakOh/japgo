import logging
import sqlite3
import time

from config import (
    DATA_BASE_PATH, GRAMMER_TABLE_NAME, QUESTIONS_TABLE_NAME, WORDS_TABLE_NAME,
)
   
logger = logging.getLogger('data_base')


def create_db(db_path: str = DATA_BASE_PATH) -> None:
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {WORDS_TABLE_NAME}(user_text TEXT, date_added TEXT)") 
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {GRAMMER_TABLE_NAME}(user_text TEXT, date_added TEXT)")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {QUESTIONS_TABLE_NAME}(question TEXT, score INT, date_added TEXT)")
    cursor.close()
   
def add_word_to_db(word: str, db_path: str = DATA_BASE_PATH) -> bool: 
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {WORDS_TABLE_NAME} WHERE user_text=?", (word,))
    if cursor.fetchone():
        logger.debug("word already exists in the database.")
        cursor.close()
        return False
    else:
        cursor.execute(
        f"INSERT INTO {WORDS_TABLE_NAME} (user_text, date_added) VALUES (?, ?)",
        (word, time.strftime('%Y-%m-%d'),)
        )
        connection.commit()
        cursor.close()
        logger.debug("word inserted to database.")
    return True
    
def add_grammer_to_db(grammer: str, db_path: str = DATA_BASE_PATH) -> None:
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {GRAMMER_TABLE_NAME} WHERE user_text=?", (grammer,))
    if cursor.fetchone():
        logger.debug("grammer already exists in the database.")
    else:
        cursor.execute(
            f"INSERT INTO {GRAMMER_TABLE_NAME} (user_text, date_added) VALUES (?, ?)",
            (grammer, time.strftime('%Y-%m-%d'),)
        )
        connection.commit()
        logger.debug("grammer inserted to database.")
    cursor.close()

def get_all_info_dates(table: str, db_path: str = DATA_BASE_PATH) -> list[str|None]:
    """ 
    Return all info learnd in the given dates
    """
    if table in [WORDS_TABLE_NAME, GRAMMER_TABLE_NAME]:
        connection = sqlite3.connect(db_path)  
        cursor = connection.cursor()
        cursor.execute(f"SELECT date_added FROM {table}")
        all_info = cursor.fetchall()
        cursor.close() 
        return all_info
    logger.error("db get_all_info was used without proper table name.")
    return [] 
    
def get_info_by_date(date_requested: str, db_path: str = DATA_BASE_PATH) -> list:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT user_text FROM {GRAMMER_TABLE_NAME} WHERE date_added=?", (date_requested,))
    all_grammer = cursor.fetchall()
    cursor.execute(f"SELECT user_text FROM {WORDS_TABLE_NAME} WHERE date_added=?", (date_requested,))
    all_words = cursor.fetchall()
    cursor.close()
    return all_grammer + all_words

def add_question_to_db(question_to_add:str, db_path: str = DATA_BASE_PATH) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {QUESTIONS_TABLE_NAME} WHERE question=?", (question_to_add,))
    if cursor.fetchone():
        cursor.close()
        return
    cursor.execute(f"INSERT INTO {QUESTIONS_TABLE_NAME} VALUES (?,?,?)", (question_to_add, 0, time.strftime('%Y-%m-%d'),))
    connection.commit()
    cursor.close()
    
def delete_user_text_in_word_or_grammer(
        table: str, user_text: str, db_path: str = DATA_BASE_PATH
) -> None:
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    if table in ({WORDS_TABLE_NAME}, {GRAMMER_TABLE_NAME}):
        cursor.execute(f"DELETE FROM {table} WHERE user_text=?", (user_text,))
        connection.commit()
    cursor.close()
    
def delete_question(question: str, db_path: str = DATA_BASE_PATH) -> None:
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {QUESTIONS_TABLE_NAME} WHERE question=?", (question,))
    connection.commit()
    cursor.close()
    
def pull_added_today(table: str, db_path: str = DATA_BASE_PATH) -> list[str]:
    connection = sqlite3.connect(db_path)  
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE date_added=?", (time.strftime('%Y-%m-%d'),))
    added_today = cursor.fetchall()
    cursor.close()
    return added_today
    


                   
