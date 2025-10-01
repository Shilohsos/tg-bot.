import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # e.g. https://tg-bot.onrender.com

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! You started the bot.")

def main():
    port = int(os.environ.get("PORT", "10000"))
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # this starts an HTTP server and registers the Telegram webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,  # secret-ish path
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
        drop_pending_updates=True,
        close_loop=False,
    )

if __name__ == "__main__":
    main()
