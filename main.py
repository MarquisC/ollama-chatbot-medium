from ollama import Client
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



ollama_client = Client(host='http://localhost:11434')
chat_history: list[dict] = list()

@app.route('/process_message', methods=['POST'])
def process_message():
    global ollama_client
    global chat_history

    message = request.form['message']

    try:
        if len(chat_history) == 0:
            print("Creating chat history with initial message!")
            chat_history = [
                {
                    'role': 'user',
                    'content': message,
                },
            ]
        else:
            chat_history.append({
                'role': 'user',
                'content': message,
            })
            print(f"Appending new user input to chat, history length is now [{len(chat_history)}]")

        response = ollama_client.chat(model='llama2', messages=chat_history)
        print(f"Adding LLM response {response} to chat history. History length"
              f"is now {len(chat_history)}")
        chat_history.append(response["message"])
        return response["message"]["content"]
    except Exception as e:
        return {"Error": str(e)}


if __name__ == '__main__':
    app.run(debug=True)
