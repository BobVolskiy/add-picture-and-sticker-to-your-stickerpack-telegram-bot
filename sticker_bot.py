#!/usr/bin/python3.8
import telebot
from telebot import types
from PIL import Image
import os
print('- BOT: Starting...')
#Tries to read bot token. If couldnt, restart the app with asking to write bot token to config.py
try: 
    from config import bot_token
    bot = telebot.TeleBot(bot_token)
except:
    f = open("config.py", "w")
    f.write("#This is a config file. Please dont touch if everything works fine. Also, consider supporting me on patreon.com/bob_volskiy\nbot_token = 'write token here'\n")
    f.close()
    print('-  ATENTION: Open config.py file, write bot token and restart this bot---------------')
    print('-  ATENTION: Open config.py file, write bot token and restart this bot---------------')
    print('-  ATENTION: Open config.py file, write bot token and restart this bot---------------')
    quit()
print('- INFO: Bot token: ',bot_token)

#Tries to read bot bot's username. If couldnt, gets bot's username using telegram api
try:
    from config import bot_username
except:
    f = open("config.py", "a")
    bot_username = bot.get_me().username
    f.write("bot_username = '"+bot_username+"'\n")
    f.close()
print('- INFO: Bot username: @',bot_username)

#Tries to read sticker link. If couldnt, creates temporary None var
try:
    from config import stickers_link
except:
    stickers_link='None'
print('- INFO: Stickerpack link: t.me/addstickers/'+stickers_link)

#Tries to read owner_id. If couldnt, creates temporary None var. Owner will be the first person to writes /css - create sticker set
try:
    from config import owner_id
except:
    owner_id=None
print('- INFO: ID of stickerpack owner: ',owner_id)

text_toggler=None #text command toggler
@bot.message_handler(commands=["css"])
def create_sticker_set(message):
    global owner_id
    global text_toggler
    if stickers_link=='None':
        owner_id=message.from_user.id
        print('- BOT: @'+message.from_user.username+' became an owner of stickerpack. Now only owner can control bot.')
        f = open("config.py", "a")
        f.write("owner_id = "+str(owner_id)+"\n")
        f.close()
        bot.send_message(message.chat.id,'Введите название стикерпака...')
        text_toggler='Ввести тайтл'
    else: bot.send_message(message.chat.id,'Стикерпак уже создан\nt.me/addstickers/'+stickers_link)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'<b>Как это работает?</b>\nВы присытате мне стикер, картинку или прозрачную картинку в виде файла, а я добавляю её в стикерпак владельца.\n\n'+'<b>В чем преимущество этого бота?</b>\nДругие боты могут добавлять в ваш стикерпак только другие стикеры. Этот же конвертирует любую картинку, стикер или *.png файл в стикер и добавляет его в стикерпак.\n\nЕго можно использовать для общего чата, куда любой может скинуть картинку, а владельцу придется лишь подтвердить  добавление стикера', parse_mode="HTML")
    bot.send_message(owner_id,'@'+str(message.from_user.username)+' /start')
@bot.message_handler(commands=["donate"])
def donate(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton(text='Исходный код', url='https://github.com/BobVolskiy/add-picture-and-sticker-to-your-stickerpack-telegram-bot'), types.InlineKeyboardButton(text='Донат', url='https://patreon.com/bob_volskiy/'))
    bot.send_message(message.chat.id,'<b>Бота создал:</b> <i>@bob_volskiy</i>\n'+'<b>Версия:</b> <i>1.3</i>\n'+'<b>Мои боты:</b><i>\n@BVSticker_bot\n@BVMusic_bot</i>\n\n', parse_mode="HTML",reply_markup = markup)
    bot.send_message(owner_id,'@'+str(message.from_user.username)+' /donate')
       
    
