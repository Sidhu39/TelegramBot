# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import sys
import requests
import json
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, \
    ConversationHandler

# ------ GLOBAL VARIABLES ------
TOKEN = "8282668081:AAFPF-f1O5RMMa-_Ii16bFVepH9rj39zkts"
weather_api = "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"
area = "Changi"
useless_fact_api = "https://uselessfacts.jsph.pl/api/v2/facts/random"
WAITING_FOR_RESPONSE = 1
FRUITS = [
    "apple", "apricot", "avocado", "banana", "bilberry", "blackberry", "blackcurrant",
    "blueberry", "boysenberry", "breadfruit", "cactus pear", "canistel", "cantaloupe",
    "cherry", "cherimoya", "chico fruit", "cloudberry", "coconut", "cranberry", "currant",
    "custard apple", "damson", "date", "dragonfruit", "durian", "elderberry", "feijoa",
    "fig", "goji berry", "gooseberry", "grape", "raisin", "grapefruit", "guava", "honeyberry",
    "huckleberry", "jabuticaba", "jackfruit", "jambul", "jujube", "kiwano", "kiwi", "kumquat",
    "lemon", "lime", "loganberry", "longan", "loquat", "lychee", "mandarin", "mango", "mangosteen",
    "marionberry", "melon", "miracle fruit", "mulberry", "nance", "nectarine", "olive", "orange",
    "blood orange", "tangerine", "clementine", "papaya", "passionfruit", "peach", "pear", "persimmon",
    "plantain", "plum", "prune", "pineapple", "pineberry", "pomegranate", "pomelo", "quince",
    "raspberry", "redcurrant", "salak", "santol", "sapodilla", "sapote", "soursop", "star apple",
    "starfruit", "strawberry", "surinam cherry", "tamarillo", "tamarind", "tangelo", "ugli fruit",
    "watermelon", "white currant", "white sapote", "yumberry", "ziziphus fruit"
]
fruit_db = {}
user_list = []


# ---------- Reuseable functions ----------

def store_chat_id(chat_id: int):
    if chat_id not in user_list:
        user_list.append(chat_id)

    # Only show after teaching DB
    # with open('user.json', 'w', encoding='utf-8') as f:
    #     json.dump(user_list, f, ensure_ascii=False, indent=4)


# ---------- End of Reuseable functions ----------

# ---------- Starter code ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Stores user id
    store_chat_id(context._chat_id)

    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Stores user id
    store_chat_id(context._chat_id)

    help_msg = """
    Welcome to the Telegram Bot workshop. 
    These are the commands that you would attempt to recreate!

    /start - Greets you
    /help - Brings up the help menu
    /broadcast - Saves users that has used the bot
    /fun - Calls API to retrieve information!
    /fruit - Save your favourite fruit
    /fav - Show your favourite fruit

    Have fun!!
    """

    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_msg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # Stores user id
    store_chat_id(context._chat_id)

    await update.message.reply_text(update.message.text)


# ---------- End of Starter code ----------

# ---------- TODO 1: Build a broadcasting feature ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    for id in user_list:
        await context.bot.send_message(id,'hi')
    # TODO 1.1: Sends each stored user id a message


# ---------- END OF TODO 1 ----------


# ---------- TODO 2: BUTTONS + API CALLS ----------
async def fun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with inline buttons attached."""

    # TODO 2.1: Define buttons using InlineKeyboardButton
    keyboard = [
        [
            InlineKeyboardButton("Fact of the day", callback_data="fact"),
            InlineKeyboardButton("Weather", callback_data="weather"),
        ],
    ]

    # TODO 2.2: Define InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup(keyboard)

    # TODO 2.3: Send message to the users
    await update.message.reply_text("Please choose: ",reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    # TODO 2.4: Processing to determine its reply
    if query.data == "weather":
        response = requests.get(weather_api)
        data = response.json()['data']['items'][0]
        await query.edit_message_text(text=f"{data}")
    elif query.data == "fact":
        response = requests.get(useless_fact_api)
        data1 = response.json()["text"]
        await query.edit_message_text(text=f"{data1}")
    else:
        await query.edit_message_text(text="Todo 2.4 is not done")

# ---------- END OF TODO 2 ----------


# ---------- TODO 3: CONVOS + DB ----------
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stores favourite fruit."""

    # TODO 3.1: set a update.message.reply_text message

    # TODO 3.2: Return a state (Waiting or end)


async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receives and processes the user's response."""
    user_answer = update.message.text  # Get the text the user sent

    store_to_database(chat_id=context._chat_id, fruit=user_answer)

    # TODO 3.3: Do something with the answer

    # TODO 3.4: If the condition is right, return an end the conversation. Else return a waiting state


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""
    await update.message.reply_text('Okay, cancelled.')
    return ConversationHandler.END


def store_to_database(chat_id, fruit):
    fruit_db[chat_id] = fruit

    with open('fruit.json', 'w', encoding='utf-8') as f:
        json.dump(fruit_db, f, ensure_ascii=False, indent=4)


async def fav(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open('fruit.json', 'r') as f:
            fruit_db = json.load(f)
            chat_id_str = str(context._chat_id)
            if chat_id_str in fruit_db:
                await update.message.reply_text(f"Your favorite fruit is: {fruit_db[chat_id_str]}")
            else:
                await update.message.reply_text("You haven't told me your favorite fruit yet! Use /fruit to set it.")


    except FileNotFoundError:  # Error handling
        # If data.json doesn't exist, create it with an empty dictionary
        fruit_db = {}
        with open('fruit.json', 'w') as f:
            json.dump(fruit_db, f)
        await update.message.reply_text("You haven't told me your favorite fruit yet! Use /fruit to set it.")
    except KeyError:
        await update.message.reply_text("You haven't told me your favorite fruit yet! Use /fruit to set it.")
    except Exception as e:
        await update.message.reply_text("Sorry, something went wrong while retrieving your favorite fruit.")


# ---------- END OF TODO 3 ----------


# ---------- MAIN HANDLERS FOR BOT ----------
def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Todo 1 - Broadcast feature
    application.add_handler(CommandHandler("broadcast", broadcast))

    # Todo 2 - API Calls
    application.add_handler(CommandHandler("fun", fun))
    application.add_handler(CallbackQueryHandler(button))

    # Todo 3 - Conversation + database feature
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('fruit', ask_question)],  # /start begins the conversation
        states={
            WAITING_FOR_RESPONSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("fav", fav))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# ---------- END OF HANDLERS FOR BOT ----------

if __name__ == "__main__":
    main()  # ENTRY POINT