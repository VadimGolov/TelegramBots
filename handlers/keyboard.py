from telebot import types


def set_keyboard(short_cook: list[dict]) -> types.InlineKeyboardMarkup:

    markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

    for index, item in enumerate(short_cook):
        one_button: types.InlineKeyboardButton = types.InlineKeyboardButton(item['name'], callback_data=str(index))
        markup.add(one_button)

    return markup