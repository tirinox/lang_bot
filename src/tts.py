import io
import random
from datetime import datetime, timedelta

import gtts


def random_date():
    # random date
    year = random.randint(2010, 2034) if random.uniform(0, 1) > 0.4 else random.randint(1800, 2050)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    return datetime(
        year,
        month,
        day,
    )


def random_date_interval(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)


def generate_date_text_ja(dt, with_year=False):
    fmt = "%Y年%m月%d日" if with_year else "%m月%d日"
    return dt.strftime(fmt)


def tts(text, lang='ja') -> io.BytesIO:
    tts = gtts.gTTS(text, lang=lang)  # request google to get synthesis
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file
