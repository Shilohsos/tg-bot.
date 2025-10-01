import os
import threading
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]

# --- tiny web server for Render's port scan ---
async def _ok(_request):
    return web.Response(text="ok")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", _ok)
    app.router.add_get("/healthz", _ok)
    port = int(os.environ.get("PORT", "10000"))
    web.run_app(app, port=port)

# --- telegram bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! You started the bot.")

def main():
    # start the web server in the background
    threading.Thread(target=start_web_server, daemon=True).start()

    # start the bot (long polling)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(drop_pending_updates=True, close_loop=False)

if __name__ == "__main__":
    main()