@bot.message_handler(content_types=["text"])
def main(message):
    print('- CHAT: @'+message.from_user.username+': '+message.text)
    global text_toggler
    global create_new_sticker_set_title
    global stickers_link
    if text_toggler=='Ввести тайтл':
        create_new_sticker_set_title=message.text+' @'+bot_username 
        text_toggler='Ввести линк'
        bot.send_message(message.chat.id,'Введите тег вашего стикерпака...\nСтикерпак можно будет найти по ссылке t.me/addstickers/ВАШТЕГ')
    elif text_toggler=='Ввести линк':
        stickers_link=message.text+'_by_'+bot_username
        text_toggler='Выслать фото'
        bot.send_message(message.chat.id,'Вышлите картинку для вашего первого стикера...')



def resizing(im):
    width, height = im.size
    if width>height:
        resized_im = im.resize((512, round(height/width*512)))
    elif height>=width:
        resized_im = im.resize((round(width/height*512),512))
    return resized_im

def converting(file_id,chat_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    im = Image.open('image.jpg')
    resizing(im).save('resized.png')
    with open("resized.png", "rb") as image:
        f = image.read()
        b = bytearray(f)
    os.remove("resized.png")
    os.remove("image.jpg")
    return b

@bot.message_handler(content_types=["photo","sticker","document"])
def startq(message):
    chat_id=message.chat.id
    ms_type=message.content_type
    print('- BOT: @'+message.from_user.username+' sent a '+ms_type)
    if ms_type=="photo":
        file_id = message.photo[-1].file_id
    elif ms_type=="sticker":
        file_id = message.sticker.file_id
    elif ms_type=="document":
        file_id = message.document.file_id
    global text_toggler
    if text_toggler=='Выслать фото':
        global create_new_sticker_set_title
        global stickers_link
        try:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Стикерпак', url='https://t.me/addstickers/'+stickers_link))
            bot.create_new_sticker_set(user_id = owner_id,name = stickers_link,title = create_new_sticker_set_title,png_sticker = converting(file_id,chat_id),emojis="👍")
            bot.send_message(chat_id,'Стикерпак создан!',reply_markup = markup)
            f = open("config.py", "a")
            f.write("stickers_link = '"+stickers_link+"'\n")
            f.close()
            text_toggler=None
        except: 
            bot.send_message(chat_id,'Что-то пошло не так,\nПопробуйте ввести другой тег стикерпака...\n'+stickers_link)
            text_toggler='Ввести линк'
    elif stickers_link=='None':
        bot.send_message(chat_id,'Стикерпак не создан. Используйте команду /css')
    else:
        if chat_id==owner_id:
            try:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='Стикерпак', url='https://t.me/addstickers/'+stickers_link))
                bot.add_sticker_to_set(owner_id,stickers_link,converting(file_id,chat_id),'😘')
                bot.send_message(chat_id,'Добавлено!',reply_markup = markup)
            except:
                bot.send_message(chat_id,'😫 Что-то пошло не так...')
        else:
            bot.send_message(chat_id,'Поскольку стикерпак\nt.me/addstickers/'+stickers_link+'\nсоздан не тобою (а ты пытаешься добавить стикер именно туда), я вышлю эту картинку владельцу стикерпака на проверку :)')
            if ms_type=="photo":
                file_id = message.photo[-1].file_id
                bot.send_photo(owner_id, bot.download_file(bot.get_file(file_id).file_path),caption='Эту картинку прислал @'+str(message.from_user.username))
            elif ms_type=="sticker":
                file_id = message.sticker.file_id
                bot.send_sticker(owner_id, bot.download_file(bot.get_file(file_id).file_path))
                bot.send_message(owner_id, 'Этот стикер прислал @'+str(message.from_user.username))
            elif ms_type=="document":
                if message.document.file_name.split('.')[-1]=='png' or message.document.file_name.split('.')[-1]=='jpg':
                    if message.document.file_size<25000000:
                        file_id = message.document.file_id
                        bot.send_document(owner_id, bot.download_file(bot.get_file(file_id).file_path),caption='Это прислал @'+str(message.from_user.username))
                    else: bot.send_message(message.chat.id,'❌ Размер файла превышает 25 МБ')
                else: bot.send_message(message.chat.id,'❌ Поддерживаются форматы *.jpg и *.png')
print('- BOT: Started...')
bot.polling()