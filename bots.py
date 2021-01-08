#!/usr/bin/python3.8
import telebot
from PIL import Image
import os
from config import * #create config.py file next to this one. config.py example copy from https://github.com/BobVolskiy/adding-to-your-stickerpack/blob/main/README.md



bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,'Отправь мне картинку или стикер, чтобы начать...\n❗Если картинка прозрачная, отправляйте в виде файла')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул старт')
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,'Этот бот добавляет любое отправленное фото или стикер в стикерпак Боба '+str(stickerlink)+'\n\nБота создал @bob_volskiy\nИсходный код: github.com/BobVolskiy/\n\nМои боты:\n@BVSticker_bot\n@BVMusic_bot')
    bot.send_message(owner,'@'+str(message.from_user.username)+' кинул хелп')

def resizing(im):
    width, height = im.size
    if width>height:
        resized_im = im.resize((512, round(height/width*512)))
    elif height>=width:
        resized_im = im.resize((round(width/height*512),512))
    return resized_im

def converting(fileID,CHATID):
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    im = Image.open('image.jpg')
    resizing(im).save('resized.png')
    with open("resized.png", "rb") as image:
        f = image.read()
        b = bytearray(f)
    try:
        bot.add_sticker_to_set(owner,'bv_by_bvsticker_bot',b,'😘')
        bot.send_message(CHATID,'Добавлено!\n'+stickerlink)
    except:
        bot.send_message(CHATID,'😫 Что-то пошло не так...')
    os.remove("resized.png")
    os.remove("image.jpg")

@bot.message_handler(content_types=["photo"])
def photo(message):
    bot.send_message(message.chat.id,'Принял фотку. Конвертирую и добавляю...')
    fileID = message.photo[-1].file_id
    if message.chat.id==owner:
        converting(fileID,message.chat.id)
        bot.delete_message(message.chat.id,message.message_id+1)
    else: 
        bot.send_message(message.chat.id,'Стоп, ты не Боб 😆\nНо я вышлю ему эту картинку')
        bot.send_photo(owner, bot.download_file(bot.get_file(fileID).file_path),caption='Эту картинку прислал @'+str(message.from_user.username))

@bot.message_handler(content_types=["sticker"])
def sticker(message):
    bot.send_message(message.chat.id,'Принял стикер. Конвертирую и добавляю...')
    fileID = message.sticker.file_id
    if message.chat.id==owner:
        converting(fileID,message.chat.id)
        bot.delete_message(message.chat.id,message.message_id+1)
    else: 
        bot.send_message(message.chat.id,'Стоп, ты не Боб 😆\nНо я вышлю ему этот стикер')
        bot.send_sticker(owner, bot.download_file(bot.get_file(fileID).file_path))
        bot.send_message(owner, 'Этот стикер прислал @'+str(message.from_user.username))

@bot.message_handler(content_types=["document"])
def document(message):
    if message.document.file_name.split('.')[-1]=='png' or message.document.file_name.split('.')[-1]=='jpg':
        if message.document.file_size<25000000:
            bot.send_message(message.chat.id,'Принял файл. Конвертирую и добавляю...')
            fileID = message.document.file_id
            if message.chat.id==owner:
                converting(fileID,message.chat.id)
                bot.delete_message(message.chat.id,message.message_id+1)
            else: 
                bot.send_message(message.chat.id,'Стоп, ты не Боб 😆\nНо я вышлю ему эту картинку')
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(message.document.file_name, 'wb') as new_file:
                    new_file.write(downloaded_file)
                im = open(message.document.file_name,'r+b')
                bot.send_document(owner, im,caption='Эту картинку прислал @'+str(message.from_user.username))
                im.close()
                os.remove(message.document.file_name)
        else: bot.send_message(message.chat.id,'❌ Размер файла превышает 25 МБ')
    else: bot.send_message(message.chat.id,'❌ Поддерживаются форматы *.jpg и *.png')

print('Бот начал свою работу...')
bot.polling()