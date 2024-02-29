import telebot
import buttons as bt
import database as db
from geopy import Nominatim

bot = telebot.TeleBot('7180973455:AAF-Yu9gCGNdLWU1Mtrn8SUr2a9hySteRpw')
# work with maps
geolocator = Nominatim(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 '
               'Safari/537.36')
#id of admin
admin_id = 631104511
# temprory data
users = {}


# обработчик команды/start

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = db.check_user(user_id)
    prods = db.get_pr()
    if check:
        bot.send_message(user_id, 'Shalom, welcome to Podliy Magaziin!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, "Choose a product:",
                        reply_markup=bt.main_menu_buttons(prods))
    else:
        bot.send_message(user_id, 'Shalom!'
                                  'Lets to make registration!\n'
                                  'Enter your name',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # step to get a name
        bot.register_next_step_handler(message, get_name)


# get name
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Cool, and now send a number!',
                     reply_markup=bt.num_button())
    # step to get of number
    bot.register_next_step_handler(message, get_number, user_name)


# step of getting of number
def get_number(message, user_name):
    user_id = message.from_user.id
    # if user sent a number through button
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'And now location too',
                         reply_markup=bt.loc_button())
        # step for getting location
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number)

        # if user sent a number not through button
    else:
        bot.send_message(user_id, 'Send a num through button!',
                         reply_markup=bt.num_button())
        bot.register_next_step_handler(message, get_number, user_name)


# step of getting location
def get_location(message, user_name, user_number):
    user_id = message.from_user.id
    # if user sent from button
    if message.location:
        user_location = geolocator.reverse(f'{message.location.latitude}, '
                                           f'{message.location.longitude}')
        db.register(user_id, user_name, user_number, str(user_location))
        bot.send_message(user_id, 'Registration was succesfully passed!')
    # if user sent location not from button
    else:
        bot.send_message(user_id, 'Send message through button!',
                         reply_markup=bt.loc_button())
        # return to step of getting location
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number)

#hcoice of amount
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_pr_amount(call):
    chat_id = call.message.chat.id
    if call.data == 'increment':
        new_amount = users[chat_id]['pr_count']
        new_amount += 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message.id,
                                      reply_markup=bt.count_buttons(new_amount, 'increment'))
    elif call.data == 'decrement':
        new_amount = users[chat_id]['pr_count']
        new_amount -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message.id,
                                      reply_markup=bt.count_buttons(new_amount, 'decrement'))

    elif call.data == 'back':
        prods = db.get_pr()
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id, "Returning you back to menu",
                         reply_markup=bt.main_menu_buttons(prods))
    elif call.data == 'to_cart':
        product = db.get_exact_pr(users[chat_id]['pr_name'])
        pr_amount = users[chat_id]['pr_count']
        total = product[3]*pr_amount
        db.add_pr(chat_id, product[0], pr_amount, total)
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id, 'Product was successfully add to cart, what you are going to do?',
                                  reply_markup=bt.cart_buttons())


#cart
@bot.callback_query_handler(lambda call: call.data in ['cart', 'order', 'back', 'clear'])
def cart_handle(call):
    chat_id = call.message.chat.id
    if call.data == 'cart':
        cart = db.show_cart(chat_id)
        text = (f'Your cart\n\n' 
                f'Product:{cart[1]}\n' 
                f'Amount:{cart[2]}\n' 
                f'Total: ${cart[3]}')
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id, text, reply_markup=bt.cart_buttons())
    elif call.data == 'clear':
        db.clear_cart(chat_id)
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id, 'Your cart was cleared',
                         reply_markup=bt.main_menu_buttons(prods))
    elif call.data == 'order':
        cart = db.make_order(chat_id)
        text =  f'New order!\n\n'
                f'id user:{cart[0][0]},\n'
                f'product:{cart[0][1]}\n'
                f'amount:{cart[0][2]}\n'
                f'total sum: ${cart[0][3]}\n'
                f'address:{cart[1][0]}'
            bot.send_message(admin_id, text)
            bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
            bot.send_message(chat_id, "Your order was successfully admited, empoyers connect to you soon!",
                             reply_markup=bt.main_menu_buttons(prods))

    elif call.data == 'back':
        prods = db.get_pr()
        bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
        bot.send_message(chat_id, "Returning you back to menu",
                         reply_markup=bt.main_menu_buttons(prods))

