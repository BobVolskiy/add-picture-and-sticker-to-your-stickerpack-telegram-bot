import telebot
from telebot import types

bot = telebot.TeleBot("1590672741:AAFLJ0wgTFR6CkjqIdr_r6oL0cIsK-tRyp4")

def revokestickerset():
    global capibaras
    stickers=bot.get_sticker_set('bv_by_bvsticker_bot').stickers
    capibaras=[]
    for i in range(len(stickers)):
            print(i,stickers[i].file_id)
            capibara1 = types.InlineQueryResultCachedSticker(
                id=i,
                sticker_file_id=stickers[i].file_id,
            )
            capibaras.append(capibara1)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text="Switch", switch_inline_query_current_chat="")
    keyboard.add(switch_button)
    bot.send_message(message.chat.id, "1", reply_markup=keyboard)
@bot.inline_handler(func=lambda query: True)
def inline_mode(query):
    global capibaras
    bot.answer_inline_query(query.id, capibaras)

    
print('started')

bot.polling()