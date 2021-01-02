import telebot
from PIL import Image
import os
from config import * #config file with Bot token and owner id
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def help(message):
    bot.send_message(message.chat.id,'Этот бот добавляет любое отправленное фото или стикер в стикерпак\nПользоваться ботом невозможно, если вы не Боб\n\n'+str(stickerlink)+'\n\nБота создал @bob_volskiy\nИсходный код на Github: github.com/BobVolskiy/adding-photo-and-stickers-to-your-stickerpack')

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
        bot.send_message(CHATID,'Добавил в стикерпак изображение выше \n'+stickerlink)
    except:
        bot.send_message(CHATID,'Что-то пошло не так...')
    os.remove("resized.png")
    os.remove("image.jpg")

@bot.message_handler(content_types=["photo"])
def photo(message):
    if message.chat.id==owner:
        bot.send_message(message.chat.id,'Принял фотку. Конвертирую и добавляю...')
        fileID = message.photo[-1].file_id
        converting(fileID,message.chat.id)
    else: 
        bot.send_message(message.chat.id,'Стоп, ты не Боб. Пиздуй лесом')

@bot.message_handler(content_types=["sticker"])
def sticker(message):
    if message.chat.id==owner:
        bot.send_message(message.chat.id,'Принял стикер. Конвертирую и добавляю...')
        fileID = message.sticker.file_id
        converting(fileID,message.chat.id)
    else: 
        bot.send_message(message.chat.id,'Стоп, ты не Боб. Пиздуй лесом')
print('Бот начал свою работу')
bot.polling()