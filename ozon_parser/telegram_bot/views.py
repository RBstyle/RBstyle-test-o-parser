from django.http import HttpResponse

from telegram_bot.bot import run_bot


def index(request):
    run_bot()
    return HttpResponse("<h1>Ты подключился!</h1>")
