from flask import Flask, request, jsonify
from database import insert_message, get_chat_history

app = Flask(__name__)

# Predefined responses (as a fallback)
responses = {
    "hello": "Hi there! How can I assist you today? 😊",
    "how are you": "I'm just a chatbot, but I'm always here to help! 🚀",
    "bye": "Goodbye! Have a great day! 👋",
    "help": "I can assist with general questions. Try asking me something!",
}

# Generate a response based on chat history
def get_bot_response(user_message):
    user_message = user_message.lower()
    chat_history = get_chat_history(5)  # Retrieve last 5 messages

    # Convert chat history into a simple text log
    chat_log = " ".join([msg[1] for msg in chat_history])  # msg[1] = message text

    # Check chat history for context
    if "weather" in user_message and "rain" in chat_log:
        return "It looks like we talked about rain earlier. Do you need an umbrella? ☂️"
    if "thank you" in user_message:
        return "You're very welcome! 😊"

    # Default to predefined responses
    for keyword in responses:
        if keyword in user_message:
            return responses[keyword]

    # Fallback response if no context is found
    return "I'm not sure how to respond to that yet, but I'm learning! 🤖"

# Route to handle user messages
@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user = data.get("user", "User")
    message = data.get("message", "")

    if message:
        bot_response = get_bot_response(message)
        insert_message(user, message)  # Store user message
        insert_message("CelestiChat", bot_response)  # Store bot response

        return jsonify({"user": message, "bot": bot_response})
    
    return jsonify({"error": "Message cannot be empty!"})

# Route to fetch chat history
@app.route('/history', methods=['GET'])
def chat_history():
    messages = get_chat_history()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
