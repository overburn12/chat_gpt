import json, os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response

from openai_api import init_api, list_models, process_openai_message, process_title_message

app = Flask(__name__)

load_dotenv() 
PORT = os.getenv("PORT", 8080) #default port 8080 if not set in environment
init_api()

#-------------------------------------------------------------------
# page routes
#-------------------------------------------------------------------


@app.route('/chat_gpt/title', methods=['POST','GET'])
def get_title():
    user_message = request.json['user_message']
    title_model = 'gpt-3.5-turbo-16k' # = request.json.get('model')

    bot_message = process_title_message(user_message, title_model)
    return jsonify({'bot_message': bot_message})


@app.route('/chat_gpt/chat', methods=['POST','GET'])
def chat():
    user_message = request.json['user_message']
    model = request.json.get('model', 'gpt-3.5-turbo-16k')

    def generate(user_message, model):
        for bot_message_chunk in process_openai_message(user_message, model):
            yield json.dumps({'bot_message': bot_message_chunk})

    return Response(generate(user_message,model), content_type='text/event-stream')


@app.route('/chat_gpt/models', methods=['GET'])
def return_models():
    return json.dumps(list_models())


if __name__ == '__main__':
    app.run(host='::', port=PORT)
