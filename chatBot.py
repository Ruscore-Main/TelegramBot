import telebot
from pickle import load, dump
from time import sleep

# Bot Url 
URL = r''
# Bot token
TOKEN = ''
# Люди, которые имеют доступ к отправке
admins = []

try:
    with open('chats_id.data', 'rb') as f:
        chats = load(f)
except:
    chats = set()

bot = telebot.TeleBot(TOKEN)

#start
@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def get_chat_id(message):
    chats.add(message.chat.id)
    with open('chats_id.data', 'wb') as f:
        dump(chats, f)
    print('чаты:  ', chats)

#add
@bot.message_handler(commands=['add'])
@bot.edited_message_handler(commands=['add'])
def add_chat(message):
    #Бот обязательно должен присутсвовать в добавляемом чате
    bot.send_message(message.chat.id, 'Бот обязательно должен присутсвовать в добавляемом чате')
    new_chat = int(message.text[4:])
    bot.send_message(message.chat.id, f'{new_chat} был добавлен в рассылку')
    chats.add(new_chat)
    with open('chats_id.data', 'wb') as f:
        dump(chats, f)

#delete
@bot.message_handler(commands=['delete'])
@bot.edited_message_handler(commands=['delete'])
def delete_chat(message):
    chats.discard(int(message.text.split()[1]))
    with open('chats_id.data', 'wb') as f:
        dump(chats, f)

def sender(message, chats):
    i = 0
    for id in chats:
            i += 1
            bot.send_message(id, message.text[5:])
            bot.send_message(message.chat.id, f'Отправлено {i} чату из {len(chats)}; \nid чата:       {id}')
            print(chats)
    sleep(15)
    sender(message, chats)

# Send
@bot.message_handler(commands=['send'])
@bot.edited_message_handler(commands=['send'])
def send_message(message):
    if message.chat.id in admins:
        sender(message, chats)

bot.polling(timeout=30)