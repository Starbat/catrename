# Here functions can be defined, which can be used in the defined categories
# for transformations and postprocessing.

import datetime

_MONTHS = {
    'ENG': ['january', 'february', 'march', 'april', 'may', 'june', 'july',
        'august', 'september', 'october', 'november', 'december'],
    'GER': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
        'August', 'September', 'Oktober', 'November', 'Dezember']
    }

def encode_month(month_name, lang='ENG'):
    encoding = {name.lower(): f'{num+1:02d}'
                for num, name in enumerate(_MONTHS[lang])}
    return encoding[month_name.lower()]

def decode_month(month_num, lang='ENG'):
    return _MONTHS[lang][month_num-1]

def replace_whitespace_by_underscore(string):
    return string.replace(' ', '_')

def time_of_day(time_string):
    time = datetime.datetime.strptime(time_string, '%H%M%S')
    if time.hour >= 6 and time.hour < 12:
        return 'morning'
    elif time.hour >= 12 and time.hour < 18:
        return 'afternoon'
    elif time.hour >= 18 and time.hour < 24:
        return 'evening'
    else:
        return 'night'
