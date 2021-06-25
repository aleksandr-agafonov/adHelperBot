from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import Actions
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook


token = '1615105002:AAGPdbHvBXLiHCG4hxlB87YQIMt4DFCTQOA'
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


# создаем клавиатуру
show_yandex_add_button = InlineKeyboardButton('Конкуренты в Яндексе', callback_data='c_show_yandex_add')
show_google_add_button = InlineKeyboardButton('Конкуренты в Google', callback_data='c_show_google_add')
screen_yandex_add_button = InlineKeyboardButton('Скрин рекламы в Яндексе', callback_data='c_screen_yandex_add')
screen_google_add_button = InlineKeyboardButton('Скрин рекламы в Google', callback_data='c_screen_google_add')

keyboard = InlineKeyboardMarkup(resize_keyboard=True)
keyboard.add(show_yandex_add_button, show_google_add_button)
keyboard.add(screen_yandex_add_button, screen_google_add_button)


# Приветственный блок
@dp.message_handler(commands=['start'])  # приветствуем и показываем клавиатуру
async def say_hello(message: types.Message):
    await message.answer('Привет! Чего изволите?', reply_markup=keyboard)
# Приветственный блок


# Блок запросов Яндекса
@dp.callback_query_handler(lambda c: c.data == 'c_show_yandex_add')
async def get_yandex_add_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введи поисковой запрос для Yandex')
    await Actions.yandex_add_state.set()


@dp.message_handler(state=Actions.yandex_add_state)
async def get_yandex_add_text(message: types.message, state: FSMContext):
    if message.text != '/start':
        url = 'https://yandex.ru/search/?lr=1&text=' + message.text.replace(' ', '+')
        await message.answer('Вот ваша ссылка на Яндекс, босс: ' + url, reply_markup=keyboard)
        await state.finish()
    else:
        await state.finish()
        await message.answer('Привет! Чего изволите?', reply_markup=keyboard)
# Блок запросов Яндекса


# Блок запросов Google
@dp.callback_query_handler(lambda c: c.data == 'c_show_google_add')  # обрабатываем клик по кнопке и ставим состояние
async def get_google_add_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введи поисковой запрос для Google')
    await Actions.google_add_state.set()


@dp.message_handler(state=Actions.google_add_state)
async def get_google_add_text(message: types.message, state: FSMContext):
    if message.text != '/start':
        url = 'https://www.google.ru/search?q=' + message.text.replace(' ', '+')
        await message.answer('Вот ваша ссылка на Google, босс: ' + url, reply_markup=keyboard)
        await state.finish()
    else:
        await state.finish()
        await message.answer('Привет! Чего изволите?', reply_markup=keyboard)
# Блок запросов Google


# блок скринов Яндекса
@dp.callback_query_handler(lambda c: c.data == 'c_screen_yandex_add')  # обрабатываем клик по кнопке и ставим состояние
async def get_yandex_add_screenshot(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введи поисковой запрос для Yandex для снятия скриншота')
    await Actions.yandex_screen_state.set()


@dp.message_handler(state=Actions.yandex_screen_state)
async def get_yandex_screen(message: types.message, state: FSMContext):
    if message.text != '/start':
        await message.answer('Давай притворимся что это скриншот Яндекса по запросу "' + message.text + '" ?',
                             reply_markup=keyboard)
        await state.finish()
    else:
        await state.finish()
        await message.answer('Привет! Чего изволите?', reply_markup=keyboard)
# блок скринов Яндекса


# блок скринов Goolge
@dp.callback_query_handler(lambda c: c.data == 'c_screen_google_add')  # обрабатываем клик по кнопке и ставим состояние
async def get_google_add_screenshot(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введи поисковой запрос для Google для снятия скриншота')
    await Actions.google_screen_state.set()


@dp.message_handler(state=Actions.google_screen_state)
async def get_google_screen(message: types.message, state: FSMContext):
    if message.text != '/start':
        await message.answer('Давай притворимся что это скриншот Google по запросу "' + message.text + '" ?',
                             reply_markup=keyboard)
        await state.finish()
    else:
        await state.finish()
        await message.answer('Привет! Чего изволите?', reply_markup=keyboard)
# блок скринов Goolge


executor.start_polling(dp)
