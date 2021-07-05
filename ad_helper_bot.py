from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Actions
import requests
from bs4 import BeautifulSoup
import json
from parse_auto_ru import parse_auto_ru


token = '1615105002:AAGPdbHvBXLiHCG4hxlB87YQIMt4DFCTQOA'
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


# создаем клавиатуру
show_yandex_add_button = InlineKeyboardButton('Конкуренты в Яндексе', callback_data='c_show_yandex_add')
screen_yandex_add_button = InlineKeyboardButton('Скрин выдачи в Яндексе', callback_data='c_screen_yandex_add')
screen_google_add_button = InlineKeyboardButton('Скрин выдачи в Google', callback_data='c_screen_google_add')
parse_auto_ru_button = InlineKeyboardButton('Спарсить Auto.ru', callback_data='c_parse_auto_ru')

keyboard = InlineKeyboardMarkup(resize_keyboard=True)
keyboard.add(show_yandex_add_button)
keyboard.add(screen_yandex_add_button)
keyboard.add(screen_google_add_button)
keyboard.add(parse_auto_ru_button)


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
        url = 'https://www.yandex.ru/search/ads?text='
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        search_query = message.text.replace(' ', '+')

        req = requests.get(url + search_query + '&lr=1', headers=headers, stream=True)
        soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')

        try:
            for ad in soup.find_all('li', attrs={'class': 'serp-item'})[:3]:
                head = ad.find('div', attrs={'class': 'OrganicTitle-LinkText'}).text  # заголовок
                ad_text = ad.find('div', attrs={'class': 'Typo_text_m'}).text  # тексты
                domain = ad.find('div', attrs={'class': 'Organic-Path'}).find('b').text  # видимый домен

                await message.answer(head + '\n\n' + ad_text + '\n\n' + domain)

        except:
            await message.answer('По данному запросу нет рекламных объявлений')

        finally:
            await state.finish()
            await message.answer('Чего изволите?', reply_markup=keyboard)

    else:
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)
# Блок запросов Яндекса


# блок скринов Яндекса
@dp.callback_query_handler(lambda c: c.data == 'c_screen_yandex_add')  # обрабатываем клик по кнопке и ставим состояние
async def get_yandex_add_screenshot(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введи поисковой запрос для Yandex для снятия скриншота')
    await Actions.yandex_screen_state.set()


@dp.message_handler(state=Actions.yandex_screen_state)
async def get_yandex_screen(message: types.message, state: FSMContext):
    if message.text != '/start':
        search_query = message.text.replace(' ', '+')
        yandex_ad_url = 'https://www.yandex.ru/search/ads?text=' + search_query + '&lr=1'

        url = ' https://api.topvisor.com/v2/json/get/webScreens_2'
        api_key = '43012ad5e875832a46fe'

        headers = {
            'User-Id': '291326',
            'Authorization': 'bearer ' + api_key,
            'Content-type': 'application/json'
        }

        params = {
            'url': yandex_ad_url,
            'w': 1000,
            'h': 2350,
        }

        body = json.dumps(params)
        req = requests.post(url, body, headers=headers)

        with open('myfile.png', 'wb') as f:
            f.write(req.content)

        screen = open('myfile.png', 'rb')
        await message.answer_document(screen)
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)
    else:
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)
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
        search_query = message.text.replace(' ', '+')
        google_ad_url = 'https://www.google.ru/search?q=' + search_query

        url = ' https://api.topvisor.com/v2/json/get/webScreens_2'
        api_key = '43012ad5e875832a46fe'

        headers = {
            'User-Id': '291326',
            'Authorization': 'bearer ' + api_key,
            'Content-type': 'application/json'
        }

        params = {
            'url': google_ad_url,
            'w': 1000,
            'h': 2350,
        }

        body = json.dumps(params)
        req = requests.post(url, body, headers=headers)

        with open('myfile.png', 'wb') as f:
            f.write(req.content)

        screen = open('myfile.png', 'rb')
        await message.answer_document(screen)
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)
    else:
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)
# блок скринов Goolge


# запрос IP адресс - скрытый функционал
@dp.message_handler(commands=['ip'])
async def get_my_ip(callback_query: types.CallbackQuery):
    req = requests.get('https://api.myip.com/')
    await bot.send_message(callback_query.from_user.id, req.json()['ip'])


# Парсинг Авто.ру
@dp.callback_query_handler(lambda c: c.data == 'c_parse_auto_ru')
async def get_yandex_add_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите марку')
    await Actions.parse_auto_ru_state_get_mark.set()


@dp.message_handler(state=Actions.parse_auto_ru_state_get_mark)
async def get_auto_ru_data(message: types.message, state: FSMContext):
    await message.answer('Введите модель')
    global mark
    mark = message.text
    await Actions.parse_auto_ru_state_get_model.set()


@dp.message_handler(state=Actions.parse_auto_ru_state_get_model)
async def get_model_and_parse_auto_ru(message: types.message, state: FSMContext):
    global model
    model = message.text

    if len(parse_auto_ru(mark, model)) != 0:
        try:
            for i in parse_auto_ru(mark, model):
                await message.answer(
                    i['mark'] + ' ' +
                    i['model'] + '\n' +
                    'Цена: ' + i['price'] + '\n' +
                    'Год выпуска: ' + i['year'] + '\n' +
                    'Комплектация: ' + i['complectation'] + '\n' +
                    'Дилер: ' + i['dealer'] + '\n' +
                    'Регион: ' + i['region'] + '\n' +
                    'Максимальная выгода: ' + i['discount']
                )

            await state.finish()
            await message.answer('Чего изволите?', reply_markup=keyboard)

        except:
            await message.answer(parse_auto_ru(mark, model))

    else:
        await message.answer('По вашему запросу ничего не найдено')
        await state.finish()
        await message.answer('Чего изволите?', reply_markup=keyboard)


executor.start_polling(dp)
