"""
Boring stuff
Author: Daniel Ferguson
Auth ID: 3374690
Date: Start -> 10/04/22 Completion -> 12/04/22
Task: INFT1004 Assignment 2: Spending Spree
I have ported large parts of this program from assessment 1 :)
I have integrated Pandas Dataframes into the ported code for csv manipulation
On first start this program will create the required csv files, thus this .py is the only submitted file
You DO NOT need to write defs into the console, just run the entire program.
"""
import os
import sys
import time as t
import pandas as pd
from getpass import getuser


class MainMenu:
    def __init__(self):
        self.dt = 0.3  # default time for t.sleep

        # vars ported from assess1, may cull over time
        self.gc_items_lst = []  # init variables so that other defs can use them
        self.gc_cost_lst = []
        self.loop_count = 0
        self.gc_name = ""
        self.gc_max_spend = 0
        self.gc_max_items = 0
        self.username = ""
        self.name_assigned = False

    def menu(self):
        if not self.name_assigned:  # if not implemented so user only enters name once
            print("Hello " + str(getuser()) + "!\n")  # :)
            self.username = str(getuser())
            self.name_assigned = True
            t.sleep(1)

        print("Welcome to the Spending Spree Menu!\n")
        t.sleep(self.dt)

        print('')
        print("Options:\n 1. Define a gift card. \n 2. Go on a Spending Spree. \n 3. Display list of existing gift "
              "cards.\n 4. Display spending history. \n Q. Quit the program (Q).\n")

        choice = input("Choose 1, 2, 3, 4 or Q: ")
        if choice == '1':
            self.gift_card()  # pretty self-explanatory, launches the def gift_card
        if choice == '2':
            self.spending_spree()
        if choice == '3':
            self.gc_names()
        if choice == '4':
            self.gc_history()
        if choice.lower() == 'q':
            print("Goodbye! ")

    def gift_card(self):  # 1
        print("Hello, I am Delilah, your personal gift card management system.")
        t.sleep(self.dt)  # stops the sequence for .3, adds readability
        print("Please enter the specifications of your gift card.\n")

        # all inputs are for the gift card specifications.
        gc_name = input("Gift card name:")
        gc_name = input_checker(gc_name, 'giftCards.csv', 'GiftCardName')  # runs input_checker method
        # input_checker is used to determine if gift card name has been used, gc_name will be reassigned if it has

        # check_input_type is used to make sure the input given is the type wanted, will be reassigned if it isn't
        gc_max_spend = check_input_type(input("Gift card maximum spending ($100-$500): "), float)
        while gc_max_spend > 500 or gc_max_spend < 100:  # checks if input fits requirements, loops until it does
            gc_max_spend = check_input_type(input("Please enter a value in a range of $100-$500: "), float)

        gc_max_items = check_input_type(input("Maximum number of items allowed to purchase (1-5): "), int)
        while gc_max_items < 1 or gc_max_items > 5:
            gc_max_items = check_input_type(input("Please enter a value in a range of 1-5: "), int)

        print('')

        # prints out the previously input details
        t.sleep(self.dt)
        print("These are your gift card details:\n" + "\nGift card name: " + gc_name)
        t.sleep(self.dt)
        print("Gift card maximum spending allowed: $" + str(gc_max_spend))
        t.sleep(self.dt)
        print("Gift card maximum number of items allowed to purchase: " + str(gc_max_items) + "\n")

        df = pd.read_csv('giftCards.csv')  # reads giftCards.csv into Dataframe df
        df.loc[len(df)] = [gc_name, gc_max_spend, gc_max_items]  # creates a new row and adds the gc details into it
        df.to_csv('giftCards.csv', index=None)  # writes the Dataframe to the csv file.

        re_to_menu = input("Would you like to return to the menu (Yes or No): ")
        if re_to_menu.upper() == "Y" or re_to_menu.upper() == "YES":
            self.menu()  # returns to menu
        else:
            sys.exit()  # ends program

    def spending_spree(self):  # 2
        df = pd.read_csv('giftCards.csv')  # reads giftCards.csv into Dataframe df

        print("\nPlease choose a gift card from this list: \n")
        for col in range(len(df)):
            t.sleep(self.dt)
            if col == 0:
                print(str(col + 1) + ". " + str(df.loc[col, 'GiftCardName']) + " (Default)")
            else:
                print(str(col + 1) + ". " + str(df.loc[col, 'GiftCardName']))

        col_ch = check_input_type(input("Please enter which card you would like to use (1, 2, 3 etc): "), int) - 1
        allowed_ans = False
        # stops user being able to choose an option that will error out the rest of the program.
        while not allowed_ans:
            if col_ch < 0 or col_ch > (len(df) - 1):  # only allows user to choose a number inside
                col_ch = check_input_type(input("Please enter a number listed above: "), int) - 1
            else:
                allowed_ans = True

        print('')
        # column choice (gc choice), used to assign vars below

        gc_card_name = df.loc[col_ch, 'GiftCardName']  # pulls item specified by col_ch from column 'SpendingLimit'
        gc_max_spend = df.loc[col_ch, 'SpendingLimit']  # assigns to local vars so ported program can be used
        gc_max_items = df.loc[col_ch, 'MaxItems']

        print("You have chosen:\n Gift Card : " + str(gc_card_name) + "\n Spending Limit: $" + str(gc_max_spend) +
              "\n Item Limit: " + str(gc_max_items))
        print('')

        # ported from assess 1 :)

        t.sleep(self.dt)
        temp_max = 0
        # gc_max_items = self.gc_max_items  # pulls variable values from init def  # deprecated by df.loc
        # gc_max_spend = self.gc_max_spend
        gc_cost_lst = self.gc_cost_lst
        gc_items_lst = self.gc_items_lst
        loop_count = self.loop_count

        # no str into int input exception handling has been implemented, as isn't mentioned in marking guidelines.
        # loop will repeat until loop_count is greater than gc_max_items or temp_max is higher than gc_max_spend
        while loop_count < gc_max_items and temp_max < gc_max_spend:
            cost = check_input_type(input("Purchase price: "), float)  # takes user input into cost variable

            temp_max = temp_max + cost  # stores the temporary total cost

            if temp_max <= gc_max_spend:  # checks if temp max is lower or equal to max spend
                gc_cost = cost  # assigns gc_cost the value of cost
                gc_cost_lst.append(gc_cost)  # appends gc_cost value into gc_cost_lst

                gc_items_desc = input("Purchase description: ")  # takes user input for item description
                gc_items_lst.append(gc_items_desc)  # appends input desc into items lst
                loop_count = loop_count + 1  # increments loop count

            else:
                print("\nThe gift card doesn't have enough funds to process this purchase, please try again.")

                # resets temp_max back to the last accepted spending amount by settings its value to gc_cost_lst
                temp_max = sum(gc_cost_lst)

            t.sleep(self.dt)
            print("Gift card used so far: $" + str(temp_max) + " out of $" + str(gc_max_spend) + "\n")
            self.loop_count = loop_count  # loop is modified after assignment so self.loop needs to be updated

        # ported def loop from assess 1.
        # nests Cost and Items into sublists so that Cost var can be manipulated using sorted function
        # use prints on the below lists after manipulation to gain greater understanding of what is happening :)
        gc_list_nested = [list(x) for x in zip(gc_cost_lst, gc_items_lst)]
        # uses nested list to sort nested items based on cost, because desc is nested it follows cost movement
        gc_list_sorted = sorted(gc_list_nested, key=lambda l: l[0], reverse=True)

        # creates a dataframe out of the sorted list, adds columns
        export_df = pd.DataFrame(gc_list_sorted, columns=['ItemPrice', 'ItemDescription'])
        export_df['GiftCardName'] = gc_card_name  # creates a new column with the name of the gift card used
        export_df = export_df.loc[:, ['GiftCardName', 'ItemDescription', 'ItemPrice']]  # rearranges the columns

        combined_df = pd.concat([pd.read_csv('spendingHistory.csv'), export_df])
        pd.DataFrame(combined_df).to_csv('spendingHistory.csv', index=False)

        print("Gift card expended, purchases are listed below, they are ordered from most to least expensive.\n")
        for x in range(loop_count):  # prints the list of transactions ordered highest cost to lowest :)
            print("Cost: $" + str(gc_list_sorted[x][0]) + ", item description: " + str(gc_list_sorted[x][1]))
            t.sleep(self.dt)  # exceeds requirement to print most expensive item.

        gc_num_item_purchased = len(gc_list_sorted)  # counts number of nested list items for average computation
        gc_average_cost = sum(gc_cost_lst) / gc_num_item_purchased  # average cost with sum of lst / num of purchases

        t.sleep(self.dt)
        print("\nGift card used: " + str(gc_card_name) + ", spending limit: $" + str(gc_max_spend))
        t.sleep(self.dt)
        print("The number of items purchased was: " + str(gc_num_item_purchased))
        t.sleep(self.dt)
        print("The average cost was: $" + str(round(gc_average_cost, 2)) + "\n")  # rounds avg cost -> 2 dec places
        t.sleep(self.dt)

        re_to_menu = input("Would you like to return to the menu (Yes or No): ")
        if re_to_menu.upper() == "Y" or re_to_menu.upper() == "YES":
            self.menu()  # returns to menu
        else:
            sys.exit()  # ends program

    def gc_names(self):  # 3
        print("\nList of existing gift cards: ")
        init = pd.read_csv('giftCards.csv')

        gc_names = init['GiftCardName'].copy()  # creates a series from the 'GiftCardName' column in init
        gc_names = gc_names.drop_duplicates()  # removes duplicate names from the series
        gc_names = gc_names.to_frame()  # turns the series into a dataframe
        gc_names.reset_index(inplace=True, drop=True)  # fixes the index, when duplicates are removed index breaks

        for i in range(len(gc_names.index)):  # loops for the number of gift card names in the dataframe
            print(str(gc_names.loc[i, 'GiftCardName']))  # prints each name in the dataframe

        print('')

        re_to_menu = input("Would you like to return to the menu (Yes or No): ")
        if re_to_menu.upper() == "Y" or re_to_menu.upper() == "YES":
            self.menu()  # returns to menu
        else:
            sys.exit()  # ends program

    def gc_history(self):  # 4
        print("List of gift cards: ")
        init = pd.read_csv('spendingHistory.csv')

        gc_names = init['GiftCardName'].copy()  # creates a series from the 'GiftCardName' column in init
        gc_names = gc_names.drop_duplicates()  # removes duplicate names from the series
        gc_names = gc_names.to_frame()  # turns the series into a dataframe
        gc_names.reset_index(inplace=True, drop=True)  # fixes the index, when duplicates are removed index breaks

        if len(gc_names.index) == 0:  # checks index number, if 0 then nothing has been entered, no gc data exists
            print("You haven't gone on a spending spree yet, so no gift card history has been recorded.")

            re_to_menu = input("Would you like to return to the menu (Yes or No): ")
            if re_to_menu.upper() == "Y" or re_to_menu.upper() == "YES":
                self.menu()  # returns to menu
            else:
                sys.exit()  # ends program

        for i in range(len(gc_names.index)):  # loops for the number of gift card names in the dataframe
            print(str(i + 1) + ". " + str(gc_names.loc[i, 'GiftCardName']))  # prints each name in the dataframe

        temp_choice = int(input("\nPlease enter the number of the gift card you would like to view: "))
        # takes user input as 1,2,3 etc
        print("")
        gc_indiv_ch = gc_names.loc[(temp_choice - 1), 'GiftCardName']  # gift card individual choice
        # converts 1,2,3 etc into the actual GiftCardName required for steps below

        init.set_index('GiftCardName', inplace=True)  # makes column 'GiftCardName' the index
        gc_indiv_purchases = init.loc[[gc_indiv_ch], :]  # passes rows based on index name, selected by gc_indiv_ch
        print(gc_indiv_purchases)
        gc_indiv_purchases.reset_index(inplace=True, drop=True)  # removes GiftCardName as the index

        t.sleep(self.dt)
        print(gc_indiv_purchases)
        print(len(gc_indiv_purchases))
        print(len(gc_indiv_purchases.index))
        #print(gc_indiv_purchases.loc['ItemDescription'])
        #print(str(0 + 1) + ". $" + str(gc_indiv_purchases.loc[0, 'ItemPrice']) + ", " + str(gc_indiv_purchases.loc[0, 'ItemDescription']))
        print('')
        print("Purchase History of " + gc_indiv_ch + ": ")
        print('ItemPrice' in gc_indiv_purchases.columns)
        try:
            for col in range(len(gc_indiv_purchases)):  # loops for the number of items purchases by selected gift card
                t.sleep(self.dt)
                print(str(col + 1) + ". $" + str(gc_indiv_purchases.loc[col, 'ItemPrice']) + ", " + str(
                    gc_indiv_purchases.loc[col, 'ItemDescription']))
                # prints out gift card purchase price and description
        except:
            print("1. $"+str(gc_indiv_purchases.loc[1])+", "+str(gc_indiv_purchases.loc[0]))




        print('')
        re_to_menu = input("Would you like to return to the menu (Yes or No): ")
        if re_to_menu.upper() == "Y" or re_to_menu.upper() == "YES":
            self.menu()  # returns to menu
        else:
            sys.exit()  # ends program

    def create_initial_csv(self):
        # this def will be launched on the first run of this program on a new computer.
        # it creates the two csv files needed and fills them with the data required by the program
        # creates giftCards.csv
        gift_cards = pd.DataFrame(columns=['GiftCardName', 'SpendingLimit', 'MaxItems'])
        # creates dataframe and adds specified columns
        gift_cards.loc[0, 'GiftCardName'] = 'Victory-day gift card'  # adds specified data into dataframe
        gift_cards.loc[0, 'SpendingLimit'] = 200
        gift_cards.loc[0, 'MaxItems'] = 4

        pd.DataFrame(gift_cards).to_csv('giftCards.csv', index=False)  # exports dataframe to csv

        # creates spendingHistory.csv
        spending_history = pd.DataFrame(columns=['GiftCardName', 'ItemDescription', 'ItemPrice'])
        pd.DataFrame(spending_history).to_csv('spendingHistory.csv', index=False)
        print("Initialisation complete: csv files created and setup.\n")

        with open("settings.ini", 'w') as file_edit:  # creates file that tells the program it has been run before
            file_edit.write("1")  # writes a '1' into the file
            os.system("attrib +h settings.ini")  # hides file

        self.menu()  # starts menu

    def on_launch(self):
        if os.path.exists("settings.ini"):  # checks if file exists
            os.system("attrib -h settings.ini")  # unhides file
            with open("settings.ini", 'r') as launched_before:
                if launched_before.readline() == '1':  # checks if it has a '1' in it
                    os.system("attrib +h settings.ini")  # rehides file (stops tampering)
                    self.menu()
                else:
                    self.create_initial_csv()  # runs initial startup
        else:
            self.create_initial_csv()


