import csv
import datetime
import random


# Reads Opening Hours csv
with open('data/openHr.csv') as csv_hrs:
    csv_reader = csv.reader(csv_hrs)
    stores_opened = list(csv_reader)

# Reads Menu csv
with open('data/menu.csv') as csv_menu:
    menu_reader = csv.reader(csv_menu)
    menu = list(menu_reader)


# Get current Day
day = datetime.datetime.today().weekday()

# Get current time
now = datetime.datetime.now().time()
current_time = now.strftime('%H:%M:%S')
current_time = datetime.datetime.strptime(current_time, '%H:%M:%S').time()


# Matches user_time to breakfast/ lunch/ dinner/ closed
def time_check(time):
    if datetime.time(6, 0, 0) <= time <= datetime.time(11, 0, 0):
        time_period = 'Breakfast'
        return time_period
    elif datetime.time(11, 0, 1) <= time <= datetime.time(17, 0, 0):
        time_period = 'Lunch'
        return time_period
    elif datetime.time(17, 0, 1) <= time <= datetime.time(23, 0, 0):
        time_period = 'Dinner'
        return time_period
    else:
        time_period = 'Closed'
        return time_period

######################################################################################################################
# View Today's stores
def today_store_func():
    today_stores = []
    with open('data/storesopened.csv') as storesopencsv:
        reader = csv.DictReader(storesopencsv)
        for rows in reader:
            if day == int(rows['Day']):
                store_hrs_str=rows['Store']
                today_stores.append(store_hrs_str)

    return today_stores
#####################################################################################################################

# Parses user store input
def menu_input_parser(user_store_choice):
    time_period = time_check(current_time)  # Checks for current time_period: Breakfast/ Lunch/ Dinner/ Closed
    shop_list = list(today_store_func())
    store_menu = ""
    if user_store_choice in shop_list:  # Return items if store is opened
        for row in menu:
            if day == int(row[0]) and time_period == row[1] and user_store_choice == row[2]:
                store_menu = store_menu + (row[3] + " " + row[4] + "\n")

        if store_menu == "":  # Return string if none available
            return (user_store_choice + " " + time_period + " Menu currently has nothing available." +
                    "\n\n Press /start to return to main menu")

        else:
            return (user_store_choice + " " + time_period + " Menu currently has: \n" + store_menu +
                    "\n\n Press /start to return to main menu")

    else:  # Return error message if input is invalid
        return "I don't understand, please do try the command again \n\n Press /start to return to main menu"


def store_input_parser(user_store_choice):
    every_store_list = ['MiniWok', 'Mcdonalds', 'KFC', 'The Sandwich Guys', 'Malay', 'Indian']
    opening_days = ""
    if user_store_choice in every_store_list:
        for rows in stores_opened:
            if user_store_choice == rows[1]:
                opening_days = opening_days + ("\n"+user_store_choice + " is open on " + rows[2])

        return (user_store_choice + " are opened on the following days: \n" +
                opening_days + "\n\n Press /start to return to main menu")

    else:
        return "Invalid input, please do try /OperatingHours again" + "\n\n Press /start to return to main menu"


# Feature E: Waiting Time calculator
def waiting_time_func(queue_number):
    calculated_time = queue_number * 5
    hours = calculated_time // 60
    minutes = calculated_time % 60
    return hours, minutes


# Feature F: Prints store opening hours
def operating_hours_func():
    today_store_func()
    user_store_choice = input("Which store's operating hours would you like to check? ")
    for rows in stores_opened:
        if user_store_choice == rows[1]:
            print(user_store_choice + " is open on " + rows[2])


# Resets csv file to today's date
def datecsvchecker():
    now = datetime.datetime.now()
    current_date = now.strftime('%d:%m:%Y')
    lines = [line.rstrip('\n') for line in open('data/claimedvoucher.txt')]
    if current_date in lines:  # If current date is in csv, ignore
        pass
    else:  # Otherwise, rewrite whole csv file and write today's date
        with open('data/claimedvoucher.txt', 'w+') as csv_voucherwrite:
            csv_voucherwrite.write("\n" + current_date)
            csv_voucherwrite.close()


# Checks whether user has already claimed voucher for the day
def voucher_check(user_name):
    claimed_flag = 0  # Flag to verify whether user has already claimed voucher
    lines = [line.rstrip('\n') for line in open('data/claimedvoucher.txt')]
    if user_name in lines:
        claimed_flag = 1

    if claimed_flag == 0:  # If user has not claimed, return voucher number
        random_no = random.randint(1, 5)
        with open('data/claimedvoucher.txt', 'a', newline='') as csv_voucherwrite:
            csv_voucherwrite.write('\n' + user_name)  # Update name in csv and close file
            csv_voucherwrite.close()
            path = send_voucher_path(random_no)
            return path
        ###return "Your Voucher is " + str(random_no) + "\n\n Press /start to return to main menu"
    elif claimed_flag == 1:  # Otherwise, return message
        return "You have already claimed your voucher for today.\n\n Press /start to return to main menu"


# Returns catch of the day item and price
def catchoftheday_func():
    with open('data/catch.csv') as csv_catch:
        csv_reader_catch = csv.reader(csv_catch, delimiter=',')
        for row in csv_reader_catch:
            catch_list = row
        catch = catch_list[0]  # Returns today's catch item
        catch_price = catch_list[1]  # Returns today's catch price
        csv_catch.close()

    # Returns catch of the day photo
    if catch == "Cheeseburger":
        bot_photo = open('images/cheeseburger.jpg', 'rb')

    elif catch == "Big Mac":
        bot_photo = open('images/bigmac.jpg', 'rb')

    elif catch == "KFC Pocket":
        bot_photo = open('images/pocket.jpg', 'rb')

    bot_response = catch + " is at " + catch_price + " only for today!\nPress /start to return to main menu"
    return bot_photo, bot_response


# Returns day as integer from date
def usertime_store_func(day):
    today_stores = []
    for rows in stores_opened:
        if day == int(rows[0]):
            today_stores.append(rows[1])
    return today_stores
#######################################################################################################################
def send_voucher_path(number):
    with open('data/vouchers.csv') as vouchersCheck:
        reader = csv.DictReader(vouchersCheck)
        for rows in reader:
            if number == int(rows['VoucherNo']):
                return str("images/voucher"+rows['VoucherPath'])

#######################################################################################################################
# Returns menu items according to date, timeperiod and stall
def user_menu_input_parser(user_store_choice, user_day, user_timeperiod):
    time_period = time_check(current_time)  # Checks for current time_period: Breakfast/ Lunch/ Dinner/ Closed
    store_menu = ""
    for row in menu:
        if user_day == int(row[0]) and user_timeperiod == row[1] and user_store_choice == row[2]:
            store_menu = store_menu + (row[3] + " " + row[4] + "\n")

    if store_menu == "":  # Return string if none available
        return (user_store_choice + " " + time_period + " Menu has nothing available then." +
                "\n\n Press /start to return to main menu")

    else:
        return (user_store_choice + " " + time_period + " Menu will have: \n" + store_menu +
                "\n\n Press /start to return to main menu")
