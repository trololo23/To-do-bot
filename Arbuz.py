import telebot
import database
from states import UserState
from keyboards import Menu_board, Keys, Suda_Keyboard
token = '2024475749:AAFjWzucPeHxWGLEtX15UCwyKE8rRvk0OeY'
bot = telebot.TeleBot(token)

mydb = database.Database()
Tasks_List = database.Operate()


Message_Id = database.Local_Message_Id()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Типа меню, доступные команды:', reply_markup=Menu_board)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "1":
        block = Tasks_List.Get_Tasks(call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Список тасок ага да", reply_markup=Suda_Keyboard(block))
    if call.data == "2":
        smile = b'\xF0\x9F\x91\xBD'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=smile.decode() + 'Пиши что хочешь сделать)' + smile.decode())
        Message_Id.Change_Id_Message(call.message.chat.id, call.message.id, "menu")
        mydb.UpdateUser(call.message.chat.id, UserState.Waiting_For_Task)
    if call.data == "3":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Типа меню, доступные команды:", reply_markup=Menu_board)


@bot.message_handler()
def post(message):
    user_state = mydb.GetUserState(message.chat.id)
    if user_state == UserState.Waiting_For_Task:
        Tasks_List.Add_Tasks(message.chat.id, str(message.text))
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=Message_Id.Get_Id_Message(message.chat.id, "menu"), text="Таска добавлена дед)", reply_markup=Keys)
        mydb.UpdateUser(message.chat.id, UserState.Start_Task)
    else:
        bot.delete_message(message.chat.id, message.message_id)


bot.polling(none_stop=True, interval=0)
