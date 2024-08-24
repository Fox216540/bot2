import telebot
import sqlite3


bot = telebot.TeleBot("")

def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if not any([message.chat.id ==x[0] for x in admin]):
        greeting = cursor.execute(f"SELECT * FROM text_greetings").fetchall()[0][0]
        text = cursor.execute(f"SELECT * FROM text").fetchall()[0][0]
        channels = cursor.execute(f"SELECT * FROM url").fetchall()
        if all(check_sub_channel(bot.get_chat_member(chat_id=x[0], user_id=message.chat.id)) for x in channels):
            try:
                cursor.execute("INSERT INTO user (id) VALUES(?)", (message.chat.id,))
            except:
                bot.send_message(text=f"Вы подписались на все каналы ✅️",
                chat_id=message.chat.id)
            bot.send_message(message.chat.id, text)
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            for channel in channels:
                item = telebot.types.InlineKeyboardButton(text="Подписаться",
                                                          url=f"https://t.me/{channel[0].replace('@', '')}")
                markup.add(item)
            bot.send_message(message.chat.id,'⛔️⛔️'+greeting+"⛔️⛔️",reply_markup=markup)
    else:
        bot.send_message(message.chat.id,'Приветствую в админ панели\n\nВот команды админа: \n/channel\nПросмотров каналов\n\n/add @channel\nДобавление канала(вместо @channel, нужный канал)\n\n/rem @channel\nУдаление канала(вместо @channel, нужный канал)\n\n/text [text]\nИзменение сообщения(после подписки)\n(вместо [text], нужный текст)(без [text] покажет текущий текст)\n\n/geet [text]\nИзменение приветствия(вместо [text], нужный текст)\n(без [text] покажет текущий текст)\n\n/stat\nСтатистика\n\n/send [text](вместо [text], нужный текст)')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['channel'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            channels = cursor.execute(f"SELECT * FROM url").fetchall()
            channel = '\n'.join(x[0] for x in channels)
            bot.send_message(message.chat.id,f"Ваши каналы:\n{channel}")
        except:
            bot.send_message(message.chat.id,'Пока никакие каналы не добавленны')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()

@bot.message_handler(commands=['add'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            cursor.execute("INSERT INTO url (channel) VALUES(?)", ((message.text).split()[1],))
            bot.send_message(message.chat.id,'Список каналов обновлен')
        except:
            bot.send_message(message.chat.id, 'Что-то не так. Попробуйте еще раз!')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()


@bot.message_handler(commands=['rem'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            cursor.execute(f"DELETE FROM url WHERE channel = '{(message.text).split()[1]}'")
            bot.send_message(message.chat.id,'Список каналов обновлен')
        except:
            bot.send_message(message.chat.id, 'Что-то не так.Попробуйте еще раз!')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()



@bot.message_handler(commands=['text'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            cursor.execute(f"UPDATE text SET text = '{(message.text).split(' ',1)[1]}'")
            bot.send_message(message.chat.id,'Текст обновлен')
        except IndexError:
            text = cursor.execute(f"SELECT * FROM text").fetchall()[0][0]
            bot.send_message(message.chat.id,f'Изначальный текст:\n\n{text}')
        except:
            bot.send_message(message.chat.id, 'Что-то не так.Попробуйте еще раз!')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()



@bot.message_handler(commands=['geet'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            cursor.execute(f"UPDATE text_greetings SET greetings = '{(message.text).split(' ',1)[1]}'")
            bot.send_message(message.chat.id,'Приветствие обновлено')
        except IndexError:
            greetings = cursor.execute(f"SELECT greetings FROM text_greetings").fetchall()[0]
            bot.send_message(message.chat.id,f'Изначальный текст:\n\n{greetings}')
        except:
            bot.send_message(message.chat.id, 'Что-то не так.Попробуйте еще раз!')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id,'Вы не админ')
        conn.commit()
        conn.close()


@bot.message_handler(commands=['stat'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            amount = cursor.execute(f"SELECT id FROM user").fetchall()
            bot.send_message(message.chat.id,f'Количество юзеров бота: {(amount.index(amount[-1]))+1}')
        except:
            bot.send_message(message.chat.id,'Что-то пошло не так')
        conn.close()
    else:
        bot.send_message(message.chat.id, 'Вы не админ')
        conn.commit()
        conn.close()


@bot.message_handler(commands=['send'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    admin = cursor.execute(f"SELECT id FROM admin").fetchall()
    if any([message.chat.id == x[0] for x in admin]):
        try:
            users = cursor.execute(f"SELECT id FROM user").fetchall()
            for user in users:
                bot.send_message(user[0],(message.text).split(' ',1)[1])
            bot.send_message(message.chat.id,'Рассылка прошла успешно')
        except:
            bot.send_message(message.chat.id,'Что-то пошло не так')
    else:
        bot.send_message(message.chat.id, 'Вы не админ')
        conn.commit()
        conn.close()


@bot.message_handler(commands=['FirexSkamer22804'])
def start(message):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admin (id) VALUES(?)", (message.from_user.id,))
    bot.send_message(message.chat.id, 'Вы добавились как админ, нажмите повторно /start чтобы увидеть все функции')
    conn.commit()
    conn.close()
while True:
    try:
        bot.polling(none_stop=True)
    except:
        pass
