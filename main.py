import asyncio
import logging
import sys
from image_generator import generate, init, generate_with_reference, reference_img

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, BotCommand

is_chat = False

TOKEN = "7997799086:AAEJ5980N9jG2MOWPSSLMyMGmSLGdH16Mq0"
GENERATED_IMAGE_PATH = "result.png"
dp = Dispatcher()

pipe = init()

def generate_image(prompt: str):
    if is_chat:
        img = generate(pipe, prompt)
        img.save(GENERATED_IMAGE_PATH)
    else:
        img = generate_with_reference(pipe, prompt)
        img.save(GENERATED_IMAGE_PATH)

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command("img"))
async def send_photo_handler(message: Message):
    try:
        prompt = message.text.removeprefix("/img ")
        await message.reply("Получен запрос.\nГенерируем изображение...")

        generate_image(prompt)
        await message.answer_photo(photo=FSInputFile(GENERATED_IMAGE_PATH))
    except Exception as e:
        await message.reply(f"Произошла ошибка при генерации изображения: {str(e)}")

@dp.message(Command("chat_with"))
async def chat_with_image_handler(message: Message):
    await message.answer("Принято! Жду последующих указаний с данным персонажем")
    global is_chat
    is_chat = True

@dp.message(Command("off_chat"))
async def chat_with_image_handler(message: Message):
    await message.answer("Принято! Жду последующих указаний с данным персонажем")
    global is_chat
    is_chat = False


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="img", description="Сгенерировать изображение"),
        BotCommand(command="chat_with", description="Чат с персонажем"),
        BotCommand(command="off_chat", description="Чат с персонажем"),
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
