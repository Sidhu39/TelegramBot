import sys
import requests
from telegram import ForceReply,Update,InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8282668081:AAFPF-f1O5RMMa-_Ii16bFVepH9rj39zkts"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello! this is your custom Telegram bot!")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - say hi \n/help - show this \ntype anything and i will echo it back to you")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text and not update.message.text.startswith("/"):
        await update.message.reply_text(update.message.text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
