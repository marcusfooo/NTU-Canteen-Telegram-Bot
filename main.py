from utils import today_store_func, menu_func, waiting_time_func, operating_hours_func
from time import sleep


def user_menu():
    while True:
        user_input = input("Hello! Please select a function :) \n"
                         "1) View Stores opened today \n"
                         "2) Check Menu for Stores opened today \n"
                         "3) Check Waiting Time \n"
                         "4) View Store Opening Hours \n"
                         "\n"
                         "Select Option Number: ")

        try:
            int_input = int(user_input)
            if int_input == 1:
                today_store_func()
                break

            elif int_input == 2:
                menu_func()
                break

            elif int_input == 3:
                waiting_time_func()
                break

            elif int_input == 4:
                operating_hours_func()
                break

            else:
                print("Kindly enter a valid option number")

        except:
            print("Kindly enter a number")






if __name__ == "__main__":
    while True:
        user_menu()

        print('*********************************** \n'
              '*********************************** \n'
              '*********************************** \n')
        sleep(3)
