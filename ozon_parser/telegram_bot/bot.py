import asyncio
import os
import logging
from requests import api
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from django.urls import reverse
from parser.utils import (
    get_product_list_from_last_package,
    get_product_by_id,
    get_status,
)


load_dotenv()
token = os.getenv("BOT_TOKEN")

if not token:
    exit("Error: no token provided")

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class ParserStates(StatesGroup):
    id = State()
    quantity = State()
    common = State()


@dp.message_handler(commands="start", state="*")
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data.clear()
    await ParserStates.common.set()
    await message.answer(
        "/start - перейти к началу\n\
/parsing - Начать парсинг товаров\n\
/product_list - список товаров последнего парсинга\n\
/product - найти товар по ID"
    )


@dp.message_handler(commands="parsing", state="*")
async def parsing(message: types.Message):
    await ParserStates.quantity.set()
    await message.answer("Введите количество продуктов(от 0 до 50)")


@dp.message_handler(commands="product_list", state="*")
async def product_list(message: types.Message, state: FSMContext):
    n = 1
    text = str()
    products = await get_product_list_from_last_package()
    for product in products:
        text += f"\n<b>{n}.</b> {product.name}\nСсылка на продукт: {product.link}"
        n += 1
        if len(text) >= 3000:
            await message.answer(text)
            text = str()
    if text:
        await message.answer(text)
    await start(message=message, state=state)


@dp.message_handler(commands="product", state="*")
async def get_product_id(message: types.Message):
    await ParserStates.id.set()
    await message.answer("Введите ID товара")


@dp.message_handler(state=ParserStates.id)
async def get_product(message: types.Message, state: FSMContext):
    try:
        product = await get_product_by_id(int(message.text))
    except:
        product = None
    if product == None:
        await message.answer(f"Такого товара не существует")
        await get_product_id(message=message)
    else:
        await message.answer(
            f"Название товара: {product.name}\nСсылка на товар: {product.link}"
        )
        await ParserStates.common.set()
        await start(message=message, state=state)


@dp.message_handler(state=ParserStates.quantity)
async def parsing_products(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            status = await get_status(data["task_id"])
        except:
            status = None

        if status == "PENDING":
            await message.answer("Дождитесь завершения парсинга")
            return

    try:
        int(message.text)
    except:
        await message.answer("Введите количество продуктов(от 0 до 50)")

    if int(message.text) in range(0, 50 + 1):
        response = api.post(
            url="http://127.0.0.1:8000" + reverse("products"),
            data={"num_of_products": int(message.text), "chat_id": message.chat.id},
        )

        async with state.proxy() as data:
            data["task_id"] = response.json()["task_id"]

        await message.answer(f"Парсинг...\nПродуктов: {message.text}")
    else:
        await message.answer("Введите количество продуктов(от 0 до 50)")


async def success_message(chat_id, num_of_products: int):
    await bot.send_message(
        chat_id=chat_id,
        text=f"Задача на парсинг товаров с сайта Ozon завершена.\nСохранено: {num_of_products} товаров.",
    )
    await bot.send_message(
        chat_id=chat_id,
        text="/start - начало работы с ботом\n\
/product_list - список товаров последнего парсинга\n\
/product - найти товар по ID\n\
/help - вызов этого сообщения",
    )


def run_bot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        executor.start_polling(dp, skip_updates=True)

    except Exception as e:
        print("Error!", e)
