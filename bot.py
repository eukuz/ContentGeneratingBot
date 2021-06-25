import telebot
import requests
import re
import urllib.request
from PIL import Image
from PyDictionary import PyDictionary
from strings import connections
dictionary=PyDictionary()
bot = telebot.TeleBot(connections["key"])

flag = True


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = message.text.lower()
    if msg == 'hello':
        bot.send_message(message.from_user.id, 'hello')
    elif msg == 'bye':
        bot.send_message(message.from_user.id, 'goodbye')
    elif msg == 'die':
        bot.stop_bot()
    else:
        res = requests.get('https://unsplash.com/s/photos/'+msg)
        result = re.search(r'https:\/\/images.unsplash.com\/photo[^"]+', res.text)
        print(dictionary.meaning(msg)['Noun'])

        urllib.request.urlretrieve(result[0], "a.jpg")

        bg = Image.open('b.png')
        bg_w, bg_h = bg.size
        img = Image.open('a.jpg')

        basewidth = 1500

        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)

        offset = ((bg_w-basewidth) // 2, (bg_h-hsize) // 2)
        bg.paste(img, offset)
        bot.send_photo(-1001183439671,bg,dictionary.meaning(msg)['Noun'])


bot.polling(none_stop=flag)
