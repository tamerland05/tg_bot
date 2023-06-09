import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests
import json

TELEGRAM_TOKEN = '6184113642:AAGePg5xdK-tKiM88Bqb9MoF5tMbUP89kWg'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_TOKEN = '7e147060eeebf48a839c58e50667b967'
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def get_weather(lon, lat):
    WEATHER_PARAMS = {
        'appid': WEATHER_TOKEN,
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'lang': 'ru'
    }
    response = json.loads(requests.get(WEATHER_URL, params=WEATHER_PARAMS).text)
    message = f'Weather in {response["name"]}'
    message += f'\nTemperature is {response["main"]["temp"]}'
    message += f'\nTemperature fells like {response["main"]["feels_like"]}'
    message += f'\nPrecipitation {response["cod"]}, {response["weather"][0]["description"]}'
    return message


@bot.message_handler(commands=['start', 'help'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Get weather', request_location=True))
    keyboard.add(KeyboardButton('About'))
    bot.send_message(message.chat.id, 'Hello! I am simple weather bot!', reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon, lat = message.location.longitude, message.location.latitude
    weather = get_weather(lon, lat)
    bot.send_message(message.chat.id, weather)


@bot.message_handler(regexp='About')
def about(message):
    bot.send_message(message.chat.id, 'This bot gives information about weather.')


@bot.message_handler(regexp=r'hello[!.]*')
def hello(message):
    bot.send_message(message.chat.id, 'Hello!')


@bot.message_handler(func=lambda message: 'bye' in message.text)
def hello(message):
    bot.send_message(message.chat.id, 'Goodbye!')


if __name__ == '__main__':
    bot.infinity_polling()