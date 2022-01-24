import logging
from aiohttp import web
from aiogram import Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage, get_new_configured_app
import keyboards as kb
import glob
import image_processing
import threading
import asyncio
from os import environ
from aiogram.utils.executor import start_webhook
import warnings
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")

API_TOKEN = environ.get('API_TOKEN')
CONNECTION_TYPE = environ.get('CONNECTION_TYPE')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST')
WEBHOOK_PORT = int(environ.get("WEBHOOK_PORT"))
WEBHOOK_URL_PATH = environ.get('WEBHOOK_URL_PATH')
WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
loop = asyncio.get_event_loop()
bot = Bot(API_TOKEN, loop=loop)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_photos = {}

with open("images/styles/description.txt") as f:
    styles_text = f.read()
style_images = sorted([file for file in glob.glob('images/styles/*.jpg')])


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.style_img = 0
        self.type_algo = None

    def restart(self, algo=None):
        self.style_img = 0
        self.type_algo = algo
        
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    db_photos[message.from_user.id] = User(message.from_user.id)
    logging.info(f"New User! Current number of users in dict: {len(db_photos)}")

    await message.answer(f"Привет, *{message.from_user.first_name}*! \U0001F44B\n\n {kb.start_message}", parse_mode='Markdown', reply_markup=kb.start_keyboard())
    #await message.answer(kb.start_message, reply_markup=kb.start_keyboard())

@dp.callback_query_handler(text="menu")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart()

    await call.message.answer(kb.menu_message, parse_mode='Markdown', reply_markup=kb.start_keyboard())
    await call.answer()

@dp.callback_query_handler(text="button_style")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart('nst')

    await call.message.answer("Мне нужно 2 фотографии. Давай начнем с фотографии стиля, отправь мне ее.\n"
                              "Если не знаешь какую, то я могу помочь. "
                              "Для просмотра вариантов нажми на кнопку ниже \U0001F447",
                              reply_markup=kb.style_images())
    await call.answer()

@dp.callback_query_handler(text="style_images")
async def transfer_style(call: types.CallbackQuery):
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    for i, image in enumerate(style_images):
        if i == 0:
            media.attach_photo(types.InputFile(image), f"У меня есть такие картины:\n\n{styles_text}")
        else:
            media.attach_photo(types.InputFile(image))
    await call.message.answer_media_group(media)
    await call.message.answer("Если что-то приглянулось, то выбери стиль кнопкой, если нет - отправляй собственную"
                              " фотографию для стиля", reply_markup=kb.select_style())
    await call.answer()


@dp.callback_query_handler(lambda call: call.data.startswith('style_'))
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.style_img = style_images[int(call.data[-1]) - 1]
    await call.message.answer(f"Я запомнил, что ты выбрал {int(call.data[-1])} стиль" +
                              "\nТеперь отправь мне фотографию, на которую перенести стиль")
    await call.answer()


@dp.callback_query_handler(text="horse2zebra")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart('horse2zebra')
    await call.message.answer("А теперь пришли мне фотографию ЛОШАДИ \U0001F40E")
    await call.answer()


@dp.callback_query_handler(text="zebra2horse")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart('zebra2horse')
    await call.message.answer("А теперь пришли мне фотографию ЗЕБРЫ \U0001F993")
    await call.answer()

@dp.callback_query_handler(text="examples")
async def transfer_style(call: types.CallbackQuery):
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()

    media.attach_photo(types.InputFile("images/examples/nst.jpg"), "Перенос стиля")
    media.attach_photo(types.InputFile("images/examples/horse2zebra.jpg"), "Лошадь стала зеброй")
    media.attach_photo(types.InputFile("images/examples/zebra2horse.jpg"), "Зебра стала лошадью")
    await call.message.answer_media_group(media)

    await call.message.answer("Выберите вариант алгоритма  \U0001F447\n",
                              reply_markup=kb.algo_keyboard())
    await call.answer()


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    image = message.photo[-1]
    file_info = await bot.get_file(image.file_id)
    photo = await bot.download_file(file_info.file_path)

    user = db_photos[message.from_user.id]
    if user.type_algo == 'horse2zebra':
        await message.answer("Подожди минутку и будет готово!")
        logging.info(f"Start CycleGAN horse2zebra")

        threading.Thread(
            target=lambda mess, img, type_algo:
            asyncio.run(image_processing.cycle_gan(mess, img, type_algo)),
            args=(message, photo, user.type_algo)).start()

    elif user.type_algo == 'zebra2horse':
        await message.answer("Подожди минутку и будет готово!")
        logging.info(f"Start CycleGAN zebra2horse")

        threading.Thread(
            target=lambda mess, img, type_algo:
            asyncio.run(image_processing.cycle_gan(mess, img, type_algo)),
            args=(message, photo, user.type_algo)).start()

    elif user.type_algo == 'nst':
        if user.style_img == 0:
            user.style_img = photo
            await message.answer("Теперь отправь фотографию, на которую перенести стиль")
        else: 
            await message.answer("Подожди не более 5 минут, и я отправлю результат  \n\U0001F40C   \U0001F40C   \U0001F40C")
            logging.info(f"Start Style Transfer")

            threading.Thread(
                target=lambda mess, style_img, content_img:
                asyncio.run(image_processing.style_transfer(mess, style_img, content_img)),
                args=(message, user.style_img, photo)).start()
    else:
        await message.answer("Прежде чем отправлять мне фотографии скажи мне какой алгоритм использовать \U0001F447",
                             reply_markup=kb.algo_keyboard())

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(kb.menu_message, reply_markup=kb.start_keyboard())

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.warning("Hello!")
    
async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")

if __name__ == '__main__':

    webhook_settings = False if CONNECTION_TYPE == 'POLLING' else True
    if webhook_settings:
        WEBAPP_PORT = int(environ.get("WEBAPP_PORT"))
        WEBAPP_HOST = environ.get("WEBAPP_HOST")
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_URL_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(dp, skip_updates=True)
