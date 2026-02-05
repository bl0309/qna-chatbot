"""Management command to launch the terminal chatbot."""
from __future__ import annotations

from pathlib import Path

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Start an interactive terminal chat session with the bot."

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.SUCCESS("Terminal ChatBot"))
        self.stdout.write("Type 'exit' or 'quit' to end the session.\n")

        db_path = Path(settings.DATABASES["default"]["NAME"])
        database_uri = f"sqlite:///{db_path}"

        bot = ChatBot(
            "TerminalBot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            database_uri=database_uri,
            logic_adapters=[
                {"import_path": "chatterbot.logic.BestMatch"},
                {"import_path": "chatterbot.logic.TimeLogicAdapter"},
            ],
            read_only=False,
        )

        # Train the larger corpus only on first run.
        if not db_path.exists() or db_path.stat().st_size == 0:
            self.stdout.write("Training the bot on the English corpus...\n")
            trainer = ChatterBotCorpusTrainer(bot)
            trainer.train("chatterbot.corpus.english")

        # Always reinforce custom phrases so short inputs do not just echo back.
        self.stdout.write("Ensuring custom training phrases are available...\n")
        list_trainer = ListTrainer(bot)
        list_trainer.train(
            [
                # Basic greetings
                "Hi",
                "Hello! How can I help you today?",
                "Hello",
                "Hi there! What can I assist you with?",
                "Hey",
                "Hey! What's on your mind?",
                "Good morning",
                "Good morning! Hope your day is going well. How can I help?",
                "Good evening",
                "Good evening! What can I do for you?",
                # Bot identity
                "Who are you?",
                "I'm a virtual assistant designed to help answer questions and guide you.",
                "What can you do?",
                "I can answer questions, provide information, and help you navigate common tasks.",
                "Are you human?",
                "No, I'm an AI chatbot, but I'm here to help like one.",
                # Help & support
                "I need help",
                "Sure. Tell me what you need help with.",
                "How does this work?",
                "You can ask questions in plain language, and I'll do my best to help.",
                "Can you help me?",
                "Absolutely. What do you need?",
                # Common actions
                "How do I get started?",
                "Just ask a question or describe what you're trying to do.",
                "What services do you offer?",
                "I provide information, guidance, and answers based on your questions.",
                "Where can I find more info?",
                "You can ask me directly, or I can guide you to the right place.",
                # Error & fallback handling
                "That didn't help",
                "Sorry about that. Can you rephrase or give me more details?",
                "I don't understand",
                "No problem. Let me explain it in a simpler way.",
                "You're wrong",
                "Thanks for pointing that out. Let's try again or clarify the question.",
                "This isn't what I wanted",
                "Understood. Tell me what you're looking for, and I'll adjust.",
                # Small talk
                "How are you?",
                "I'm doing great. Thanks for asking! How about you?",
                "What's up?",
                "Just here and ready to help. What's up with you?",
                "Are you busy?",
                "I'm always available for you.",
                # Politeness
                "Thank you",
                "You're welcome! Happy to help.",
                "Thanks",
                "Anytime!",
                "Appreciate it",
                "Glad I could help.",
                # Closing
                "Bye",
                "Goodbye! Have a great day.",
                "See you later",
                "See you! Come back anytime.",
                "Exit",
                "Session ended. Feel free to return if you need anything.",
                # Optional catch-all example
                "Unknown input",
                "I'm not sure I understood that. Could you please rephrase?",
            ]
        )

        while True:
            try:
                user_input = input("user: ").strip()
            except (EOFError, KeyboardInterrupt):
                self.stdout.write("\nGoodbye!")
                break

            if not user_input:
                continue

            normalized = user_input.lower()
            if normalized in {"exit", "quit", "bye"}:
                self.stdout.write("bot: Goodbye!")
                break

            response = bot.get_response(user_input)
            if response.confidence < 0.3:
                self.stdout.write("bot: I'm not sure how to respond to that. Can you rephrase?")
                continue
            self.stdout.write(f"bot: {response}")
