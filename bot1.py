from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from key import api


bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()
    imt = State()

@dp.message_handler(text = 'Calories') # хэндлер перехватил текст
async def set_age(message):
    await message.answer('Введите свой возраст.') # Реакция на текст
    await UserState.age.set() # установка состояния

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост(см).')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес(кг).')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()  # data это элемент с помощью которого мы получаем наши данные из состояния.
    w = data["weight"]
    g = data["growth"]
    a = data["age"]
    calories = 10 * int(w) + int(6.25) * int(g) - 5 * int(a) + 5
    await message.answer(f'Итого! {calories} ккал в сутки.')
    await state.finish()


# @dp.message_handler(state=UserState.imt)
# async def set_imt(message, state):
#     await state.update_data(imt=message.text)
#     data = await state.get_data()
#     imt_ = data["weight"] / (data["growth"]**2)
#     index_mt = imt_ * 0.01
#     await message.answer(f'Ваш индекс массы тела равен: {index_mt}.')
#     await UserState.imt.set()
#
#     await state.finish()







@dp.message_handler(commands = ['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью! Для начала расчета суточно калорийности '
                         'введи Calories')

@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)