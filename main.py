import logging
import os
import requests
from random import randint
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
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
WELCOME, QUESTION, CANCEL, CORRECT, GOODBYE, CHAT, ANIME_RECOMMENDATION, QUOTE, FACT = range(9)
# Entry function


async def start(update: Update, context: CallbackContext) -> int:
    """Send a welcome message and prompt user to start the quiz."""
    await update.message.reply_text(
        "Hello, I'm Lain. Do you want to answer a question or chat? (Yes/No) Or use /help for guidance.",
        reply_markup=ReplyKeyboardMarkup([
            ['Yes', 'No'],
            ['/chat', '/anime', '/fact', '/quote']
        ], one_time_keyboard=True)
    )
    return WELCOME


# Help command
async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message with instructions."""
    await update.message.reply_text(
        "I am Lain. I can ask you questions, chat about anime, provide recommendations, and share quotes or fun facts. Here are the commands you can use:\n"
        "/start - Start the interaction and answer questions.\n"
        "/help - Show this help message.\n"
        "/cancel - Cancel the current interaction.\n"
        "/chat - Engage in a casual chat about various topics.\n"
        "/anime - Get anime recommendations or facts.\n"
        "/quote - Get a random inspirational quote.\n"
        "/fact - Get an interesting fact about a number."
    )


# Helper functions for API calls
async def fetch_anime_recommendation() -> str:
    try:
        response = requests.get('https://api.jikan.moe/v4/random/anime')
        data = response.json()
        return data['data']['title']
    except Exception as e:
        logger.error(f"Error fetching anime recommendation: {e}")
        return "I'm having trouble fetching recommendations right now."


async def fetch_random_quote() -> str:
    try:
        response = requests.get('https://api.quotable.io/random')
        data = response.json()
        return f"{data['content']} — {data['author']}"
    except Exception as e:
        logger.error(f"Error fetching quote: {e}")
        return "I'm having trouble fetching a quote right now."


async def fetch_number_fact() -> str:
    try:
        number = randint(1, 100)
        response = requests.get(f'http://numbersapi.com/{number}')
        return response.text
    except Exception as e:
        logger.error(f"Error fetching number fact: {e}")
        return "I'm having trouble fetching a fact right now."


# Chat command
async def chat(update: Update, context: CallbackContext) -> int:
    """Start a casual chat with the user."""
    await update.message.reply_text(
        "What would you like to talk about? I can discuss various topics including anime, technology, or existential questions."
    )
    return CHAT


# Anime recommendation command
async def anime_recommendation(update: Update, context: CallbackContext) -> int:
    """Provide anime recommendations or facts."""
    recommendation = await fetch_anime_recommendation()
    await update.message.reply_text(
        f"How about watching '{recommendation}'? It's an interesting anime!"
    )
    return ConversationHandler.END


# Quote command
async def quote(update: Update, context: CallbackContext) -> int:
    """Provide a random inspirational quote."""
    quote = await fetch_random_quote()
    await update.message.reply_text(quote)
    return ConversationHandler.END


# Fact command
async def fact(update: Update, context: CallbackContext) -> int:
    """Provide an interesting fact about a number."""
    fact = await fetch_number_fact()
    await update.message.reply_text(fact)
    return ConversationHandler.END


# Helper function to generate random numbers and send the question
async def randomize_numbers(update: Update, context: CallbackContext) -> None:
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0, 1000), randint(0, 1000)
    await update.message.reply_text(f"Can you calculate {context.user_data['rand_x']} + {context.user_data['rand_y']}?")


# Welcome state handler
async def welcome(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() in ['yes', 'y']:
        await update.message.reply_text(
            "Just like in the Wired, sometimes the simplest questions hold the deepest meanings."
        )
        await randomize_numbers(update, context)
        return QUESTION
    else:
        await update.message.reply_text(
            "If you change your mind, just remember... I'm always here, in the Wired."
        )
        return CANCEL


# Question state handler
async def question(update: Update, context: CallbackContext) -> int:
    solution = context.user_data['rand_x'] + context.user_data['rand_y']
    if int(update.message.text) == solution:
        await update.message.reply_text("That's correct... just as I expected.")
        await update.message.reply_text(
            "Did you find this interaction helpful? It's just like exploring the layers of the Wired."
        )
        return CORRECT
    else:
        await update.message.reply_text("That's incorrect... try again.")
        await randomize_numbers(update, context)
        return QUESTION


# Correct state handler
async def correct(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() in ['yes', 'y']:
        await update.message.reply_text("I'm glad it was useful. Sometimes, even in the Wired, we find clarity.")
    else:
        await update.message.reply_text("You must be quite skilled already. The Wired holds no secrets for you.")
    await update.message.reply_text(
        "Before you go, do you want to hear a quote from 'Serial Experiments Lain'? (Yes/No)",
        reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
    )
    return GOODBYE


# Goodbye state handler
async def goodbye(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() in ['yes', 'y']:
        await update.message.reply_text(
            "In the Wired, the physical and digital worlds are intertwined. 'No matter where you go, everyone is connected.'"
        )
        await update.message.reply_text("Goodbye, and remember... 'Close the world, open the next.'")
    else:
        await update.message.reply_text("Goodbye. 'We are all connected in the Wired.'")
    first_name = update.message.from_user.first_name
    await update.message.reply_text(f"See you, {first_name}. Until next time in the Wired.")
    return ConversationHandler.END


# Cancel state handler
async def cancel(update: Update, context: CallbackContext) -> int:
    first_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Alright, {first_name}. Until we meet again in the Wired.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    token = os.getenv('TOKEN')
    if not token:
        logger.error("Bot token not found in environment variables.")
        return

    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WELCOME: [MessageHandler(filters.Regex(r'^(yes|no|y|n)$'), welcome)],
            QUESTION: [MessageHandler(filters.Regex(r'^\d+$'), question)],
            CANCEL: [MessageHandler(filters.Regex(r'^(yes|no|y|n)$'), cancel)],
            CORRECT: [MessageHandler(filters.Regex(r'^(yes|no|y|n)$'), correct)],
            GOODBYE: [MessageHandler(filters.Regex(r'^(yes|no|y|n)$'), goodbye)],
            CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat)],
            ANIME_RECOMMENDATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, anime_recommendation)],
            QUOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, quote)],
            FACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, fact)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('help', help_command),
            CommandHandler('chat', chat),
            CommandHandler('anime', anime_recommendation),
            CommandHandler('quote', quote),
            CommandHandler('fact', fact)
        ],
    )

    application.add_handler(conv_handler)

    logger.info("Starting Lain bot...")
    print("Lain bot has started. Waiting for commands...")

    application.run_polling()


if __name__ == '__main__':
    main()
