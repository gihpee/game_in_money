import telebot
import time
import psycopg2
from telebot import types
import threading
from telebot.apihelper import ApiTelegramException

conn = psycopg2.connect(host='127.0.0.1', user='user', password='pwd', database='db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users_demo(
    userid BIGINT PRIMARY KEY,
    username VARCHAR,
    chat_id BIGINT,
    name VARCHAR,
    script INT,
    finished INT, 
    ban INT,
    friend_id BIGINT,
    quest_1 INT,
    quest_2 INT,
    quest_3 INT,
    quest_4 INT,
    quest_5 INT
)""")
conn.commit()
bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()
        if info is None:
            msg = bot.send_message(message.chat.id, 'Хочешь поиграть в Деньги?\n\nСначала представься📝')
            bot.register_next_step_handler(msg, user_ok)
        else:
            if info[6] == 1:
                banned(message)
            elif info[6] == 0:
                cur.execute(f"DELETE FROM users_demo WHERE userid={message.from_user.id}")
                conn.commit()
                msg = bot.send_message(message.chat.id, 'Хочешь поиграть в Деньги?\n\nСначала представься📝')
                bot.register_next_step_handler(msg, user_ok)
    except ApiTelegramException:
        pass


def user_ok(message):
    try:
        if message.content_type == 'text':
            cur.execute(f"INSERT INTO users_demo VALUES('{message.from_user.id}', '{message.from_user.username}',"
                        f" '{message.chat.id}', '{message.text}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}',"
                        f" '{0}', '{0}', '{0}')")
            conn.commit()
            bot.send_message(message.chat.id, message.text + ', счастливых вам голодных игр! (нет).'
                                                             ' Потому что в новом времени они уже давно начались.')

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Неправда!')
            btn2 = types.KeyboardButton(text='Сталкиваюсь с этим')
            kb.add(btn1, btn2)
            msg = bot.send_photo(message.chat.id, open('data/баннер1 (3).jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, post_4)
        else:
            bot.register_next_step_handler(message, user_ok)
    except ApiTelegramException:
        pass


def post_4(message):
    try:
        if message.text in ['Неправда!', 'Сталкиваюсь с этим']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='И не говори')
            btn2 = types.KeyboardButton(text='Не говори такой бред')
            kb.add(btn1, btn2)
            msg = bot.send_photo(message.chat.id, open('data/баннер2 (2).jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, post_5)
        else:
            bot.register_next_step_handler(message, post_4)
    except ApiTelegramException:
        pass


def post_5(message):
    try:
        if message.text in ['И не говори', 'Не говори такой бред']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='И правда, кто?')
            btn2 = types.KeyboardButton(text='Столько вопросов, когда уже будут ответы?')
            kb.add(btn1, btn2)
            msg = bot.send_photo(message.chat.id, open('data/баннер1-1.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, post_6)
        else:
            bot.register_next_step_handler(message, post_5)
    except ApiTelegramException:
        pass


def post_6(message):
    try:
        if message.text in ['И правда, кто?', 'Столько вопросов, когда уже будут ответы?']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Иду бороться за деньги')
            btn2 = types.KeyboardButton(text='А что там за выход сзади?')
            kb.add(btn1, btn2)
            msg = bot.send_photo(message.chat.id, open('data/53.png', 'rb'), 'Они уже зовут тебя. Зовут бороться за свои'
                                                    ' деньги.\n<b>Разрывать всех и идти по головам.</b>'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, post_7_1)
        else:
            bot.register_next_step_handler(message, post_6)
    except ApiTelegramException:
        pass


def post_7_1(message):
    try:
        if message.text == 'А что там за выход сзади?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton(text='Идем!')
            kb.add(btn1)
            msg = bot.send_message(message.chat.id, 'Кажется, они отвернулись. Пойдем и посмотрим, пока есть время.'
                                                    '\n<b>Принимай решение быстро.</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, post_8_1)
        elif message.text == 'Иду бороться за деньги':
            post_7_2(message)
    except ApiTelegramException:
        pass


def post_8_1(message):
    try:
        if message.text == 'Идем!':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Боже, что там?!')
            kb.add(btn1)
            msg = bot.send_voice(message.chat.id, open('data/aud1.mp3', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, post_9)
        else:
            bot.register_next_step_handler(message, post_8_1)
    except ApiTelegramException:
        pass


def post_7_2(message):
    try:
        if message.text == 'Иду бороться за деньги':
            bot.send_photo(message.chat.id, open('data/54.png', 'rb'), '5...')
            time.sleep(1)
            bot.send_message(message.chat.id, '4...')
            time.sleep(1)
            bot.send_message(message.chat.id, '3...')
            time.sleep(1)
            bot.send_message(message.chat.id, '2...')
            post_9(message)
        else:
            bot.register_next_step_handler(message, post_7_2)
    except ApiTelegramException:
        pass


def post_9(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton(text='Откуда ты взялась?')
        kb.add(btn1)
        msg = bot.send_photo(message.chat.id, open('data/55 (2).jpg', 'rb'), reply_markup=kb)
        bot.register_next_step_handler(msg, post_10_11)
    except ApiTelegramException:
        pass


def post_10_11(message):
    try:
        if message.text == 'Откуда ты взялась?':
            bot.send_photo(message.chat.id, open('data/59 (1).jpg', 'rb'))
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='А как мне найти свои деньги нового времени?')
            kb.add(btn1)
            msg = bot.send_message(message.chat.id, 'В новом времени работает только <b>система</b>. Там мы строим ее,'
                                                    ' потому что поняли, кто, сколько и где теряет деньги.\nА потом'
                                                    ' переходим на <b>новый уровень дохода</b>, как в игре 💎'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, post_12_13)
        else:
            bot.register_next_step_handler(message, post_10_11)
    except ApiTelegramException:
        pass


def post_12_13(message):
    try:
        if message.text == 'А как мне найти свои деньги нового времени?':
            bot.send_video(message.chat.id, open('data/vidpolina1.mov', 'rb'), timeout=20, height=1920, width=1080)
            bot.send_message(message.chat.id, '<b>Деньги – это не голодные игры.\n'
                                              'Это то, что будет для тебя доступно.</b>\n'
                                              'И ты сам выберешь, как они к тебе будут приходить в Новое Время.\n\n'
                                              'Смотри видео ⬆️ где я рассказываю, как попасть туда', parse_mode='HTML')
            time.sleep(2) #5 min

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Хочу выйти из этого лабиринта. Куда идти дальше?')
            kb.add(btn1)
            msg = bot.send_photo(message.chat.id, open('data/post13.jpg', 'rb'), '<b>Ты точно готов узнать, где теряешь свои деньги?</b>\n\n'
                                                    'Я Полина Грановская, трансформационный тренер. Лидер в <b>Игре в '
                                                    'Деньги</b>💎.\nИ сейчас я смотрю на твой денежный лабиринт,'
                                                    ' в котором ты запутался.\n\nВижу, где ты выбираешь лишаться денег'
                                                    ' уже долгое время. А еще здесь мелькают твои зоны квантового'
                                                    ' скачка в доходе.\n\nУже скорее хочу, чтобы <b>ты их тоже увидел!</b>'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, post_14)
        else:
            bot.register_next_step_handler(message, post_12_13)
    except ApiTelegramException:
        pass


def post_14(message):
    try:
        if message.text == 'Хочу выйти из этого лабиринта. Куда идти дальше?':
            file = open('data/56.png', 'rb')

            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='А что работает?')
            kb.add(btn1)

            msg = bot.send_photo(message.chat.id, file, f'{info[3]}, ты опять хочешь, чтобы за тебя решили все проблемы?🤨'
                                                    f'\n\nОпять думаешь, что для больших денег тебе'
                                                    f' должен кто-то помочь?', reply_markup=kb)

            bot.register_next_step_handler(msg, post_15)
        else:
            bot.register_next_step_handler(message, post_14)
    except ApiTelegramException:
        pass


def post_15(message):
    try:
        if message.text == 'А что работает?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Играть в Деньги!')
            kb.add(btn1)

            bot.send_video(message.chat.id, open('data/vidpolina2.mov', 'rb'), timeout=20, height=1920, width=1080)
            msg = bot.send_message(message.chat.id, 'Давай так. Ты сделаешь свой доход в новом времени'
                                                    ' <b>сам.</b> Смотри видео, как это будет происходить.\n\n'
                                                    'Дойди до конца <b>Игры</b>💎. Так ты узнаешь, почему не выходишь на'
                                                    ' новый уровень дохода и как это сделать именно'
                                                    ' тебе🫵🏻', reply_markup=kb, parse_mode='HTML')

            bot.register_next_step_handler(msg, post_16)
        else:
            bot.register_next_step_handler(message, post_15)
    except ApiTelegramException:
        pass


def post_16(message):
    try:
        if message.text == 'Играть в Деньги!':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
            btn1 = types.KeyboardButton(text='1')
            btn2 = types.KeyboardButton(text='2')
            btn3 = types.KeyboardButton(text='3')
            btn4 = types.KeyboardButton(text='4')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/47.jpg', 'rb'), 'Ответь на 5 вопросов – и твой персонаж'
                                                                             ' в <b>Игре</b>💎 будет готов\n\n'
                                                        '1) Возможность приобрести что-то больше\n\n'
                                                        '2) Чем больше я буду работать, тем больше я заработаю\n\n'
                                                        '3) Инструмент улучшения жизни и решения проблем\n\n'
                                                        '4) Ресурс и энергия для развития тебя, как личности'
                                                        , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, post_17_18)
        else:
            bot.register_next_step_handler(message, post_16)
    except ApiTelegramException:
        pass


def post_17_18(message):
    try:
        if message.text in ['1', '2', '3', '4']:
            bot.send_message(message.chat.id, 'Формируем мышление твоего персонажа…')
            cur.execute(f"""UPDATE users_demo SET quest_1={message.text} WHERE userid={message.from_user.id}""")
            conn.commit()
            time.sleep(2)

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
            btn1 = types.KeyboardButton(text='1')
            btn2 = types.KeyboardButton(text='2')
            btn3 = types.KeyboardButton(text='3')
            btn4 = types.KeyboardButton(text='4')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/49.jpg', 'rb'), '1) Не могу управлять деньгами, они зависят не от меня\n\n'
                                                        '2) Чем больше зарабатываю, тем сильнее устаю\n\n'
                                                        '3) Я пока недостаточно развил навыки и узнаваемость\n\n'
                                                        '4) Нет заряженного окружения, которое будет помогать мне расти'
                                                        , reply_markup=kb)
            bot.register_next_step_handler(msg, post_19_20)
        else:
            bot.register_next_step_handler(message, post_17_18)
    except ApiTelegramException:
        pass


def post_19_20(message):
    try:
        if message.text in ['1', '2', '3', '4']:
            bot.send_message(message.chat.id, 'Подбираем место жительство для твоего персонажа…')
            cur.execute(f"""UPDATE users_demo SET quest_2={message.text} WHERE userid={message.from_user.id}""")
            conn.commit()
            time.sleep(2)

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
            btn1 = types.KeyboardButton(text='1')
            btn2 = types.KeyboardButton(text='2')
            btn3 = types.KeyboardButton(text='3')
            btn4 = types.KeyboardButton(text='4')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/50.jpg', 'rb'), '1) Найти работу/клиента\n\n'
                                                        '2) Преодолеть страх продаж, высокого чека, коммуникации\n\n'
                                                        '3) Вложения в рекламу, в инвестиции, в себя, в психолога\n\n'
                                                        '4) Смена вектора в работе и в состоянии', reply_markup=kb)
            bot.register_next_step_handler(msg, post_21_22)
        else:
            bot.register_next_step_handler(message, post_19_20)
    except ApiTelegramException:
        pass


def post_21_22(message):
    try:
        if message.text in ['1', '2', '3', '4']:
            bot.send_message(message.chat.id, 'Определяем, кто окружает твоего персонажа…')
            cur.execute(f"""UPDATE users_demo SET quest_3={message.text} WHERE userid={message.from_user.id}""")
            conn.commit()
            time.sleep(2)

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
            btn1 = types.KeyboardButton(text='1')
            btn2 = types.KeyboardButton(text='2')
            btn3 = types.KeyboardButton(text='3')
            btn4 = types.KeyboardButton(text='4')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/51.jpg', 'rb'), '1) Повысить скилл в своем деле\n\n'
                                                        '2) Успешно построить команду и бизнес\n\n'
                                                        '3) Понимание, как масштабировать себя и свое дело\n\n'
                                                        '4) Сделать так, чтобы о моих успехах узнали', reply_markup=kb)
            bot.register_next_step_handler(msg, post_23_24)
        else:
            bot.register_next_step_handler(message, post_21_22)
    except ApiTelegramException:
        pass


def post_23_24(message):
    try:
        if message.text in ['1', '2', '3', '4']:
            bot.send_message(message.chat.id, 'Выбираем, что может убить твоего персонажа,'
                                              ' а что сделать долларовым миллиардером…')
            cur.execute(f"""UPDATE users_demo SET quest_4={message.text} WHERE userid={message.from_user.id}""")
            conn.commit()
            time.sleep(2)

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
            btn1 = types.KeyboardButton(text='1')
            btn2 = types.KeyboardButton(text='2')
            btn3 = types.KeyboardButton(text='3')
            btn4 = types.KeyboardButton(text='4')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/52.jpg', 'rb'), '*в ближайшие пару месяцев\n\n1) 50к-100к\n\n'
                                                          '2) 100к-300к\n\n'
                                                          '3) 300к-700к\n\n'
                                                          '4) 1м+', reply_markup=kb)
            bot.register_next_step_handler(msg, post_25_26)
        else:
            bot.register_next_step_handler(message, post_23_24)
    except ApiTelegramException:
        pass


def post_25_26(message):
    try:
        if message.text in ['1', '2', '3', '4']:
            bot.send_message(message.chat.id, 'Твой герой почти готов. Подожди немного, остались последние штрихи…')
            cur.execute(f"""UPDATE users_demo SET quest_5={message.text} WHERE userid={message.from_user.id}""")
            conn.commit()

            time.sleep(4) #5min

            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            script = round((info[8]+info[9]+info[10]+info[11]+info[12])/5)
            if script == 4:
                script = 3

            cur.execute(f'UPDATE users_demo SET script={script} WHERE userid={message.from_user.id}')
            conn.commit()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Начать игру')
            kb.add(btn1)
            msg = bot.send_message(message.chat.id, f'{info[3]}, твой персонаж в Новом Времени Денег готов!\nНачинаем?🎲',
                                   reply_markup=kb)
            bot.register_next_step_handler(msg, post_27_28)
        else:
            bot.register_next_step_handler(message, post_25_26)
    except ApiTelegramException:
        pass


def post_27_28(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        friend_timer_5h = threading.Timer(18000, reminder_5h, [message])  # 5h
        friend_timer_5h.start()

        friend_timer_15h = threading.Timer(54000, ban_user, [message])  # 15h
        friend_timer_15h.start()

        bot.send_photo(message.chat.id, open('data/57.png', 'rb'), 'Один в поле Нового Времени не воин. Особенно, если мы говорим про Деньги.\n\n'
                                                                   'Давай позовем кого-то проходить игру вместе с тобой, чтобы все получилось?\n\n'
                                                                   '➡️ Друг запускает Игру и вводит своё имя\n\n➡️ Ты копируешь нам его ник через @\n\n➡️ Вы оба в игре'
                                                                   '\n\nУ тебя есть 15 часов. Без твоего друга игра закрывается❌')

        msg = bot.send_photo(message.chat.id, open('data/58.png', 'rb'), f'{info[3]} уже в игре. Читай: с новым уровнем дохода\n\n'
                                          f'Переходи в @game_in_money_bot и запускай ИГРУ В ДЕНЬГИ\n\n')

        bot.register_next_step_handler(msg, check_friend, [friend_timer_5h, friend_timer_15h])
    except ApiTelegramException:
        pass


def check_friend(message, lst_timer, flag=True):
    try:
        if message.content_type == 'text':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info_user = cur.fetchone()

            if info_user[6] == 1:
                banned(message)
            else:
                if flag:
                    bot.send_message(message.chat.id, 'Сейчас посмотрим, сможет ли твой друг идти вместе с тобой'
                                                      ' с твоим новым масштабом💎')
                    time.sleep(1)

                if message.text == 'admin':
                    info_friend = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    friend_name = message.text[1:]
                    cur.execute(f"""SELECT * FROM users_demo WHERE username={"'" + friend_name + "'"}""")
                    info_friend = cur.fetchone()
                cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
                info_user = cur.fetchone()

                if info_friend is not None or message.text == 'admin':
                    if info_friend[0] == info_user[0]:
                        msg = bot.send_message(message.chat.id,
                                                f'Ты решил хакнуть Игру в Деньги? Не получится, {info_user[3]}. '
                                                f'Лучше позови друга вместе хакнуть новый уровень дохода \n\n'
                                                f'Следующим сообщением ждем ник друга через @')
                        bot.register_next_step_handler(msg, check_friend, [lst_timer[0], lst_timer[1]], flag=False)
                    elif info_user[0] == info_friend[7]:
                        msg = bot.send_message(message.chat.id, f'Нас не обманешь, *Имя*.\n\nПоделись постом про нашу Игру,'
                                                                f' которую присылали выше.\nЭто просто! А большие деньги пойдут'
                                                                f' к тебе так же легко после этого ⚡\n\nСледующим сообщением'
                                                                f' пришли ник друга через @')
                        bot.register_next_step_handler(msg, check_friend, [lst_timer[0], lst_timer[1]], flag=False)
                    else:
                        bot.send_message(message.chat.id, f'{info_user[3]}, ты знаешь, что зарабатывать много – это твое'
                                                          f' предназначение?\n\nПотому что ты принимаешь решения быстро.'
                                                          f' Это важнейший навык сейчас.\n\nТак держать! Это правильная стратегия'
                                                          f' с деньгами Нового Времени.\n\n💎 <b>Ты предприимчивый по жизни'
                                                          f' – а скорость в деньгах решает.</b>', parse_mode='HTML')

                        lst_timer[0].cancel()
                        lst_timer[1].cancel()
                        if message.text != 'admin':
                            cur.execute(f"""UPDATE users_demo SET friend_id={info_friend[0]} WHERE userid={message.from_user.id}""")
                            conn.commit()

                        time.sleep(1)
                        bot.send_message(message.chat.id, 'Игра с твоим персонажем начнется через…')
                        bot.send_video(message.chat.id, open('data/vid3.mov', 'rb'))
                        time.sleep(1)
                        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
                        info = cur.fetchone()

                        if info[4] == 1:
                            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

                            btn1 = types.KeyboardButton(text='Взять трубку')
                            btn2 = types.KeyboardButton(text='Продолжить дальше спать')
                            kb.add(btn1, btn2)

                            msg = bot.send_message(message.chat.id, f'{info[3]}, вставай, звонят!', reply_markup=kb)
                            bot.register_next_step_handler(msg, script1_1_2)
                        elif info[4] == 2:
                            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

                            btn1 = types.KeyboardButton(text='пойти')
                            btn2 = types.KeyboardButton(text='не пойти')
                            kb.add(btn1, btn2)
                            msg = bot.send_photo(message.chat.id, open('data/10.jpg', 'rb'), '🔺 3 года назад вы прошли'
                                                                                             ' бизнес-тренинг. Сегодня – встреча вашей'
                                                                                             ' Десятки.', reply_markup=kb)
                            bot.register_next_step_handler(msg, script2_1_2)
                        elif info[4] == 3:
                            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
                            btn1 = types.KeyboardButton(text='сказать тост о сестре')
                            btn2 = types.KeyboardButton(text='передать тост папе')
                            kb.add(btn1, btn2)

                            bot.send_message(message.chat.id, 'Ваша сестра – тихий, но очень талантливый художник.\n'
                                                              'А вы – предприниматель.')

                            msg = bot.send_photo(message.chat.id, open('data/zastolye.jpg', 'rb'), 'Вы собрались с'
                                                                                                   ' родителями на ее день'
                                                                                                   ' рождения.', reply_markup=kb)
                            bot.register_next_step_handler(msg, script3_1_3)

                else:
                    msg = bot.send_message(message.chat.id, f'{info_user[3]}, Мы не видим твоего друга. Спроси,'
                                                            f' точно ли он начал <b>Игру в Деньги?</b>\n\n'
                                                            f'Следующим сообщением ждем ник друга через @', parse_mode='HTML')
                    bot.register_next_step_handler(msg, check_friend, [lst_timer[0], lst_timer[1]], flag=False)
        else:
            bot.register_next_step_handler(message, check_friend, [lst_timer[0], lst_timer[1]], flag=True)
    except ApiTelegramException:
        pass


def reminder_5h(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()
        bot.send_message(message.chat.id, f'{info[3]}, ты как обычно откладываешь всё на потом?\n\nОсталось 10 часов,'
                                          f' чтобы успеть в последний вагон поезда.\n\nЖдем тебя и твоего друга в игре.'
                                          f' <b>Отправь нам юзернейм друга (ник через @) – и все продолжится.</b>\n\n'
                                          f'Быть предприимчивым, действовать быстро – главный'
                                          f' принцип Денег Нового Времени💎', parse_mode='HTML')
    except ApiTelegramException:
        pass


def ban_user(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()
        bot.send_message(message.chat.id, f'{info[3]}, ну как обычно ты думаешь, что отложишь на потом, а сейчас – '
                                          f'не лучшее время. На самом деле ты упускаешь возможности.\n\n<b>Хотя именно новые'
                                          f' действия поменяют твой уровень дохода.</b>\nВедь об этом ты'
                                          f' мечтаешь?\n\nИгра для тебя закрывается❌\n\n<b>Откладывать – это твоя стратегия'
                                          f' по жизни, и поэтому ты не зарабатываешь столько, сколько'
                                          f' хочешь.</b>\nПодумай об этом...', parse_mode='HTML')
        bot.send_message(message.chat.id, 'Следи за обновлениями в канале @granovskaya_prodengi и может быть'
                                          ' тебе выпадет шанс пройти <b>Игру</b>💎 ещё раз…\n\nДо встречи!', parse_mode='HTML')
        cur.execute(f"""UPDATE users_demo SET ban={1} WHERE userid={message.from_user.id}""")
        conn.commit()
    except ApiTelegramException:
        pass


def script1_1_2(message):
    try:
        if message.text == 'Продолжить дальше спать':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Взять трубку')
            kb.add(btn)

            bot.send_message(message.chat.id, 'Вы отклонили звонок.')
            msg = bot.send_message(message.chat.id, '👩🏻‍💼: – Да возьми трубку, ну сколько можно! Поди с агентства'
                                                    ' звонят. Дай Бог взяли тебя.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_1_21)
        elif message.text == 'Взять трубку':
            script1_1_21(message)
        else:
            bot.register_next_step_handler(message, script1_1_2)
    except ApiTelegramException:
        pass


def script1_1_21(message):
    try:
        if message.text == 'Взять трубку':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='А может быть вам и Reels снять?')
            btn2 = types.KeyboardButton(text='А как вы выбрали работать именно со мной?')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '🤵🏼‍♂️: — Доброе утро. Я посмотрел ваш профиль, ну меня если'
                                                    ' честно не зацепило. Но я готов с вами поработать бартером:'
                                                    ' вы мне съемки, я вам отметку. А вам + несколько сотен новых'
                                                    ' заказчиков.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_1_3)
        else:
            bot.register_next_step_handler(message, script1_1_21)
    except ApiTelegramException:
        pass


def script1_1_3(message):
    try:
        if message.text in ['А может быть вам и Reels снять?', 'А как вы выбрали работать именно со мной?']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Купить новую')
            btn2 = types.KeyboardButton(text='Попросить мамину')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '…Телефон выключился.\n\nУ вас заряжалась всю ночь камера.\n\nА'
                                                    ' купить вторую зарядку, чтобы ставить с телефоном одновременно'
                                                    ' — <b>руки не доходят.</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_1_4)
        else:
            bot.register_next_step_handler(message, script1_1_3)
    except ApiTelegramException:
        pass


def script1_1_4(message):
    try:
        if message.text in ['Купить новую', 'Попросить мамину']:
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='рассказать, кто звонил')
            kb.add(btn)

            file = open('data/1-1.jpg', 'rb')
            bot.send_message(message.chat.id, '🔺 Вы спустились вниз.')
            msg = bot.send_photo(message.chat.id, file, f'👩🏻‍💼: – {info[3]}, тебе из агентства звонили? Тебя взяли?', reply_markup=kb)

            bot.register_next_step_handler(msg, script1_1_6)
        else:
            bot.register_next_step_handler(message, script1_1_4)
    except ApiTelegramException:
        pass


def script1_1_6(message):
    try:
        if message.text == 'рассказать, кто звонил':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='высказать, что она не права')
            btn2 = types.KeyboardButton(text='рассказать новость про повышение')
            kb.add(btn1, btn2)

            file = open('data/6.jpg', 'rb')
            bot.send_message(message.chat.id, '– Нет, мне…')
            time.sleep(1)
            bot.send_message(message.chat.id, '👩🏻‍💼: – А я уж надеялась, что устроишься в место получше!\n\n'
                                              'Только и делаешь, что помогаешь всем на входе… Не то, что твоё окружение… '
                                              'Инфобизнесменами все стали… Блогерами…\n\nА ты? <b>Просто в шапке профиля'
                                              ' написал, что фотограф, но даже сторис выставить боишься.</b>', parse_mode='HTML')
            time.sleep(1)
            msg = bot.send_photo(message.chat.id, file, '– Мам! Хватит!', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_1_9)
        else:
            bot.register_next_step_handler(message, script1_1_6)
    except ApiTelegramException:
        pass


def script1_1_9(message):
    try:
        if message.text == 'высказать, что она не права':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Вот и почему мы вместо Москвы переехали сюда?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/7.jpg', 'rb'), '— Мам, ну Питер такой серый, меня абсолютно'
                                                                            ' не вдохновляет на дорогие съемки. Все только'
                                                                            ' пьют чай и красивые улицы фоткают. 😼 \n<b>А я'
                                                                            ' хочу движения, хочу вперед!</b>'
                                                                            , reply_markup=kb, parse_mode='HTML')

            bot.register_next_step_handler(msg, script1_1_10)
        elif message.text == 'рассказать новость про повышение':
            script1_1_11(message)
        else:
            bot.register_next_step_handler(message, script1_1_9)
    except ApiTelegramException:
        pass


def script1_1_10(message):
    try:
        if message.text == 'Вот и почему мы вместо Москвы переехали сюда?':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='остановить маму, пока не поздно')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'👵🏻 — {info[3]}, это культурная столица! <b>А ты уже сколько лет'
                                                    f' на одном месте топчешься!?\n\n😔 Я хочу, чтобы ты хорошие деньги'
                                                    f' зарабатывал, а не творил из вдохновения.</b>\n\nВот в агентство'
                                                    f' бы попал…', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_1_11)
        else:
            bot.register_next_step_handler(message, script1_1_10)
    except ApiTelegramException:
        pass


def script1_1_11(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='улыбнуться маме')
        kb.add(btn)

        msg = bot.send_message(message.chat.id, '— Да мам, на самом деле плевать на это агентство уже.'
                                                ' Ко мне на съемки пришел блогер-миллионник!', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_1_12)
    except ApiTelegramException:
        pass


def script1_1_12(message):
    try:
        if message.text == 'улыбнуться маме':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='соврать маме')
            btn2 = types.KeyboardButton(text='сказать правду')
            kb.add(btn1, btn2)

            bot.send_photo(message.chat.id, open('data/1-1.jpg', 'rb'), '— Серьезно?!')
            time.sleep(1)
            bot.send_message(message.chat.id, '— Ко мне теперь столько клиентов с отметки придет!'
                                              ' 🤑 И для них чек <b>в 3 раза повышу уже!</b>\n\nЧто скажешь?', parse_mode='HTML')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, f'👩🏻‍💼: — {info[3]}, а с чего вдруг тебе такое предложили?? 🤔 \nТы же 10 лет только знакомых'
                                                    f' фоткал...', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_1_14)
        else:
            bot.register_next_step_handler(message, script1_1_12)
    except ApiTelegramException:
        pass


def script1_1_14(message):
    try:
        if message.text == 'соврать маме':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Пойти за мамой')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/mem1.png', 'rb'), '– Мне сказали, что мои работы впечатляют.\n\n'
                                                                         '🥲 <b>Ты же знаешь, как я много всего делаю.'
                                                                         ' Каждый день работаю как за троих.</b>', parse_mode='HTML')
            msg = bot.send_message(message.chat.id, '👩🏻‍💼:– Ну пойдем завтракать! Горжусь тобой!', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_1_16)
        elif message.text == 'сказать правду':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Пойти за мамой')
            kb.add(btn)

            bot.send_message(message.chat.id, '— Ой, да у меня телефон сел на этом моменте.\n\n'
                                              '<b>У меня все нет времени зарядку новую купить.</b>', parse_mode='HTML')
            bot.send_message(message.chat.id, '👩🏻‍💼: — Держи мою. И пойдём кофе пить ☺️', reply_markup=kb)
            script1_1_16(message)
        else:
            bot.register_next_step_handler(message, script1_1_14)
    except ApiTelegramException:
        pass


def script1_1_16(message):
    try:
        if message.text == 'Пойти за мамой':
            bot.send_message(message.chat.id, '🔺 Вы ушли пить кофе с мамой.\n Поставили телефон на зарядку, и…\n\n…увидели новое сообщение')
            time.sleep(1)
            bot.send_photo(message.chat.id, open('data/8 (1).jpg', 'rb'), '🔺 Вы упустили 10 клиента за месяц')
            time.sleep(1)
            bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'), '🔺 Вам нужно позвонить друзьям и спросить, как подняться.')
            t1_1 = threading.Timer(3, day_2, [message])  # 15h
            t1_1.start()
            #day_2(message)
        else:
            bot.register_next_step_handler(message, script1_1_16)
    except ApiTelegramException:
        pass


def day_2(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Даа, что там дальше?')
        kb.add(btn)
        msg = bot.send_message(message.chat.id, f'{info[3]}, привет! Продолжаем играть в деньги?', reply_markup=kb)

        if info[4] == 1:
            bot.register_next_step_handler(msg, script1_2_2)
        elif info[4] == 2:
            bot.register_next_step_handler(msg, script2_2_1)
        elif info[4] == 3:
            bot.register_next_step_handler(msg, script3_2_2, [message.text])
    except ApiTelegramException:
        pass


def script1_2_2(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Быстро допить кофе, восстановить ресурс')
        btn2 = types.KeyboardButton(text='Не допивать кофе, убежать сразу')
        kb.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, 'Вы скорее хотите позавтракать, чтобы встретиться'
                                                ' с крупным клиентом.', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_2_3)
    except ApiTelegramException:
        pass


def script1_2_3(message):
    try:
        if message.text in ['Быстро допить кофе, восстановить ресурс', 'Не допивать кофе, убежать сразу']:
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Сказать маме, что торопишься')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'👵🏻: – {info[3]}, как я все-таки рада, что что-то поменялось в'
                                                    f' твоей жизни! Я блинчики испекла, давай перекусим?', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_4)
        else:
            bot.register_next_step_handler(message, script1_2_3)
    except ApiTelegramException:
        pass


def script1_2_4(message):
    try:
        if message.text == 'Сказать маме, что торопишься':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='порадоваться за себя')
            kb.add(btn)

            bot.send_message(message.chat.id, '– Мам, я тороплюсь! Надо еще встретиться с тем блогером.')
            bot.send_message(message.chat.id, '👵🏻: – А как же твой курс по продажам через диалоги, который ты купил'
                                              ' в рассрочку?\nПомню твои слова, что сегодня наконец-то начнешь'
                                              ' смотреть его.')
            time.sleep(1)
            msg = bot.send_photo(message.chat.id, open('data/mem8.jpg', 'rb'), '– <b>А зачем он мне?</b>\n\n'
                                                                               '😉 Клиент теперь есть,\n'
                                                                               'а курс потом посмотрю!', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_7)
        else:
            bot.register_next_step_handler(message, script1_2_4)
    except ApiTelegramException:
        pass


def script1_2_7(message):
    try:
        if message.text == 'порадоваться за себя':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='напомнить маме, что торопишься')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/26.jpg', 'rb'), f'–👵🏻: …{info[3]}, ты знаешь, что мы с'
                                                    f' папой уже как 30 лет переехали'
                                                    f' из Челябинска в Питер.\n<b>Жить в культурной столице – это мечта всех'
                                                    f' наших друзей! 🫢 И только мы ее исполнили.</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_8)
        else:
            bot.register_next_step_handler(message, script1_2_7)
    except ApiTelegramException:
        pass


def script1_2_8(message):
    try:
        if message.text == 'напомнить маме, что торопишься':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='дослушать маму')
            btn2 = types.KeyboardButton(text='бежать к новому клиенту')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '– Мам, мне бежать надо.\n\n🥴 А в этой столице нет'
                                                    ' никаких перспектив, как оказалось.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_9)
        else:
            bot.register_next_step_handler(message, script1_2_8)
    except ApiTelegramException:
        pass


def script1_2_9(message):
    try:
        if message.text in ['дослушать маму', 'бежать к новому клиенту']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='напомнить маме, что твоя жизнь тоже сейчас поменяется')
            kb.add(btn)
            bot.send_message(message.chat.id, '– Ну постой...')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '– Папа тогда купил крупную франшизу.\n\n😱 <b>Он наконец-то быстро принял'
                                                    ' решение сам, несмотря на то, что все ему говорили'
                                                    ' не вкладываться.</b>\n\nИ это выстрелило!\n\n😉 <b>Без тех действий так бы мы'
                                                    ' и сидели</b> в Челябинске на 35 тысяч в месяц.'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_10)
        else:
            bot.register_next_step_handler(message, script1_2_9)
    except ApiTelegramException:
        pass


def script1_2_10(message):
    try:
        if message.text == 'напомнить маме, что твоя жизнь тоже сейчас поменяется':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='разобраться с мамой')
            btn2 = types.KeyboardButton(text='уйти от разговора')
            kb.add(btn1, btn2)

            bot.send_message(message.chat.id, '<b>— Мам, моя жизнь сейчас изменилась.\n\n 🙏🏻 Я дальше продолжу делать то, что'
                                              ' делаю.</b>\n\nИ тоже буду жить богато.\nПерееду в Москву из этой пещеры!', parse_mode='HTML')
            time.sleep(1)
            msg = bot.send_photo(message.chat.id, open('data/mem9.jpg', 'rb'), f'— Но {info[3]}, не в Питере дело…\n\n'
                                                                               f'<b>Разве за это время ты сделал то,'
                                                                               f' что не делал раньше? 🤔 Что-то новое?</b>'
                                                                                , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_12)
        else:
            bot.register_next_step_handler(message, script1_2_10)
    except ApiTelegramException:
        pass


def script1_2_12(message):
    try:
        if message.text == 'разобраться с мамой':

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='убежать')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '—🙄 Мам, вообще-то мною прочитаны две книги по кратному росту в доходе', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_12_2)
        elif message.text == 'уйти от разговора':
            script1_2_12_2(message)
        else:
            bot.register_next_step_handler(message, script1_2_12)
    except ApiTelegramException:
        pass


def script1_2_12_2(message):
    try:
        if message.text in ['уйти от разговора', 'убежать']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='взять трубку')
            kb.add(btn)

            bot.send_message(message.chat.id, '– Все, мам, меня нет 🫣\n\n🙏🏻 Бегу на встречу. Видишь, не зря мы денежную'
                                              ' свечу на выходных зажигали…\n\n🕯 <b>Теперь будут деньги!</b>', parse_mode='HTML')
            bot.send_video(message.chat.id, open('data/vid4.mov', 'rb'), timeout=100, height=1920, width=1080)
            bot.send_message(message.chat.id, '🔺 Вы выходите на улицу.\nЕдете по своему району под любимую песню.\n'
                                              'До места встречи здесь недалеко.')
            msg = bot.send_message(message.chat.id, 'Ваш телефон зазвонил.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_15)
        else:
            bot.register_next_step_handler(message, script1_2_12_2)
    except ApiTelegramException:
        pass


def script1_2_15(message):
    try:
        if message.text == 'взять трубку':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='согласиться')
            btn2 = types.KeyboardButton(text='проанализировать, правильно ли я поступаю')

            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, f'👩🏻‍🦳: – Добрый день, это вы {info[3]}, фотограф?\n\nБыла на вас'
                                                    f' подписана года два, ничего не знала. А тут вы сторис выставили…\n\n'
                                                    f'🙏🏻 Можете меня на индивидуальное менторство по фотографии взять?\n\n'
                                                    f'☺️ <b>Я в Москву еду на ивент фотографов, у нас там постоянно движ\n\n'
                                                    f'Хочу тоже сотрудничать с селебами!</b> Готова любые деньги платить.\n'
                                                    f'🥺 Возьмете?', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_16)
        else:
            bot.register_next_step_handler(message, script1_2_15)
    except ApiTelegramException:
        pass


def script1_2_16(message):
    try:
        if message.text == 'согласиться':
            bot.send_message(message.chat.id, '– Да, здравствуйте! Могу взять.\n\nПо цене чуть позже перезвоню.')
            bot.send_photo(message.chat.id, open('data/mem10.JPG', 'rb'), '🔺 Вы согласились работать и фотографом, и ментором.')
            script1_2_18(message)
        elif message.text == 'проанализировать, правильно ли я поступаю':
            script1_2_18(message)
        else:
            bot.register_next_step_handler(message, script1_2_16)
    except ApiTelegramException:
        pass


def script1_2_18(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='сразу рассказать клиентке о своих возможностях')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/27.jpg', 'rb'), '– Это получается раньше я так, часика три на съемки тратил\n\n'
                                                                         '🤔 А сейчас придется полный день работать!\n\n'
                                                                         'Еще и дополнительно заниматься после…\n\n'
                                                                         '😳 <b>У меня же так никакого времени не хватит…</b>'
                                                                          , reply_markup=kb, parse_mode='HTML')
        bot.register_next_step_handler(msg, script1_2_20)
    except ApiTelegramException:
        pass


def script1_2_20(message):
    try:
        if message.text == 'сразу рассказать клиентке о своих возможностях':

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Посмотреть')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/mem6.JPG', 'rb'), '– Я сейчас думаю, что мне трудно будет вас взять.\n\n'
                                                                         '😮‍ 💨<b>Постоянно в работе, дел полно.</b>\n\n'
                                                                         'Я подумаю, как с вами успевать, но пока держу'
                                                                         ' вас в курсе.', parse_mode='HTML')
            time.sleep(1)
            bot.send_message(message.chat.id, '👩🏻‍🦳: – Как это? Жаль…\n\nПоняла вас, ну попробуйте подумать, да.'
                                              '\n\nЯ на связи. До свидания')
            time.sleep(1)
            bot.send_photo(message.chat.id, open('data/mem10.JPG', 'rb'), 'Вы не стали ментором.')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, 'Вам пришло новое уведомление.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_24)
        else:
            bot.register_next_step_handler(message, script1_2_20)
    except ApiTelegramException:
        pass


def script1_2_24(message):
    try:
        if message.text == 'Посмотреть':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Проигнорировать сообщение')
            btn2 = types.KeyboardButton(text='Посмотреть, что за книга')

            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/28.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_25)
        else:
            bot.register_next_step_handler(message, script1_2_24)
    except ApiTelegramException:
        pass


def script1_2_25(message):
    try:
        if message.text == 'Проигнорировать сообщение':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='посмотреть')
            kb.add(btn)
            bot.send_message(message.chat.id, '– Фух, достали со своими рассылками.\n\n🫠 Я и так на стрессе, а книга мне'
                                              ' явно не поможет больше успевать.\n\n<b>Но как себя разгружать, не понимаю…</b>', parse_mode='HTML')
            msg = bot.send_message(message.chat.id, 'Вам пришло новое уведомление.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_27)
        elif message.text == 'Посмотреть, что за книга':
            script1_2_00(message)
        else:
            bot.register_next_step_handler(message, script1_2_25)
    except ApiTelegramException:
        pass


def script1_2_27(message):
    try:
        if message.text == 'посмотреть':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='купить')
            btn2 = types.KeyboardButton(text='проигнорировать')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/29.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_2831)
        else:
            bot.register_next_step_handler(message, script1_2_27)
    except ApiTelegramException:
        pass


def script1_2_2831(message):
    try:
        if message.text == 'купить':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='купить денежные свечи')
            btn2 = types.KeyboardButton(text='постоять на гвоздях')
            btn3 = types.KeyboardButton(text='купить книгу для личностного роста')
            kb.add(btn1, btn2, btn3)

            bot.send_message(message.chat.id, '🔺 Вы потратили 1/3 месячной зарплаты на денежную медитацию.')
            bot.send_photo(message.chat.id, open('data/IMG_6212.PNG', 'rb'), '– Надо срочно все менять, чтобы жить лучше. Нынешние'
                                              ' события – знак. 😶‍🌫️ Такие медитации – это шаг вперед. <b>Прошлая вон как'
                                              ' сработала!</b>', parse_mode='HTML')
            msg = bot.send_message(message.chat.id, '🔺 Вы задумались, что еще сделать для улучшения жизни', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_sgk)
        elif message.text == 'проигнорировать':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='купить еще денежные свечи')
            btn2 = types.KeyboardButton(text='подумать про свой личностный рост')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/IMG_6212.PNG', 'rb'), '– Надо срочно все менять, чтобы жить лучше.\n\n'
                                                    '😶‍🌫️Нынешние события – знак.\n<b>Чем больше для своего ресурса'
                                                    ' я сделаю, тем лучше я справлюсь.</b>\n\nМедитации мне не'
                                                    ' помогут. А вот после денежной свечи меня повысили!🕯🙏🏻', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_2_3200)
        else:
            bot.register_next_step_handler(message, script1_2_2831)
    except ApiTelegramException:
        pass


def script1_2_sgk(message):
    try:
        if message.text == 'купить денежные свечи':
            script1_2_s(message)

        elif message.text == 'постоять на гвоздях':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='купить еще денежные свечи')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '🔺 Вы потратили 1/3 месячной зарплаты на сеанс'
                                                    ' гвоздей в Питере.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_2_s)

        elif message.text == 'купить книгу для личностного роста':
            script1_2_00(message)
    except ApiTelegramException:
        pass


def script1_2_s(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Это знак Вселенной, купить!')
        btn2 = types.KeyboardButton(text='Для начала нужно полистать и понять, реально ли она будет полезна')
        kb.add(btn1, btn2)

        bot.send_message(message.chat.id, '🔺 Вы потратили 1/4 месячной зарплаты на лучшие денежные свечи в Питере.')
        msg = bot.send_photo(message.chat.id, open('data/30.jpg', 'rb'), 'В месте, где покупали свечи,'
                                                ' вы увидели ту самую книгу по тайм-менеджменту.', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_2_34)
    except ApiTelegramException:
        pass


def script1_2_3200(message):
    try:
        if message.text == 'купить еще денежные свечи':
            script1_2_s(message)
        elif message.text == 'подумать про свой личностный рост':
            script1_2_00(message)
    except ApiTelegramException:
        pass


def script1_2_00(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Это знак Вселенной, купить!')
        btn2 = types.KeyboardButton(text='Для начала нужно полистать и понять, реально ли она будет полезна')
        kb.add(btn1, btn2)

        msg = bot.send_photo(message.chat.id, open('data/30.jpg', 'rb'), 'Вы приехали в магазин и увидели ту самую'
                                                ' книгу по тайм-менеджменту.', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_2_34)
    except ApiTelegramException:
        pass


def script1_2_34(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Ответить')
        kb.add(btn)

        bot.send_message(message.chat.id, '🔺 Вы пролистали первые 5 страниц книги и поняли, что здесь дельные инсайты.')
        time.sleep(1)
        bot.send_message(message.chat.id, '🔺 Вы потратили на книгу для личностного роста 1/4 месячной зарплаты.')
        time.sleep(1)
        msg = bot.send_photo(message.chat.id, open('data/IMG_6211.JPG', 'rb'), 'Ваш телефон зазвонил.', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_2_37)
    except ApiTelegramException:
        pass


def script1_2_37(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Начать тревожиться')
        btn2 = types.KeyboardButton(text='Проявить силу перед обстоятельствами')
        kb.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, '👨🏻‍💼: Здравствуйте, это Тинькофф-банк.\n\nСегодня последний день, когда'
                                                ' можно закрыть рассрочку без процентов.\n\n❗️<b>На вашей'
                                                ' карте недостаточно средств</b>', reply_markup=kb, parse_mode='HTML')
        bot.register_next_step_handler(msg, script1_2_38)
    except ApiTelegramException:
        pass


def script1_2_38(message):
    try:
        if message.text in ['Начать тревожиться', 'Проявить силу перед обстоятельствами']:
            bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'))
            t1_2 = threading.Timer(3, day_3, [message]) #20h
            t1_2.start()
            #time.sleep(72000)
            #day_3(message)
    except ApiTelegramException:
        pass


def day_3(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Даа, что там дальше?')
        kb.add(btn)

        msg = bot.send_message(message.chat.id, f'{info[3]}, привет! Продолжаем играть в деньги?', reply_markup=kb)

        if info[4] == 1:
            bot.register_next_step_handler(msg, script1_3_2, [message.text])
        elif info[4] == 2:
            bot.register_next_step_handler(msg, script2_3_2)
        elif info[4] == 3:
            bot.register_next_step_handler(msg, script3_3_2)
    except ApiTelegramException:
        pass


def script1_3_2(message, last_message):
    try:
        if last_message[0] == 'Начать тревожиться':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Попросить друзей занять денег')
            btn2 = types.KeyboardButton(text='Спросить денег у родителей')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '– Боже, у меня из головы вылетела эта рассрочка!'
                                                    '\n\nКак ее погашать?', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_3_ps)
        elif last_message[0] == 'Проявить силу перед обстоятельствами':
            script1_3_3(message)
    except ApiTelegramException:
        pass


def script1_3_ps(message):
    try:
        if message.text == 'Попросить друзей занять денег':
            script1_3_3(message)
        elif message.text == 'Спросить денег у родителей':
            script1_3_4(message)
        else:
            bot.register_next_step_handler(message, script1_3_ps)
    except ApiTelegramException:
        pass


def script1_3_3(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Спросить денег у родителей')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/IMG_6217.JPG', 'rb'), 'Вы обзвонили друзей, которые обычно вам занимают,'
                                                ' но ни у кого денег для вас нет. ', reply_markup=kb)
        bot.register_next_step_handler(msg, script1_3_4)
    except ApiTelegramException:
        pass


def script1_3_4(message):
    try:
        if message.text == 'Спросить денег у родителей':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='договориться на менторство')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '– 👴🏻 Привет, это папа. Я сейчас в автосалоне,'
                                                    ' маме новую машину берём.\n\n🫢 <b>Почти все сбережения'
                                                    ' вкладываем.</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script1_3_5)
        else:
            bot.register_next_step_handler(message, script1_3_4)
    except ApiTelegramException:
        pass


def script1_3_5(message):
    try:
        if message.text == 'договориться на менторство':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='назвать цену')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'– Здравствуйте, это {info[3]}, фотограф звезд!\n\nУ меня появилось'
                                                    f' время, могу вас взять. Это будет стоить…', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_3_6)
        else:
            bot.register_next_step_handler(message, script1_3_5)
    except ApiTelegramException:
        pass


def script1_3_6(message):
    try:
        if message.text == 'назвать цену':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Взять трубку')
            kb.add(btn)

            bot.send_message(message.chat.id, '👩🏻‍🦳: – Здравствуйте еще раз. А я подумала, что уже все, вы с концами'
                                              ' ушли.\n\n 😮‍💨 Нашла за это время другого звездного фотографа, извините.'
                                              ' <b>Мне же быстро надо решать и действовать, чтобы все получилось.</b>', parse_mode='HTML')
            time.sleep(1)
            bot.send_message(message.chat.id, '🔺 Вы потеряли хороший источник дохода.')

            msg = bot.send_photo(message.chat.id, open('data/mem6.JPG', 'rb'), 'Вам звонит ваш новый клиент-блогер.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_3_9)
        else:
            bot.register_next_step_handler(message, script1_3_6)
    except ApiTelegramException:
        pass


def script1_3_9(message):
    try:
        if message.text == 'Взять трубку':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Посмотреть')
            kb.add(btn)

            bot.send_message(message.chat.id, '🤵🏼‍♂️:– Добрый вечер, я вам позвонил недавно. Фотограф, да?\n\nМне съемку'
                                              ' предложил контент-продюсер из отличного агентства.\n\n☺️ Еще и Reels мне будет'
                                              ' создавать.\nТак перспектив больше.\n\nВы только поймите меня правильно:'
                                              ' мне блог дальше развивать надо.\n\n😒 <b>Просто фоточки недостаточно сделать,'
                                              ' мне прямо упаковка и креатив нужны.</b>\n\nИзвините, до свидания.', parse_mode='HTML')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, 'Вам пришло новое уведомление.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_3_11)
        else:
            bot.register_next_step_handler(message, script1_3_9)
    except ApiTelegramException:
        pass


def script1_3_11(message):
    try:
        if message.text == 'Посмотреть':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='попробовать денежную медитацию')
            btn2 = types.KeyboardButton(text='зажечь денежную свечу')
            btn3 = types.KeyboardButton(text='начать читать новую книгу по личностному росту')
            btn4 = types.KeyboardButton(text='узнать, что делать в такой ситуации')
            kb.add(btn1, btn2, btn3, btn4)

            bot.send_photo(message.chat.id, open('data/IMG_6222.JPG', 'rb'), 'Вам стали отвечать другие потенциальные клиенты')

            msg = bot.send_message(message.chat.id, '🔺 Вы остались без дохода.', reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_1)
    except ApiTelegramException:
        pass


def portraits_1(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Хочу узнать')
        kb.add(btn)
        time.sleep(1)
        msg = bot.send_photo(message.chat.id, open('data/75.jpg', 'rb'), f' {info[3]}, ты сыграл в деньги. Я все это время анализировала действия'
                                          f' твоего персонажа, чтобы составить твой денежный портрет.\n\nТеперь я'
                                          f' точно понимаю, где ты теряешь деньги. Поэтому знаю, где в новом'
                                          f' времени тебе их можно найти.', reply_markup=kb)
        bot.register_next_step_handler(msg, portraits_2)
    except ApiTelegramException:
        pass


def portraits_2(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Договорились!')
        kb.add(btn)

        msg = bot.send_video(message.chat.id, open('data/vidpolina3.mov', 'rb'), timeout=60, height=1920, width=1080, reply_markup=kb)

        if info[4] == 1:
            bot.register_next_step_handler(msg, script1_3_p3)
        elif info[4] == 2:
            bot.register_next_step_handler(msg, script2_3_p3)
        elif info[4] == 3:
            bot.register_next_step_handler(msg, script3_3_p3)
    except ApiTelegramException:
        pass


def portraits_5(message):
    try:
        if message.text == 'Соглашусь с тобой, Полин!':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Хочу систему для нового уровня дохода')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/73.jpg', 'rb'), 'В игре вы увидели, какие ошибки в деньгах нового времени'
                                                    ' вам лучше исправить.\n\nНо ошибки –  это следствие отсутствия системы.'
                                                    '\n\n❗️Когда есть система, то вы растете на новый финансовый масштаб'
                                                    ' регулярно. И регулярно делаете иксы в доходе.\n\n'
                                                    'Хотите такую систему своих денег?', reply_markup=kb)
            if info[4] == 1:
                bot.register_next_step_handler(msg, script1_3_p6)
            elif info[4] == 2:
                bot.register_next_step_handler(msg, script2_3_p6)
            elif info[4] == 3:
                bot.register_next_step_handler(msg, script3_3_p6)
        else:
            bot.register_next_step_handler(message, portraits_5)
    except ApiTelegramException:
        pass


def script1_3_p3(message):
    try:
        if message.text == 'Договорились!':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Как это сделать?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/67.jpg', 'rb'), f'{info[3]}, внимательно прочитай свою карточку.', reply_markup=kb)
            bot.register_next_step_handler(msg, script1_3_p4)
        else:
            bot.register_next_step_handler(message, script1_3_p3)
    except ApiTelegramException:
        pass


def script2_3_p3(message):
    try:
        if message.text == 'Договорились!':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Как это сделать?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/66 (1).jpg', 'rb'), f'{info[3]}, внимательно прочитай свою карточку.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_p4)
        else:
            bot.register_next_step_handler(message, script2_3_p3)
    except ApiTelegramException:
        pass


def script3_3_p3(message):
    try:
        if message.text == 'Договорились!':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Как это сделать?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/68.jpg', 'rb'), f'{info[3]}, внимательно прочитай свою карточку.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_3_p4)
        else:
            bot.register_next_step_handler(message, script3_3_p3)
    except ApiTelegramException:
        pass


def script1_3_p4(message):
    try:
        if message.text == 'Как это сделать?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Соглашусь с тобой, Полин!')
            kb.add(btn)

            msg = bot.send_voice(message.chat.id, open('data/gsp1.ogg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_5)
        else:
            bot.register_next_step_handler(message, script3_3_p4)
    except ApiTelegramException:
        pass


def script2_3_p4(message):
    try:
        if message.text == 'Как это сделать?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Соглашусь с тобой, Полин!')
            kb.add(btn)

            msg = bot.send_voice(message.chat.id, open('data/gsp2.ogg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_5)
    except ApiTelegramException:
        pass


def script3_3_p4(message):
    try:
        if message.text == 'Как это сделать?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Соглашусь с тобой, Полин!')
            kb.add(btn)

            msg = bot.send_voice(message.chat.id, open('data/gsp3.ogg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_5)
    except ApiTelegramException:
        pass


def script1_3_p6(message):
    try:
        if message.text == 'Хочу систему для нового уровня дохода':
            kb = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text='Загрузить в лабиринт', url='https://denginovogovremeni.com/')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/67.jpg', 'rb'), 'Это твой денежный портрет. Благодаря нему'
                                                                       ' ты получаешь пропуск к выходу из лабиринта.\n\n'
                                                                       '⚡️ Нажми на кнопку ниже, чтобы наконец-то '
                                                                       'получить систему Денег Нового Времени:', reply_markup=kb)
            '''конец 3 дня 1 сцеария'''
            t1_3 = threading.Timer(3, day4_1, [message])  # 15h
            t1_3.start()
            #time.sleep(72000)  # 20h
            #day4_1(message)
    except ApiTelegramException:
        pass


def script2_3_p6(message):
    try:
        if message.text == 'Хочу систему для нового уровня дохода':
            kb = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text='Загрузить в лабиринт', url='https://denginovogovremeni.com/')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/66 (1).jpg', 'rb'), 'Это твой денежный портрет. Благодаря нему'
                                                                       ' ты получаешь пропуск к выходу из лабиринта.\n\n'
                                                                       '⚡️ Нажми на кнопку ниже, чтобы наконец-то '
                                                                       'получить систему Денег Нового Времени:', reply_markup=kb)
            #time.sleep(72000) #20h
            #day4_1(message)
            t2_3 = threading.Timer(3, day4_1, [message])  # 15h
            t2_3.start()
    except ApiTelegramException:
        pass


def script3_3_p6(message):
    try:
        if message.text == 'Хочу систему для нового уровня дохода':
            kb = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text='Загрузить в лабиринт', url='https://denginovogovremeni.com/')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/68.jpg', 'rb'), 'Это твой денежный портрет. Благодаря нему'
                                                                       ' ты получаешь пропуск к выходу из лабиринта.\n\n'
                                                                       '⚡️ Нажми на кнопку ниже, чтобы наконец-то '
                                                                       'получить систему Денег Нового Времени:', reply_markup=kb)
            #time.sleep(72000)  # 20h
            #day4_1(message)
            t3_3 = threading.Timer(3, day4_1, [message])  # 15h
            t3_3.start()
    except ApiTelegramException:
        pass


def script2_1_2(message):
    try:
        if message.text == 'пойти':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='найти новых партнеров для запусков')
            btn2 = types.KeyboardButton(text='преодолеть страх проявления, поделиться новыми кейсами')
            btn3 = types.KeyboardButton(text='интересно провести время с Десяткой')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/11.jpg', 'rb'), '🔺 Вы вызвали такси и поехали на встречу'
                                                    '\nЧто для вас важно будет сделать там <b>в первую очередь?</b>'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_3_1)
        elif message.text == 'не пойти':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='кальянная')
            btn2 = types.KeyboardButton(text='коворкинг')
            btn3 = types.KeyboardButton(text='кофейня')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_message(message.chat.id, '🔺 Вы решили <b>отказаться</b> от встречи с Десяткой.\n\n'
                                                    'Тогда куда пойдете сегодня вечером?', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_3_2)
    except ApiTelegramException:
        pass


def script2_1_3_1(message):
    try:
        if message.text in ['найти новых партнеров для запусков',
                            'преодолеть страх проявления, поделиться новыми кейсами',
                            'интересно провести время с Десяткой']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='заказать кальян')
            btn2 = types.KeyboardButton(text='созвониться перед встречей с командой по запуску')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/12.jpg', 'rb'), '🔺 О, а вот и место встречи. Вы приехали раньше остальных.',
                                   reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_4_1)
        else:
            bot.register_next_step_handler(message, script2_1_3_1)
    except ApiTelegramException:
        pass


def script2_1_4_1(message):
    try:
        if message.text == 'заказать кальян':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у эксперта про его состояние')
            btn2 = types.KeyboardButton(text='настроить Геткурс с техспецом')
            btn3 = types.KeyboardButton(text='сверить с копирайтером план прогрева')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/13.jpg', 'rb'), 'Пока вы ждете свою Десятку, нужно поработать.'
                                                    '\n\nСкоро запуск с планом по выручке в 5 миллионов.\n\n'
                                                    '<b>Что сейчас важно сделать?</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_5)
        elif message.text == 'созвониться перед встречей с командой по запуску':
            script2_1_5(message)
        else:
            bot.register_next_step_handler(message, script2_1_4_1)
    except ApiTelegramException:
        pass


def script2_1_3_2(message):
    try:
        if message.text == 'кальянная':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='заказать кальян')
            btn2 = types.KeyboardButton(text='созвониться с командой по запуску')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/12.jpg', 'rb'), '🔺 Вы на месте.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_4_2)

        elif message.text == 'коворкинг':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='выпить энергетик')
            btn2 = types.KeyboardButton(text='созвониться с командой по запуску')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/15.jpg', 'rb'), '🔺 Вы на месте.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_4_2)

        elif message.text == 'кофейня':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='заказать кофе')
            btn2 = types.KeyboardButton(text='созвониться с командой по запуску')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/14.jpg', 'rb'), '🔺 Вы на месте.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_4_2)
        else:
            bot.register_next_step_handler(message, script2_1_3_2)
    except ApiTelegramException:
        pass


def script2_1_4_2(message):
    try:
        if message.text == 'заказать кальян':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у эксперта про его состояние')
            btn2 = types.KeyboardButton(text='настроить Геткурс с техспецом')
            btn3 = types.KeyboardButton(text='сверить с копирайтером план прогрева')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/13.jpg', 'rb'), 'Скоро запуск с планом'
                                                    ' по выручке в 5 миллионов.\n\n'
                                                    ' <b>Что сейчас важно сделать?</b>?', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_5)

        elif message.text == 'выпить энергетик':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у эксперта про его состояние')
            btn2 = types.KeyboardButton(text='настроить Геткурс с техспецом')
            btn3 = types.KeyboardButton(text='сверить с копирайтером план прогрева')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/16.jpg', 'rb'), 'Скоро запуск с планом'
                                                    ' по выручке в 5 миллионов. <b>\n\nЧто сейчас важно сделать?</b>'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_5)

        elif message.text == 'заказать кофе':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у эксперта про его состояние')
            btn2 = types.KeyboardButton(text='настроить Геткурс с техспецом')
            btn3 = types.KeyboardButton(text='сверить с копирайтером план прогрева')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/17.jpg', 'rb'), ' Скоро запуск с планом'
                                                    ' по выручке в 5 миллионов.\n\n<b>Что сейчас'
                                                    ' важно сделать?</b>', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_5)

        elif message.text == 'созвониться с командой по запуску':
            script2_1_5(message)

        else:
            bot.register_next_step_handler(message, script2_1_4_2)
    except ApiTelegramException:
        pass


def script2_1_5(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='поздороваться с Викой')
        kb.add(btn)

        bot.send_message(message.chat.id, '🔺 К вам подошла девушка.')
        msg = bot.send_message(message.chat.id, '👩🏻: — Привет, можно тебя отвлечь?\n\nУслышала, как ты работаешь,'
                                                ' вспомнила тебя.\n\nМы же с тобой были в одной Десятке, помнишь?\n\n'
                                                '😉 Я Вика, у меня свой секс шоп', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_1_6)
    except ApiTelegramException:
        pass


def script2_1_6(message):
    try:
        if message.text == 'поздороваться с Викой':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='соврать')
            btn2 = types.KeyboardButton(text='сказать правду')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, f'👩🏻: – Расскажи, как у тебя дела, {info[3]}? Все'
                                                    f' хорошо?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_7)
        else:
            bot.register_next_step_handler(message, script2_1_6)
    except ApiTelegramException:
        pass


def script2_1_7(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='спросить у Вики, где найти клиентов в ее нише')
        btn2 = types.KeyboardButton(text='поинтересоваться, как дела у Вики')
        kb.add(btn1, btn2)
        if message.text == 'сказать правду':
            msg = bot.send_photo(message.chat.id, open('data/18.jpg', 'rb'), '– Если честно, у меня сейчас неопределенность.'
                                                    ' Вроде делаю хорошо, деньги есть, <i>но масштаба нет.</i>\n\nХочу дальше,'
                                                    ' делаю новые действия, меняю гипотезы, а как лучше'
                                                    ' – не знаю.', reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_8)
        elif message.text == 'соврать':
            msg = bot.send_message(message.chat.id, '– ☺️Да все потрясающе! У меня сейчас вообще никаких проблем'
                                                    ' нет, делаю миллионы, постоянно расту.\n\nКаждое новое действие'
                                                    ' приводит к росту в доходе.\n\nВ общем, лучший специалист'
                                                    ' на рынке!🫰🏻', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_8)
        else:
            bot.register_next_step_handler(message, script2_1_7)
    except ApiTelegramException:
        pass


def script2_1_8(message):
    try:
        if message.text in ['спросить у Вики, где найти клиентов в ее нише', 'поинтересоваться, как дела у Вики']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='поинтересоваться у Вики, о чем она')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/mem2.png', 'rb'), '👩🏻: – Мы недавно сделали оборот в 700 тысяч за месяц.'
                                                    '\n\nЗнаю, не густо, но я поэтому к тебе и пришла. Это даже больше,'
                                                    ' чем просто клиенты.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_9)
        else:
            bot.register_next_step_handler(message, script2_1_8)
    except ApiTelegramException:
        pass


def script2_1_9(message):
    try:
        if message.text == 'поинтересоваться у Вики, о чем она':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Что ты предлагаешь?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/mem3.jpg', 'rb'), '👩🏻: – У меня есть свой офис и куча связей, большой капитал.'
                                                    ' А у тебя – крутой потенциал.\n\nЯ слышала, что о тебе говорят на рынке.'
                                                    '\n\nХочу, чтобы мы сделали прорыв.'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script2_1_10)
        else:
            bot.register_next_step_handler(message, script2_1_9)
    except ApiTelegramException:
        pass


def script2_1_10(message):
    try:
        if message.text == 'Что ты предлагаешь?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='согласиться и заключить договор')
            btn2 = types.KeyboardButton(text='сказать, что тебе нужно время')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/19.jpg', 'rb'), '👩🏻: — Давай откроем свое агентство. И будем партнерами. '
                                                    'Выручку делим 50/50.\n\nЧто скажешь?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_11_12)
        else:
            bot.register_next_step_handler(message, script2_1_10)
    except ApiTelegramException:
        pass


def script2_1_11_12(message):
    try:
        if message.text == 'согласиться и заключить договор':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='подписать договор')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '– Мне долго думать не надо, я за любой движ.\n'
                                                    'Давай договор на совместное ООО.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_12_1)

        elif message.text == 'сказать, что тебе нужно время':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='попросить у Вики 3 дня')
            btn2 = types.KeyboardButton(text='попросить у Вики неделю')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '– Слушай, так резко я не могу, нужно все взвесить.'
                                                    ' Дай мне время на подумать🤔', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_12_2)
        else:
            bot.register_next_step_handler(message, script2_1_11_12)
    except ApiTelegramException:
        pass


def script2_1_12_1(message):
    try:
        if message.text == 'подписать договор':
            bot.send_message(message.chat.id, '🔺 Вы только что открыли свое агентство.')
            script2_1_15(message)
        else:
            bot.register_next_step_handler(message, script2_1_12_1)
    except ApiTelegramException:
        pass


def script2_1_12_2(message):
    try:
        if message.text in ['попросить у Вики 3 дня', 'попросить у Вики неделю']:
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Что предлагаешь, Вика?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'👩🏻: – Это очень много, {info[3]}. Ты на самом деле уже все знаешь,'
                                                    f' просто боишься новых действий…', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_13)
        else:
            bot.register_next_step_handler(message, script2_1_12_2)
    except ApiTelegramException:
        pass


def script2_1_13(message):
    try:
        if message.text == 'Что предлагаешь, Вика?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Попробовать поработать с Викой')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/20.jpg', 'rb'), '– Давай мы с тобой попробуем. Всегда же можем расторгнуть'
                                                    ' договор, если не выйдет.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_14)
        else:
            bot.register_next_step_handler(message, script2_1_13)
    except ApiTelegramException:
        pass


def script2_1_14(message):
    try:
        if message.text == 'Попробовать поработать с Викой':
            bot.send_message(message.chat.id, '🔺 Вы только что открыли свое агентство.')
            time.sleep(1)
            script2_1_15(message)
        else:
            bot.register_next_step_handler(message, script2_1_14)
    except ApiTelegramException:
        pass


def script2_1_15(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='3 месяца')
        btn2 = types.KeyboardButton(text='полгода')
        btn3 = types.KeyboardButton(text='1 год')
        btn4 = types.KeyboardButton(text='1,5 года')
        kb.add(btn1, btn2, btn3, btn4)

        msg = bot.send_message(message.chat.id, 'Сколько времени вы даете агентству'
                                                ' на испытательный срок?', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_1_16)
    except ApiTelegramException:
        pass


def script2_1_16(message):
    try:
        if message.text == '3 месяца':
            bot.send_message(message.chat.id, '🔺 Прошло 3 месяца с открытия общего бизнеса с Викой.\n'
                                              'В основном вы работаете с привлечением трафика для секс-шопов.\n'
                                              '<i>Вам это стало надоедать.</i>', parse_mode='HTML')
            script2_1_16_0(message)
        elif message.text == 'полгода':
            bot.send_message(message.chat.id, '🔺 Прошло 6 месяцев с открытия общего бизнеса с Викой.\n'
                                              'В основном вы работаете с привлечением трафика для секс-шопов.\n'
                                              '<i>Вам это стало надоедать.</i>', parse_mode='HTML')
            script2_1_16_0(message)
        elif message.text == '1 год':
            bot.send_message(message.chat.id, '🔺 Прошел год с открытия общего бизнеса с Викой.\n'
                                              'В основном вы работаете с привлечением трафика для секс-шопов.\n'
                                              '<i>Вам это стало надоедать.</i>', parse_mode='HTML')
            script2_1_16_0(message)
        elif message.text == '1,5 года':
            bot.send_message(message.chat.id, '🔺 Прошло 1,5 года с открытия общего бизнеса с Викой.\n'
                                              'В основном вы работаете с привлечением трафика для секс-шопов.\n'
                                              '<i>Вам это стало надоедать.</i>', parse_mode='HTML')
            script2_1_16_0(message)
        else:
            bot.register_next_step_handler(message, script2_1_16)
    except ApiTelegramException:
        pass


def script2_1_16_0(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='обсудить с Викой привлечение других клиентов')
        btn2 = types.KeyboardButton(text='разозлиться на Вику')
        kb.add(btn1, btn2)

        time.sleep(1)
        msg = bot.send_message(message.chat.id, 'Ваш доход благодаря агентству увеличился на 40-60 тысяч,'
                                          ' но работать меньше вы не стали.\n\nВсе так же устаете и не понимаете,'
                                          ' как масштабировать то, что вы хотите, а не то,'
                                          ' что вам советуют.', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_1_17)
    except ApiTelegramException:
        pass


def script2_1_17(message):
    try:
        if message.text in ['обсудить с Викой привлечение других клиентов', 'разозлиться на Вику']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Да, давай встретимся с ним прямо завтра')
            btn2 = types.KeyboardButton(text='Вот сначала встретимся с ним, а потом поговорим')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '👩🏻: — Не беспокойся, мы же в ноль не уходим. А я как раз недавно была'
                                                    ' в Ростове-на-Дону и нашла там на бизнес-завтраке одного клиента.\n\n'
                                                    ' Нам с ним нужно встретиться как можно раньше.'
                                                    ' Ты со мной?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_18)
        else:
            bot.register_next_step_handler(message, script2_1_17)
    except ApiTelegramException:
        pass


def script2_1_18(message):
    try:
        if message.text in ['Да, давай встретимся с ним прямо завтра', 'Вот сначала встретимся с ним, а потом поговорим']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='предложить на встрече клиенту сразу начать сотрудничать')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/mem4.JPG', 'rb'), '– Ок, я тогда ему звоню, договариваюсь. А там дальше видно будет.')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '🔺 Маржинальность вашего бизнеса выросла на 5%.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_20)
        else:
            bot.register_next_step_handler(message, script2_1_18)
    except ApiTelegramException:
        pass


def script2_1_20(message):
    try:
        if message.text == 'предложить на встрече клиенту сразу начать сотрудничать':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='услышать клиента')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/die.jpg', 'rb'), '🔺 Вы приехали на встречу и решительно обратились к новому'
                                                    ' клиенту.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_21)
        else:
            bot.register_next_step_handler(message, script2_1_20)
    except ApiTelegramException:
        pass


def script2_1_21(message):
    try:
        if message.text == 'услышать клиента':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='отнестись с пониманием')
            btn2 = types.KeyboardButton(text='отвести Вику в сторону и спросить, что делать')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '🧑🏻‍🦲: — Я бы с радостью, но в последнее время мой бизнес'
                                                    ' в упадке📉\n Поставки цветов стали дорожать, конкуренты ликуют.'
                                                    ' Вы мне нравитесь, ребят, но денег у меня немного', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_22)
        else:
            bot.register_next_step_handler(message, script2_1_21)
    except ApiTelegramException:
        pass


def script2_1_22(message):
    try:
        if message.text == 'отнестись с пониманием':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='извиниться перед клиентов и выйти')
            btn2 = types.KeyboardButton(text='недоверчиво посмотреть на Вику и выйти')
            kb.add(btn1, btn2)

            bot.send_message(message.chat.id, '– Мы вас понимаем, но мы же вкладываемся в трафик с вами, чтобы'
                                              ' увеличить продажи!')
            bot.send_message(message.chat.id, '🔺 Вам пришло новое уведомление')
            msg = bot.send_photo(message.chat.id, open('data/22.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_25)
        elif message.text == 'отвести Вику в сторону и спросить, что делать':
            script2_1_25(message)
        else:
            bot.register_next_step_handler(message, script2_1_22)
    except ApiTelegramException:
        pass


def script2_1_25(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='О чем ты, Вика?')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/msc.jpg', 'rb'), f'👩🏻: – {info[3]}, я знаю, что ты особо не куришь. Но сейчас тебе реально'
                                                f' надо снять стресс.\n\nУ меня для тебя новая авантюра', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_1_26)
    except ApiTelegramException:
        pass


def script2_1_26(message):
    try:
        if message.text == 'О чем ты, Вика?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А как это будет работать?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👩🏻: – Я столько от него наслушалась про эти цветы! Реально,'
                                                    ' теперь могу и сама запустить такое\n\n'
                                                    'Да и сексами мне торговать уже надоело, хочу чего-то новенького.\n\n'
                                                    'Может ну это агентство, построим самую крупную франшизу цветочных'
                                                    ' магазинов? Весной сделаем рекордную выручку!', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_27)
        else:
            bot.register_next_step_handler(message, script2_1_26)
    except ApiTelegramException:
        pass


def script2_1_27(message):
    try:
        if message.text == 'А как это будет работать?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Вложиться стартовым капиталом')
            btn2 = types.KeyboardButton(text='Мне нужно время подумать')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/20.jpg', 'rb'), '👩🏻 – Все просто: ты занимаешься маркетингом, я поставками'
                                                    ' и реализацией.\n\nУ меня куча опыта. У нас все получится!', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_28)
        else:
            bot.register_next_step_handler(message, script2_1_27)
    except ApiTelegramException:
        pass


def script2_1_28(message):
    try:
        if message.text == 'Мне нужно время подумать':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Окей, но с условием полной свободы моих действий')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'👩🏻 – {info[3]}, мы с тобой точно сделаем результат. Просто попробуем'
                                                    f' – с нашими навыками мы точно взорвем рынок!', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_1_29)
        elif message.text == 'Вложиться стартовым капиталом':
            script2_1_29(message)
        else:
            bot.register_next_step_handler(message, script2_1_28)
    except ApiTelegramException:
        pass


def script2_1_29(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='вложиться в наружную рекламу')
        btn2 = types.KeyboardButton(text='сделать визитки')
        btn3 = types.KeyboardButton(text='развивать соцсети')
        btn4 = types.KeyboardButton(text='обсудить с Викой делегирование закупок')
        kb.add(btn1, btn2, btn3, btn4)

        msg = bot.send_photo(message.chat.id, open('data/mem5.jpg', 'rb'), '🔺 Вы только что вложились в новый бизнес.'
                                                '\nВам надо срочно взращивать его обороты, чтобы <b>восполнить'
                                                ' сбережения и сделать x2 в доходе.</b>'
                                                , reply_markup=kb, parse_mode='HTML')
        bot.register_next_step_handler(msg, script2_1_30)
    except ApiTelegramException:
        pass


def script2_1_30(message):
    try:
        if message.text in ['вложиться в наружную рекламу', 'сделать визитки', 'развивать соцсети',
                            'обсудить с Викой делегирование закупок']:
            bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'), '🔺 Вы начали развивать новый бизнес.')
            #time.sleep(72000) #20h
            #day_2(message)
            t2_1 = threading.Timer(3, day_2, [message])  # 15h
            t2_1.start()
        else:
            bot.register_next_step_handler(message, script2_1_30)
    except ApiTelegramException:
        pass


def script2_2_1(message):
    try:
        if message.text == 'Даа, что там дальше?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='пообщаться с Десяткой')
            btn2 = types.KeyboardButton(text='посоветоваться с Викой')
            btn3 = types.KeyboardButton(text='погуглить')
            btn4 = types.KeyboardButton(text='посмотреть видео на You-Tube по теме')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_message(message.chat.id, 'Вы поняли, что нужно искать другие способы привлечения клиентов.'
                                                    ' Старые гипотезы уже изжили себя.'
                                                    ' Где найдете новые?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_2_0)
        else:
            bot.register_next_step_handler(message, script2_2_1)
    except ApiTelegramException:
        pass


def script2_2_2_0(message):
    try:
        if message.text == 'пообщаться с Десяткой':
            bot.send_message(message.chat.id, 'Вы позвонили вашим друзьям из Десятки.')
            script2_2_2(message)
        elif message.text == 'посоветоваться с Викой':
            bot.send_message(message.chat.id, 'Вы обсудили этот вопрос с вашим бизнес-партнером.')
            script2_2_2(message)
        elif message.text == 'погуглить':
            bot.send_message(message.chat.id, 'Вы почитать опыт лучших бизнес-фаундеров в Гугле.')
            script2_2_2(message)
        elif message.text == 'посмотреть видео на You-Tube по теме':
            bot.send_message(message.chat.id, 'Вы посмотрели, как продают в лучших франшизах бизнес-фаундеры.')
            script2_2_2(message)
        else:
            bot.register_next_step_handler(message, script2_2_2_0)
    except ApiTelegramException:
        pass


def script2_2_2(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='обсудить с ОП продажи на Авито')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/IMG_6213.JPG', 'rb'), 'Выяснили, что лучший вариант сейчас – выходить'
                                                ' на Авито.', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_2_3)
    except ApiTelegramException:
        pass


def script2_2_3(message):
    try:
        if message.text == 'обсудить с ОП продажи на Авито':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А кто это?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👩🏽‍💻: — Привет, это Вика.\n\n🥰Слушай, рада твоей идее с Авито. Давай пробовать.'
                                                    '\n\nА я к нам на производство нашла одного мужчину потрясающего☺️'
                                                    ' Чтобы нам логистику наладил. Я у него офис снимала, когда'
                                                    ' секс-игрушки продавала 🤭', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_4)
        else:
            bot.register_next_step_handler(message, script2_2_3)
    except ApiTelegramException:
        pass


def script2_2_4(message):
    try:
        if message.text == 'А кто это?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Ок, давай попробуем')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/100.jpg', 'rb'), '👩🏽‍💻: – Это Никита.\n\nМы с ним постоянно по городам ездим на'
                                                    ' всякие тендеры, бизнес-форумы, конференции.\n\n👍🏻Вот такой мужик,'
                                                    ' надо брать. Пропадет без него производство.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_5)
        else:
            bot.register_next_step_handler(message, script2_2_4)
    except ApiTelegramException:
        pass


def script2_2_5(message):
    try:
        if message.text == 'Ок, давай попробуем':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='И я тебя!')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '– Люблю тебя!', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_6)
        else:
            bot.register_next_step_handler(message, script2_2_5)
    except ApiTelegramException:
        pass


def script2_2_6(message):
    try:
        if message.text == 'И я тебя!':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='2 месяца')
            btn2 = types.KeyboardButton(text='4 месяца')
            btn3 = types.KeyboardButton(text='6 месяцев')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_photo(message.chat.id, open('data/IMG_6214.PNG', 'rb'), 'Сколько времени вы даете бизнесу на'
                                                    ' то, чтобы он вышел в хороший плюс?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_7)
        else:
            bot.register_next_step_handler(message, script2_2_6)
    except ApiTelegramException:
        pass


def script2_2_7(message):
    try:
        if message.text == '2 месяца':
            bot.send_photo(message.chat.id, open('data/31.jpg', 'rb'))
            script2_2_8(message)
        elif message.text == '4 месяца':
            bot.send_photo(message.chat.id, open('data/32.jpg', 'rb'))
            script2_2_8(message)
        elif message.text == '6 месяцев':
            bot.send_photo(message.chat.id, open('data/33.jpg', 'rb'))
            script2_2_8(message)
        else:
            bot.register_next_step_handler(message, script2_2_7)
    except ApiTelegramException:
        pass


def script2_2_8(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='обрадовать Вику результатами')
        kb.add(btn)

        msg = bot.send_message(message.chat.id, 'Идея с Авито выстрелила!\n+ 200 тысяч к месячной выручке', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_2_9)
    except ApiTelegramException:
        pass


def script2_2_9(message):
    try:
        if message.text == 'обрадовать Вику результатами':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Вик, а что у тебя с животом?..')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/34.jpg', 'rb'), 'Вы встречаетесь с бизнес-партнером обсудить дальнейшие планы.')
            msg = bot.send_message(message.chat.id, '👩🏽‍💻: — Привет, прости, что опоздала. Я в больнице была. Ты говорил,'
                                                    ' у тебя какие-то супер классные новости! Поделишься?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_11)
        else:
            bot.register_next_step_handler(message, script2_2_9)
    except ApiTelegramException:
        pass


def script2_2_11(message):
    try:
        if message.text == 'Вик, а что у тебя с животом?..':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А кто отец, Вика?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/36.jpg', 'rb'), f'{info[3]}, да я беременна.\n\nНо ты внимание не обращай, это не'
                                                    f' должно нашему общему делу мешать.\n\n'
                                                    f'☺️С Авито все супер идет, я так понимаю?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_12)
        else:
            bot.register_next_step_handler(message, script2_2_11)
    except ApiTelegramException:
        pass


def script2_2_12(message):
    try:
        if message.text == 'А кто отец, Вика?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='ну удачи вам! главное, чтобы у нас обороты росли')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Да там завертелось, закрутилось. С одним мужчиной очень умным.. '
                                                    'Говорить не хотела, чтобы не сглазить', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_13)
        else:
            bot.register_next_step_handler(message, script2_2_12)
    except ApiTelegramException:
        pass


def script2_2_13(message):
    try:
        if message.text == 'ну удачи вам! главное, чтобы у нас обороты росли':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Гении, однозначно!')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👩🏽‍💻: – Да за это не переживай, мы с ним хорошо справляемся.\n\n'
                                                    ' А с твоими идеями и нашим маркетингом выйдем в обороты на 7 лимонов'
                                                    ' уже через три месяца.\n\n😏Скажи же, у нас команда'
                                                    ' гениев?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_14)
        else:
            bot.register_next_step_handler(message, script2_2_13)
    except ApiTelegramException:
        pass


def script2_2_14(message):
    try:
        if message.text == 'Гении, однозначно!':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='восхищение')
            btn2 = types.KeyboardButton(text='усталость')
            btn3 = types.KeyboardButton(text='мандраж')
            btn4 = types.KeyboardButton(text='страх')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_message(message.chat.id, 'Ваш бизнес вышел на новый уровень по выручке.\n'
                                                    'Что вы чувствуете?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_15)
        else:
            bot.register_next_step_handler(message, script2_2_14)
    except ApiTelegramException:
        pass


def script2_2_15(message):
    try:
        if message.text in ['восхищение', 'усталость', 'мандраж', 'страх']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Посмотреть')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вам пришло новое уведомление.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_16)
        else:
            bot.register_next_step_handler(message, script2_2_15)
    except ApiTelegramException:
        pass


def script2_2_16(message):
    try:
        if message.text == 'Посмотреть':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='потратиться на сессию с психологом')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/35.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_17)
        else:
            bot.register_next_step_handler(message, script2_2_16)
    except ApiTelegramException:
        pass


def script2_2_17(message):
    try:
        if message.text == 'потратиться на сессию с психологом':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Мальдивы')
            btn2 = types.KeyboardButton(text='Бали')
            btn3 = types.KeyboardButton(text='Шри-Ланка')
            btn4 = types.KeyboardButton(text='Испания')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_message(message.chat.id, '🔺 На сеансе с психологом вы разобрались, что в любом случае тебе'
                                                    ' сейчас нужен отдых. Это важно, чтобы сделать иксы'
                                                    ' в выручке на новом этапе бизнеса.\n\nКуда поедете'
                                                    ' в отпуск?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_18)
        else:
            bot.register_next_step_handler(message, script2_2_17)
    except ApiTelegramException:
        pass


def script2_2_18(message):
    try:
        if message.text in ['Мальдивы', 'Бали', 'Шри-Ланка', 'Испания']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='назначить планерку со всеми отделами')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы отправились покупать билеты.\nНо вспомнили,'
                                                    ' что нужно делегировать задачки команде и'
                                                    ' оповестить Вику.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_19)
        else:
            bot.register_next_step_handler(message, script2_2_18)
    except ApiTelegramException:
        pass


def script2_2_19(message):
    try:
        if message.text == 'назначить планерку со всеми отделами':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Рассказать ей о своем состоянии')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/46.jpg', 'rb'), 'Вы отправились на встречу с командой.\n'
                                                    'Первым делом встретились с Викой.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_20)
        else:
            bot.register_next_step_handler(message, script2_2_19)
    except ApiTelegramException:
        pass


def script2_2_20(message):
    try:
        if message.text == 'Рассказать ей о своем состоянии':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Да, давай, хочу уже в отпуск!')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👩🏽‍💻: — Слушай, да, я тебя прекрасно понимаю.\n\nЕзжай конечно отдыхать.\n\n'
                                                    'Кстати, пока тебя не будет, давай часть маркетинга отдадим Никите.\n\n'
                                                    'Он нас так выручает по логистике, с продажами тоже поможет.\n\n'
                                                    '😉А ты восстановишь ресурс, солнце мое', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_21)
        else:
            bot.register_next_step_handler(message, script2_2_20)
    except ApiTelegramException:
        pass


def script2_2_21(message):
    try:
        if message.text == 'Да, давай, хочу уже в отпуск!':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='отключить все рабочие чаты')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы оформили на Никиту ИП и'
                                                    ' улетели в отпуск на месяц.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_22)
        else:
            bot.register_next_step_handler(message, script2_2_21)
    except ApiTelegramException:
        pass


def script2_2_22(message):
    try:
        if message.text == 'отключить все рабочие чаты':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='выключить телефон')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/37.jpg', 'rb'), '– Ой, совсем из головы вылетело!\n\nЯ же уведомления'
                                                    ' об операциях в банке со счета Никита со своего телефона'
                                                    ' не убрал.🫠\n\nЛадно, все равно'
                                                    ' все на мою карту приходит.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_23)
        else:
            bot.register_next_step_handler(message, script2_2_22)
    except ApiTelegramException:
        pass


def script2_2_23(message):
    try:
        if message.text == 'выключить телефон':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='посмотреть')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вам пришло новое уведомление перед выключением.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_24)
        else:
            bot.register_next_step_handler(message, script2_2_23)
    except ApiTelegramException:
        pass


def script2_2_24(message):
    try:
        if message.text == 'посмотреть':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Что это?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/38.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_25)
        else:
            bot.register_next_step_handler(message, script2_2_24)
    except ApiTelegramException:
        pass


def script2_2_25(message):
    try:
        if message.text == 'Что это?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Откуда это столько у Никиты?')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/39.jpg', 'rb'))
            msg = bot.send_photo(message.chat.id, open('data/40.jpg', 'rb'), reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_27)
        else:
            bot.register_next_step_handler(message, script2_2_25)
    except ApiTelegramException:
        pass


def script2_2_27(message):
    try:
        if message.text == 'Откуда это столько у Никиты?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='позвонить Вике и разобраться')
            btn2 = types.KeyboardButton(text='позвонить Никите и разобраться')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, 'Вы отследили, что на счет Никиты'
                                                    ' перечислили за месяц 9 миллионов.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_28)
        else:
            bot.register_next_step_handler(message, script2_2_27)
    except ApiTelegramException:
        pass


def script2_2_28(message):
    try:
        if message.text == 'позвонить Вике и разобраться':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='узнать, как дела')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/41.jpg', 'rb'), '– Вика, привет! откуда столько денег пришло?'
                                              ' Почему не на основной счет?')
            time.sleep(1)
            bot.send_message(message.chat.id, '👩🏽‍💻: — Привет, солнце! Да это у Никиты еще свой бизнес есть помимо нашего,'
                                              ' он у меня мужчина серьезный. Не переживай, наши деньги всегда на общий'
                                              ' счет поступают. Ты лучше расскажи, как отдыхается?')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '– Вик, все хорошо. Приеду 30 числа уже в ресурсе', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_31)

        elif message.text == 'позвонить Никите и разобраться':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='узнать, как дела у Вики')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/41.jpg', 'rb'), '– Никит, привет! откуда столько денег'
                                              ' пришло? Почему не на основной счет?')
            bot.send_message(message.chat.id, '🧔🏻: — Ты как узнал… Странно, что ты по моему банку шаришься.\n\n😐 Свой бизнес'
                                              ' у меня параллельно, не слышал что ли?\n\nСемью то надо кормить, у нас с'
                                              ' Викой скоро ребенок')
            msg = bot.send_message(message.chat.id, '– Извини, Никит, я на взводе и в стрессе.'
                                                    ' Приеду 30 числа уже в ресурсе', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_2_31)
        else:
            bot.register_next_step_handler(message, script2_2_28)
    except ApiTelegramException:
        pass


def script2_2_31(message):
    try:
        if message.text == 'узнать, как дела':
            bot.send_photo(message.chat.id, open('data/IMG_6214.PNG', 'rb'), '– Ой, кажется схватки… Люблю тебя, солнце!')
            time.sleep(1)
            script2_2_32(message)
        elif message.text == 'узнать, как дела у Вики':
            bot.send_photo(message.chat.id, open('data/IMG_6214.PNG', 'rb'), '– Ой, кажется схватки у Вики… До связи!')
            time.sleep(1)
            script2_2_32(message)
        else:
            bot.register_next_step_handler(message, script2_2_31)
    except ApiTelegramException:
        pass


def script2_2_32(message):
    try:
        bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'))
        #time.sleep(72000) #20h
        #day_3(message)
        t2_2 = threading.Timer(3, day_3, [message])  # 15h
        t2_2.start()
    except ApiTelegramException:
        pass


def script2_3_2(message):
    try:
        if message.text == 'Даа, что там дальше?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='разобрать почту')
            btn2 = types.KeyboardButton(text='удалить старые фото из галереи')
            btn3 = types.KeyboardButton(text='денежно помедитировать')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_message(message.chat.id, 'Вы почти месяц отдыхали, и 20-го числа решили очистить карму,'
                                                    ' душу и ненужные архивы.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_3)
        else:
            bot.register_next_step_handler(message, script2_3_2)
    except ApiTelegramException:
        pass


def script2_3_3(message):
    try:
        if message.text == 'денежно помедитировать':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='разобрать почту')
            btn2 = types.KeyboardButton(text='удалить старые фото из галереи')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, 'Вы сделали денежную медитацию.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_3)
        elif message.text == 'удалить старые фото из галереи':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='разобрать почту')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/IMG_6220.JPG', 'rb'), 'Вы удалили воспоминания со всеми бывшыми, и добавили в'
                                                    ' Избранное фото с партнером'
                                                    ' вашего курортного романа.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_3)
        elif message.text == 'разобрать почту':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Открыть папку Бизнес')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы зашли удалить старые письма, но подозрительно большой'
                                                    ' поток пришел свежих.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_6)
        else:
            bot.register_next_step_handler(message, script2_3_3)
    except ApiTelegramException:
        pass


def script2_3_6(message):
    try:
        if message.text == 'Открыть папку Бизнес':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Ответить всем')
            btn2 = types.KeyboardButton(text='Все бросить и уехать разбираться')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/hz.jpg', 'rb'), 'И еще +27 новых писем', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_7)
        else:
            bot.register_next_step_handler(message, script2_3_6)
    except ApiTelegramException:
        pass


def script2_3_7(message):
    try:
        if message.text == 'Ответить всем':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Купить билеты обратно в Москву')
            btn2 = types.KeyboardButton(text='Провести отпуск до конца')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, 'Вы пообещали всем клиентам разобраться в ситуации.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_7)

        elif message.text == 'Провести отпуск до конца':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Посмотреть, остались ли сейчас билеты до Москвы')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы решили успокоиться и действовать с холодной головой.'
                                                    ' Но поток сообщений увеличился, поэтому через три дня вам стало'
                                                    ' трудно не беспокоится.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_7)

        elif message.text in ['Все бросить и уехать разбираться',
                              'Купить билеты обратно в Москву',
                              'Посмотреть, остались ли сейчас билеты до Москвы']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn1 = types.KeyboardButton(text='Где Вика?!')
            btn2 = types.KeyboardButton(text='Покурить перед разборками')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, 'Вы купили билеты обратно в Москву и прилетели на производство'
                                                    ' на 5 дней раньше планируемой даты.', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_9)
        else:
            bot.register_next_step_handler(message, script2_3_7)
    except ApiTelegramException:
        pass


def script2_3_9(message):
    try:
        if message.text in ['Где Вика?!', 'Покурить перед разборками']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Уехать и разорвать совместное ООО втихую')
            btn2 = types.KeyboardButton(text='Поймать Никиту и Вику с поличным')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '👩🏽‍💻: — У нас с тобой еще есть дня 3, чтобы это все закрыть и'
                                                    ' исправить.\n\nПотом вернется со своих отпусков там, будем дальше'
                                                    ' разбираться.\n\n🤫 Я тут сейчас закрою документацию, которую выносить'
                                                    ' нельзя.\n\nСейчас поедем в офис, пока можешь'
                                                    ' заводить машину.\n\nГлавное, что бабок мы срубили.\n\n😉 Еще несколько'
                                                    ' месяцев на крючке посидит и потом вообще ничего сделать не'
                                                    ' сможет', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_10_0)
        else:
            bot.register_next_step_handler(message, script2_3_9)
    except ApiTelegramException:
        pass


def script2_3_10_0(message):
    try:
        if message.text == 'Поймать Никиту и Вику с поличным':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='подраться с Никитой')
            btn2 = types.KeyboardButton(text='достать договора и разорвать')
            kb.add(btn1, btn2)

            bot.send_voice(message.chat.id, open('data/aud2.mp3', 'rb'))
            msg = bot.send_message(message.chat.id, '– Вика, просто скажите мне сумму, которую вы украли из бизнеса'
                                                    ' за все это время', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_12_0)
        elif message.text == 'Уехать и разорвать совместное ООО втихую':
            script2_3_13(message)
        else:
            bot.register_next_step_handler(message, script2_3_10_0)
    except ApiTelegramException:
        pass


def script2_3_12_0(message):
    try:
        if message.text == 'подраться с Никитой':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='посмотреть злобно на Никиту')
            kb.add(btn)

            bot.send_photo(message.chat.id, open('data/74.jpg', 'rb'), f'👩🏽‍💻: – {info[3]}, я тут вообще не при чем. Это была его идея.'
                                              f' Я и ребенка от него не хотела, это он меня уговорил не делать аборт')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '🧔🏻: – Замолчи! Кто мне предложил эту схему с ИП? Кто рассказывал'
                                                    ' мне, как владеет компанией практически'
                                                    ' как собственной?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_14_0)
        elif message.text == 'достать договора и разорвать':
            script2_3_13(message)
        else:
            bot.register_next_step_handler(message, script2_3_12_0)
    except ApiTelegramException:
        pass


def script2_3_14_0(message):
    try:
        if message.text == 'посмотреть злобно на Никиту':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Принять, что с ними больше не о чем разговаривать')
            kb.add(btn)
            msg = bot.send_message(message.chat.id, '🔺 Вы разорвали отношения с одним из совладельцев вашего бизнеса', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_13)
        else:
            bot.register_next_step_handler(message, script2_3_14_0)
    except ApiTelegramException:
        pass


'''def script2_3_12_1(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text='Принять, что с ними больше не о чем разговаривать')
    kb.add(btn)

    msg = bot.send_video(message.chat.id, open('data/vid5.mov', 'rb'), reply_markup=kb, timeout=60, height=1920, width=1080)
    bot.register_next_step_handler(msg, script2_3_13)'''


def script2_3_13(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='Мир несправедлив, у меня к ней злость')
        btn2 = types.KeyboardButton(text='Жизнь – это бумеранг. Ей вернется, а я останусь в выигрыше')
        btn3 = types.KeyboardButton(text='Жизнь послала мне ее для опыта. И теперь он у меня есть')
        btn4 = types.KeyboardButton(text='Это была моя карма, и хорошо что она теперь чиста')
        kb.add(btn1, btn2, btn3, btn4)

        bot.send_video(message.chat.id, open('data/vid5.mov', 'rb'), timeout=60, height=1920, width=1080)
        msg = bot.send_message(message.chat.id, 'Вы вызвали такси. Думаете и размышляете над всем, что произошло.\n\n'
                                                'Никита – всего лишь пешка. Но Вика — что вы думаете'
                                                ' о ней теперь?', reply_markup=kb)
        bot.register_next_step_handler(msg, script2_3_14)
    except ApiTelegramException:
        pass


def script2_3_14(message):
    try:
        if message.text in ['Мир несправедлив, у меня к ней злость',
                            'Жизнь – это бумеранг. Ей вернется, а я останусь в выигрыше',
                            'Жизнь послала мне ее для опыта. И теперь он у меня есть',
                            'Это была моя карма, и хорошо что она теперь чиста']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Перенестись на момент через 2 месяца')
            btn2 = types.KeyboardButton(text='Перенестись на момент через полгода')
            btn3 = types.KeyboardButton(text='Перенестись на момент через 5 лет')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_message(message.chat.id, 'Как думаете, попытается ли Вика восстановить ваши'
                                                    ' отношения?', reply_markup=kb)
            bot.register_next_step_handler(msg, script2_3_15)
        else:
            bot.register_next_step_handler(message, script2_3_14)
    except ApiTelegramException:
        pass


def script2_3_15(message):
    try:
        if message.text in ['Перенестись на момент через 2 месяца',
                            'Перенестись на момент через полгода',
                            'Перенестись на момент через 5 лет']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='Заблокировать Вику')
            btn2 = types.KeyboardButton(text='Проигнорировать')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/45.jpg', 'rb'), '…Сразу после этого момента Вика начала вам мстить.'
                                                    ' Раз в месяц она пишет вам примерно такие сообщения.', reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_1)
        else:
            bot.register_next_step_handler(message, script2_3_15)
    except ApiTelegramException:
        pass


def script3_1_3(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='выставку ее работ')
        btn2 = types.KeyboardButton(text='аукцион ее работ')
        btn3 = types.KeyboardButton(text='концерт со сценой с ее работами')
        kb.add(btn1, btn2, btn3)
        if message.text == 'сказать тост о сестре':
            msg = bot.send_message(message.chat.id, '🔺 Во время тоста вы вспомнили самую сокровенную мечту вашей сестры.\n'
                                              'Она очень хочет, чтобы ее работы видели люди.\n\n'
                                              'Что бы вы сделали, чтобы исполнить ее мечту?', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_4)

        elif message.text == 'передать тост папе':
            msg = bot.send_message(message.chat.id, '🔺 Во время папиных слов вы вспомнили самую'
                                                    ' сокровенную мечту вашей сестры.\n'
                                                    'Она очень хочет, чтобы ее работы видели люди.\n\n'
                                                    'Что бы вы сделали, чтобы исполнить ее мечту?', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_4)
        else:
            bot.register_next_step_handler(message, script3_1_3)
    except ApiTelegramException:
        pass


def script3_1_4(message):
    try:
        if message.text == 'выставку ее работ':
            bot.send_photo(message.chat.id, open('data/vystavka.png', 'rb'), '🔺 Вы организовали выставку работ своей сестры.')
            time.sleep(1)
            script3_1_5(message)
        elif message.text == 'аукцион ее работ':
            bot.send_photo(message.chat.id, open('data/auction.jpg', 'rb'), '🔺 Вы организовали аукцион работ своей сестры.')
            time.sleep(1)
            script3_1_5(message)
        elif message.text == 'концерт со сценой с ее работами':
            bot.send_photo(message.chat.id, open('data/concert.png', 'rb'), '🔺 Вы организовали концерт, на котором висели'
                                                                      ' работы вашей сестры.')
            time.sleep(1)
            script3_1_5(message)
        else:
            bot.register_next_step_handler(message, script3_1_4)
    except ApiTelegramException:
        pass


def script3_1_5(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='узнать, что он хочет')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/69.jpg', 'rb'), 'К вам подошел странный мужчина.'
                                                ' Он попросил выслушать его', reply_markup=kb)
        bot.register_next_step_handler(msg, script3_1_6)
    except ApiTelegramException:
        pass


def script3_1_6(message):
    try:
        if message.text == 'узнать, что он хочет':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='выслушать предложение')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👱🏻: – Извините, а Вы не знаете, как связаться с автором работ?'
                                                    ' У меня есть к нему <i>деловое предложение.</i>'
                                                    , reply_markup=kb, parse_mode='HTML')
            bot.register_next_step_handler(msg, script3_1_7)
        else:
            bot.register_next_step_handler(message, script3_1_6)
    except ApiTelegramException:
        pass


def script3_1_7(message):
    try:
        if message.text == 'выслушать предложение':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у сестры, хочет ли она продать работы')
            btn2 = types.KeyboardButton(text='спросить у сестры, хочет ли она 1млн $ с одной работы')
            kb.add(btn1, btn2)

            bot.send_message(message.chat.id, '– Здравствуйте, это работы моей сестры. Можете поговорить со'
                                              ' мной, я обсужу это с ней.')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '👱🏻: – Я творческий инвестор. И хотел бы выкупить эти картины.'
                                                    ' Штук пять. За сумму, которую ваша сестра предложит.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_9)
        else:
            bot.register_next_step_handler(message, script3_1_7)
    except ApiTelegramException:
        pass


def script3_1_9(message):
    try:
        if message.text == 'спросить у сестры, хочет ли она продать работы':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            bot.send_photo(message.chat.id, open('data/mem6.JPG', 'rb'), '— Привет, дорогая! Где ты? Тут у тебя работы купить хотят – за любую'
                                              ' сумму, штук 5. Ты хочешь обсудить?')
            time.sleep(1)
            bot.send_message(message.chat.id, f'👩🏻‍🦰:—{info[3]}, мне деньги не нужны. Я хочу, чтобы их видели люди.'
                                              f' Чтобы каждый что-то свое видел в моих картинах, делился этим в соцсетях,'
                                              f' а не кто-то один повесил пылиться над диваном. Скажи, что я не готова💔.')
            time.sleep(1)
            script3_1_11(message)
        elif message.text == 'спросить у сестры, хочет ли она 1млн $ с одной работы':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            bot.send_photo(message.chat.id, open('data/mem6.JPG', 'rb'), '— Привет, дорогая! Где ты? Ты продашь свои работы за миллион долларов'
                                              ' каждую, или еще больше хочешь?')
            time.sleep(1)
            bot.send_message(message.chat.id, f'👩🏻‍🦰:– {info[3]}, мне деньги не нужны. Я хочу, чтобы их видели люди.'
                                              f' Чтобы каждый что-то свое видел в моих картинах, делился этим в соцсетях,'
                                              f' а не кто-то один повесил пылиться над диваном. Скажи, что я не готова.')
            time.sleep(1)
            script3_1_11(message)
        else:
            bot.register_next_step_handler(message, script3_1_9)
    except ApiTelegramException:
        pass


def script3_1_11(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='поблагодарить мужчину за интерес')
        btn2 = types.KeyboardButton(text='не объясняться с мужчиной')
        kb.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, '🔺 Сделка не состоялась.', reply_markup=kb)
        bot.register_next_step_handler(msg, script3_1_12)
    except ApiTelegramException:
        pass


def script3_1_12(message):
    try:
        if message.text == 'поблагодарить мужчину за интерес':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='попросить номер телефона на всякий случай')
            kb.add(btn)

            bot.send_message(message.chat.id, '– Спасибо за проявленный интерес!'
                                              ' Моя сестра не хочет продавать работы, но ей приятно ваше внимание к ним.'
                                              ' Ей важно, чтобы картины оценивали люди и'
                                              ' делились своими эмоциями с другими.')
            msg = bot.send_message(message.chat.id, 'Мужчина понял вас и направился в сторону выхода.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_13_1)

        elif message.text == 'не объясняться с мужчиной':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Что он хочет?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы направились к выходу, но мужчина вас догнал.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_13_2)
    except ApiTelegramException:
        pass


def script3_1_13_1(message):
    try:
        if message.text == 'попросить номер телефона на всякий случай':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Порефлексировать')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👱🏻: – Если нужно – звоните. Например, проинвестировать в вашу'
                                                    ' следующую выставку.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_14)
        else:
            bot.register_next_step_handler(message, script3_1_13_1)
    except ApiTelegramException:
        pass


def script3_1_13_2(message):
    try:
        if message.text == 'Что он хочет?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='записать номер инвестора')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👱🏻: – Извините, задержу вас еще на минуту. Запишите мой контакт,'
                                                    ' пожалуйста. Я бы хотел проинвестировать в следующую вашу'
                                                    ' выставку.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_14)
        else:
            bot.register_next_step_handler(message, script3_1_13_2)
    except ApiTelegramException:
        pass


def script3_1_14(message):
    try:
        if message.text in ['записать номер инвестора', 'Порефлексировать']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А что, если…')
            kb.add(btn)

            bot.send_video(message.chat.id, open('data/vid5.mov', 'rb'), timeout=100, height=1920, width=1080)
            msg = bot.send_message(message.chat.id, 'Вы ехали в такси и рефлексировали над последними событиями.'
                                                    ' Слова сестры и спрос на ее работы,'
                                                    ' натолкнули вас на мысль…', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_15)
        else:
            bot.register_next_step_handler(message, script3_1_14)
    except ApiTelegramException:
        pass


def script3_1_15(message):
    try:
        if message.text == 'А что, если…':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='предложить инвестору идею')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/mem7.JPG', 'rb'), '– А что, если создать соцсеть-выставку разных художников?'
                                                    '\n\nЧтобы по всей соцсети разлетались впечатления людей на работы?'
                                                    '\n\nА если они хотят приобрести, то мы оформляем NFT-токен на картины…'
                                                    , reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_16)
        else:
            bot.register_next_step_handler(message, script3_1_15)
    except ApiTelegramException:
        pass


def script3_1_16(message):
    try:
        if message.text == 'предложить инвестору идею':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='перезвонить ему')
            btn2 = types.KeyboardButton(text='оставить все, как есть, не судьба')
            btn3 = types.KeyboardButton(text='написать ему в ТГ')
            kb.add(btn1, btn2, btn3)

            msg = bot.send_message(message.chat.id, 'Вы позвонили мужчине с выставки.\n\nОн долго молчал,'
                                                    ' и просто отключился.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_1_17)
        else:
            bot.register_next_step_handler(message, script3_1_16)
    except ApiTelegramException:
        pass


def script3_1_17(message):
    try:
        if message.text in ['перезвонить ему', 'оставить все, как есть, не судьба', 'написать ему в ТГ']:
            bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'))
            #time.sleep(72000)
            #day_2(message)
            t3_1 = threading.Timer(3, day_2, [message])  # 15h
            t3_1.start()
        else:
            bot.register_next_step_handler(message, script3_1_17)
    except ApiTelegramException:
        pass


def script3_2_2(message, last_message):
    try:
        if message.text == 'Даа, что там дальше?':
            if last_message[0] == 'перезвонить ему':
                bot.send_message(message.chat.id, '🔺 Вы стали набирать инвестора снова.'
                                                  '\nИ он наконец-то ответил вам – только с пятого раза.')
                time.sleep(1)
                script3_2_3(message)
            elif last_message[0] == 'оставить все, как есть, не судьба':
                bot.send_message(message.chat.id, 'Вы решили, что это знак судьбы, и не стали перезванивать инвестору.'
                                                  '\n\nНо через два дня он позвонил вам сам.')
                time.sleep(1)
                script3_2_3(message)
            elif last_message[0] == 'написать ему в ТГ':
                bot.send_message(message.chat.id, 'Вы написали инвестору в Телеграме. Он не отвечал неделю.\n\n'
                                                  'Рассчитывать на сотрудничество вы уже перестали.\nКак вдруг…')
                time.sleep(1)
                script3_2_3(message)
    except ApiTelegramException:
        pass


def script3_2_3(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Какой?')
        kb.add(btn)

        msg = bot.send_message(message.chat.id, '👱🏻: – Я не отвечал, потому что думал. Мне интересно ваше предложение,'
                                                ' но… Есть один нюанс.', reply_markup=kb)
        bot.register_next_step_handler(msg, script3_2_4)
    except ApiTelegramException:
        pass


def script3_2_4(message):
    try:
        if message.text == 'Какой?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Как, Дубай?')
            kb.add(btn)

            msg = bot.send_photo(message.chat.id, open('data/IMG_6216.PNG', 'rb'), '👱🏻: – Я сейчас живу в Дубае, и в ближайшее'
                                                    ' время в Россию больше возвращаться не планирую.\n\n'
                                                    'Мне важен личный контакт с инициатором идеи, потому что всегда'
                                                    ' рассчитываю на долгосрочное сотрудничество.\n\n'
                                                    'Хотите – переезжайте в Дубай. У меня тут свой офис в центре,'
                                                    ' если что.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_5)
        else:
            bot.register_next_step_handler(message, script3_2_4)
    except ApiTelegramException:
        pass


def script3_2_5(message):
    try:
        if message.text == 'Как, Дубай?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='согласиться на город мечты')
            btn2 = types.KeyboardButton(text='посоветоваться с семьей и друзьями')
            kb.add(btn1, btn2)

            msg = bot.send_photo(message.chat.id, open('data/70.jpg', 'rb'), 'Вы всегда хотели попробовать жить именно в Дубае.'
                                                    ' Это новый уровень жизни и скоростей. Новый уровень бизнесов,'
                                                    ' выручки и раскрытия потенциала.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_6)
        else:
            bot.register_next_step_handler(message, script3_2_5)
    except ApiTelegramException:
        pass


def script3_2_6(message):
    try:
        if message.text == 'посоветоваться с семьей и друзьями':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А друзья?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы посоветовались с родителями.\n'
                                                    'Они считают, что за бугром развиваться сложнее –'
                                                    ' против.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_6)
        elif message.text == 'А друзья?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='А… сестра?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, 'Вы рассказали друзьям.\n'
                                                    'Им было выгодно обращаться к вам за советами и социальным'
                                                    ' капиталом в России – против.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_6)
        elif message.text == 'А… сестра?':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            bot.send_photo(message.chat.id, open('data/71.jpg', 'rb'), f'👩🏻‍🦰: – Слушай, я очень тебя люблю! И ценю, что эта авантюра началась'
                                              f' от твоей любви ко мне. Я приму любое твое решение. Твой потенциал'
                                              f' бесконечен! Слетай на 3 дня просто в эту атмосферу. Это же город'
                                              f' твоей мечты, {info[3]}! На месте тебе все станет ясно.')
            time.sleep(1)
            bot.send_message(message.chat.id, 'Вы улетели в Дубай на 3 дня.')
            time.sleep(1)
            script3_2_7(message)
        elif message.text == 'согласиться на город мечты':
            bot.send_message(message.chat.id, 'Вы уехали в Дубай, чтобы развивать свой стартап.')
            time.sleep(1)
            script3_2_7(message)
        else:
            bot.register_next_step_handler(message, script3_2_6)
    except ApiTelegramException:
        pass


def script3_2_7(message):
    try:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='надеть костюм')
        btn2 = types.KeyboardButton(text='надеть кэжуал')
        btn3 = types.KeyboardButton(text='надеть яркую выразительную одежду')
        kb.add(btn1, btn2, btn3)

        msg = bot.send_message(message.chat.id, 'Сегодня у вас состоится встреча с инвестором', reply_markup=kb)
        bot.register_next_step_handler(msg, script3_2_8)
    except ApiTelegramException:
        pass


def script3_2_8(message):
    try:
        if message.text in ['надеть костюм', 'надеть кэжуал', 'надеть яркую выразительную одежду']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='вода')
            btn2 = types.KeyboardButton(text='кофе')
            btn3 = types.KeyboardButton(text='коньяк')
            btn4 = types.KeyboardButton(text='апероль')
            kb.add(btn1, btn2, btn3, btn4)

            msg = bot.send_photo(message.chat.id, open('data/dubai2.jpg', 'rb'), '👱🏻: – Сегодня обсуждаем планы по стартапу и наши с тобой условия.'
                                                    ' Поверь, я тебя не обижу. Что будешь пить?', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_9)
        else:
            bot.register_next_step_handler(message, script3_2_8)
    except ApiTelegramException:
        pass


def script3_2_9(message):
    try:
        if message.text in ['вода', 'кофе', 'коньяк', 'апероль']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='идея в первую очередь')
            btn2 = types.KeyboardButton(text='деньги в первую очередь')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '👱🏻: – Я бы хотел с тобой поближе познакомиться. Ты сорвался с места,'
                                                    ' потому что тебе дорога идея, или потому что ты хочешь побольше'
                                                    ' заработать?', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_10)
        else:
            bot.register_next_step_handler(message, script3_2_9)
    except ApiTelegramException:
        pass


def script3_2_10(message):
    try:
        if message.text in ['идея в первую очередь', 'деньги в первую очередь']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Да, ты прав')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, '👱🏻: – Поверь, что хороший бизнес не может существовать без одного'
                                                    ' из этих двух компонентов. Он начинается и продолжает быть с большой'
                                                    ' идеи, а двигается вперед – с большими оборотами.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_11)
        else:
            bot.register_next_step_handler(message, script3_2_10)
    except ApiTelegramException:
        pass


def script3_2_11(message):
    try:
        if message.text == 'Да, ты прав':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='рассказать про выставку сестры')
            btn2 = types.KeyboardButton(text='рассказать про прошлый опыт в бизнесе')
            kb.add(btn1, btn2)

            msg = bot.send_message(message.chat.id, '👱🏻: – Расскажи мне, как к тебе пришла Большая Идея этой авантюры?', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_12)
        else:
            bot.register_next_step_handler(message, script3_2_11)
    except ApiTelegramException:
        pass


def script3_2_12(message):
    try:
        if message.text in ['рассказать про выставку сестры', 'рассказать про прошлый опыт в бизнесе']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить у него про его бизнес')
            btn2 = types.KeyboardButton(text='спросить про его семью')
            btn3 = types.KeyboardButton(text='спросить про то, как он переехал в Америку')
            kb.add(btn1, btn2, btn3)

            bot.send_message(message.chat.id, 'Вы чувствуете, что сблизились с инвестором')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, '👱🏻: – Я сразу увидел в тебе не просто стартапера, а креативного'
                                                    ' стратега. Это гениально!', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_14)
        else:
            bot.register_next_step_handler(message, script3_2_12)
    except ApiTelegramException:
        pass


def script3_2_14(message):
    try:
        if message.text in ['спросить у него про его бизнес', 'спросить про его семью',
                            'спросить про то, как он переехал в Америку']:
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='спросить его о разделении выручки бизнеса')
            btn2 = types.KeyboardButton(text='сблизиться еще больше для выгоды')
            kb.add(btn1, btn2)

            bot.send_message(message.chat.id, '👱🏻:– О, это долгая история…')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, 'Вы стали с инвестором друзьями', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_16)
        else:
            bot.register_next_step_handler(message, script3_2_14)
    except ApiTelegramException:
        pass


def script3_2_16(message):
    try:
        if message.text == 'сблизиться еще больше для выгоды':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='спросить его о разделении выручки бизнеса')
            kb.add(btn)

            bot.send_message(message.chat.id, '– А расскажите, какие неудачи у вас были в инвестировании?')
            time.sleep(1)
            bot.send_photo(message.chat.id, open('data/72.jpg', 'rb'), '👱🏻: – Как-то я стал совладельцем одной компании по производству'
                                              ' топлива. Больше с российскими бизнесами я не работал. Дело было так…')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, 'Вы узнали, что ваш стартап – единственный бизнес из России,'
                                              ' в который инвестор захотел вкладываться.', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_2_16)
        elif message.text == 'спросить его о разделении выручки бизнеса':
            bot.send_message(message.chat.id, '– А вот мы и подошли к самому интересному…')
            time.sleep(1)
            bot.send_photo(message.chat.id, open('data/24.jpg', 'rb'))
            #time.sleep(72000) #20h
            #day_3(message)
            t3_2 = threading.Timer(3, day_3, [message])  # 15h
            t3_2.start()
        else:
            bot.register_next_step_handler(message, script3_2_16)
    except ApiTelegramException:
        pass


def script3_3_2(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn = types.KeyboardButton(text='Спасибо, к чему это?')
        kb.add(btn)

        msg = bot.send_photo(message.chat.id, open('data/72.jpg', 'rb'), f'👱🏻: – Итак, {info[3]}, мне очень нравится идея твоего стартапа.'
                                          f' Но российские бизнесы мне не интересны.\n\nС тобой я начал работать,'
                                          f' потому что твоя идея исключительна.\n\nДа и сестра у тебя – высший'
                                          f' пилотаж таланта!', reply_markup=kb)
        bot.register_next_step_handler(msg, script3_3_3)
    except ApiTelegramException:
        pass


def script3_3_3(message):
    try:
        if message.text == 'Спасибо, к чему это?':
            cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
            info = cur.fetchone()

            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            btn = types.KeyboardButton(text='Что?')
            kb.add(btn)

            msg = bot.send_message(message.chat.id, f'👱🏻: 90 на 10, {info[3]}', reply_markup=kb)
            bot.register_next_step_handler(msg, script3_3_4)
        else:
            bot.register_next_step_handler(message, script3_3_3)
    except ApiTelegramException:
        pass


def script3_3_4(message):
    try:
        if message.text == 'Что?':
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(text='договориться только с условиями 50/50, иначе не сотрудничать')
            btn2 = types.KeyboardButton(text='принять условия, лишь бы бизнес пошел')
            kb.add(btn1, btn2)

            bot.send_message(message.chat.id, '👱🏻: – 90% выручки стартапа – мои. 10 – твои. Договариваемся?')
            time.sleep(1)
            msg = bot.send_message(message.chat.id, 'Это стартап в честь вашей любимой сестры. Вы – в городе вашей мечты.'
                                                    ' Инвестор, который увидел в вас исключительность, берет ваш проект'
                                                    ' единственный из страны.\n\nВаши действия?', reply_markup=kb)
            bot.register_next_step_handler(msg, portraits_1)
        else:
            bot.register_next_step_handler(message, script3_3_4)
    except ApiTelegramException:
        pass


def day4_1(message):
    try:
        cur.execute(f'SELECT * FROM users_demo WHERE userid={message.from_user.id}')
        info = cur.fetchone()

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton(text='тот, кто работает над своим духовным ресурсом')
        btn2 = types.KeyboardButton(text='тот, кто всегда спрашивает советов, помощи знакомых')
        btn3 = types.KeyboardButton(text='тот, кто занимается спортом, соблюдает дисциплину')
        btn4 = types.KeyboardButton(text='тот, кто решил разобраться с системой денег')
        kb.add(btn1, btn2, btn3, btn4)

        msg = bot.send_message(message.chat.id, f'Привет, {info[3]}! Ты понял, кто быстрее'
                                                f' достигает миллионов?', reply_markup=kb)
        bot.register_next_step_handler(msg, day4_2)
    except ApiTelegramException:
        pass


def day4_2(message):
    try:
        if message.text in ['тот, кто работает над своим духовным ресурсом',
                            'тот, кто всегда спрашивает советов, помощи знакомых',
                            'тот, кто занимается спортом, соблюдает дисциплину',
                            'тот, кто решил разобраться с системой денег']:
            kb = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton(text='💎 ХАКНУТЬ ДЕНЬГИ 💎', url='https://denginovogovremeni.com/')
            kb.add(btn)
            bot.send_message(message.chat.id, 'Узнали свои мысли у героев Игры в деньги?\n\nЕсть 5 принципов отношений'
                                              ' с деньгами, которых придерживаются все миллионеры.\n\nДаже если доход'
                                              ' пока сильно меньше — с ними в голове у вас верное мышление.\n\n'
                                              'Проверьте, входите ли вы в список потенциальных миллионеров\nНа'
                                              ' канале Автора Игры в деньги  ➡️ @granovskaya_prodengi\n\n')
            bot.send_video(message.chat.id, open('data/vidpolina4.mov', 'rb'), timeout=60, height=1920, width=1080)
            time.sleep(1)
            bot.send_message(message.chat.id, 'Не забудьте получить для себя эту систему денег нового времени!\nЗагрузи'
                                              ' карточку своего финансового портрета прямо сюда ⬇️', reply_markup=kb)

            cur.execute(f"""UPDATE users_demo SET finished={1} WHERE userid={message.from_user.id}""")
            conn.commit()
    except ApiTelegramException:
        pass


def banned(message):
    try:
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='Получить второй шанс', url='https://denginovogovremeni.com/')
        kb.add(btn)

        msg = bot.send_message(message.chat.id, f'Не в этот раз. Ты уже отказался играть в деньги,'
                                          f' а значит и зарабатывать их, помнишь?\nЕсли ты понял, что деньги нового'
                                          f' времени тебе действительно важны, и ты хочешь управлять своим'
                                          f' доходом — заходи в этот лабиринт ⬇', reply_markup=kb)
        bot.register_next_step_handler(msg, banned)
    except ApiTelegramException:
        pass


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)

