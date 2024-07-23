# Telegram Lain Bot

This is a Telegram bot inspired by the anime Serial Experiments Lain. It interacts with users by asking philosophical questions, providing anime recommendations, and sharing inspirational quotes and fun facts.

## Features

- **Interactive Questions**: Engage in thought-provoking conversations with philosophical questions.
- **Anime Recommendations**: Receive random anime recommendations to explore new shows.
- **Inspirational Quotes**: Get a dose of motivation with random quotes.
- **Fun Facts**: Learn interesting facts about numbers and more.

## Getting Started

### Prerequisites

- Python 3.7+
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/telegram-lain-bot.git
    cd telegram-lain-bot
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your Telegram bot token:
    ```env
    TELEGRAM_TOKEN=your-telegram-bot-token
    ```

### Running the Bot
Start the bot with the following command:
```bash
python main.py
```

### Usage
Interact with the bot on Telegram using the following commands:

- **/start**: Initiate a conversation and get started with our interactions.
- **/help**: Display a help message with all available commands.
- **/cancel**: Terminate the current interaction and return to the main menu.
- **/chat**: Engage in a casual conversation about various topics.
- **/anime**: Receive anime recommendations or learn interesting facts.
- **/quote**: Get an inspiring or motivational quote.
- **/fact**: Discover a fascinating fact about a number.
- **/allah**: Receive a thoughtful message related to the concept of focus.
- **/bo**: Get a response related to surprises and connections.
- **/philosophical_question**: Jump straight to a philosophical question.

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Acknowledgements
- **Inspired by**: The anime [Serial Experiments Lain](https://en.wikipedia.org/wiki/Serial_Experiments_Lain).
- **Built using**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
- **Quotes fetched from**: [Quotable.io](https://quotable.io/).
- **Anime recommendations fetched from**: [Jikan API](https://jikan.moe/).
- **Number facts fetched from**: [Numbers API](http://numbersapi.com/).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
