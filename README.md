# Terminal ChatBot (Django + ChatterBot)

This project provides a terminal-based chat client built with Django and ChatterBot.
The Django app supplies a management command that launches an interactive chat loop.

## Requirements
- Python 3.10+
- Django
- ChatterBot
- spaCy (plus the English model)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Run the chatbot
```bash
python manage.py chat
```

Example session:
```
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
```

## Notes
- The first run trains the bot using the built-in English corpus and stores data in `db.sqlite3`.
- Use `exit` or `quit` to end the session.

## Troubleshooting
- If you see an error about `en_core_web_sm` being missing, run:
  ```bash
  python -m spacy download en_core_web_sm
  ```
