# 🇯🇵 Japgo: Japanese Instructor Discord Bot  
*A Discord bot that helps you learn Japanese: built in Python.*

---

## 📘 Overview  
**Japgo** Discord bot designed to assist Japanese learners through AI-powered exercises and reminders, using information learned in class.  
---

## ✨ Features  
- Instead of a notebook, add all your notes to appropriate Discord server.  
- The bot will help you generate Japanese exercises based on what you learned, and will shame you when you don't do your homework.  
- Integrates OpenAI for quiz creation.   
---

## Structure: 
  - `main.py` - bot entry point  
  - `config.py` - configuration and tokens  
  - `services/` - AI and business logic  
  - `handlers/` - Discord event and command handlers  
  - `tests/` - unit and integration tests  
---

## ⚙️ Setup  

### 1. Prerequisites  
- Python 3.8+  
- Discord Bot Token  
- OpenAI API Key  

### 2. Installation  
```bash
git clone https://github.com/AdiBarakOh/japgo.git
cd japgo
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration  
Edit `config.py` (or use environment variables) with your keys and settings, and adjust to your Japanease server and channel names. 
```

### Run the Bot  
```bash
python main.py
```

---

## License  
Educational and non-commercial use only.  

---

- Built by **Adi Barak**

---

**📚 勉強しましょう - Let’s learn together!**
