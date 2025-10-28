import logging

from openai import OpenAI

from config import (
    AI_INSTRUCTIONS,
    clean_user_input_for_ai,
    LONGEST_INPUT_OF_DATA_TO_QUIZ,
    MAX_OUTPUT_TOKENS,
    OPENAI_API_KEY,
    OPENAI_MODEL_NAME, 
)
logger = logging.getLogger('AI_responses')

if OPENAI_API_KEY is not None:
    ai_client = OpenAI(api_key=OPENAI_API_KEY)


def create_quiz(
    how_many_questions: int, info_to_test: list, more_instructions=''
    ) -> str:
    """
    Creates a quiz from learned knowledge using open-ai api system.
    """
    if len(str(info_to_test)) > LONGEST_INPUT_OF_DATA_TO_QUIZ:
        logger.debug("the create quiz received too much info to proccess.")
        info_to_test = str(info_to_test)[:LONGEST_INPUT_OF_DATA_TO_QUIZ]
        
    try:
        response = ai_client.responses.create(
            model=OPENAI_MODEL_NAME,
            # for gpt >= 5: add reasoning={"effort": "low"},
            instructions=AI_INSTRUCTIONS,
            input=clean_user_input_for_ai(
                how_many_questions, info_to_test, more_instructions
            ),
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
    except Exception as e:
        logger.error(f"OpenAI request failed: {e}")
        return "Error creating quiz. Please try again later."
    
    logger.debug(f"the create quiz took {response.usage.total_tokens} tokens")
    return(response.output_text)

    
    

