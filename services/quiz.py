import asyncio
import logging
import random
from typing import Optional

import discord

from config import (
    ANSWER_SEPARATION,
    DATA_BASE_PATH,
    GENERAL_REACTION_SECONDS,
    GRAMMER_TABLE_NAME,
    LONG_QUIZ_QUESTIONS,
    LONG_QUIZ_REACTION,
    MAX_DATES_TO_QUIZ,
    MEDIUM_QUIZ_QUESTIONS,
    MEDIUM_QUIZ_REACTION,
    QUESTION_SEPERATION,
    SECONDS_FOR_ANSWER_QUIZ,
    SHORT_QUIZ_QUESTIONS,
    SHORT_QUIZ_REACTION,
    WORDS_TABLE_NAME,
)
from services.ai_responses import create_quiz
from services.database import add_question_to_db, get_all_info_dates, get_info_by_date

logger = logging.getLogger('quiz')


class Quiz:
    QUIZ_START_MESSAGE: str = """Do you want me to create a quiz for you?
            React with 👍 for a short quiz, 😆 for medium, or 🙏 for a long one.
            After each question, every message you send WILL count as your answer.
            Please answer carefully."""   
    NOT_ENOUGH_INPUT: str = (
                    "Not enough data to test, " +
                    "try and add more words and grammer!"
    )
    

    def __init__(self, message: discord.Message, client: discord.Client):
        self.original_message: discord.Message = message
        self.client: discord.Client = client
        self.ai_quiz: list[str] | None = None
    
    def clean_sql_data(self, data: str) -> str:
        return str(data).strip("""('" ,)""")
        
    def calc_how_many_questions(self, reaction: str) -> int:
        question_number: int = 0
        if reaction == SHORT_QUIZ_REACTION:
            question_number = SHORT_QUIZ_QUESTIONS
        elif reaction == MEDIUM_QUIZ_REACTION:
            question_number = MEDIUM_QUIZ_QUESTIONS
        elif reaction == LONG_QUIZ_REACTION:
            question_number = LONG_QUIZ_QUESTIONS
        else:
            logger.debug("Invalid reaction to start quiz question.")
        return question_number
    
    
    def pull_dates_for_quiz(self, db_path: str = DATA_BASE_PATH) -> Optional[list[str]]:
        """
        Returns random dates on which information was learned
        """
        words: list[str | None] = get_all_info_dates(WORDS_TABLE_NAME, db_path)
        grammers: list[str | None] = get_all_info_dates(GRAMMER_TABLE_NAME, db_path)
        all_dates = words + grammers
        if len(all_dates) >= 1:
            dates_to_choose_count: int = min(len(all_dates), MAX_DATES_TO_QUIZ)
            random_dates_unclean: list[str] = random.choices(all_dates, k=dates_to_choose_count)
            random_dates_cleaned: list[str] = [(self.clean_sql_data(str(day))) for day in set(random_dates_unclean)]
            return random_dates_cleaned
        return None
    
    
    def pull_info_for_quiz(self, dates: list[str], db_path: str = DATA_BASE_PATH) -> list[str]:
        info_for_test: list[str | None] = []
        for day in dates:
            for info in get_info_by_date(day, db_path):
                info_for_test.append((self.clean_sql_data(str(info))))
        return info_for_test
    
       
    def check_reaction_to_message(self, reaction: discord.Reaction, user: discord.User) -> bool:
        if user == self.original_message.author and str(reaction.emoji) in [
            SHORT_QUIZ_REACTION, MEDIUM_QUIZ_REACTION, LONG_QUIZ_REACTION
            ]:
            return True
        return False
    
            
    async def reaction_to_quiz_start(self) -> discord.Reaction | None:  
        await self.original_message.channel.send(self.QUIZ_START_MESSAGE)
        try:
            reaction, _ = await self.client.wait_for(
                'reaction_add',
                timeout=GENERAL_REACTION_SECONDS,
                check=self.check_reaction_to_message
            )     
        except asyncio.TimeoutError:
            await self.original_message.channel.send(
                "Nevermind. maybe another time?"
            )
            return None
        return reaction
    
    
    async def configure_quiz(self, question_number: int) -> None:
        dates_to_test: list[str | None] = self.pull_dates_for_quiz()
        knowledge_for_test: list[str] = None
        if dates_to_test:
            knowledge_for_test: list[str] = self.pull_info_for_quiz(dates_to_test)
            self.ai_quiz = create_quiz(question_number, knowledge_for_test)
        else:
            await self.original_message.channel.send(self.NOT_ENOUGH_INPUT)
            
      
    async def quiz_the_user(self):
        for sentence in self.ai_quiz.split("\n"):
            if len(sentence) < 1:
                continue
            
            if sentence.startswith(QUESTION_SEPERATION):
                sentence = sentence.removeprefix(QUESTION_SEPERATION)
                add_question_to_db(sentence)    
                await self.original_message.channel.send(sentence)
                try: 
                    await self.client.wait_for(
                        'message',
                        timeout=SECONDS_FOR_ANSWER_QUIZ,
                        check=(
                        lambda answer: answer.author == self.original_message.author
                        )
                    )
                except asyncio.TimeoutError:
                    return
            else:
                sentence = sentence.removeprefix(ANSWER_SEPARATION) 
                await self.original_message.channel.send("Answer: " + sentence)
        await self.original_message.channel.send('Quiz is over. Hope you enjoyed!')    
            # might add a check and scores to user answers


    async def main_quiz(self) -> None:
        reaction: discord.Reaction | None = await self.reaction_to_quiz_start()
        if reaction is None:
            return
        
        questions_number: int = self.calc_how_many_questions(str(reaction.emoji))
        if questions_number == 0:
            return
        
        await self.configure_quiz(questions_number)
        if self.ai_quiz:
            await self.quiz_the_user()







