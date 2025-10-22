import os
import logging

from openai import OpenAI

logger = logging.getLogger('API_AI_REQURSTS')

open_ai_token = os.getenv('open_ai_token') # Requires token as an env variable
if not open_ai_token:
    raise RuntimeError("Missing OPENAI token environment variable")

ai_client = OpenAI(api_key=open_ai_token) 

def create_quiz(
    how_many_questions: int, info_to_test: list, more_instructions=''
    ) -> str:
    """
    Creates a quiz from learned knowledge using open-ai api system
    """
    if len(str(info_to_test)) > 500:
        logger.warning("the create quiz received too much info to proccess.")
        info_to_test = str(info_to_test)[:500]
        
    try:
        response = ai_client.responses.create(
            model="gpt-4.1-nano",
            # for gpt >= 5: add reasoning={"effort": "low"},
            instructions="return only questions(no numbering) and answers like: question:, answer:.",
            input=(f"this is what I learned at japanease class: {info_to_test}. " +
                f"create {how_many_questions} questions to help me practice (translate, fill the word, verb formations) and more." +
                more_instructions
            ),
            max_output_tokens=1000
        )
    except Exception as e:
        logger.error(f"OpenAI request failed: {e}")
        return "Error creating quiz. Please try again later."
    
    logger.debug(f"the create quiz took {response.usage.total_tokens} tokens")
    return(response.output_text)

    
    

