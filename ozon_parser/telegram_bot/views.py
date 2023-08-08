import asyncio
import threading
from django.http import HttpResponse
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application
from django.conf import settings


# Create your views here.
def index(request):
    threading.Thread(target=run_bot, daemon=True).start()
    return HttpResponse("<h1>Ты подключился!</h1>")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def run_bot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        application = (
            Application.builder()
            .token("6153040485:AAF7X_hE8FA9bfKoDk7r6Tm8r9BNKIuJZTk")
            .build()
        )

        start_handler = CommandHandler("start", start)
        application.add_handler(start_handler)
        application.run_polling()

    except Exception as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", e)


# run_bot()
