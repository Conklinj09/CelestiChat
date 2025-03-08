# 🌙✨ CelestiChat 🌸🌟

CelestiChat is a **whimsical, AI-powered chatbot** built with **Flask** and enhanced with **SQLite**, **Tailwind CSS**, and **JavaScript (Fetch API)** for a seamless and beautiful user experience. Designed with celestial and floral aesthetics in mind, CelestiChat brings magic and functionality together! 🌿🌠🌷

## 🌌 Project Structure
```
CelestiChat/
│── app.py              # 🌟 Main Flask app
│── config.py           # 🎨 Configuration settings
│── requirements.txt    # 📜 Dependencies
│── database.db         # 🌍 SQLite database
│── /static/            # 🎨 CSS, JS, and images (Styled with Tailwind CSS)
│── /templates/         # 🏗️ HTML templates (if applicable)
│── /models/            # 🔍 Database models
│── /routes/            # 🚀 API routes
│── /tests/             # ✅ Unit tests
│── /venv/              # 🧪 Virtual environment (optional)
```

## 🚀 Installation Guide
### 1️⃣ Clone the Repository ✨
```bash
git clone https://github.com/yourusername/CelestiChat.git
cd CelestiChat
```

### 2️⃣ Set Up a Virtual Environment 🌀
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies 🌙
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up the Database 🌸
Run the following to create the SQLite database and necessary tables:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### 5️⃣ Run the Application 🌠
```bash
python app.py
```
The Flask app will start running at **http://127.0.0.1:5000/**. Open your browser and chat with CelestiChat under the stars! 🌟✨

## 🛠 Installed Dependencies 🌿
Here are the key packages used in this project:
- **Flask** – Web framework 🌍
- **Flask-SQLAlchemy** – ORM for database handling 📚
- **Flask-CORS** – Enables cross-origin requests 🔗
- **python-dotenv** – Load environment variables 🔐
- **fuzzywuzzy** – String matching for chatbot interactions 🧩
- **python-Levenshtein** – Optimized string matching performance ⚡
- **Tailwind CSS** – Modern styling framework 🎨
- **JavaScript (Fetch API)** – Handles API requests dynamically 🚀

## 🌟 API Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/add` | POST | Add a new user |
| `/users/` | GET | Retrieve all users |

## 🧪 Running Tests 🔬
To run all unit tests, execute:
```bash
python -m unittest discover -s tests
```

## 🌠 Future Features 🌙
- ✨ NLP-powered chatbot responses
- 🔑 User authentication & sessions
- 🌎 Multi-language support
- 🌿 Interactive celestial UI improvements

---
Developed with 💫 love, 🌻 flowers, and 🌙 cosmic energy by [Your Name]

