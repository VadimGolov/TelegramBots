import asyncio
from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f

from loader import dp, bot, logger
from extras import get_live_url


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer('Здравствуйте! Вас приветствует оживляющий бот')
    await message.answer('Для вывода справки введите /help или help')


@dp.message(or_f(Command('help'), F.text.casefold().func(lambda text: text == 'help')))
async def help_handler(message: Message) -> None:
    await message.answer('Отправьте мне любой портрет, и я его оживлю!')


@dp.message(F.photo)
async def get_live_photo(message: Message) -> None:
    """
    Получает URL живого фото и отправляет видео в чат
    """
    video_url: str = await get_live_url(message)
    if video_url:
        await message.answer_video(video=video_url, caption='Ваше «живое» фото')


@logger.catch
async def start_bot():
    logger.info('Бот запущен')
    await dp.start_polling(bot)


async def stop_bot() -> None:
    await bot.session.close()
    logger.info('Бот остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())