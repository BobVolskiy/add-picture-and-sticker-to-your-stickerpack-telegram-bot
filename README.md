# This Telegram bot adds any sent photo or image sticker to your OWN STICKERPACK created BY THIS BOT.
 - It temporary cant create stickerpack!

[![N|Solid](images/logo.png)](https://twitter.com/bob_volskiy)

# Installation: 
  - Download Python 3+
  - In the terminal enter the command `pip install pyTelegramBotAPI`
  - Create bot here https://t.me/BotFather and copy it's Token
  - Download latest release and create `config.py` in folder with `bot.py`. `config.py` example down below
  - Run `bot.py`. If ok, it will print `Бот начал свою работу...`

# User guide: 
  - Sticker pack must be created by bot. Create it using xxxx command
  - Send sticker, photo or png file and bot will add it to your stickerpack really faster than usual "Stickers" bot. You also dont need to convert your images by yourself to follow 512px width image rule. Bot will do it :D

# Working example: 
<img src="images/preview_1.jpg">
<img src="images/preview_2.jpg">

# config.py example
```
owner = xxxxxxxxx # int var of your telegram id
token = "TOKEN" # Bot token https://t.me/BotFather
stickerlink = "t.me/addstickers/STICKERLINK" # not required, using for help command
```
