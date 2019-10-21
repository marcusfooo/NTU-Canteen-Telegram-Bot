import csv
import random
from fileinput import close

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import utils
import telebot
import datetime
import json
import traceback

TOKEN = '712534091:AAGDpXymyg8wlAMvd7QEWwi9umNsRsXxUlE'

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Start handler, Choose a route\n" +
        "1) Press /OpenShops for shops that are currently open\n"+
        "2) Press /WaitingTime to calculate estimated queue time\n"+
        "3) Press /MenuDisplay to see your menu of choice\n"+
        "4) Press /OperatingHours to find the Operating hours for your desired shop\n"+
        "5) Press /Voucher to get your daily voucher"
    )
@bot.message_handler(commands=['OpenShops'])
def openShops(message):
    data = utils.today_store_func()
    openShops = '\n'.join(data)
    bot.send_message(message.chat.id,
                    "Stores opened today are: \n" + openShops + "\n\n Press /start to return to main menu")

#calculate waiting time
@bot.message_handler(commands=['WaitingTime'])
def waitingTime(message):
    queue_number=bot.send_message(message.chat.id, "Enter number of people in queue\nor\nPress /start to return to main menu")
    bot.register_next_step_handler(queue_number, calculate)#waits for user reply, once reply calls function calculate



def calculate(message):
    queue_number = message.text
    while True:
        try:
            queue_number = int(queue_number)
            break
        except:
            bot.send_message(message.chat.id,"Error, please send a number\nPress /WaitingTime to try again\nor\n/start to pick another option")

    calculated_time = queue_number * 5
    hours = calculated_time // 60
    minutes = calculated_time % 60
    bot.send_message(message.chat.id,"The estimated queue time is %s hours and %s minutes." % (hours, minutes))

#displays menu for selected store
@bot.message_handler(commands=['MenuDisplay'])
def MenuDisplay(message):
    openShops(message)
    time_period = utils.time_check()
    store_menu = []
    store_choice = bot.send_message(message.chat.id,"Please input your store choice")
    bot.register_next_step_handler(store_choice, MenuFinder)#waits for user to reply then calls menufinder function

def MenuFinder(message):
    correctflag=0
    time_period = utils.time_check()
    store_menu = ""
    for row in utils.menu:
        if utils.day == int(row[0]) and time_period == row[1] and message.text == row[2]:
            store_menu=store_menu+(row[3]+" "+row[4])
            correctflag = 1

    if correctflag==1:
        bot.send_message(message.chat.id, "Menu for today is \n" + store_menu)
    else:
        bot.send_message(message.chat.id,"Please enter proper store name \n\n Press /MenuDisplay to try again \n\nor\n press /start to return main menu")

#finds the operating hours for store selected
@bot.message_handler(commands=['OperatingHours'])
def OperatingHours(message):
    openShops(message)
    store_choice = bot.send_message(message.chat.id,"Which store's operating hours would you like to check? ")
    bot.register_next_step_handler(store_choice, StoreFinder)#waits for user reply and calls function storefinder

def StoreFinder(message):
    user_store_choice=message.text
    openingDays=""
    for rows in utils.stores_opened:
        if user_store_choice == rows[1]:
            openingDays=openingDays+("\n"+user_store_choice + " is open on " + rows[2])
            Openflag=1
        else:
            Closedflag=1
    print(openingDays)
    if Openflag==1:
        bot.send_message(message.chat.id, openingDays)
    else:
        bot.send_message(message.chat.id,"Please input valid store name")

    #read csv, if username has claimed voucher today reply voucher claimed
    #else give voucher & store username into csv

@bot.message_handler(commands=['Voucher'])
def voucher(message):
    #create function to check header with date if date is not current date replace header with current date and erase list
    Claimedflag=0
    Unclaimedflag=1
    data=[]
    user_name = str(message.from_user.username)#getusername
    print(user_name)
    with open('claimedvoucher.csv') as csv_vouchers:
        csv_reader = csv.reader(csv_vouchers, delimiter=',')
        for row in csv_reader:
            if user_name == row[0]:
                Claimedflag = 1
                Unclaimedflag = 0
                break
            else:
                print(1)
                Unclaimedflag = 1

    if(Unclaimedflag==1):
        randomno=random.randint(1,5)
        bot.send_message(message.chat.id,"Your Voucher is "+ str(randomno))
        with open('claimedvoucher.csv', 'w', newline='') as csv_voucherwrite:
            csv_voucherwrite.write(user_name)
    elif(Claimedflag==1):
        bot.send_message(message.chat.id,"Voucher has been claimed")

bot.polling(none_stop=True)


