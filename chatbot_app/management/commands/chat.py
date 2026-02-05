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

        # Train only when the database does not exist yet.
        if not db_path.exists() or db_path.stat().st_size == 0:
            self.stdout.write("Training the bot on the English corpus...\n")
            trainer = ChatterBotCorpusTrainer(bot)
            trainer.train("chatterbot.corpus.english")

            self.stdout.write("Adding custom training phrases...\n")
            list_trainer = ListTrainer(bot)
            list_trainer.train(
                [
                    "hi",
                    "Hello! How can I help you today?",
                    "hello",
                    "Hi there! What can I do for you?",
                    "how are you?",
                    "I am doing well, thanks for asking. How about you?",
                    "i am doing fine",
                    "Glad to hear that! What would you like to chat about?",
                    "what is your name?",
                    "I'm TerminalBot, your class assignment chatbot.",
                    "thank you",
                    "You're welcome!",
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
            if response.confidence < 0.65:
                self.stdout.write("bot: I'm not sure how to respond to that. Can you rephrase?")
                continue
            self.stdout.write(f"bot: {response}")
