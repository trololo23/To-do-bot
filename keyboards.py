from telebot import types
Menu_board = types.InlineKeyboardMarkup()
Tasks = types.InlineKeyboardButton("Таски", callback_data='1')
Add = types.InlineKeyboardButton("Добавить", callback_data= '2')
Menu_board.add(Tasks)
Menu_board.add(Add)


Keys = types.InlineKeyboardMarkup()
Back = types.InlineKeyboardButton("Назад", callback_data='3')
Keys.add(Back)


def Suda_Keyboard(List_Tasks):
    smile_complete = b'\xE2\x9C\x85'
    smile_not_complete = b"\xE2\x9D\x8C"
    smile_trash = b'\xF0\x9F\x9A\xBD'
    smile_left = b'\xE2\x8F\xAA'
    smile_right = b'\xE2\x8F\xA9'
    Big_Klava = types.InlineKeyboardMarkup()
    for i in range(len(List_Tasks)):
        text = str(List_Tasks[i][0])
        if List_Tasks[i][0] == 0:
            patch = types.InlineKeyboardButton(str(smile_not_complete.decode()), callback_data="patch=" + str(i))
        else:
            patch = types.InlineKeyboardButton(str(smile_complete.decode()), callback_data="patch=" + str(i))
        taska = types.InlineKeyboardButton(text, callback_data="sth")
        delete = types.InlineKeyboardButton(str(smile_trash.decode()), callback_data="delete=" + str(i))
        Big_Klava.add(taska, patch, delete)
    left_button = types.InlineKeyboardButton(str(smile_left.decode()), callback_data="nth")
    right_button = types.InlineKeyboardButton(str(smile_right.decode()), callback_data="sth")
    Big_Klava.add(left_button, Back, right_button)
    return Big_Klava
