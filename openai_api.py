import openai, os
from openai.error import OpenAIError

def init_api():   
    if not os.getenv('MY_API_KEY'):
        print("Warning: OpenAI API key missing from .env file")
    else:
        openai.api_key = os.getenv('MY_API_KEY')

#-------------------------------------------------------------------
# chat functions 
#-------------------------------------------------------------------


def list_models():
    response = openai.Model.list()
    include_keywords = ['gpt']
    exclude_keywords = ['vision', 'instruct']

    # First filter to include models containing 'gpt' keyword
    included_models = [model for model in response['data'] 
                       if any(keyword in model['id'] for keyword in include_keywords)]

    # Second filter to remove models containing excluded keywords
    filtered_models = [model for model in included_models
                       if not any(keyword in model['id'] for keyword in exclude_keywords)]

    # Extracting IDs and sorting them
    models = [model['id'] for model in filtered_models]
    models.sort()
    return models


def process_openai_message(chat_history, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=chat_history,
            stream=True
        )
        for message in response:
            yield message
    except OpenAIError as e:
        yield {'error': str(e)}


def process_title_message(chat_history, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=chat_history  
        )
        ai_message = {'role': 'assistant', 'content': response['choices'][0]['message']['content']}
        return ai_message
    except OpenAIError as e:
        return {'error': str(e)}
