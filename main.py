import os
import asyncio
import aiohttp

from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f

from loader import dp, bot, logger, router
from config_data.bot_config import BOT_TOKEN


# from extras import get_live_url
# from keyboards import work_keyboard


@router.message(or_f(CommandStart(), F.text.casefold().func(lambda text: text == 'start')))
async def start_handler(message: Message) -> None:
    await message.answer('Здравствуйте! Я тест-бот')


@router.message(or_f(Command('help'), F.text.casefold().func(lambda text: text == 'help')))
async def help_handler(message: Message) -> None:
    await message.answer('Отправьте мне одну или несколько фото и я отправлю вам их url в телеграм')


media_groups = {}

download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

convertible_files: list[str] = []


def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1].lower()


def is_convertible(file_path: str) -> bool:
    return get_file_extension(file_path) in ['.heic', '.webp']


async def download_file(url: str, save_path: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await resp.read())


async def handle_file(robot: Bot, file_id: str) -> None:
    file = await robot.get_file(file_id)
    # ext: str = get_file_extension(file.file_path)

    if is_convertible(file.file_path):
        url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}'
        filename = os.path.basename(file.file_path)
        save_path = os.path.join(download_dir, filename)

        await download_file(url, save_path)
        convertible_files.append(save_path)
        print(f'[CONVERT] Saved: {save_path}')
    else:
        print(f'[SKIP] {file.file_path} — no need to convert')


@router.message(F.media_group_id, F.photo)
async def handle_media_group_photo(message: Message, robot: Bot) -> None:
    group_id = message.media_group_id

    if group_id not in media_groups:
        media_groups[group_id] = []

    media_groups[group_id].append(message)

    await asyncio.sleep(1)

    if len(media_groups[group_id]) >= 1:
        for msg in media_groups[group_id]:
            file_id = msg.photo[-1].file_id
            await handle_file(robot, file_id)

        del media_groups[group_id]


@router.message(F.photo)
async def handle_single_photo(message: Message, robot: Bot) -> None:
    file_id = message.photo[-1].file_id
    await handle_file(robot, file_id)


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