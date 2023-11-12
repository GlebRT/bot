import telebot
import psycopg2
from telebot import types
bot = telebot.TeleBot('6933975810:AAFA-Oi2ILObDdWROSRv50f3GVFsh-llPFc')
db_params = {
    'host': 'rain.db.elephantsql.com',
    'database': 'lemubttw',
    'user': 'lemubttw',
    'password': 'tYLVuu3PtgrWLcUBMG5AYLR9n3Z0jEzo'
}
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()


@bot.message_handler(commands=['admin'])

def parol(message):
    # Начинаем процесс ввода данных с помощью состояний
    bot.send_message(message.chat.id, 'Введите пароль от админ-панели:')
    bot.register_next_step_handler(message, parol2)

def parol3(message):
    # Начинаем процесс ввода данных с помощью состояний
    bot.send_message(message.chat.id, 'Неверный пароль, повторите попытку:\n\n/back - назад')
    bot.register_next_step_handler(message, parol2)
def parol2(message):
    k = message.text
    if k=='admin12345':
        handle_admin(message)
    elif k == '/back':
        handle_start(message)
    else:
        parol3(message)
def handle_admin(message):
    # Начинаем процесс ввода данных с помощью состояний
    bot.send_message(message.chat.id, 'Введите населенный пункт:')
    bot.register_next_step_handler(message, process_punkt_step)


def process_punkt_step(message):
    try:
        # Получаем введенный пользователем населенный пункт
        punkt = message.text

        # Запрашиваем следующую информацию
        bot.send_message(message.chat.id, 'Введите адрес:')
        bot.register_next_step_handler(message, process_adress_step, punkt)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def process_adress_step(message, punkt):
    try:
        # Получаем введенный пользователем адрес
        adress = message.text

        # Запрашиваем следующую информацию
        bot.send_message(message.chat.id, 'Введите время работы в формате 11:00-20:00:')
        bot.register_next_step_handler(message, process_time_step, punkt, adress)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def process_time_step(message, punkt, adress):
    try:
        # Получаем введенное пользователем время работы
        time = message.text

        # Запрашиваем следующую информацию
        bot.send_message(message.chat.id, 'Введите направления через запятую:')
        bot.register_next_step_handler(message, process_nap_step, punkt, adress, time)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def process_nap_step(message, punkt, adress, time):
    try:
        # Получаем введенное пользователем направление
        nap = message.text

        # Запрашиваем следующую информацию
        bot.send_message(message.chat.id, 'Введите телефон:')
        bot.register_next_step_handler(message, process_phone_step, punkt, adress, time, nap)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def process_phone_step(message, punkt, adress, time, nap):
    try:
        # Получаем введенный пользователем телефон
        phone = message.text

        # Запрашиваем последнюю информацию
        bot.send_message(message.chat.id, 'Введите сайт:')
        bot.register_next_step_handler(message, process_site_step, punkt, adress, time, nap, phone)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def process_site_step(message, punkt, adress, time, nap, phone):
    try:
        # Получаем введенный пользователем сайт
        site = message.text
        bot.send_message(message.chat.id,'Проверьте введенные данные, если все верно введите /public, в противном случае /back')
        # Записываем данные в базу данных
        nap3 = nap.split(",")
        nap2 = ''
        for i in nap3:
            if i[0] == ' ':
                i = i[1::]
            nap2 += '🔹 ' + i + '\n'
        response2 = f"\n📍 <b>Адрес:</b> {adress}\n\n🕓 <b>Время работы:</b> {time}\n\n⬆️ <b>Направления:</b>\n{nap2}\n📱 <b>Телефон: </b>{phone}\n\n🖥️ <b>Сайт: </b> {site}\n\n\n"
        bot.send_message(message.chat.id, response2, parse_mode='html',disable_web_page_preview=True)
        bot.register_next_step_handler(message, process_site_step2, punkt, adress, time, nap, phone, site)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

def process_site_step2(message, punkt, adress, time, nap, phone, site):
    t = message.text
    if t == '/public':
        try:
            query = "INSERT INTO bp (punkt, adress, time_work, nap, phone_number, site) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (punkt, adress, time, nap, phone, site))

            # Подтверждение добавления данных
            bot.send_message(message.chat.id, 'Данные успешно добавлены в базу данных. Введите /start, чтобы выйти в главное меню')

            # Отправка изменений в базу данных
            conn.commit()
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
    elif t == '/back':
        bot.send_message(message.chat.id, f'Выход из админ-панели в главное меню...')
        handle_start(message)
    else:
        bot.send_message(message.chat.id, f'Команда не найдена, повторите попытку:')
        process_site_step(message, punkt, adress, time, nap, phone)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    file = open('./itkub.jpg', 'rb')
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Посетить сайт', url = 'https://it-cube.ficto.ru/')
    markup.add(button)
    bot.send_photo(message.chat.id, file,  caption=f'<b>Привет, {message.from_user.first_name} {message.from_user.last_name}</b>!\n\nДанный бот поможет вам узнать информацию об открытых центрах проекта IT-Куб.\n\n<b>Введите населенный пункт (только название, не пишите город, село и тд.):</b>', parse_mode='html',reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Получаем введенный пользователем текст
    user_input = message.text

    # Поиск в базе данных по введенному населенному пункту
    query = "SELECT * FROM bp WHERE punkt = %s"
    cursor.execute(query, (user_input,))
    rows = cursor.fetchall()
    cursor.execute(query, (user_input,))
    rows = cursor.fetchall()

    # Формирование и отправка ответа пользователю
    if rows:
        response = ''
        for row in rows:
            nap = row[4].split(",")
            nap2 = ''
            for i in nap:
                if i[0] == ' ':
                    i = i[1::]
                nap2 += '🔹 '+i+'\n'
            response += f"\n📍 <b>Адрес:</b> {row[2]}\n\n🕓 <b>Время работы:</b> {row[3]}\n\n⬆️ <b>Направления:</b>\n{nap2}\n📱 <b>Телефон: </b>{row[5]}\n\n🖥️ <b>Сайт: </b> {row[6]}\n\n\n"
        response = f"🚩<b>{row[1]}</b>\n" + response
        bot.send_message(message.chat.id, response, parse_mode='html', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "<b>К сожалению, в введенном населенном пункте нет открытых центров проекта ИТ-Куб.</b>\n\nНемного терпения и мы появимся у вас!", parse_mode='html')


bot.polling(none_stop=True)