import numpy as np
import telebot

# from numpy import random
import tensorflow as tf

import cv2

bot = telebot.TeleBot("1936414610:AAEgHUPfDd-NOaLnoLuL58JMdDZGoj7HLfg")
model = tf.keras.models.load_model('model_new .h5')


def predict(img):
    pred_img = model.predict(img)
    return pred_img
# buttons = telebot.types.ReplyKeyboardMarkup(row_width=1)
# bt_0 = telebot.types.KeyboardButton('/start')
#
# buttons.add(bt_0)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, ' welcome to sheykh detector bot. ' + message.from_user.username)
    text = 'please upload image '
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo'])
def image(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('img.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
    img = cv2.imread('img.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=(256, 256))
    img = img / 255
    img = np.expand_dims(img, axis=0)
    # cv2.imshow('ing', img)
    # cv2.waitKey()
    lable = predict(img)
    lable = str(np.argmax(lable[0]))
    print(lable)
    if lable=='0':
        bot.send_message(message.chat.id, 'normal person')
    else:
        bot.reply_to(message,'sheykh')

@bot.message_handler(func= lambda message:True)
def send_normal_message(message):
    bot.reply_to(message, 'Not expecting text. ')

bot.polling()