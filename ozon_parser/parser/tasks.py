from celery import Task
from ozon_parser.settings import BASE_DIR
import os
from celery.utils.log import get_task_logger
from aiogram import types
from .utils import get_products, save_product, get_last_package
from .models import Product
from parser.core.celery import app
import asyncio
from celery.result import AsyncResult

from telegram_bot.bot import success_message

logger = get_task_logger(__name__)

driver_path = os.path.join(BASE_DIR, "drivers/chromedriver")


class BaseClassOfTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("{0!r} failed: {1!r}".format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        if args[1] is not None:
            asyncio.get_event_loop().run_until_complete(
                success_message(chat_id=args[1], num_of_products=args[0])
            )
        AsyncResult(task_id).revoke()
        return super().on_success(retval, task_id, args, kwargs)


@app.task(bind=True, base=BaseClassOfTask)
def create_product(self, num_of_products: int, chat_id: int):
    try:
        products = get_products(num_of_products=num_of_products)
        save_product(products=products, num_of_products=num_of_products)
        self.on_success_args = [chat_id, num_of_products]
        self.on_success_kwargs = {
            "chat_id": chat_id,
            "num_of_products": num_of_products,
        }
        last_package = get_last_package()
        return last_package
    except Exception as ex:
        logger.exception(ex)
