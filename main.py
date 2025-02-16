import telebot
from telebot import types

from config_data.bot_config import BOT_TOKEN
from handlers import recipe_names, reduce_names, set_keyboard

# Инициализация бота
bot: telebot = telebot.TeleBot(token=BOT_TOKEN, parse_mode='html')
data_storage: list = []


@bot.message_handler(commands=['start'])
def start_bot(message: types.Message) -> None:
    bot.send_message(message.chat.id, text='Привет, введите список ваших продуктов и я найду подходящий рецепт')


@bot.message_handler(commands=['help'])
def bot_help(message: types.Message) -> None:
    info: str = '''
    <b>Команда start</b> - Выводит краткую информацию о боте
    <b>Команда help</b> - Выводит это сообщение
    <b>Другие сообщения</b> - Воспринимаются как список продуктов для поиска рецептов

    Рекомендации по запросам: Пишите в запросах простые названия
    продуктов например: картошка, морковка, консервы из лосося.
    Если бот не находит рецепт, сократите запрос.
    Приятного использования!'''

    bot.send_message(message.chat.id, text=info)


@bot.message_handler(content_types=['text'])
def request_messages(message: types.Message) -> None:

    if message.text != '':

        full_recipes: list[dict] = recipe_names(message.text)
        short_recipes: list[dict] = reduce_names(full_recipes)
        markup: types.InlineKeyboardMarkup = set_keyboard(short_recipes)

        if full_recipes[0]['name'] == 'Error':
            bot.send_message(message.chat.id, text='К сожалению у меня нет подходящих рецептов')
        else:
            full_len: int = len(full_recipes)
            short_len: int = len(short_recipes)

            global data_storage
            data_storage = short_recipes

            if full_len == short_len:
                msg_text: str = f'Найдено {short_len} рецептов:'
                bot.send_message(message.chat.id, text=msg_text, reply_markup=markup)
            else:
                msg_text: str = f'Найдено {full_len} рецептов. Вот {short_len} случайных из {full_len}'
                bot.send_message(message.chat.id, text=msg_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_inline(callback: types.CallbackQuery) -> None:
    # Обработка нажатий на inline кнопки
    if callback.message:
        for index in range(12):
            if int(callback.data) == index:

                global data_storage
                name: str = data_storage[index]['name']
                cont: str = data_storage[index]['content']

                msg_text: str = f'<b>{name}</b>\n\n{cont}'
                bot.send_message(callback.message.chat.id, text=msg_text)

                break

    bot.answer_callback_query(callback_query_id=callback.id)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)


bot.polling(none_stop=True)