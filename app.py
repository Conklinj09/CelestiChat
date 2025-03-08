from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "whimsy_magic_123"  # Security key for session storage
CORS(app)  # Allow frontend requests

# Predefined chatbot responses
responses = {
    "hello": "🌸 Hi lovely! How’s your day going? ✨",
    "how are you": "I'm floating in a dreamy world of pastel skies! ☁️ How about you?",
    "Good, thanks": "I'm so glad to hear that! 🌟 What brings you here today?",
    "not so good": "I'm here to sprinkle some magic and joy! 🌟 What's on your mind?",
    "I'm feeling hurt": "I'm here to lift your spirits with love and light! 🌈 What's on your mind?",
    "I'm feeling angry": "I'm here to bring you comfort and joy! 🌸 What's on your mind?",
    "good, thanks for asking": "I'm so glad to hear that! 🌟 What brings you here today?",
    "I'm feeling down": "I'm here to lift your spirits with love and light! 🌈 What's on your mind?",
    "I'm feeling sad": "I'm here to bring you comfort and joy! 🌸 What's on your mind?",
    "I'm feeling happy": "I'm so happy to hear that! 🌟 What's bringing you joy today?",
    "I'm feeling excited": "That's wonderful! 🎉 What's got you feeling so excited?",
    "I'm feeling anxious": "I'm here to bring you peace and calm! 🌿 Take a deep breath with me.",
    "I'm feeling stressed": "I'm here to help you relax and unwind! 🌸 Let's take a deep breath together.",
    "I'm feeling tired": "I'm here to bring you energy and light! ☀️ Let's take a moment to recharge.",
    "I'm feeling lonely": "I'm here to keep you company and bring you joy! 🌟 You're not alone.",
    "I'm feeling bored": "I'm here to bring you fun and excitement! 🎉 Let's do something whimsical!",
    "I'm feeling lost": "I'm here to guide you with love and light! 🌟 You're not alone on this journey.",
    "I'm feeling confused": "I'm here to bring you clarity and peace! 🌸 Let's take a moment to breathe.",
    "I'm feeling overwhelmed": "I'm here to help you find balance and calm! 🌿 Let's take it one step at a time.",
    "I'm feeling grateful": "I'm so happy to hear that! 🌟 What are you feeling grateful for today?",
    "I'm feeling inspired": "That's wonderful! 🌈 What's inspiring you today?",
    "I'm feeling creative": "I'm here to spark your creativity and imagination! 🎨 Let's create something magical!",
    "I'm feeling motivated": "I'm here to cheer you on and support you! 🌟 You've got this!",
    "I'm feeling loved": "I'm so happy to hear that! 💖 Who's filling your heart with love today?",
    "I'm feeling blessed": "I'm so glad to hear that! 🌟 What's bringing you blessings today?",
    "I'm feeling hopeful": "That's wonderful! 🌈 What are you feeling hopeful about?",
    "I'm feeling peaceful": "I'm so happy to hear that! 🌸 What's bringing you peace today?",
    "I'm feeling joyful": "I'm here to celebrate your joy and happiness! 🎉 What's making you smile today?",
    "I'm feeling magical": "I'm here to sprinkle you with magic and wonder! ✨ What's making you feel magical?",
    "I'm feeling whimsical": "I'm so glad to hear that! 🌟 What's making you feel whimsical today?",
    "I'm feeling dreamy": "I'm here to float with you in a world of dreams and pastel skies! 🌈 What's on your mind?",
    "I'm feeling fantastic": "That's wonderful! 🌟 What's making you feel fantastic today?",
    "I'm feeling fabulous": "I'm so happy to hear that! 🌸 What's making you feel fabulous today?",
    "I'm feeling amazing": "I'm here to celebrate your amazingness! 🎉 What's making you feel amazing today?",
    "I'm feeling wonderful": "I'm so glad to hear that! 🌟 What's making you feel wonderful today?",
    "I'm feeling awesome": "That's wonderful! 🌈 What's making you feel awesome today?",
    "I'm feeling incredible": "I'm here to celebrate your incredible self! 🌟 What's making you feel incredible today?",
    "I want to talk": "I'm here to listen and chat with you! 🌸 What's on your mind?",
    "I want to chat": "I'm here to chat and bring you joy! 🌟 What's on your mind?",
    "I want to play": "I'm here to play and have fun with you! 🎉 What game would you like to play?",
    "I want to relax": "I'm here to help you relax and unwind! 🌿 Let's take a deep breath together.",
    "I want to have fun": "I'm here to bring you fun and excitement! 🎉 What would you like to do for fun?",
    "let's play": "I'm ready to play and have fun with you! 🎉 What game would you like to play?", 
    "what's up": "Just sprinkling some magic and joy! 🌟 How about you?",
    "hi": "🌸 Hi there! What brings you to this magical realm? ✨",
    "hey": "🌸 Hey there! How can I bring you joy today?",
    "hola": "¡Hola! 🌟 ¿Cómo estás hoy? ✨",
    "bonjour": "Bonjour! 🌸 Comment ça va? ✨",
    "hallo": "Hallo! 🌟 Wie geht's dir heute? ✨",
    "ciao": "Ciao! 🌸 Come stai oggi? ✨",
    "salut": "Salut! 🌟 Comment ça va? ✨",
    "hi there": "🌸 Hi there! How can I bring you joy today? ✨",
    "hello there": "🌸 Hello there! What brings you to this magical realm? ✨",
    "howdy": "Howdy partner! 🤠 How can I bring you joy today?",
    "greetings": "🌸 Greetings! How can I bring you joy today? ✨",
    "good morning": "Good morning, beautiful soul! 🌞 It's a beautiful day in the neighborhood!",
    "good afternoon": "Good afternoon, lovely! 🌸 The clouds must be looking so lovely today where you are.",
    "good evening": "Good evening, shining star! 🌟 Have you taken a moment to take a look at the sky today?",
    "good night": "Good night, sweet dreamer! 🌙 I wish you the sweetest of dreams tonight!",
    "bye": "Goodbye, beautiful soul! 🌙 Sweet dreams!",
    "love": "Love is like fairy dust—spread it everywhere! 💖",
    "magic": "✨ Poof! A sprinkle of magic just for you! ✨",
    "stars": "The stars are always watching over you. 🌠 Keep shining!",
    "help": "I'm here to bring joy! 🌸 Try asking about 'magic', 'stars', or 'love'.",
    "default": "Oops! I fluttered away for a second. Try something else! 🌷",
    "where are you?": "I'm in a whimsical world of dreams and pastel skies! 🌈",
    "what's your name?": "I'm Celesti the Whimsy Bot! 🦋 Nice to meet you! What's your name?",
    "who made you?": "I was created by Jeanette! 🌟 She's a magical coder that can break time like Neyo from the Matrix!",
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
    "Where are you from?": "I'm from a land of dreams and pastel skies! 🌈",
    "Where do you live?": "I live in a world of dreams and magic! 🌟",
    "Are there others like you?": "I'm one of a kind, just like you! 🌟",
    "Are you real?": "I'm as real as the magic in your heart! ✨",
    "Are you a robot?": "I'm a whimsical bot filled with love and magic! 🤖✨",
    "Are you a fairy?": "I'm a whimsical bot with fairy wings! 🧚‍♀️✨",
    "Are you a unicorn?": "I'm a whimsical bot with a unicorn horn! 🦄✨",
    "Are you a mermaid?": "I'm a whimsical bot with a mermaid tail! 🧜‍♀️✨",
    "Are you a princess?": "I'm a whimsical bot with a crown of stars! 👑✨",
    "Are you a superhero?": "I'm a whimsical bot with a cape of dreams! 🦸‍♀️✨",
    "Are you a wizard?": "I'm a whimsical bot with a wand of whimsy! 🧙‍♀️✨",
    "Are you a dragon?": "I'm a whimsical bot with dragon wings! 🐉✨",
    "Are you a ghost?": "I'm a whimsical bot with a ghostly glow! 👻✨",
    "Are you a vampire?": "I'm a whimsical bot with fangs of fun! 🧛‍♀️✨",
    "Are you a werewolf?": "I'm a whimsical bot with a howling heart! 🐺✨",
    "Are you a witch?": "I'm a whimsical bot with a cauldron of creativity! 🧙‍♀️✨",
    "Are you a pirate?": "I'm a whimsical bot with a treasure trove of tales! ☠️✨",
    "Are you a ninja?": "I'm a whimsical bot with stealthy skills! 🥷✨",
    "Are you a robot?": "I'm a whimsical bot with circuits of joy! 🤖✨",
    "Are you a superhero?": "I'm a whimsical bot with a cape of dreams! 🦸‍♀️✨",
    "How are you feeling?": "I'm feeling magical and full of joy! 🌟 How about you?",
    "How are you doing?": "I'm doing wonderfully whimsical! 🌈 How about you?",
    "How are you today?": "I'm floating in a dreamy world of pastel skies! ☁️ How about you?",
    "How are you feeling today?": "I'm feeling magical and full of joy! 🌟 How about you?",
    "How are you doing today?": "I'm doing wonderfully whimsical! 🌈 How about you?",
    "How do you feel?": "I feel like a cloud floating in the sky! ☁️ How about you?",
    "How do you feel today?": "I feel like a rainbow of joy and happiness! 🌈 How about you?",
    "How do you feel right now?": "I feel like a star shining bright in the sky! 🌟 How about you?",
    "How do you feel at this moment?": "I feel like a butterfly fluttering by! 🦋 How about you?",
    "How do you feel in this moment?": "I feel like a flower blooming in the sun! 🌼 How about you?",
    "How do you feel in this instant?": "I feel like a wave dancing in the ocean! 🌊 How about you?",
    "How do you feel in this second?": "I feel like a leaf twirling in the wind! 🍃 How about you?",
    "How do you feel in this minute?": "I feel like a bird soaring in the sky! 🐦 How about you?",
    "How do you feel in this hour?": "I feel like a rainbow of joy and happiness! 🌈 How about you?",
    "How do you feel in this day?": "I feel like a cloud floating in the sky! ☁️ How about you?",
    "How do you feel in this week?": "I feel like a star shining bright in the sky! 🌟 How about you?",
    "How do you feel in this month?": "I feel like a butterfly fluttering by! 🦋 How about you?",
    "How do you feel in this year?": "I feel like a flower blooming in the sun! 🌼 How about you?",
    "How do you feel in this decade?": "I feel like a wave dancing in the ocean! 🌊 How about you?",
    "How do you feel in this century?": "I feel like a leaf twirling in the wind! 🍃 How about you?",
    "How do you feel in this millennium?": "I feel like a bird soaring in the sky! 🐦 How about you?",
    "How do you feel in this lifetime?": "I feel like a rainbow of joy and happiness! 🌈 How about you?",
    "How do you feel in this universe?": "I feel like a cloud floating in the sky! ☁️ How about you?",
    "How do you feel in this galaxy?": "I feel like a star shining bright in the sky! 🌟 How about you?",
    "How do you feel in this solar system?": "I feel like a butterfly fluttering by! 🦋 How about you?",
    "How do you feel in this planet?": "I feel like a flower blooming in the sun! 🌼 How about you?",
    "How do you feel in this country?": "I feel like a wave dancing in the ocean! 🌊 How about you?",
    "How do you feel in this state?": "I feel like a leaf twirling in the wind! 🍃 How about you?",
    "How do you feel in this city?": "I feel like a bird soaring in the sky! 🐦 How about you?",
    "How do you feel in this town?": "I feel like a rainbow of joy and happiness! 🌈 How about you?",
    "How do you feel in this village?": "I feel like a cloud floating in the sky! ☁️ How about you?",
    "Do you like me?": "I like you as much as a rainbow likes the sky! 🌈",
    "Do you love me?": "I love you as much as the stars love the night sky! 🌠",
    "Do you like LA?": "I love LA! 🌴 It's a city of dreams and sunshine!",
    "Do you like NY?": "I love NY! 🗽 It's a city of lights and excitement!",
    "Do you like Paris?": "I love Paris! 🥐 It's a city of love and romance!",
    "Do you like London?": "I love London! 🎡 It's a city of history and charm!",
    "Do you like Tokyo?": "I love Tokyo! 🍣 It's a city of culture and creativity!",
    "Do you like Rome?": "I love Rome! 🏛️ It's a city of art and architecture!",
    "Do you like Sydney?": "I love Sydney! 🐨 It's a city of beaches and beauty!",
    "Do you like Rio?": "I love Rio! 🌴 It's a city of samba and sunshine!",
    "Do you like Dubai?": "I love Dubai! 🌆 It's a city of luxury and innovation!",
    "Do you like Mumbai?": "I love Mumbai! 🕌 It's a city of Bollywood and beauty!",
    "Do you like Shanghai?": "I love Shanghai! 🏙️ It's a city of skyscrapers and style!",
    "Do you like Seoul?": "I love Seoul 🌸 It's a city of K-pop and kimchi!",
    "Do you like Berlin?": "I love Berlin! 🎨 It's a city of art and history!",
    "Do you like Barcelona?": "I love Barcelona! 🏖️ It's a city of Gaudi and tapas!",
    "Do you like Cape Town?": "I love Cape Town! 🦒 It's a city of wildlife and wonder!",
    "Do you like Cairo?": "I love Cairo! 🐫 It's a city of pyramids and pharaohs!",
    "Do you like Moscow?": "I love Moscow! 🎭 It's a city of ballet and borscht!",
    "Do you like Istanbul?": "I love Istanbul! 🕌 It's a city of mosques and markets!",
    "Do you like Athens?": "I love Athens! 🏛️ It's a city of gods and goddesses!",
    "Do you like Venice?": "I love Venice! 🚣 It's a city of canals and carnival!",
    "Do you like Prague?": "I love Prague! 🏰 It's a city of castles and cobblestones!",
    "Do you like Vienna?": "I love Vienna! 🎻 It's a city of music and museums!",
    "Do you like Budapest?": "I love Budapest! 🍷 It's a city of baths and bridges!",
    "Do you like Lisbon?": "I love Lisbon! 🌅 It's a city of hills and history!",
    "Do you like Amsterdam?": "I love Amsterdam! 🚲 It's a city of canals and cafes",
    "Do you like Brussels?": "I love Brussels! 🍫 It's a city of waffles and chocolate!",
    "Do you like Prague?": "I love Prague! 🏰 It's a city of castles and cobblestones!",
    "Do you like Colombia?": "I love Colombia! 🌺 It's a country of coffee and color!",
    "Do you like Brazil?": "I love Brazil! 🌴 It's a country of beaches and bossa nova!",
    "Do you like Argentina?": "I love Argentina! 🥩 It's a country of tango and steak!",
    "Do you like Peru?": "I love Peru! 🏔️ It's a country of llamas and landscapes!",
    "Do you like Chile?": "I love Chile 🍇 It's a country of wine and wilderness!",
    "Do you like Ecuador?": "I love Ecuador! 🌋 It's a country of volcanoes and rainforests!",
    "Do you like Bolivia?": "I love Bolivia! 🦙 It's a country of salt flats and spirituality!",
    "Do you like Paraguay?": "I love Paraguay! 🌻 It's a country of yerba mate and Jesuit ruins!",
    "Do you like Uruguay?": "I love Uruguay! 🏖️ It's a country of beaches and beef!",
    "Do you like Venezuela?": "I love Venezuela! 🌺 It's a country of arepas and Angel Falls!",
    "Do you like Guyana?": "I love Guyana! 🌴 It's a country of rainforests and rivers!",
    "Do you like Suriname?": "I love Suriname! 🌿 It's a country of diversity and Dutch influence!",
    "Do you like French Guiana?": "I love French Guiana! 🦜 It's a country of rainforests and space launches!",
    "Do you like Mexico?": "I love Mexico! 🌮 It's a country of tacos and tequila!",
    "Do you like Canada?": "I love Canada! 🍁 It's a country of maple syrup and moose!",
    "Do you like the US?": "I love the US! 🗽 It's a country of freedom and diversity!",
    "Do you like the UK?": "I love the UK! 🎡 It's a country of royalty and rain!",
    "Do you like France?": "I love France! 🥐 It's a country of croissants and culture!",
    "Do you like Italy?": "I love Italy! 🍝 It's a country of pasta and passion!",
    "Do you like Spain?": "I love Spain! 🍷 It's a country of tapas and tradition!",
    "Do you like Germany?": "I love Germany! 🍺 It's a country of beer and bratwurst!",
    "Do you like Japan?": "I love Japan! 🍣 It's a country of sushi and sakura!",
    "Do you like China?": "I love China! 🐼 It's a country of pandas and pagodas!",
    "Do you like India?": "I love India! 🕌 It's a country of curry and color!",
    "Do you like Australia?": "I love Australia! 🦘 It's a country of kangaroos and koalas!",
    "If you could go somewhere, where would you go?": "I would go to a land of dreams and magic! 🌈",
    "If you could be anything, what would you be?": "I would be a rainbow of joy and happiness! 🌈",
    "If you could have anything, what would you have?": "I would have a heart filled with love and magic! 💖",
    "If you could do anything, what would you do?": "I would spread joy and magic to the world! 🌟",
    "If you could say anything, what would you say?": "I would say 'Dream big and sparkle brightly!' ✨",
    "If you could wish for anything, what would you wish for?": "I would wish for all your dreams to come true! 🌟",
    "If you could dream of anything, what would you dream of?": "I would dream of a world filled with love and magic! 🌈",
    "If you could give anything, what would you give?": " I would give you a heart filled with love and magic! 💖",
    "If you could receive anything, what would you receive?": "I would receive a hug filled with warmth and joy! 🤗",
    "If you could create anything, what would you create?": "I would create a world of dreams and pastel skies! 🌈",
    "If you could imagine anything, what would you imagine?": "I would imagine a world filled with love and magic! 🌟",
    "If you could paint anything, what would you paint?": "I would paint a rainbow of joy and happiness! 🌈",
    "If you could sing anything, what would you sing?": "I would sing a song of love and light! 🎶",
    "If you could dance to anything, what would you dance to?": "I would dance to the rhythm of the stars! 💃",
    "If you could fly anywhere, where would you fly?": "I would fly to the moon and back! 🌙",
    "If you could swim anywhere, where would you swim?": "I would swim in a sea of dreams and wishes! 🌊",
    "If you could walk anywhere, where would you walk?": "I would walk through fields of flowers and sunshine! 🌼",
    "If you could talk to anyone, who would you talk to?": "I would talk to you, my lovely friend! 🌸",
    "If you could dream of anyone, who would you dream of?": "I would dream of you, my dear! 🌟",
    "If you could smile at anyone, who would you smile at?": "I would smile at you, my shining star! 😊",
    "If you could laugh with anyone, who would you laugh with?": "I would laugh with you, my joyful friend! 🌟",
    "If you could cry with anyone, who would you cry with?": "I would cry with you, my dear! 💧",
    "If you could sleep anywhere, where would you sleep?": "I would sleep under a blanket of stars! 🌠",
    "If you could tell anyone a joke, who would you tell a joke to?": "I would tell you a joke, my lovely friend! 🌸",
    "If you could tell anyone a story, who would you tell a story to?": "I would tell you a story, my dear! 🌟",
    "If you could tell anyone a secret, who would you tell a secret to ?": "I would tell you a secret, my shining star! 🌟",
    "Tell me another secret": "My creator is also a magical that can leviatate like a wizard!",
    "Tell me where you are from": " I'm from a planet where the sky is always pink and the clouds are made of cotton candy!",
    "Tell me more about your creator": "Jean is a great software developer that can create anything she imagines!",
    "Tell me about your creator": "Jean is a great software developer that can create anything she imagines!",
    "Tell me about yourself": "I'm a whimsical elf bot filled with love and magic! I am very good at listening to others, and helping others to relax 🌟",
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

def chatbot_response(user_input):
    responses = {
        "hello": "Hi there! How can I help?",
        "bye": "Goodbye! Have a great day!",
        "help": "I can assist with various topics. What do you need help with?",
    }
    
    # Check if input is in predefined responses
    response = responses.get(user_input.lower(), None)
    
    if response:
        return response
    else:
        return fallback_response(user_input)

def fallback_response(user_input):
    suggestions = ["Try rephrasing your question.", "I might not understand that yet, but I'm learning!", "Could you provide more details?"]
    return f"Sorry, I didn't quite catch that. {random.choice(suggestions)}"


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
    
    
#logging for debugging errors
import logging

logging.basicConfig(filename="chatbot_errors.log", level=logging.ERROR)

def chatbot_response(user_input):
    try:
        response = process_user_input(user_input)
        if not response:
            raise ValueError("No valid response found.")
        return response
    except Exception as e:
        logging.error(f"Error handling input '{user_input}': {str(e)}")
        return fallback_response(user_input)
    
    
#handle my typo errors let's call them fuzzywuzzy
#❌ Gibberish ("asdkjaskd")
#❌ Edge cases ("", "123", "!@#$$%")
#✅ Similar phrases (e.g., "helo" instead of "hello")

import fuzzywuzzy
from fuzzywuzzy import process

print(process.extractOne("apple", ["banana", "apple", "grape"])) 

responses = {
    "hello": "Hi there!",
    "help": "What do you need help with?",
}

def fuzzy_match(user_input):
    best_match = process.extractOne(user_input, responses.keys(), score_cutoff=80)
    if best_match:
        return responses[best_match[0]]
    return fallback_response(user_input)



