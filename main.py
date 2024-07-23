import logging
import os
from typing import Any

import requests
from random import randint
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, filters
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define states
WELCOME, QUESTION, CANCEL, CORRECT, GOODBYE, CHAT, ANIME_RECOMMENDATION, QUOTE, FACT, PHILOSOPHICAL_QUESTION = range(10)


# Entry function
async def start(update: Update, context: CallbackContext) -> int:
    """Send a welcome message and prompt user to start the quiz."""
    try:
        await update.message.reply_text(
            "Hello, I'm Lain. Do you want to answer a question or chat? (Yes/No) Or use /help for guidance.",
            reply_markup=ReplyKeyboardMarkup([
                ['Yes', 'No'],
                ['/chat', '/anime', '/fact', '/quote', '/allah', '/bo']
            ], one_time_keyboard=True)
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return WELCOME


# Help command
async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message with instructions."""
    try:
        await update.message.reply_text(
            "Greetings from Lain! I can assist with a variety of tasks, from answering questions to chatting and providing interesting content. Here’s a guide to what I can do:\n\n"
            "/start - Initiate a conversation and get started with our interactions.\n"
            "/help - Display this help message with all available commands.\n"
            "/cancel - Terminate the current interaction and return to the main menu.\n"
            "/chat - Engage in a casual conversation about various topics.\n"
            "/anime - Receive anime recommendations or learn interesting facts.\n"
            "/quote - Get an inspiring or motivational quote.\n"
            "/fact - Discover a fascinating fact about a number.\n"
            "/allah - Receive a thoughtful message related to the concept of focus.\n"
            "/bo - Get a response related to surprises and connections.\n"
            "/philosophical_question - Jump straight to a philosophical question."
        )
    except Exception as e:
        logger.error(f"Error in help_command: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")


# Helper functions for API calls
async def fetch_anime_recommendation() -> str:
    try:
        response = requests.get('https://api.jikan.moe/v4/random/anime')
        response.raise_for_status()
        data = response.json()
        return data['data']['title']
    except Exception as e:
        logger.error(f"Error fetching anime recommendation: {e}")
        return "I'm having trouble fetching recommendations right now."


async def fetch_random_quote() -> str:
    try:
        response = requests.get('https://api.quotable.io/random')
        response.raise_for_status()
        data = response.json()
        return f"{data['content']} — {data['author']}"
    except Exception as e:
        logger.error(f"Error fetching quote: {e}")
        return "I'm having trouble fetching a quote right now."


async def fetch_number_fact() -> str:
    try:
        number = randint(1, 100)
        response = requests.get(f'http://numbersapi.com/{number}')
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching number fact: {e}")
        return "I'm having trouble fetching a fact right now."


async def fetch_philosophical_quotes() -> tuple[None, None] | tuple[Any, Any]:
    try:
        response = requests.get('https://zenquotes.io/api/random')
        logger.info(f"ZenQuotes API response status code: {response.status_code}")
        logger.info(f"ZenQuotes API response text: {response.text}")

        response.raise_for_status()
        if not isinstance(response.json(), list) or len(response.json()) == 0:
            return None, None

        quote = response.json()[0]
        return quote, quote['a']
    except Exception as e:
        logger.error(f"Error fetching philosophical quotes: {e}")
        return None, None


# Command handlers
async def chat(update: Update, context: CallbackContext) -> int:
    """Start a casual chat with the user."""
    try:
        await update.message.reply_text(
            "What would you like to talk about? I’m here to discuss various topics, from anime to technology and beyond."
        )
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return CHAT


async def anime_recommendation(update: Update, context: CallbackContext) -> int:
    """Provide anime recommendations or facts."""
    try:
        recommendation = await fetch_anime_recommendation()
        await update.message.reply_text(
            f"How about watching '{recommendation}'? It's an interesting anime you might enjoy!"
        )
    except Exception as e:
        logger.error(f"Error in anime_recommendation: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def quote(update: Update, context: CallbackContext) -> int:
    """Provide a random inspirational quote."""
    try:
        quote = await fetch_random_quote()
        await update.message.reply_text(quote)
    except Exception as e:
        logger.error(f"Error in quote: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def fact(update: Update, context: CallbackContext) -> int:
    """Provide an interesting fact about a number."""
    try:
        fact = await fetch_number_fact()
        await update.message.reply_text(fact)
    except Exception as e:
        logger.error(f"Error in fact: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def randomize_numbers(update: Update, context: CallbackContext) -> None:
    try:
        context.user_data['rand_x'], context.user_data['rand_y'] = randint(0, 1000), randint(0, 1000)
        await update.message.reply_text(
            f"Can you calculate {context.user_data['rand_x']} + {context.user_data['rand_y']}?")
    except Exception as e:
        logger.error(f"Error in randomize_numbers: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")


async def welcome(update: Update, context: CallbackContext) -> int:
    try:
        if update.message.text.lower() in ['yes', 'y']:
            await update.message.reply_text(
                "Just like in the Wired, sometimes the simplest questions hold the deepest meanings."
            )
            await philosophical_question(update, context)
            return PHILOSOPHICAL_QUESTION
        else:
            await update.message.reply_text(
                "If you change your mind, just remember... I'm always here, in the Wired."
            )
            return CANCEL
    except Exception as e:
        logger.error(f"Error in welcome: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
        return WELCOME


async def philosophical_question(update: Update, context: CallbackContext) -> int:
    """Send a philosophical question."""
    try:
        quote, author = await fetch_philosophical_quotes()
        if not author:
            await update.message.reply_text("I couldn't fetch a philosophical quote at the moment.")
            await randomize_numbers(update, context)
            return QUESTION

        question_text = (
            f"Here's a philosophical quote:\n\n\"{quote['q']}\"\n\n"
            f"Who said this?\n1. {author}\n2. [Another Author]\n"
            "Reply with '1' or '2'."
        )

        await update.message.reply_text(question_text)
        context.user_data['philosophical_quote'] = True
        context.user_data['correct_author'] = author
        context.user_data['correct_option'] = '1'
    except Exception as e:
        logger.error(f"Error in philosophical_question: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return QUESTION


async def question(update: Update, context: CallbackContext) -> int:
    """Handle the user's response to the philosophical question."""
    try:
        user_answer = update.message.text.strip()

        if 'philosophical_quote' in context.user_data:
            correct_option = context.user_data.get('correct_option')

            if user_answer == correct_option:
                await update.message.reply_text("That's correct! Well done.")
                await update.message.reply_text(
                    "Did you find this interaction insightful? Sometimes, our perceptions shape our understanding of reality."
                )
                return CORRECT
            else:
                await update.message.reply_text("That's incorrect. Try again.")
                await philosophical_question(update, context)
                return PHILOSOPHICAL_QUESTION
        else:
            rand_x = context.user_data.get('rand_x')
            rand_y = context.user_data.get('rand_y')
            correct_answer = rand_x + rand_y

            if user_answer.isdigit() and int(user_answer) == correct_answer:
                await update.message.reply_text("That's correct! Well done.")
                return CORRECT
            else:
                await update.message.reply_text(f"That's incorrect. The correct answer was {correct_answer}.")
                return QUESTION
    except Exception as e:
        logger.error(f"Error in question: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
        return QUESTION


async def correct(update: Update, context: CallbackContext) -> int:
    """Handle correct answer acknowledgment and continue."""
    try:
        await update.message.reply_text(
            "Do you want to answer another question or continue chatting? (Yes/No)"
        )
    except Exception as e:
        logger.error(f"Error in correct: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return WELCOME


async def goodbye(update: Update, context: CallbackContext) -> int:
    """Send a goodbye message and end the conversation."""
    try:
        await update.message.reply_text("Goodbye. 'We are all connected in the Wired.'")
    except Exception as e:
        logger.error(f"Error in goodbye: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Handle cancellation of the conversation."""
    try:
        await update.message.reply_text(
            "The conversation has been canceled. If you want to start again, just type /start."
        )
    except Exception as e:
        logger.error(f"Error in cancel: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def allah(update: Update, context: CallbackContext) -> int:
    """Send a thoughtful message related to the concept of focus."""
    try:
        await update.message.reply_text(
            "Focus is the bridge between dreams and reality. Sometimes, we must let go of distractions to achieve clarity."
        )
    except Exception as e:
        logger.error(f"Error in allah: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


async def bo(update: Update, context: CallbackContext) -> int:
    """Send a response related to surprises and connections."""
    try:
        await update.message.reply_text(
            "In the Wired, surprises are common. Embrace the unexpected and stay open to new connections."
        )
    except Exception as e:
        logger.error(f"Error in bo: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    try:
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            logger.error("Bot token not found in environment variables.")
            return

        application = Application.builder().token(token).build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                WELCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, welcome)],
                QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question)],
                CANCEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)],
                CORRECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, correct)],
                GOODBYE: [MessageHandler(filters.TEXT & ~filters.COMMAND, goodbye)],
                CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat)],
                ANIME_RECOMMENDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, anime_recommendation)],
                QUOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, quote)],
                FACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, fact)],
                PHILOSOPHICAL_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, philosophical_question)],
            },
            fallbacks=[
                CommandHandler('cancel', cancel),
                CommandHandler('help', help_command),
                CommandHandler('chat', chat),
                CommandHandler('anime', anime_recommendation),
                CommandHandler('quote', quote),
                CommandHandler('fact', fact),
                CommandHandler('allah', allah),
                CommandHandler('bo', bo),
                CommandHandler('philosophical_question', philosophical_question),
            ],
        )

        application.add_handler(conv_handler)

        logger.info("Starting Lain bot...")
        print("Lain bot has started. Waiting for commands...")

        application.run_polling()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print("Something went wrong. Please try again later.")


if __name__ == '__main__':
    main()
