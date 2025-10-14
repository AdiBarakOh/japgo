import sqlite3
import string
import random

from data_bases import add_grammer_to_db, add_word_to_db, delete_from_db


def create_random_text(lengh: int):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_characters = ''.join([random.choice(characters) for i in range(lengh)])
    return random_characters

def test_adding_word_to_db(word: str) -> bool:
    add_word_to_db(word)
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM word WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_from_db('word', word)
    return added_result is not None

def test_adding_grammer_to_db(word: str) -> bool:
    add_grammer_to_db(word)
    connection = sqlite3.connect('japgo_db')  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM grammer WHERE user_text=?", (word,)) 
    added_result = cursor.fetchone()
    cursor.close()
    delete_from_db('grammer', word)
    return added_result is not None
    




print(test_adding_word_to_db(create_random_text(10)))
print(test_adding_grammer_to_db(create_random_text(10)))