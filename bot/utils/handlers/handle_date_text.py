from datetime import date, timedelta

import settings


def get_selected_date(date_text):
    if date_text == settings.YESTERDAY_BUTTON:
        yesterday = date.today() - timedelta(days=1)
        return yesterday.strftime('%d.%m.%Y')

    elif date_text == settings.TODAY_BUTTON:
        today = date.today()
        return today.strftime('%d.%m.%Y')

    elif date_text == settings.TOMORROW_BUTTON:
        tomorrow = date.today() + timedelta(days=1)
        return tomorrow.strftime('%d.%m.%Y')
