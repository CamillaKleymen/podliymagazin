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
#create button showing products
def main_menu_buttons(all_prods):
    #create space
    kb = types.InlineKeyboardMarkup(row_width=2)
    prod_buttons = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}')
                   for i in all_prods if i[2]>0
                   ]
    cart = types.InlineKeyboardButton(text='Cart', callback_data='cart')
    #make commmon button in space
    kb.add(*prod_buttons)
    kb.row(cart)
    return kb
#buttons with choice of count

def count_buttons(amount=1, plus_or_minus=''):
    #create cpace
    kb = types.InlineKeyboardMarkup(row_width=3)
    #create buttons
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    to_cart = types.InlineKeyboardButton(text = 'Add to cart', callback_data='to cart')
    back = types.InlineKeyboardButton(text='Back', callback_data='back')

    #algorithm of addition and substarction amount
    if plus_or_minus == 'increment':
        amount +=1
        current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)
    elif plus_or_minus == 'decrement':
        if amount > 1:
            amount -= 1
            current_amount = types.InlineKeyboardButton(text=str(amount), callback_data=amount)

    #add buttons to space

    kb.add(minus, current_amount, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb

#cart of buttons
def cart_buttons():
    kb = types.InlineKeyboardMarkup(row_width=2)
    #create button
    order = types.InlineKeyboardButton(text='Make an order', callback_data='order')
    back = types.InlineKeyboardButton(text='Back', callback_data='back')
    clear = types.InlineKeyboardButton(text="Clear cart", callback_data='clear')
    kb.add(order, back)
    kb.row(order)
    return kb