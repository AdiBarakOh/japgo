# 🇯🇵 Japgo — Japanese Instructor Discord Bot  
*A lightweight Discord bot that helps you learn Japanese — built in Python.*

---

## 📘 Overview  
**Japgo** is an educational Discord bot designed to support Japanese learners through interactive exercises, grammar tips, and AI-powered prompts (via the OpenAI API).  
Ideal for **personal or small-group use**, it offers a modular structure for easy expansion.

---

## ✨ Features  
- Responds to learners’ prompts and commands on Discord.  
- Generates Japanese exercises, translations, and grammar explanations.  
- Integrates OpenAI for dynamic, natural-language assistance.  
- Simple configuration via environment variables or `config.py`.  
- Modular architecture (services, handlers, and tests) for maintainability.

---

## 🧠 Tech Stack  
- **Language:** Python ≥ 3.8  
- **Framework:** `discord.py`  
- **AI:** OpenAI API  
- **Structure:**  
  - `main.py` — bot entry point  
  - `config.py` — configuration and tokens  
  - `services/` — AI and business logic  
  - `handlers/` — Discord event and command handlers  
  - `tests/` — unit and integration tests  

---

## ⚙️ Setup  

### 1️⃣ Prerequisites  
- Python 3.8+  
- Discord Bot Token  
- OpenAI API Key  

### 2️⃣ Installation  
```bash
git clone https://github.com/AdiBarakOh/japgo.git
cd japgo
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configuration  
Edit `config.py` (or use environment variables as showed https://www.youtube.com/watch?v=Z2k7ZBMZT3Y) with your keys and settings:
```python
DISCORD_TOKEN = "your_discord_token"
OPENAI_API_KEY = "your_openai_key"
PREFIX = "!"
LOG_LEVEL = "INFO"
```
🚫 *Never commit tokens or keys to GitHub.*

### 4️⃣ Run the Bot  
```bash
python main.py
```
Then invite the bot to your server and use commands (e.g., `!help`).

---

## 🧪 Testing  
Tests live in the `tests/` directory.  
Run them with:
```bash
pytest
```

---

## 🤝 Contributing  
1. Fork the repo → create a branch (`feature/YourFeature`)  
2. Write clear commit messages  
3. Add or update tests  
4. Open a pull request describing your changes  

---

## ⚖️ License  
Educational and non-commercial use only.  
(You can replace this with an open-source license like MIT or Apache 2.0.)

---

## 🙏 Acknowledgements  
- [Discord.py](https://discordpy.readthedocs.io/) community  
- [OpenAI](https://openai.com/) API team  
- Built by **Adi Barak Oh**

---

**📚 勉強しましょう — Let’s learn together!**
