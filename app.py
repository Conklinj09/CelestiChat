from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = "whimsy_magic_123"  # Session security key

# Predefined responses
responses = {
    "hello": "🌸 Hi lovely! How’s your day going? ✨",
    "how are you": "I'm floating in a dreamy world of pastel skies! ☁️ How about you?",
    "bye": "Goodbye, beautiful soul! 🌙 Sweet dreams!",
    "love": "Love is like fairy dust—spread it everywhere! 💖",
    "magic": "✨ Poof! A sprinkle of magic just for you! ✨",
    "stars": "The stars are always watching over you. 🌠 Keep shining!",
    "help": "I'm here to bring joy! 🌸 Try asking about 'magic', 'stars', or 'love'."
}

def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return responses[key]
    return "Oops! I fluttered away for a second. Try something else! 🌷"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Store conversation in session
    if "history" not in session:
        session["history"] = []
    
    bot_response = get_response(user_message)
    session["history"].append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
