from telebot import types

#send number button

def num_button():
    #create space
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('Send number', request_contact=True)
    #add button to space
    kb.add(number)
    return kb

#send location button
def loc_button():
    #create space
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Send location', request_location=True)
    kb.add(location)
    return kb

#button for admin

def admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #createabuttons
    add_pr = types.KeyboardButton('Add a product')
    del_pr = types.KeyboardButton('Delete a product')
    edit_pr = types.KeyboardButton('Edit an amount of products')
    to_menu = types.KeyboardButton('To main page')
    #make buttons common
    kb.add(add_pr, edit_pr, del_pr)
    kb.row(to_menu)
    return kb 