import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

from conf import config
from conf.log_conf import get_logger, LOG_LEVEL
from handler import poem
import time


# файл логов
logger = get_logger('app')


# декоратор-обработчик ошибок
def error_decor(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            logger.log(LOG_LEVEL, f"{ex.__class__}: {ex}")
            print("Something went wrong. Details in the logs.")
    return wrapper


# тестовая функция для отправки времени в чат
@error_decor
def send_time(chat_id):
    bot.send_message(chat_id=chat_id, text=time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# отправка сообщения со стихотворениями в чат
@error_decor
def send_poem(chat_id, n=1):
    msg = poem(n)
    bot.send_message(chat_id=chat_id, text=msg, parse_mode='HTML')


# Создаем экземпляр бота и планировщика
bot = telebot.TeleBot(token=config.BOT_TOKEN)
scheduler = BackgroundScheduler(timezone=config.SCHEDULER_TIMEZONE)


# Функция, обрабатывающая команду /start
@error_decor
@bot.message_handler(commands=["start", "help"])
def start(m, res=False):
    logger.log(LOG_LEVEL, f"New user: {m.chat.id} - {m.chat.username}")

    # создание кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Now")
    item2 = types.KeyboardButton("Daily")
    markup.add(item1)
    markup.add(item2)

    bot.send_message(
        m.chat.id,
        f'Я на связи {chr(config.emoji["hi"])}\n\t\t<b>Now</b> - получение стихотворения сейчас\n\t\t<b>Daily</b> — получение стихотворения каждый день',
        reply_markup=markup,
        parse_mode='HTML'
    )


# Функция, обрабатывающая команду /daily
@error_decor
@bot.message_handler(commands=["daily"])
def daily(m, res=False):
    logger.log(LOG_LEVEL, f"New daily chat: {m.chat.id} - {m.chat.username}")
    scheduler.add_job(
        func=send_poem,
        kwargs={
            'chat_id': m.chat.id
        },
        **config.daily_trigger['every_day']
    )
    bot.send_message(m.chat.id, f"Вы зарагистрировались на ежедневную рассылку {chr(config.emoji['smile'])}")


# Функция, обрабатывающая команду /now
@error_decor
@bot.message_handler(commands=["now"])
def now(message, res=False):
    try:
        send_poem(chat_id=message.chat.id, n=int(message.text))
    except ValueError:
        send_poem(chat_id=message.chat.id)


# Функция, обрабатывающая любой присланный пользователем текст
@error_decor
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Now':
        msg = bot.reply_to(message, "How much?")
        bot.register_next_step_handler(msg, now)
    elif message.text.strip() == 'Daily':
        daily(message)


# Запуск экземпляр бота и планировщика
if __name__ == '__main__':
    scheduler.start()
    bot.polling(none_stop=True, interval=0)
