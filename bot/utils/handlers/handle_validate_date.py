from datetime import datetime


def validate_date(date_text):
    try:
        return bool(datetime.strptime(date_text, "%d.%m.%Y"))
    except ValueError:
        return False