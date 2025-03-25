import requests
from aiogram.types import Message
from config_data.bot_config import BOT_TOKEN, API_KEY

from loader import bot


async def get_pic_url(message: Message) -> str | None:
    """
    Возвращает URL переданного зображения.
    """
    if not message.photo:
        await message.reply("Пожалуйста, отправьте фото.")
        return None
    else:
        photo: dict[str: str] = message.photo[-1]
        print(photo)
        pic_info: dict[str: str] = await bot.get_file(photo.file_id)
        pic_path: str = pic_info.file_path

        # Формируем URL файла
        pic_url: str = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{pic_path}'
        return pic_url


async def get_live_url(message: Message) -> str | None:
    """
    Загружает фото в Cutout.pro и получает url анимированного фото
    """
    photo_url = await get_pic_url(message)
    response = requests.get(
        f'https://www.cutout.pro/api/v1/faceDriven/submitTaskByUrl?imageUrl={photo_url}&templateId=1',
        headers={'APIKEY': API_KEY},
    )

    query: dict[str: int | str] = response.json()
    live_url: str = query.get('url', None)

    if not live_url:
        err_description: str = query.get('message', None)
        await message.reply('Ошибка при обработке фото. Попробуйте дугую фотографию.')
        await message.reply(err_description[0].upper() + err_description[1:])

    return live_url