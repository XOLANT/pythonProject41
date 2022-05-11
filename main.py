from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = '5259101785:AAHNsgI-yc-NDB8pElbgl8uroQM6wQiWIBU'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

available_clothes_names = ["футболка", "шорты", "худи"]
available_clothes_sizes = ["S", "M", "L"]


class OrderClothes(StatesGroup):
    waiting_for_clothes_name = State()
    waiting_for_clothes_size = State()


@dp.message_handler(commands="clothes", state="*")
async def clothes_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_clothes_names:
        keyboard.add(name)
    await message.answer("Выберите одежду:", reply_markup=keyboard)
    await OrderClothes.waiting_for_clothes_name.set()


@dp.message_handler(state=OrderClothes.waiting_for_clothes_name)
async def clothes_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_clothes_names:
        await message.answer("Пожалуйста, выберите одежду, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_clothes=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_clothes_sizes:
        keyboard.add(size)
    await OrderClothes.next()
    await message.answer("Теперь выберите размер:", reply_markup=keyboard)


@dp.message_handler(state=OrderClothes.waiting_for_clothes_size)
async def clothes_size_chosen(message: types.Message, state: FSMContext):
    if message.text not in available_clothes_sizes:
        await message.answer("Пожалуйста, выберите размер одежды, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {user_data['chosen_clothes']} размером {message.text}.\n")
    await state.finish()


# async def cmd_start(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer(
#         "Выберите, что хотите заказать: ботинки (/boots) или одежу (/clothes).",
#         reply_markup=types.ReplyKeyboardRemove()
#     )


@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(text="отмена", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
