import asyncio
import discord
import logging
import random
from typing import Optional

from services.ai_responses import create_quiz
from data.database import add_question_to_db, get_info_by_date, get_all_info_dates

logger = logging.getLogger('quizes')


class Quiz:
    QUIZ_START_MESSAGE = """Do you want me to create a quiz for you?
            React with 👍 for a short quiz, 😆 for medium, or 🙏 for a long one.
            After each question, every message you send WILL count as your answer and will be scored.
            No backsies!
            Please answer carefully."""   
    NOT_ENOUGH_INPUT = (
                    "Not enough data to test, " +
                    "try and add more words and grammer!"
    )
    SHORT_QUIZ_QUESTIONS = 1
    MEDIUM_QUIZ_QUESTIONS = 2
    LONG_QUIZ_QUESTIONS = 3
    SHORT_QUIZ_REACTION, MEDIUM_QUIZ_REACTION, LONG_QUIZ_REACTION = "👍", "😆", "🙏"


    def __init__(self, message: discord.Message, client: discord.Client):
        self.original_message = message
        self.client = client
        self.ai_quiz = None
    
        
    def calc_how_many_questions(self, reaction: str) -> int:
        if reaction == self.SHORT_QUIZ_REACTION:
            question_number = self.SHORT_QUIZ_REACTION
        elif reaction == self.MEDIUM_QUIZ_REACTION:
            question_number = self.MEDIUM_QUIZ_REACTION
        elif reaction == self.LONG_QUIZ_REACTION:
            question_number = self.LONG_QUIZ_REACTION
        else:
            question_number = 0
            logger.debug("invalid reaction to start quiz question")
        return question_number
    
    
    def pull_dates_for_quiz(self) -> Optional[list[str]]:
        """
        Returns random dates that information was learned at
        """
        words = get_all_info_dates('word')
        grammers = get_all_info_dates('grammer')
        all_dates = words + grammers
        if len(all_dates) >= 1:
            dates_to_choose_count = min(len(all_dates), 3)
            random_dates_unclean = random.choices(all_dates, k=dates_to_choose_count)
            random_dates_cleaned = [(str(day)).strip("""('" ,)""") for day in set(random_dates_unclean)]
            return random_dates_cleaned
        return None
    
    
    def pull_info_for_quiz(self, dates: list[str]) -> list[str]:
        info_for_test = []
        for day in dates:
            for info in get_info_by_date(day):
                info_for_test.append(str(info).strip("""('" ,)"""))
        return info_for_test
    
       
    def check_reaction_to_message(self, reaction: discord.Reaction, user: discord.User) -> bool:
        if user == self.original_message.author and str(reaction.emoji) in (
            self.SHORT_QUIZ_REACTION + self.MEDIUM_QUIZ_REACTION + self.LONG_QUIZ_REACTION
            ):
            return True
        return False
    
            
    async def reaction_to_quiz_start(self) -> Optional[discord.Reaction]:  
        await self.original_message.channel.send(self.QUIZ_START_MESSAGE)
        try:
            reaction, _ = await self.client.wait_for('reaction_add', timeout=100, check=self.check_reaction_to_message)     
        except asyncio.TimeoutError:
            await self.original_message.channel.send("Nevermind. maybe another time?")
            return None
        return reaction
    
    
    async def configure_quiz(self, question_number: int) -> None:
        dates_to_test = self.pull_dates_for_quiz()
        knowledge_for_test = None
        if dates_to_test:
            knowledge_for_test = self.pull_info_for_quiz(dates_to_test)
        if knowledge_for_test is not None:
            self.ai_quiz = create_quiz(question_number, knowledge_for_test)
        else:
            await self.original_message.channel.send(self.NOT_ENOUGH_INPUT)
            
      
    async def quiz_the_user(self):
        for question in self.ai_quiz.split("\n"):
            if len(question) < 1:
                return
            if question.startswith('answer:'):
                await self.original_message.channel.send(question)
            else:   
                add_question_to_db(question)    
                await self.original_message.channel.send(question)
                try: 
                    await self.client.wait_for('message',timeout=600, check=(
                        lambda answer: answer.author == self.original_message.author
                    ))
                except asyncio.TimeoutError:
                    return
        self.original_message.channel.send('Quiz is over. Hope you enjoyed!')    
            # might add a check and scores to user answers


    async def main_quiz(self) -> None:
        reaction = await self.reaction_to_quiz_start()
        if reaction is None:
            return
        
        questions_number = self.calc_how_many_questions(str(reaction.emoji))
        if questions_number == 0:
            return
        
        await self.configure_quiz(questions_number)
        if self.ai_quiz:
            await self.quiz_the_user()
            
        
        
        
                
            
        
    