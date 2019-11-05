import utils
import telebot
import datetime
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

# Bot Settings

TOKEN = '712534091:AAHhTpG7i6AlRizqs1WfOU4rITwvBG_0Y4I'
bot = telebot.TeleBot(TOKEN)

# UI inputs
hideBoard = ReplyKeyboardRemove()  # function to hide inline keyboard

# Stored Values
user_selected_menu = ''
user_day = ''
user_timeperiod = ''

# Start Menu
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

# A)Call for AboutUs function
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


# B)Function for today's special deal
@bot.message_handler(commands=['CatchOfTheDay'])
def catchoftheDay(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot_photo, bot_response = utils.catchoftheday_func()  # Returns today's catch photo and response
    bot.send_photo(message.chat.id, bot_photo)  # Send catch photo
    bot.send_message(message.chat.id, bot_response)  # Send catch response


# C)Call to MenuDisplay
@bot.message_handler(commands=['MenuDisplay'])
def getMenu(message):
    shop_list = list(utils.today_store_func())  # Returns list of stores opened today
    item_select = ReplyKeyboardMarkup(one_time_keyboard=True)  # Converts list of stores to keyboard
    for i in shop_list:
        item_select.add(i)
    cid = message.chat.id
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    store_choices = bot.send_message(cid, "The stores opened today are: "
                                     , reply_markup=item_select)  # Provides user inline keyboard

    utils.today_store_func()
    bot.register_next_step_handler(store_choices, menuSelect)


# D)Call for Stall and Menu selection
@bot.message_handler(commands=['CheckStalls'])
def input_date(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_date = bot.reply_to(message, "Enter Date in the format: \nYYYY/MM/DD")  # Requests for date
    bot.register_next_step_handler(user_date, parse_user_date)


def parse_user_date(message):
    try:
        user_date = datetime.datetime.strptime(message.text, '%Y/%m/%d')  # Checks if date is valid
        global user_day
        user_day = user_date.weekday()  # Sets weekday integer as global var
        user_time = bot.reply_to(message, "Enter Time of specified Date in the format:"  # Requests for time
                                          "\nHH:MM")
        bot.register_next_step_handler(user_time, datetime_to_menu)

    except:
        bot.send_message(message.chat.id, "Invalid input given. Press /CheckStalls to try again"
                                          " or press /start to return to main menu.")


def datetime_to_menu(message):
    try:
        input_time = message.text + ":00"  # Adds Seconds to user given time for datetime conversion
        user_time = datetime.datetime.strptime(input_time, '%H:%M:%S').time()  # Converts to time format
        global user_timeperiod
        user_timeperiod = utils.time_check(user_time)  # Sets Breakfast/ Lunch/ Dinner as global var
        if user_timeperiod == 'Closed':
            bot.send_message(message.chat.id, "None of the stalls are opened at this time."
                             + "\n\n Press /start to return to Main Menu.")
        else:
            global user_selected_menu
            user_selected_menu = utils.usertime_store_func(user_day)  # Returns list of stores opened on given date
            item_select = ReplyKeyboardMarkup(one_time_keyboard=True)  # Converts list of stalls to keyboard
            for i in user_selected_menu:
                item_select.add(i)
            bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
            store_choices = bot.reply_to(message, "The stores opened today are: "
                                         , reply_markup=item_select)  # Provides user inline keyboard
            bot.register_next_step_handler(store_choices, user_menu_select)

    except:
        bot.send_message(message.chat.id, "Invalid input given. Press /CheckStalls to try again"
                                          " or press /start to return to main menu.")


def user_menu_select(message):
    user_store_choice = message.text
    if user_store_choice in user_selected_menu:  # Checks if user selects valid store
        bot_response = utils.user_menu_input_parser(user_store_choice, user_day, user_timeperiod)  # Returns response
        bot.send_message(message.chat.id, bot_response, reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, "I don't understand, please do try the command again."
                         + "\n\nPress /start to return to Main Menu.")


# E)Call to calculate waiting time
@bot.message_handler(commands=['WaitingTime'])
def waitingTime(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    queue_number = bot.send_message(message.chat.id, "Enter number of people in queue: ")
    bot.register_next_step_handler(queue_number, calculate)  # Proceeds to calculate function after user input


# Function to calculate waiting time
def calculate(message):
    try:
        queue_number = int(message.text)
        hours, minutes = utils.waiting_time_func(queue_number)  # Returns waiting time
        bot.send_message(message.chat.id, "The estimated queue time is %s hours and %s minutes." % (hours, minutes)
                         + "\n\nPress /start to return to Main Menu.")

    except:
        bot.send_message(message.chat.id,"Error, please enter a valid number\nPress /WaitingTime to try again "
                                         "or /start to return to Main Menu.")


# F)Finds the operating hours for store selected
@bot.message_handler(commands=['OperatingHours'])
def operatingHours(message):
    store_select = ReplyKeyboardMarkup(one_time_keyboard=True)
    store_select.add('MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian')
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_choice = bot.send_message(message.chat.id, "Which store's operating hours would you like to check? ",
                                   reply_markup=store_select)  # Provides user inline keyboard
    bot.register_next_step_handler(user_choice, storeFinder)


# G)Call for voucher function
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


# Followup function for MenuDisplay
@bot.message_handler(func=lambda message: True)
def menuSelect(message):
    cid = message.chat.id
    user_store_choice = message.text
    bot.send_chat_action(cid, 'typing')  # Bot typing action
    bot_response = utils.menu_input_parser(user_store_choice)  # Returns selected store items and price
    bot.send_message(message.chat.id, bot_response, reply_markup=hideBoard)  # Removes inline keyboard


# Followup function for Operating hours
@bot.message_handler(func=lambda message: True)
def storeFinder(message):
    user_store_choice = message.text
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot_response = utils.store_input_parser(user_store_choice)  # Returns selected store operating hours
    bot.send_message(chat_id=message.chat.id, text=bot_response, reply_markup=hideBoard)  # Removes inline keyboard


# Default fallback message
def command_default(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot.send_message(message.chat.id, "I don't understand, please do try the command again."
                     + "\n\nPress /start to return to Main Menu.")

bot.polling()
