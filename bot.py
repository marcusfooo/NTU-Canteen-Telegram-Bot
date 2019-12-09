import utils
import telebot
import datetime
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

# Bot Settings

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

# UI inputs
hideBoard = ReplyKeyboardRemove()  # function to hide inline keyboard

# Stored Values
user_selected_menu = ''
user_day = ''
user_time = ''
user_timeperiod = ''
menu_dict = {
    "/start": "start_command",
    "/AboutUs": "about_us",
    "/CatchOfTheDay": "catchoftheDay",
    "/MenuDisplay": "getMenu",
    "/CheckStalls": "input_date",
    "/WaitingTime": "waitingTime",
    "/OperatingHours": "operatingHours",
    "/Voucher": "voucher"
}

# Start Menu, Wei Rong
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "What would you like to do today :)\n\n" +
        "A) Know more about our team! /AboutUs\n" +
        "B) View today's Special Offer /CatchOfTheDay\n" +
        "C) Display current Stall Menus /MenuDisplay\n" +
        "D) Select date and time to get Stalls and Menus /CheckStalls\n" +
        "E) Display estimated waiting time /WaitingTime\n" +
        "F) Display Operating Hours for Stalls /OperatingHours\n" +
        "G) Claim your daily voucher! /Voucher\n"
    )

