BOT_TOKEN = '1768420201:AAEscjhFU9a-4a_oeDcBCQ4rrfgD65j8XoE'
SCHEDULER_TIMEZONE = 'Europe/Moscow'

daily_trigger = {
    'every_second': {
        'trigger': 'cron',
        'second': '*/3',
    },
    'every_day': {
        'trigger': 'cron',
        'day': '*',
        'hour': 13,
        'minute': 51
    }
}

emoji = {
    'hi': 128075,
    'smile': 128522,
}
