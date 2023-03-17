from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext

from loader import dp, db
from keyboards.inline.keyboard import (ikb_complexity, complexity_list,
                                       ikb_themes, themes_list, ikb_new_tasks)
from states.get_records import GetRecords


@dp.message_handler(Command('start'), state='*')
async def start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
    
    await message.answer(
        'Здравствуйте, выберите тему',
        reply_markup=ikb_themes
    )
    await GetRecords.theme.set()


@dp.callback_query_handler(text='Выбрать новые задачи', state='*')
async def select_new_tasks(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()

    await call.message.answer(
        'Выберите тему',
        reply_markup=ikb_themes
    )
    await GetRecords.theme.set()


@dp.callback_query_handler(text=themes_list,
                           state=GetRecords.theme)
async def select_complexity(call: CallbackQuery, state: FSMContext):
    await state.update_data(theme=call.data.replace('"', ''))

    await call.message.answer(
        'Выберите сложность',
        reply_markup=ikb_complexity
    )
    await GetRecords.complexity.set()


@dp.callback_query_handler(text=complexity_list,
                           state=GetRecords.complexity)
async def get_records(call: CallbackQuery, state: FSMContext):
    await state.update_data(complexity=call.data.replace('"', ''))
    data = await state.get_data()

    random_records = db.get_random_records(
        data['complexity'], f'%{data["theme"]}%')

    if len(random_records) == 0:
        await call.message.answer(
            ('Задачи с данной темой и сложностью не найдены.\n'
             'Выберите другие параметры для задач.'),
            reply_markup=ikb_new_tasks
        )

    for i in random_records:
        if i == random_records[-1]:
            await call.message.answer(
                (f'Тема: {i[0].strip()}\n'
                 f'Количество решивших: {i[1].strip()}\n'
                 f'Название + номер: {i[2].strip()}\n'
                 f'Сложность: {i[3].strip()}'),
                reply_markup=ikb_new_tasks
            )
        else:
            await call.message.answer(
                (f'Тема: {i[0].strip()}\n'
                 f'Количество решивших: {i[1].strip()}\n'
                 f'Название + номер: {i[2].strip()}\n'
                 f'Сложность: {i[3].strip()}')
            )

    await state.finish()
