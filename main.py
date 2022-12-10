import telebot
import os
import random
from simpledemotivators import Demotivator


bot = telebot.TeleBot(
    "5661752388:AAE07pQHkT3IPpYoRdkaNoOqIVmmuSoKw5Y", parse_mode="HTML", skip_pending=True
)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "<b>Привет! Отправь фото и я сделаю из него демотиватор!</b>\n<code>Ты можешь добавить число к фотографии, чтобы увеличить число итераций</code>")


def get_text():
    with open('names.txt', 'r', encoding='utf-8') as f:
        text = [x for x in f]
    return random.choice(text)


@bot.message_handler(content_types=["photo"])
def photo_processing(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{fileID}.jpg", "wb") as new_file:
        new_file.write(downloaded_file)
    if message.caption is not None and message.caption.isdigit():
        if int(message.caption) <= 10:
            for i in range(int(message.caption)):
                dem = Demotivator(get_text(), get_text())
                dem.create(f"{fileID}.jpg", result_filename=f"{fileID}.jpg",
                           watermark='t.me/Demotivatorokcubot')
        else:
            for i in range(10):
                dem = Demotivator(get_text(), get_text())
                dem.create(f"{fileID}.jpg", result_filename=f"{fileID}.jpg",
                           watermark='t.me/Demotivatorokcubot')
    else:
        dem = Demotivator(get_text(), get_text())
        dem.create(f"{fileID}.jpg", result_filename=f"{fileID}.jpg",
                   watermark='t.me/Demotivatorokcubot')
    with open(f"{fileID}.jpg", "rb") as photo:
        bot.send_photo(
            message.chat.id, photo, caption="Сделано в\nt.me/Demotivatorokcubot"
        )
    os.remove(f"{fileID}.jpg")


bot.polling()
