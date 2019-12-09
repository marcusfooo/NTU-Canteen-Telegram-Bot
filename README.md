# ntu-canteen-app
CZ1003 Project

########################################################################

Members:
- BCG Marcus Foo
- CS Lim Wei Rong
- CS Lim Xiao Wei

*IMPORTANT*
We currently have the bot hosted on pythonanywhere.com. You may access the bot directly on Telegram by @goGrubBot
HOWEVER, in the case whereby the bot is not functioning properly, we have an alternative bot and token. You may start 
the bot by replacing the TOKEN string in bot.py with the TOKEN below and run the program. This alternative token
is for ANOTHER test bot @goGrubTest_bot instead.

TOKEN = 

For this assignment, we have decided to use the Telegram Bot API to interact with users as our frontend. The code for
our Telebot frontend is stored within the bot.py file, while our backend logic is stored within the utils.py file.
Rest our our csv and txt files are stored under the /data folder, images stored within /images and virtual environment
under /venv for the grader's convenience when loading the Python PATH.

Modules used include : csv, datetime, random, pyTelegramBotAPI

########################################################################

We have also attached the rubric along with the relevant functions for easier grading:

1. Use of string operations/functions (5)
   - Present in majority of functions

2. File operation and Exception handling (5)
   - Primarily in utils.py, we use try/ except blocks for exception handling
   - In bot.py /CheckStalls and /WaitingTime, we have try/ except blocks and bot.register_next_step_handler() to loop
     function again if user enters invalid input
   - Exception handling can also be found under bot.py, where we have a default fallback message for unknown commands
   - In the case whereby a user presses another function button during a function process, in bot.py we have check_reply()
     to execute the new function without an error

3-1. Use of Dictionary (5)
   - Implemented within utils.py today_store_func()
   - Implemented under utils.py send_voucher_path()
   - Implemented under utils.py catchoftheday_func()
   - Implemented under bot.py menu_dict for check_reply()
     
3-2. Use of tuple/list (5)
   - Present in majority of utils.py functions

4. Program correctness: Program produces the right outputhighlighted in the guideline (20)
   - All 7 commands within /start in bot.py have been tested for outputs, a default fallback is present in line 250
  of bot.py

5. Program organization: function, module (5)
   - Backend logic functions are stored under utils.py and imported in bot.py

6. Programming style: Clarity and comprehensibility of code (5)
   - All functions are commented with code explanations

7. Interface Design. User-friendliness (20)
   - Simple, clean and intuitive design using Telegram's interface

########################################################################

Features:

Feature C: Display the menu for all stalls based on current system date and time
  - bot.py /MenuDisplay

Feature D: Allow to set date and time to get opening stalls and their menu
  - bot.py /CheckStalls

Feature E: Allow to enter the number of people in the queue and calculate the corresponding estimated waiting time
  - bot.py /WaitingTime

Feature F: Allow to check the operating hours for all stalls
  - bot.py /OperatingHours

Additional Features:
  - bot.py /AboutUs
  - bot.py /CatchOfTheDay
  - bot.py /Voucher



