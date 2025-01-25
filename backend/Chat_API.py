from flask import Flask, render_template_string
from openai import OpenAI

app = Flask(__name__)

@app.route('/')
def chat_output():
    client = OpenAI(api_key="sk-148cbd347b074031b384462738683ee8", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a physics expert"},
            {"role": "system", "content": "Try to fact check your work"},
            {"role": "system", "content": "Keep it clean and concise, good formatting"},
            {"role": "user", "content": "Hello"},
            {"role": "user", "content": "Can you solve this physics problem (F=6 * 8) what is the force?"}
        ],
        stream=False
    )

    # Loop through the choices and clean up the messages
    messages = [choice.message.content for choice in response.choices]

    # Clean up multiplication symbol (replace "*" with "×") and remove slashes
    cleaned_messages = []
    for message in messages:
        # Replace "*" with multiplication sign "×" (only once)
        message = message.replace("*", "×")
        message = message.replace("###", "\n\t")
        # Remove any slashes that appear before LaTeX formatting
        message = message.replace("\\", "")  # Remove backslashes from LaTeX formatting
        message = message.replace("times", "x")

        cleaned_messages.append(message)

    # Render the output as an HTML string
    html_content = "<h1>Chat Output</h1><ul>"
    for message in cleaned_messages:
        html_content += f"<li>{message}</li>"
    html_content += "</ul>"

    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
