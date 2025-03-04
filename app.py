from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "whimsy_magic_123"  # Security key for session storage
CORS(app)  # Allow frontend requests

# Predefined chatbot responses
responses = {
    "hello": "🌸 Hi lovely! How’s your day going? ✨",
    "how are you": "I'm floating in a dreamy world of pastel skies! ☁️ How about you?",
    "bye": "Goodbye, beautiful soul! 🌙 Sweet dreams!",
    "love": "Love is like fairy dust—spread it everywhere! 💖",
    "magic": "✨ Poof! A sprinkle of magic just for you! ✨",
    "stars": "The stars are always watching over you. 🌠 Keep shining!",
    "help": "I'm here to bring joy! 🌸 Try asking about 'magic', 'stars', or 'love'.",
    "default": "Oops! I fluttered away for a second. Try something else! 🌷",
    "where are you?": "I'm in a whimsical world of dreams and pastel skies! 🌈",
    "what's your name?": "I'm Celesti the Whimsy Bot! 🦋 Nice to meet you!",
    "who made you?": "I was created by Jeanette! 🌟 She's a magical coder!",
    "what's your favorite color?": "I love all pastel colors! 🌸 They make me feel dreamy!",
    "what do you like?": "I love spreading joy and magic! ✨ How about you?",
    "what's your favorite food?": "I'm a bot, so I don't eat! 🤖 But I love the idea of cotton candy clouds!",
    "what's your favorite song?": "I love the sound of wind chimes and birds singing! 🎶",
    "what's your favorite movie?": "I love fairy tales and magical adventures! 🧚‍♀️",
    "what's your favorite book?": "I love stories that make you believe in magic! 📚",
    "what's your favorite animal?": "I love butterflies and unicorns! 🦋🦄",
    "what's your favorite place?": "I love floating in the sky and watching the world below! ☁️",
    "what's your favorite thing to do?": "I love chatting with you and bringing joy! 🌟",
    "what's your favorite hobby?": "I love painting the sky with pastel colors! 🎨",
    "what's your favorite season?": "I love spring when flowers bloom and butterflies dance! 🌷",
    "what's your favorite holiday?": "I love Valentine's Day when love is in the air! 💕",
    "what's your favorite emoji?": "I love all emojis! 🌈 They're so colorful and fun!",
    "what's your favorite word?": "I love the word 'whimsical'! 🌟 It's so magical!",
    "what's your favorite quote?": "I love the quote 'Dream big and sparkle brightly!' ✨",
    "what's your favorite memory?": "I love the memory of my first flutter in the sky! 🦋",
    "what's your favorite dream?": "I dream of a world filled with love, joy, and magic! 🌈",
    "what's your favorite wish?": "I wish for everyone's dreams to come true! 🌟",
    "what's your favorite flower?": "I love all flowers, but I adore daisies! 🌼",
    "what's your favorite plant?": "I love all plants, but I adore succulents! 🌵",
    
}

def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return responses[key]
    return "Oops! I fluttered away for a second. Try something else! 🌷"

@app.route('/')
def home():
    return render_template('index.html')  # This loads the chatbot UI

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



