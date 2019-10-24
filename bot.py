import csv
import random
import utils
import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
import datetime

# Bot Settings
TOKEN = '712534091:AAGDpXymyg8wlAMvd7QEWwi9umNsRsXxUlE'
bot = telebot.TeleBot(TOKEN)


# UI inputs
shop_list = list(utils.today_store_func())
every_store_list = ['MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian']
storeSelect = ReplyKeyboardMarkup(one_time_keyboard=True)
storeSelect.add('MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian')
itemSelect = ReplyKeyboardMarkup(one_time_keyboard=True)
for i in shop_list:
    itemSelect.add(i)
hideBoard = ReplyKeyboardRemove()


# Start Menu
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "What would you like to do today :)\n\n" +
        "1) Press /WaitingTime to calculate estimated queue time\n"+
        "2) Press /MenuDisplay to see your menu of choice\n"+
        "3) Press /OperatingHours to find the Operating hours for your desired shop\n"+
        "4) Press /Voucher to get your daily voucher"
    )


# Call to calculate waiting time
@bot.message_handler(commands=['WaitingTime'])
def waitingTime(message):
    bot.send_chat_action(message.chat.id, 'typing')
    queue_number = bot.send_message(message.chat.id, "Enter number of people in queue\nor\n"
                                                   "Press /start to return to main menu")
    bot.register_next_step_handler(queue_number, calculate)


# Function to calculate waiting time
def calculate(message):
    queue_number = message.text
    try:
        queue_number = int(queue_number)
        calculated_time = queue_number * 5
        hours = calculated_time // 60
        minutes = calculated_time % 60
        bot.send_message(message.chat.id, "The estimated queue time is %s hours and %s minutes." % (hours, minutes)
                         + "\n\n Press /start to return to main menu")

    except:
        bot.send_message(message.chat.id,"Error, please send a number\nPress /WaitingTime to try again\n"
                                         "or\n/start to pick another option")


# Call to MenuDisplay
@bot.message_handler(commands=['MenuDisplay'])
def getMenu(message):
    cid = message.chat.id
    bot.send_chat_action(message.chat.id, 'typing')
    store_choices = bot.send_message(cid, "The stores opened today are: ", reply_markup=itemSelect)
    bot.register_next_step_handler(store_choices, menuSelect)


# Finds the operating hours for store selected
@bot.message_handler(commands=['OperatingHours'])
def operatingHours(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user_choice = bot.send_message(message.chat.id, "Which store's operating hours would you like to check? ",
                                   reply_markup=storeSelect)
    bot.register_next_step_handler(user_choice, storeFinder)


# Call for voucher function
@bot.message_handler(commands=['Voucher'])
def voucher(message):
    Claimedflag = 0
    Unclaimedflag = 1
    bot.send_chat_action(message.chat.id, 'typing')
    user_name = str(message.from_user.username)#getusername
    datecsvchecker()
    with open('claimedvoucher.csv') as csv_vouchers:
        csv_reader = csv.reader(csv_vouchers, delimiter=',')
        for row in csv_reader:
            if user_name == row[0]:
                Claimedflag = 1
                Unclaimedflag = 0
                break
            else:
                Unclaimedflag = 1

    if Unclaimedflag == 1:
        randomno=random.randint(1,5)
        bot.send_message(message.chat.id, "Your Voucher is "+ str(randomno)+ "\n\n Press /start to return to main menu")
        with open('claimedvoucher.csv', 'a', newline='') as csv_voucherwrite:
            csv_voucherwrite.write("\n" + user_name)
    elif Claimedflag == 1:
        bot.send_message(message.chat.id, "You have already claimed your voucher for today."
                         + "\n\n Press /start to return to main menu")


# Resets voucher claims for the day
def datecsvchecker():
    now = datetime.datetime.now()
    current_date = now.strftime('%d:%m:%Y')
    wrong_date = 0
    with open('claimedvoucher.csv') as csv_vouchers:
        csv_reader = csv.reader(csv_vouchers, delimiter=',')
        for row in csv_reader:
            if row[0] == current_date:
                wrong_date = 0
                break
            else:
                wrong_date = 1

    if wrong_date == 1:
        filename = 'claimedvoucher.csv'
        f = open(filename, "w+")
        f.close()
        with open('claimedvoucher.csv', 'w', newline='') as csv_voucherwrite:
            csv_voucherwrite.write(current_date)
            csv_voucherwrite.write("\n")
            csv_voucherwrite.close()


# Followup function for MenuDisplay
@bot.message_handler(func=lambda message: True)
def menuSelect(message):
    cid = message.chat.id
    user_store_choice = message.text
    bot.send_chat_action(cid, 'typing')
    time_period = utils.time_check()
    store_menu = ""
    if user_store_choice in shop_list:
        for row in utils.menu:
            if utils.day == int(row[0]) and time_period == row[1] and user_store_choice == row[2]:
                store_menu = store_menu + (row[3] + " " + row[4])
                bot.send_message(chat_id=message.chat.id, text=user_store_choice + " currently has: " + store_menu
                                 + "\n\n Press /start to return to main menu", reply_markup=hideBoard)
        if store_menu == "":
            bot.send_message(chat_id=message.chat.id, text=user_store_choice + " currently has nothing available."
                                                + "\n\n Press /start to return to main menu", reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, "Invalid input, please do try /MenuDisplay again"
                         + "\n\n Press /start to return to main menu", reply_markup=hideBoard)


# Followup function for Operating hours
@bot.message_handler(func=lambda message: True)
def storeFinder(message):
    user_store_choice = message.text
    opening_days = ""
    bot.send_chat_action(message.chat.id, 'typing')
    if user_store_choice in every_store_list:
        for rows in utils.stores_opened:
            if user_store_choice == rows[1]:
                opening_days = opening_days + ("\n"+user_store_choice + " is open on " + rows[2])
        bot.send_message(chat_id=message.chat.id, text=user_store_choice + " are opened on the following days: \n"
                        + opening_days + "\n\n Press /start to return to main menu", reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, "Invalid input, please do try /OperatingHours again"
                         + "\n\n Press /start to return to main menu", reply_markup=hideBoard)


# Fallback message
def command_default(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "I don't understand, please do try the command again"
                     + "\n\n Press /start to return to main menu")


bot.polling()