#step of info count products
@bot.callback_query_handler(lambda call: int(call.data) in db.get_pr())
def get_product(call):
    chat_id = call.message.chat.id
    exact_product = db.get_exact_pr(int(call.data))
    users[chat_id] = {'pr_name': call.data, 'pr_count':1}
    bot.delete_message(chat_id=chat_id, message_id=call.message.message.id)
    bot.send_photo(chat_id, photo=exact_product[4],
                   caption=f"Name of product:{exact_product[0]}, \n\n"
                   f'Description of product: {exact_product[1]}\n)'
                   f'Amount of product:{exact_product[2]}\n)'
                   f'Price of product:{exact_product[3]}',
                   reply_markup = bt.count_buttons())







#button admin

@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Welcome to admin dashboard',
                         reply_markup=bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'You are not admin!\n'
                                                    'Enter /start')
#step of adminchoice
def admin_choice(message):
    if message.text == 'Add a product':
        bot.send_message(admin_id, 'Lets start! Enter a name of product',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        #step for get name
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Delete a product':
        pr_check = db.check_pr()
        if pr_check:
            bot.send_message(admin_id, 'Enter id of product')
            bot.register_next_step_handler(message, get_pr_to_del)
        else:
            bot.send_message(admin_id, 'There are no any products')
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Edit an amount of products':
        pr_check = db.check_pr()
        if pr_check:
            bot.send_message(admin_id, 'Enter id of product')
            bot.register_next_step_handler(message, get_pr_to_edit)
        else:
            bot.send_message(admin_id, 'There are no any products')
            bot.register_next_step_handler(message, admin_choice)
#step of getting of name product
def get_pr_name(message):
    pr_name = message.text
    bot.send_message(admin_id, 'Now create a description of product!')
    bot.register_next_step_handler(message, get_pr_description, pr_name)

def get_pr_description(message, pr_name):
    pr_description = message.text
    bot.send_message(admin_id, 'Now enter an amount of product!')
    bot.register_next_step_handler(message, get_pr_count,
                                   pr_name, get_pr_description)

#step of getting amount

def get_pr_count(message, pr_name, pr_description):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Enter only integer numbers!')
        #return to step of getting amount
        bot.register_next_step_handler(message, get_pr_count,
                                       get_pr_name, get_pr_description)
    else:
        pr_count = int(message.text)
        bot.send_message(admin_id, 'Which price of product?')
        bot.register_next_step_handler(message, get_pr_price,
                                       pr_name, pr_description, pr_count)

def get_pr_price(message, pr_name, pr_description, pr_count):
    if message.text.isdecimal() is not True:
        bot.send_message(admin_id, 'Enter only float numbers!')
        #return to step of getting amount
        bot.register_next_step_handler(message, get_pr_price,
                                       get_pr_name, get_pr_description, pr_count)
    else:
        pr_price = float(message.text)
        bot.send_message(admin_id, 'Last step enter on the website'
                                        'https://postimages.org/ and upload there photos.\n'
                                        'Then, send me right link to photo')
        #step of getting of photo
        bot.register_next_step_handler(message, get_pr_photo,
                                       pr_name, pr_description, pr_count, pr_price)
#step of getting photo
def get_pr_photo(message, pr_name, pr_description, pr_count, pr_price):
    pr_photo = message.text
    db.add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo)
    bot.send_message(admin_id, 'Ready! Anything else?',
                     reply_markup=bt.admin_buttons())
    #step on command choice
    bot.register_next_step_handler(message, admin_choice)
#edition of product
def get_pr_to_edit(message):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Enter only integer numbers!')
        #return to step of getting amount
        bot.register_next_step_handler(message, get_pr_to_edit)
    else:
        pr_id = int(message.text)
        bot.send_message(admin_id, 'How much amount of product arrived?')
        #step to getting stock
        bot.register_next_step_handler(message, get_pr_stock, pr_id)

#step of getting stock
def get_pr_stock(message, pr_id):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Enter only integer numbers!')
        #return to step of getting amount
        bot.register_next_step_handler(message, get_pr_stock, pr_id)
    else:
        pr_stock = int(message.text)
        db.change_pr_count(pr_id, pr_stock)
        bot.send_message(admin_id, 'Amount of products was edited!',
                         reply_markup=bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)


def get_pr_to_del(message):
    if message.text.isnumeric() is not True:
        bot.send_message(admin_id, 'Enter only integer numbers!')
        #return to step of getting amount
        bot.register_next_step_handler(message, get_pr_to_del)
    else:
        pr_id = int(message.text)
        db.del_pr(pr_id)
        bot.send_message(admin_id, 'Product was successfully deleted!',
                         reply_markup=bt.admin_buttons())
        bot.register_next_step_handler(message, admin_choice)


# zapusk bot

bot.polling()
