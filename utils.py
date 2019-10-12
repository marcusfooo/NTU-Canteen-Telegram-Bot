import csv
import datetime


# Reads Opening Hours csv
with open('openHr.csv') as csv_hrs:
    csv_reader = csv.reader(csv_hrs)
    stores_opened = list(csv_reader)

# Reads Menu csv
with open('menu.csv') as csv_menu:
    menu_reader = csv.reader(csv_menu)
    menu = list(menu_reader)


# Get current Day
day = datetime.datetime.today().weekday()

# Get current time
now = datetime.datetime.now().time()
current_time = now.strftime('%H:%M:%S')
current_time = datetime.datetime.strptime(current_time, '%H:%M:%S').time()


# Matches user_time to breakfast/ lunch/ dinner/ closed
def time_check():
    if datetime.time(8, 0, 0) <= current_time <= datetime.time(11, 0, 0):
        time_period = 'Breakfast'
        return time_period
    elif datetime.time(11, 0, 1) <= current_time <= datetime.time(17, 0, 0):
        time_period = 'Lunch'
        return time_period
    elif datetime.time(17, 0, 1) <= current_time <= datetime.time(23, 0, 0):
        time_period = 'Dinner'
        return time_period
    else:
        time_period = 'Closed'
        return time_period


# Feature A + B: View Today's stores
def today_store_func():
    today_stores = []
    for rows in stores_opened:
        if day == int(rows[0]):
            today_stores.append(rows[1])
    print("The stores opened today are: " + ('[%s]' % ', '.join(map(str, today_stores))))
    return today_stores


# Feature C: Assign menu to 'menu' based on current time
def menu_func():
    today_store_func()
    time_period = time_check()
    store_menu = []
    store_choice = input("\nKindly input your store choice: ")
    for row in menu:
        if day == int(row[0]) and time_period == row[1] and store_choice == row[2]:
            store_menu.append({row[3]: row[4]})
    print(store_menu)


# Feature E: Waiting Time calculator
def waiting_time_func():
    queue_number = input("Kindly input number of people in queue: ")
    while True:
        try:
            queue_number = int(queue_number)
            break
        except:
            queue_number = input("Kindly input number of people in queue: ")

    calculated_time = queue_number * 5
    hours = calculated_time // 60
    minutes = calculated_time % 60
    print("The estimated queue time is %s hours and %s minutes." % (hours, minutes))


# Feature F: Prints store opening hours
def operating_hours_func():
    today_store_func()
    user_store_choice = input("Which store's operating hours would you like to check? ")
    for rows in stores_opened:
        if user_store_choice == rows[1]:
            print(user_store_choice + " is open on " + rows[2])




