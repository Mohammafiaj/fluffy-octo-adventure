import telebot
from telebot.types import Message
from bs4 import BeautifulSoup
import requests

TOKEN = "5627265077:AAHMYipnOoOZE0NLfivVLJ7yVJoI08lskEw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, "سلام! برای استخراج اعضای یک گروه، لطفا لینک گروه را ارسال کنید.")

@bot.message_handler(func=lambda message: True)
def extract_members(message: Message):
    if message.text == 'استخراج اعضا':
        chat_id = message.chat.id
        bot.send_message(chat_id, "در حال جستجوی اعضای گروه...")
        try:
            group_chat_link = message.reply_to_message.text
            group_page = requests.get(group_chat_link)
            soup = BeautifulSoup(group_page.content, 'html.parser')
            members = []
            for link in soup.find_all('a'):
                if '/joinchat/' in str(link):
                    members.append(str(link.get('href')).split('/')[-1])
            file_name = f'{chat_id}_members.txt'
            with open(file_name, 'w') as file:
                for member in members:
                    file.write("%sn" % member)
            with open(file_name, 'r') as file:
                bot.send_document(chat_id, file.read(), caption="لیست اعضای گروه:")
        except:
            bot.send_message(chat_id, "متاسفانه نتوانستیم اعضای گروه را استخراج کنیم، لطفا مجددا امتحان کنید.")

bot.polling()