# A)Call for AboutUs function, Xiao Wei
@bot.message_handler(commands=['AboutUs'])
def about_us(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot.send_photo(message.chat.id, open('images/logo.jpg', 'rb'))
    bot.send_message(message.chat.id, "goGrub is a project for AY19/20 CZ1003.\n\n"
                     "Our team members consists of:"
                     "\n - BCG Marcus Foo"
                     "\n - CS Lim Wei Rong"
                     "\n - CS Lim Xiao Wei"
                     "\n\nThe logo above was made using logomakr.com"
                     + "\n\nPress /start to return to Main Menu.")


# B)Function for today's special deal, Xiao Wei
@bot.message_handler(commands=['CatchOfTheDay'])
def catchoftheDay(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot_photo, bot_response = utils.catchoftheday_func()  # Returns today's catch photo and response
    bot.send_photo(message.chat.id, bot_photo)  # Send catch photo
    bot.send_message(message.chat.id, bot_response)  # Send catch response


# C)Call to MenuDisplay, Xiao Wei
@bot.message_handler(commands=['MenuDisplay'])
def getMenu(message):
    shop_list = list(utils.today_store_func())  # Returns list of stores opened today
    item_select = ReplyKeyboardMarkup(one_time_keyboard=True)  # Converts list of stores to keyboard
    for i in shop_list:
        item_select.add(i)
    cid = message.chat.id
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    store_choices = bot.send_message(cid, "The stores opened today are: \n"
                                          + str(shop_list), reply_markup=item_select)  # Display Keyboard

    utils.today_store_func()
    bot.register_next_step_handler(store_choices, menuSelect)


# D)Call for Stall and Menu selection, Marcus
@bot.message_handler(commands=['CheckStalls'])
def input_date(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_date = bot.reply_to(message, "Enter Date in the format: \nYYYY/MM/DD")  # Requests for date
    bot.register_next_step_handler(user_date, parse_user_date)


# Marcus
def parse_user_date(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        try:
            user_date = datetime.datetime.strptime(message.text, '%Y/%m/%d')  # Checks if date is valid
            global user_day
            user_day = user_date.weekday()  # Sets weekday integer as global var
            user_time = bot.reply_to(message, "Enter Time of specified Date in the format:"  # Requests for time
                                      "\nHH:MM")
            bot.register_next_step_handler(user_time, datetime_to_menu)

        except ValueError:
            user_datetry = bot.reply_to(message, "Invalid input given. Try entering Date in the format: \nYYYY/MM/DD"
                                               "\nOr press /start to return to main menu.")  # Requests for date
            bot.register_next_step_handler(user_datetry, parse_user_date)


# Marcus
def datetime_to_menu(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        try:
            input_time = message.text + ":00"  # Adds Seconds to user given time for datetime conversion
            global user_timeperiod, user_time
            user_time = datetime.datetime.strptime(input_time, '%H:%M:%S').time()  # Converts to time format
            user_timeperiod = utils.time_check(user_time)
            if user_timeperiod == 'Closed':  # Checks if time given is when all stores are generally closed
                bot.send_message(message.chat.id, "None of the stalls are opened at this time."
                                 + "\n\n Press /start to return to Main Menu.")
            else:
                global user_selected_menu
                user_selected_menu = utils.usertime_store_func(user_day)  # Returns list of stores opened on given date
                item_select = ReplyKeyboardMarkup(one_time_keyboard=True)  # Converts list of stalls to keyboard
                for i in user_selected_menu:
                    item_select.add(i)
                bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
                store_choices = bot.reply_to(message, "The stores opened that day are: ", reply_markup=item_select)
                bot.register_next_step_handler(store_choices, user_menu_select)

        except ValueError:
            user_timetry = bot.reply_to(message, "Invalid input given. Try entering Time in the format: \nHH:MM"
                                                 "\nOr press /start to return to main menu.")  # Requests for time
            bot.register_next_step_handler(user_timetry, datetime_to_menu)


# Marcus
def user_menu_select(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        user_store_choice = message.text
        if user_store_choice in user_selected_menu:  # Checks if user selects valid store
            global user_timeperiod
            user_timeperiod = utils.time_close(user_store_choice, user_day, user_time)  # Specifically checks if time is open for a stall
            if user_timeperiod == 'Closed':
                bot.send_message(message.chat.id, user_store_choice + " is closed at this time."
                                 + "\n\n Press /start to return to Main Menu.")
            else:
                bot_response = utils.user_menu_input_parser(user_store_choice, user_day, user_timeperiod)  # Return response
                bot.send_message(message.chat.id, bot_response, reply_markup=hideBoard)
        else:
            item_select = ReplyKeyboardMarkup(one_time_keyboard=True)  # Converts list of stalls to keyboard
            for i in user_selected_menu:
                item_select.add(i)
            bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
            store_choices = bot.reply_to(message, "Invalid input given, please try again."
                                                  "\nThe stores opened today are: ", reply_markup=item_select)
            bot.register_next_step_handler(store_choices, user_menu_select)


# E)Call to calculate waiting time, Wei Rong
@bot.message_handler(commands=['WaitingTime'])
def waitingTime(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    queue_number = bot.send_message(message.chat.id, "Enter number of people in queue: ")
    bot.register_next_step_handler(queue_number, calculate)  # Proceeds to calculate function after user input


# Function to calculate waiting time, Wei Rong
def calculate(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        try:
            queue_number = int(message.text)
            if queue_number <= 0:
                user_intTry = bot.reply_to(message, "Error, please try again using a positive integer."
                                                    "\nOr press /start to return to Main Menu.")  # Requests for Waiting Time
                bot.register_next_step_handler(user_intTry, calculate)
            else:
                hours, minutes = utils.waiting_time_func(queue_number)  # Returns waiting time
                bot.send_message(message.chat.id, "The estimated queue time is %s hours and %s minutes." % (hours, minutes)
                                 + "\n\nPress /start to return to Main Menu.")

        except ValueError:
            user_intTry = bot.reply_to(message, "Error, please try again using a valid integer."
                                             "\nOr press /start to return to Main Menu.")  # Requests for Waiting Time
            bot.register_next_step_handler(user_intTry, calculate)


# F)Finds the operating hours for store selected, Marcus
@bot.message_handler(commands=['OperatingHours'])
def operatingHours(message):
    store_select = ReplyKeyboardMarkup(one_time_keyboard=True)
    store_select.add('MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian')
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_choice = bot.send_message(message.chat.id, "Which store's operating hours would you like to check? ",
                                   reply_markup=store_select)  # Provides user inline keyboard
    bot.register_next_step_handler(user_choice, storeFinder)


# G)Call for voucher function, Wei Rong
@bot.message_handler(commands=['Voucher'])
def voucher(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_name = str(message.from_user.username)  # Retrieves username
    utils.datecsvchecker()  # Checks if date in csv is today, if not, rewrite csv file
    bot_response = utils.voucher_check(user_name)  # Returns voucher if available
    if bot_response != "You have already claimed your voucher for today.\n\n Press /start to return to main menu":
        photo = open(bot_response, 'rb')
        bot.send_message(message.chat.id, "Here is your voucher for today!")
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, bot_response)


# Followup function for MenuDisplay, Xiao Wei
@bot.message_handler(func=lambda message: True)
def menuSelect(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        cid = message.chat.id
        user_store_choice = message.text
        bot.send_chat_action(cid, 'typing')  # Bot typing action
        bot_response = utils.menu_input_parser(user_store_choice)  # Returns selected store items and price
        bot.send_message(message.chat.id, bot_response, reply_markup=hideBoard)  # Removes inline keyboard


# Followup function for Operating , Marcus
@bot.message_handler(func=lambda message: True)
def storeFinder(message):
    if message.text in menu_dict:  # Checks whether user selects another function
        check_reply(message)  # Starts new function if user selects another function midway
    else:
        user_store_choice = message.text
        bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
        bot_response = utils.store_input_parser(user_store_choice)  # Returns selected store operating hours
        bot.send_message(chat_id=message.chat.id, text=bot_response, reply_markup=hideBoard)  # Removes inline keyboard


# Function to execute new function if user inputs and switches to another function, Marcus
def check_reply(message):
    message_input = message.text
    if message_input == "/start":
        start_command(message)
    elif message_input == "/AboutUs":
        about_us(message)
    elif message_input == "/CatchOfTheDay":
        catchoftheDay(message)
    elif message_input == "/MenuDisplay":
        getMenu(message)
    elif message_input == "/CheckStalls":
        input_date(message)
    elif message_input == "/WaitingTime":
        waitingTime(message)
    elif message_input == "/OperatingHours":
        operatingHours(message)
    elif message_input == "/Voucher":
        voucher(message)


# Default fallback message, Xiao Wei
def command_default(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot.send_message(message.chat.id, "I don't understand, please do try the command again."
                     + "\n\nPress /start to return to Main Menu.")


bot.infinity_polling()