def input_checker(input_to_be_checked, csv, column_name):
    # This method is used to determine if the argument 'input_to_be_checked' is already a 'col_name' (column)
    # in the 'csv' file. If it is, then the user will be asked to replace the name with one not in
    # the 'csv' file.

    df = pd.read_csv(csv)  # reads the csv file from the argument csv

    in_chk = input_to_be_checked  # reduce local var names for ease of use
    col_name = column_name

    name_allowed = False
    while not name_allowed:  # will loop until name_allowed = True

        name_found = False  # assigns found to false each loop to reset it
        #  this is done incase user enters another in_chk that is also used
        for col in range(len(df)):  # loops through columns of df for the number of columns in df
            if df.loc[col, col_name] == in_chk:  # if in_chk var equals the value inside the column passed in
                # 'col_name'
                name_found = True  # if in_chk is found, set to name_found to True for the next if statement

        if name_found:  # gets user to type a new in_chk
            in_chk = input("Please enter a different gift card name: ")
        else:  # if in_chk isn't found in df column 'Name' then user is allowed to name gift card in_chk val
            name_allowed = True  # this will end while loop

    return in_chk


def check_input_type(input_var, input_type):
    # This method is used to determine if the input_var is the same type as the input_type.
    # This is needed to make sure the user is entering the right var type so that the program doesn't create an error
    in_var = input_var

    is_int = False  # loop will run until bool is True

    if input_type.__name__ == 'float':  # whole numbers can also be floats, so they won't need to be re-assigned
        try:
            in_var = float(in_var)  # if this is possible then input is a float or whole number
            # and doesn't need to be reassigned.
            # this is needed so that prices, which can be both, don't ask the user to enter a float when they input
            # a whole number
            is_int = True  # stops while loop from running
        except ValueError:
            is_int = False

    if input_type.__name__ == 'int':
        # the input is always a string initially, this checks if it can be converted to an int without issue
        # if it can, then input is an int. This stops the program asking twice for input if the input is int
        try:
            in_var = int(in_var)
            is_int = True
        except ValueError:
            is_int = False

    while not is_int:
        if not isinstance(in_var, input_type):  # checks if var isn't the var type wanted, runs if true

            if input_type.__name__ == 'int':  # point of these is to prompt the user to enter the specific type wanted
                in_var = input("This input requires an integer, enter an int: ")
            elif input_type.__name__ == 'str':
                in_var = input("This input requires a String, enter a str: ")
            elif input_type.__name__ == 'float':
                in_var = input("This input requires a float, enter a float: ")

            if input_type.__name__ == 'int':
                try:  # tests if the input is an int
                    in_var = int(in_var)  # attempts to convert the str input to an int
                except ValueError:  # if input cannot be converted, below is printed and the while loops again
                    print("That wasn't an integer.")
                if type(in_var).__name__ == 'int':  # if in_var is an int below will run
                    is_int = True  # stops while loop

            #  after creating the str checker I have realised it serves no purpose unless I want to make sure the
            #  input cannot be an int or float either. The other two functions have purpose though.
            elif input_type.__name__ == 'str':
                try:  # checks if input is an int
                    in_var = int(in_var)
                    print("That wasn't a String.")
                except ValueError:
                    try:  # checks if input is a float
                        in_var = float(in_var)
                        print("That wasn't a String.")
                    except ValueError:  # if input isn't an int or float then below stops loop
                        if type(in_var).__name__ == 'str':
                            is_int = True

            elif input_type.__name__ == 'float':
                try:
                    in_var = float(in_var)
                except ValueError:
                    print("That wasn't a float.")
                if type(in_var).__name__ == 'float':
                    is_int = True

        else:
            is_int = True  # if isinstance is true then loop isn't needed

    return in_var


MainMenu_ob = MainMenu()  # instantiates a new object of the MainMenu Class
MainMenu_ob.on_launch()
# check_input_type(8.9, str)
#drugs = check_input_type(45454545, str)
#print(drugs)
