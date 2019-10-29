import utils
import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

# Bot Settings
TOKEN = '712534091:AAGDpXymyg8wlAMvd7QEWwi9umNsRsXxUlE'
bot = telebot.TeleBot(TOKEN)

# UI inputs
hideBoard = ReplyKeyboardRemove()  # function to hide inline keyboard


# Start Menu
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "What would you like to do today :)\n\n" +
        "A) Know more about our team! /AboutUs\n" +
        "B) View today's Special Offer /CatchOfTheDay\n" +
        "C) Display current Stall Menus /MenuDisplay\n" +
        "Dx) Select date and time to get stall and menu\n" +
        "E) Display estimated waiting time /WaitingTime\n" +
        "F) Display Operating Hours for Stalls /OperatingHours\n" +
        "G) Claim your daily voucher! /Voucher\n"
    )


# Function for today's special deal
@bot.message_handler(commands=['CatchOfTheDay'])
def catchoftheDay(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot_photo, bot_response = utils.catchoftheday_func()  # Returns today's catch photo and response
    bot.send_photo(message.chat.id, bot_photo)  # Send catch photo
    bot.send_message(message.chat.id, bot_response)  # Send catch response


# Call to calculate waiting time
@bot.message_handler(commands=['WaitingTime'])
def waitingTime(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    queue_number = bot.send_message(message.chat.id, "Enter number of people in queue\n"
                                                     "or\n Press /start to return to main menu")
    bot.register_next_step_handler(queue_number, calculate)  # Proceeds to calculate function after user input


# Function to calculate waiting time
def calculate(message):
    try:
        queue_number = int(message.text)
        hours, minutes = utils.waiting_time_func(queue_number)  # Returns waiting time
        bot.send_message(message.chat.id, "The estimated queue time is %s hours and %s minutes." % (hours, minutes)
                         + "\n\n Press /start to return to main menu")

    except:
        bot.send_message(message.chat.id,"Error, please send a number\nPress /WaitingTime to try again "
                                         "or /start to pick another option")


# Call to MenuDisplay
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
    bot.register_next_step_handler(store_choices, menuSelect)


# Finds the operating hours for store selected
@bot.message_handler(commands=['OperatingHours'])
def operatingHours(message):
    store_select = ReplyKeyboardMarkup(one_time_keyboard=True)
    store_select.add('MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian')
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_choice = bot.send_message(message.chat.id, "Which store's operating hours would you like to check? ",
                                   reply_markup=store_select)  # Provides user inline keyboard
    bot.register_next_step_handler(user_choice, storeFinder)


# Call for voucher function
@bot.message_handler(commands=['Voucher'])
def voucher(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    user_name = str(message.from_user.username)  # Retrieves username
    utils.datecsvchecker()  # Checks if date in csv is today, if not, rewrite csv file
    bot_response = utils.voucher_check(user_name)  # Returns voucher if available
    bot.send_message(message.chat.id, bot_response)


# Call for AboutUs function
@bot.message_handler(commands=['AboutUs'])
def voucher(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot.send_photo(message.chat.id, open('logo.jpg', 'rb'))
    bot.send_message(message.chat.id, "goGrub is a project for AY19/20 CZ1003.\n\n"
                     "Our team members consists of:"
                     "\n - BCG Marcus Foo"
                     "\n - CS Lim Wei Rong"
                     "\n - CS Lim Xiao Wei"
                     "\n\n The logo above was made using logomakr.com"
                     + "\n\nPress /start to return to main menu")


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
    bot.send_message(chat_id=message.chat.id, text= bot_response, reply_markup=hideBoard)  # Removes inline keyboard


# Default fallback message
def command_default(message):
    bot.send_chat_action(message.chat.id, 'typing')  # Bot typing action
    bot.send_message(message.chat.id, "I don't understand, please do try the command again"
                     + "\n\n Press /start to return to main menu")


bot.polling()
