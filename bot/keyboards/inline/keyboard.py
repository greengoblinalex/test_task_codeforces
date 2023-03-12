from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .constants import COUNT_COMPLEXITY_KB_BUTTONS_IN_LINE, COUNT_THEMES_KB_BUTTONS_IN_LINE
from loader import db

ikb_new_tasks = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Выбрать новые задачи',
                                 callback_data='Выбрать новые задачи')
        ]
    ]
)

complexity_list = []
complexity_kb = []
list_kb = []
j = 0
all_complexity = db.get_all_complexity()
for i in all_complexity:
    j += 1

    complexity_list.append(f'"{i}"')
    list_kb.append(
        InlineKeyboardButton(text=i,
                             callback_data=f'"{i}"')
    )

    if j == COUNT_COMPLEXITY_KB_BUTTONS_IN_LINE:
        complexity_kb.append(
            list_kb.copy()
        )
        list_kb.clear()
        j = 0

    if i == all_complexity[-1]:
        complexity_kb.append(
            list_kb.copy()
        )
        complexity_kb.append(
            ikb_new_tasks.inline_keyboard[0]
        )

themes_list = []
themes_kb = []
list_kb = []
j = 0
all_themes = db.get_all_themes()
for i in all_themes:
    j += 1

    themes_list.append(f'"{i}"')
    list_kb.append(
        InlineKeyboardButton(text=i,
                             callback_data=f'"{i}"')
    )

    if j == COUNT_THEMES_KB_BUTTONS_IN_LINE:
        themes_kb.append(
            list_kb.copy()
        )
        list_kb.clear()
        j = 0

    if i == all_themes[-1]:
        themes_kb.append(
            list_kb.copy()
        )
        themes_kb.append(
            ikb_new_tasks.inline_keyboard[0]
        )

ikb_complexity = InlineKeyboardMarkup(
    row_width=COUNT_COMPLEXITY_KB_BUTTONS_IN_LINE,
    inline_keyboard=complexity_kb
)

ikb_themes = InlineKeyboardMarkup(
    row_width=COUNT_THEMES_KB_BUTTONS_IN_LINE,
    inline_keyboard=themes_kb
)
