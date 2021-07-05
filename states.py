from aiogram.dispatcher.filters.state import StatesGroup, State

class Actions(StatesGroup):
    yandex_add_state = State()
    google_add_state = State()
    yandex_screen_state = State()
    google_screen_state = State()
    parse_auto_ru_state_get_mark = State()
    parse_auto_ru_state_get_model = State()