from django.urls import path
from telegram_bot.views import index
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", csrf_exempt(index), name="index"),
]
