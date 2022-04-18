import telebot
from telebot import types
import database
from states import UserState

token = '1971307075:AAEtkdzdnqwptnf9wM94A2LDa4POIFVSpVU'
bot = telebot.TeleBot(token)


mydb = database.Database()
Tasks_List = database.Operate()
markup = types.InlineKeyboardMarkup()
buttonA = types.InlineKeyboardButton('Add', callback_data='1')
buttonB = types.InlineKeyboardButton('Mark', callback_data='2')
buttonC = types.InlineKeyboardButton('Erase', callback_data='3')
buttonD = types.InlineKeyboardButton('Print', callback_data='4')
markup.row(buttonA, buttonD)
markup.row(buttonC, buttonB)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Дарова. Это бот, помогающий сделать нормальный список из твоих заметок')
    bot.send_message(message.chat.id, 'Доступные комманды:')
    stroka_commands = "1. /add - Добавить запись \n2. /mark - Отметить как выполненное \n3. \
/erase - Удалить к чертям \n4. /print - Вывести список тасок"
    bot.send_message(message.chat.id, stroka_commands, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == '1':
        smile = b'\xF0\x9F\x91\xBD'
        bot.send_message(call.message.chat.id, smile.decode() + 'Пиши что хочешь сделать)' + smile.decode())
        mydb.UpdateUser(call.message.chat.id, UserState.Waiting_For_Task)
    elif call.data == '2':
        smile = b'\xF0\x9F\x91\xBA'
        bot.send_message(call.message.chat.id, smile.decode() + 'Напиши номер таски, которую надо отметить' + smile.decode())
        Print_Tasks(call.message)
        mydb.UpdateUser(call.message.chat.id, UserState.Waiting_For_Marking)
    elif call.data == '3':
        smile = b'\xF0\x9F\x90\xB7'
        bot.send_message(call.message.chat.id, smile.decode() + 'Пиши номер таски, которую хочешь удалить' + smile.decode())
        Print_Tasks(call.message)
        mydb.UpdateUser(call.message.chat.id, UserState.Waiting_For_Erase)
    elif call.data == '4':
            Print_Tasks(call.message)


def Print_Tasks(message):
    block = Tasks_List.Get_Tasks(message.chat.id)
    smile_complete = b'\xE2\x9C\x85'
    smile_not_complete = b"\xE2\x9D\x8C"
    for ind in range(len(block)):
        if block[ind][1] == 0:
            bot.send_message(message.chat.id, str(ind) + ". " + smile_not_complete.decode() + block[ind][0])
        else:
            bot.send_message(message.chat.id, str(ind) + ". " + smile_complete.decode() + block[ind][0])


@bot.message_handler()
def post(message):
    user_state = mydb.GetUserState(message.chat.id)
    if user_state == UserState.Waiting_For_Task:
        smile = b'\xF0\x9F\x98\x89'
        bot.send_message(message.chat.id, "Таска добавлена. Вот что осталось сделать: " + smile.decode())
        Tasks_List.Add_Tasks(message.chat.id, str(message.text))
        tasks = Tasks_List.Get_Tasks(message.chat.id)
        print(tasks)
        Print_Tasks(message)
        mydb.UpdateUser(message.chat.id, UserState.Start_Task)
    elif user_state == UserState.Waiting_For_Marking:
        length = len(Tasks_List.Get_Tasks(message.chat.id))
        if int(message.text) not in range(0, length):
            bot.send_message(message.chat.id, "Не то пишешь. Введи номер таски дружок.")
        else:
            Tasks_List.Mark(message.chat.id, int(message.text))
            bot.send_message(message.chat.id, "Таска отмечена")
            mydb.UpdateUser(message.chat.id, UserState.Start_Marking)
    elif user_state == UserState.Waiting_For_Erase:
        length = len(Tasks_List.Get_Tasks(message.chat.id))
        if int(message.text) not in range(0, length):
            bot.send_message(message.chat.id, "Не то пишешь. Введи номер таски дружок.")
        else:
            Tasks_List.Erase(message.chat.id, int(message.text))
            bot.send_message(message.chat.id, "Таска удалена")
            mydb.UpdateUser(message.chat.id, UserState.Start_Erase)
    else:
        bot.send_message(message.chat.id, 'Ты попутал берега мальчик')


bot.polling(none_stop=True, interval=0)
