from aiogram import types


def start_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Перенести стиль", callback_data="button_style"),
        types.InlineKeyboardButton(text="\U0001F40E Лошадь в зебру \U0001F993", callback_data="horse2zebra"),
        types.InlineKeyboardButton(text="\U0001F993 Зебру в лошадь \U0001F40E", callback_data="zebra2horse"),
        types.InlineKeyboardButton(text="\U0001F4A5 Примеры", callback_data="examples"),
        types.InlineKeyboardButton(text="\U0001F4C3 GitHub", url='https://github.com/Belousov-Aleksandr/Telegram_NST_Bot')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def style_images():
    buttons = [
        types.InlineKeyboardButton(text="Выбрать фотографию для стиля", callback_data="style_images"),
        types.InlineKeyboardButton(text="Главное меню", callback_data="menu")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard


def select_style():
    buttons = [
        types.InlineKeyboardButton(text="1️⃣", callback_data="style_1"),
        types.InlineKeyboardButton(text="2️⃣", callback_data="style_2"),
        types.InlineKeyboardButton(text="3️⃣", callback_data="style_3"),
        types.InlineKeyboardButton(text="4️⃣", callback_data="style_4"),
        types.InlineKeyboardButton(text="5️⃣", callback_data="style_5"),
        types.InlineKeyboardButton(text="6️⃣", callback_data="style_6"),
        types.InlineKeyboardButton(text="Главное меню", callback_data="menu")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2).add(*buttons)

    return keyboard


def algo_keyboard():
    buttons = [
        types.InlineKeyboardButton(text="Перенести стиль", callback_data="button_style"),
        types.InlineKeyboardButton(text="\U0001F40E Лошадь в зебру \U0001F993", callback_data="horse2zebra"),
        types.InlineKeyboardButton(text="\U0001F993 Зебру в лошадь \U0001F40E", callback_data="zebra2horse"),
        types.InlineKeyboardButton(text="Главное меню", callback_data="menu")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1).add(*buttons)

    return keyboard


start_message = ("Я - *Neural-Style-Transfer* бот  \U0001F916\n\nИ я умею создавать новые фотографии с помощью нейронных сетей.\n\n"
                 "\U00002705 Ты можешь отправить мне 2 фотографии: с первой фотографии я заберу стиль и "
                 "перенесу его на твою вторую фотографию.\n\n"
                 "\U00002705 Если у тебя есть какая-нибудь фотография лошади \U0001F40E, то я могу переделать её в зебру \U0001F993\n\n"
                 "\U00002705 Или наоборот, если есть фотография зебры \U0001F993, то её можно превратить в лошадь \U0001F40E\n\n"
                 "Я подготовил для тебя примеры, нажимай на кнопку и взгляни \U0001F447\n\n"
                 "Если станет интересно, как это все работает, "
                 "то можешь ознакомиться со страницей проекта на GitHub \U0001F914")

menu_message = ("Напомню, что я умею делать:\n\n"
                "\U00002705 Переносить стиль одной фотографии на другую\n\n"
                "\U00002705 Превратить лошадь \U0001F40E в зебру \U0001F993\n\n"
                "\U00002705 Превратить \U0001F993 зебру в лошадь \U0001F40E\n\n"
                "Если я неправильно работаю, то попробуй перезапустить меня командой  */start*")
