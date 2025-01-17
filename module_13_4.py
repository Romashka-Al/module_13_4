from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Калории'])
async def set_age(sms):
    await sms.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def det_growth(sms, state):
    await state.update_data(age=float(sms.text))
    await sms.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(sms, state):
    await state.update_data(growth=float(sms.text))
    await sms.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(sms, state):
    await state.update_data(weight=float(sms.text))
    data = await state.get_data()
    await sms.answer(f'Норма калорий: {10 * data["weight"] + 6.25 * data["growth"] - 4.92 * data["age"] + 5}')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
