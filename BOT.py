import telebot
import parser_weather as p
import emoji as em
from time import sleep
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    greetings = em.emojize('Доброго времени суток! Рады Вас приветствовать!')
    bot.send_photo(message.chat.id, photo='https://clck.ru/R4sQ7', caption=greetings),
    sleep(3)
    bot.send_message(message.chat.id, text=(em.emojize(':globe_with_meridians: Введите название столицы:')))


@bot.message_handler(commands=['restart'])
def restart(message):
    bot.send_message(message.chat.id, text=(em.emojize(':globe_with_meridians: Введите столицу:')))


@bot.message_handler(content_types=['text'])
def get_capital(message):
    global capital
    capital = message.text.lower()
    if capital in config.capitals:
        global page_soup
        page_url = 'https://sinoptik.ua/погода-{0}'.format(capital)
        page_soup = p.get_page_soup(page_url)
        get_weather(message)


page_soup, capital = '', ''


def get_weather(message):
    keyboard_temp = telebot.types.InlineKeyboardMarkup()
    key_ten_days = telebot.types.InlineKeyboardButton(text=em.emojize(':crystal_ball: На неделю'),
                                                      callback_data='7 дней')
    key_today = telebot.types.InlineKeyboardButton(text=em.emojize(':crystal_ball: На cегодня'),
                                                   callback_data='Сегодня')
    key_tomorrow = telebot.types.InlineKeyboardButton(text=em.emojize(':crystal_ball: На завтра'),
                                                      callback_data='Завтра')
    key_sunrise_set = telebot.types.InlineKeyboardButton(text=em.emojize(':sun: Время восхода и заката'),
                                                         callback_data='Время восхода и заката')
    keyboard_temp.add(key_ten_days, key_today, key_tomorrow, key_sunrise_set)
    question = em.emojize('Что вас интересует?')
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard_temp)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    seven_days = p.get_weather_7_days(page_soup)
    if call.data == '7 дней':
        bot.send_message(call.message.chat.id, text="\n".join(seven_days))
    elif call.data == "Сегодня":
        weather = p.get_weather_for_today(page_soup)
        bot.send_message(call.message.chat.id, text=f'Сегодня в городе {capital.capitalize()}: {weather}')
    elif call.data == 'Завтра':
        weather = p.get_weather_for_tomorrow(page_soup)
        bot.send_message(call.message.chat.id, text=f'Погода в городе {capital.capitalize()} на завтра: {weather}')
    elif call.data == 'Время восхода и заката':
        bot.send_message(call.message.chat.id, p.get_sunrise_set(page_soup))


bot.polling()
