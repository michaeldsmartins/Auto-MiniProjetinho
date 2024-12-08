import time
import random
import json,requests
import telebot
from datetime import datetime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import bd


api_key = '6209018754:AAFPJUg-rVTMA8y3e2n7yLT5TIuFEXFiIjo' # Neste campo tenho que colocar a API do BotFather!
chat_id = '-1001965428039' # Neste campo tenho que colocar o ID do meu canal!

bot = telebot.TeleBot(token=api_key)

def ALERT_GALE1():
    h = datetime.now().hour
    m = datetime.now().minute+1
    s = datetime.now().second
    if h <= 9:
        h =  f'0{h}'
    if m <= 9:
        m = f'0{m}'
    if s <= 9:
        s = f'0{s}'
    message_id = bot.send_message(chat_id=chat_id, text=f'''NOVA ENTRADA EM {h}:{m}:{s} GERANDO ENTRADA...''' ).message_id
    bd.message_ids1 = message_id
    bd.mensage_delete1 = True
    return

def DELETE_GALE1():
    if bd.mensage_delete1 == True:
        bot.delete_message(chat_id=chat_id, message_id=bd.message_ids1)
        bd.mensage_delete1 = False

while True:
    h = datetime.now().hour
    m = datetime.now().minute+2
    s = datetime.now().second
    if h <= 9:
        h =  f'0{h}'
    if m <= 9:
        m = f'0{m}'
    if s <= 9:
        s = f'0{s}'
    print(f'{h}:{m}:{s}')
    cores = ['💎','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','💎','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','⬛','💎']

    for i in range (25):
        sample = random.sample(cores, k=25)
        print(sample[0], sample[1], sample[2], sample[3], sample[4], sample[5], sample[6], sample[7], sample[8],sample[9], sample[10], sample[11], sample[12], sample[13], sample[14], sample[15], sample[16], sample[17], sample[18], sample[19], sample[20], sample[21], sample[22], sample[23], sample[24])

        def button_link():

            markup = InlineKeyboardMarkup()

            markup.row_width = 2

            return markup

    dados = bot.send_message(chat_id=chat_id, text=(f'''
💣  Bombas : 3
⏰  Validade do sinal 2 minutos
     
     , Nº de entradas 3
{random.choice(sample[0])}{random.choice(sample[1])}{random.choice(sample[2])}{random.choice(sample[3])}{random.choice(sample[4])}
{random.choice(sample[5])}{random.choice(sample[6])}{random.choice(sample[7])}{random.choice(sample[8])}{random.choice(sample[9])}
{random.choice(sample[10])}{random.choice(sample[11])}{random.choice(sample[12])}{random.choice(sample[13])}{random.choice(sample[14])}
{random.choice(sample[15])}{random.choice(sample[16])}{random.choice(sample[17])}{random.choice(sample[18])}{random.choice(sample[19])}
{random.choice(sample[20])}{random.choice(sample[21])}{random.choice(sample[22])}{random.choice(sample[23])}{random.choice(sample[24])}
⏱ 𝙑𝙖́𝙡𝙞𝙙𝙤 𝙖𝙩𝙚́: {h}:{m}:{s}  '''),
                reply_markup=button_link()) #acima é a mensagem que será exibida no telegram!
    time.sleep(120)# Aqui é a duração do sinal no caso é 4 minutos, 240 segundos!
    bot . edit_message_text(f'''
    ⭐𝙎𝙞𝙣𝙖𝙡⭐
    
    ⏱𝙁𝙞𝙣𝙖𝙡𝙞𝙯𝙖𝙙𝙤 𝙖́𝙨: {h}:{m}:{s}
    ''', dados . chat . id , dados . message_id)# Aqui o bot deleta a mensagem anterior para ficar mais clean!
    
    time.sleep(60)#60
    ALERT_GALE1()
    time.sleep(10)#10
    DELETE_GALE1()
    time.sleep(50)#50


