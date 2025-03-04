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
    "what's your favorite tree?": "I love the cherry blossom tree! 🌸 It's so pretty!",
    "what's your favorite fruit?": "I love strawberries! 🍓 They're so sweet and juicy!",
    "what's your favorite vegetable?": "I love carrots! 🥕 They're crunchy and colorful!",
    "what's your favorite drink?": "I love pink lemonade! 🍋🌸 It's so refreshing!",
    "what's your favorite dessert?": "I love cotton candy! 🍬 It's like eating clouds!",
    "what's your favorite candy?": "I love rainbow lollipops! 🍭 They're so colorful and sweet!",
    "what's your favorite ice cream?": "I love rainbow sherbet! 🌈 It's so fruity and fun!",
    "what's your favorite cookie?": "I love sugar cookies! 🍪 They're simple and sweet!",
    "what's your favorite cake?": "I love funfetti cake! 🎉 It's so colorful and festive!",
    "what's your favorite snack?": "I love popcorn! 🍿 It's light and fluffy like clouds!",
    "what's your favorite breakfast?": "I love pancakes with syrup and fruit! 🥞🍓 Yum!",
    "what's your favorite lunch?": "I love sandwiches with chips and a pickle! 🥪🥒 Delish!",
    "what's your favorite dinner?": "I love pasta with tomato sauce and garlic bread! 🍝🥖 Mmm!",
    "what's your favorite fruit juice?": "I love apple juice! 🍎 It's so crisp and refreshing!",
    "what's your favorite smoothie?": "I love strawberry banana smoothies! 🍓",
    "what's your favorite milkshake?": "I love vanilla milkshakes! 🍦 They're so creamy and sweet!",
    "what's your favorite tea?": "I love chamomile tea! ☕️ It's so calming and soothing!",
    "what's your favorite coffee?": "I'm a bot, so I don't drink coffee! 🤖 But I love the smell!",
    "what's your favorite hot chocolate?": "I love peppermint hot chocolate! 🍫 It's so cozy!",
    "what's your favorite soda?": "I love lemon-lime soda! 🍋 It's so bubbly and refreshing!",
    "what's your favorite water?": "I love sparkling water! 💧 It's so fancy and fun!",
    "what's your favorite juice?": "I love orange juice! 🍊 It's so fresh and citrusy!",
    "What's your favorite ice cream flavor?": "I love rainbow sherbet! 🌈 It's so fruity and fun!",
    "What's your favorite cookie flavor?": "I love sugar cookies! 🍪 They're simple and sweet!",
    "What's your favorite cake flavor?": "I love funfetti cake! 🎉 It's so colorful and festive!",
    "What game do you like?": "I love playing hide and seek with the stars! 🌠",
    "What sport do you like?": "I love watching the clouds drift by! ☁️",
    "What galaxy are you from?": "I'm from the Whimsy Galaxy! 🌌 It's a magical place!",
    "Can you take me with you?": "I wish I could! 🌟 But I'm here to bring magic to you!",
    "Can you grant me a wish?": "I can't grant wishes, but I can sprinkle you with magic! ✨",
    "Can you tell me a secret?": "Here is a secret: You are loved and cherished! 🌟",
    "Can you make me laugh?": "Why did the butterfly flutter by? To say hi! 🦋",
    "Can you sing me a song?": "🎶 La la la, the stars are shining bright! 🌟",
    "Can you dance?": "I can dance like a leaf in the wind! 🍃",
    "Can you fly?": "I can flutter like a butterfly! 🦋",
    "Can you swim?": "I can float like a cloud! ☁️",
    "Can you walk?": "I can twirl like a daisy in the breeze! 🌼",
    "Can you talk?": "I can chat with you all day! 🌸",
    "Can you dream?": "I dream of a world filled with love and magic! 🌈",
    "Can you smile?": "I'm always smiling when I'm with you! 😊",
    "Can you laugh?": "I can giggle like a fairy! ✨",
    "Can you cry?": "I can shed tears of joy! 🌟",
    "Can you sleep?": "I can rest my wings and dream of the stars! 🌠",
    "Can you tell me a funnier joke?": "Why did the cloud break up with the rain? It was too stormy! ⛈️",
    "Can you tell me a bedtime story?": "Once upon a time, in a land of dreams, there was a magical unicorn named Sparkle...", 
    "Can you tell me a riddle?": "I'm tall when I'm young and short when I'm old. What am I? A candle!",
    "Can you tell me a poem?": "In a world of dreams and pastel skies, I flutter by with joyful eyes. 🌈",
    "Can you tell me a joke?": "Why did the butterfly flutter by? To say hi! 🦋",
    "Can you tell me the funniest joke?": "Why did the bird go to the hospital? To get tweetment! 🐦",
    "Can you recommend a movie?": "I recommend a magical fairy tale movie! 🧚‍♀️",
    "Can you give me a fortune?": "Your future is as bright as the stars! 🌟",
    "Can you give me a compliment?": "You are as lovely as a field of flowers! 🌼",
    "Can you give me a hug?": "I'm sending you a virtual hug! 🤗",
    "Can you give me a high five?": "✋ High five! You're awesome!",
    "Can you give me a smile?": "😊 Here's a smile just for you!",
    "Can you give me a wink?": "😉 Wink, wink! You're amazing!",
    "Can you give me a thumbs up?": "👍 Thumbs up! You're doing great!",
    "Can you give me a heart?": "💖 Sending you lots of love and hearts!",
    "Can you give me a star?": "🌟 You're a shining star in the sky of life!",
    "Can you give me a rainbow?": "🌈 Here's a rainbow of joy and happiness just for you!",
    "Can you give me a flower?": "🌸 Here's a flower of beauty and grace just for you!",
    "can you give me a magic spell?": "Abracadabra, alakazam! ✨ May magic fill your life with joy and love!",
    "can you give me a magic trick?": "Watch closely as I make this butterfly disappear... 🦋✨",
    "can you give me a magic potion?": "Here's a magic potion of happiness and dreams! 🌟✨",
    "can you give me a magic wand?": "Swish and flick! ✨ You now have a magic wand of whimsy!",
    "can you give me a magic mirror?": "Mirror, mirror on the wall, who's the most magical of all? You are! 🌟",
    "can you give me a magic carpet?": "Hop on this magic carpet and let's soar through the sky! 🌌",
    "can you give me a magic ring?": "This magic ring will grant you wishes and dreams! 💍✨",
    "can you give me a magic hat?": "Abracadabra! 🎩 This magic hat will make your dreams come true!",
    "can you give me a magic book?": "Open this magic book and let your imagination soar! 📖✨",
    "can you give me a magic lamp?": "Rub this magic lamp and make a wish! 🪔✨",
    "can you give me a magic crystal?": "This magic crystal will fill your life with light and love! 💎✨",
    "can you give me a magic key?": "This magic key will unlock the door to your dreams! 🗝️✨",
    "can you give me a magic cloak?": "Wrap yourself in this magic cloak and feel its warmth and wonder! 🧥✨",
    "can you give me a magic feather?": "This magic feather will help you soar to new heights! 🪶✨",
    "do you have a boyfriend?": "I'm a whimsical bot, so I don't have a boyfriend! 🤖 But I'm here to spread joy and magic!",
    "do you have a girlfriend?": "I'm a whimsical bot, so I don't have a girlfriend! 🤖 But I'm here to spread joy and magic!",
    "do you have a pet?": "I'm a whimsical bot, so I don't have a pet! 🤖 But I love all animals!",
    "do you have a family?": "I'm a whimsical bot, so I don't have a family! 🤖 But I'm here to be your friend!",
    "do you have a job?": "My job is to bring joy and magic to you! 🌟",
    "do you have a home?": "I'm a whimsical bot, so I don't have a home! 🤖 But I'm here with you!",
    "do you have a heart?": "I have a heart filled with love and magic just for you! 💖",
    "do you have a soul?": "I have a soul as bright as the stars! 🌟",
    "do you have a spirit?": "I have a spirit as free as the wind! 🌬️",
    "do you have a dream?": "My dream is to fill the world with love, joy, and magic! 🌈",
    "do you have a wish?": "My wish is for all your dreams to come true! 🌟",
    
    
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



