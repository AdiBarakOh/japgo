import logging
import sqlite3
import time
from typing import Optional
   

logging.basicConfig(filename='main_log.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('data_base')

def create_db() -> None:
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS word(user_text TEXT, date_added TEXT)") 
    cursor.execute("CREATE TABLE IF NOT EXISTS grammer(user_text TEXT, date_added TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS questions(question TEXT, score INT, date_added TEXT)")
    cursor.close()
   
def add_word_to_db(word: str) -> bool: #word should be in the format of WORD_TABLE_COL
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM word WHERE user_text=?", (word,))
    if cursor.fetchone():
        logger.debug("word already exists in the database.")
        cursor.close()
        return False
    else:
        cursor.execute(
        "INSERT INTO word VALUES (?, ?)",
        (word, time.strftime('%Y-%m-%d'),)
        )
        connection.commit()
        cursor.close()
        logger.debug("word inserted to database.")
    return True
    
def add_grammer_to_db(grammer: str) -> None:
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM grammer WHERE user_text=?", (grammer,))
    if cursor.fetchone():
        logger.debug("grammer already exists in the database.")
    else:
        cursor.execute(
            "INSERT INTO grammer VALUES (?, ?)",
            (grammer, time.strftime('%Y-%m-%d'),)
        )
        connection.commit()
        logger.debug("grammer inserted to database.")
    cursor.close()

def get_all_info_dates(table: str) -> Optional[list]:
    if table in ("word", "grammer"):
        connection = sqlite3.connect('japgo_db')  
        cursor = connection.cursor()
        cursor.execute(f"SELECT date_added FROM {table}")
        all_info = cursor.fetchall()
        cursor.close() 
        return all_info
    logger.error("db get_all_info was used without proper table name.")
    return  
    
def get_info_by_date(date_requested: str) -> list:
    connection = sqlite3.connect('japgo_db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_text FROM grammer WHERE date_added=?", (date_requested,))
    all_grammer = cursor.fetchall()
    cursor.execute("SELECT user_text FROM word WHERE date_added=?", (date_requested,))
    all_words = cursor.fetchall()
    cursor.close()
    return all_grammer + all_words

def add_question_to_db(question_to_add:str) -> None:
    connection = sqlite3.connect('japgo_db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM questions WHERE question=?", (question_to_add,))
    if cursor.fetchone():
        cursor.close()
        return
    cursor.execute("INSERT INTO questions VALUES (?,?,?)", (question_to_add, 0, time.strftime('%Y-%m-%d'),))
    connection.commit()
    cursor.close()
    
    
def delete_user_text_in_word_or_grammer(table: str, user_text: str) -> None:
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    if table in ['word', 'grammer']:
        cursor.execute(f"DELETE FROM {table} WHERE user_text=?", (user_text,))
        connection.commit()
    cursor.close()
    
def delete_question(question: str) -> None:
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    cursor.execute("DELETE FROM questions WHERE question=?", (question,))
    connection.commit()
    cursor.close()
    
def return_added_today(table: str):
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE date_added=?", (time.strftime('%Y-%m-%d'),))
    added_today = cursor.fetchall()
    cursor.close()
    return added_today
    


                   
