'''
This is the main file for this project.
There are two parts of this project.

1.  To print number 1-100. If the number is multiples of three print “Three” instead of the number
    and for the multiples of five print “Five”.
    For numbers which are multiples of both three and five print “ThreeFive”

2.  Validating and Formatting post codes for UK.

User can enter 1 or 2 to run the above mentioned programs.
User can also select 3 to terminate the program.
'''

import print_numbers as pn
from uk_postcodes import *


def display_message(message_type):
    message = ""
    if message_type == 'normal':
        message = "This coding challenge has 2 tasks\n" \
                   "1. Print number 1 to 100\n" \
                   "2. Validating and formatting UK post codes\n" \
                   "3. To Exit\n\n" \
                   "Please enter 1, 2 or 3 to proceed : "
    elif message_type == 'error':
        message = "\nPlease select correct option"
    return message


def display_message_postcode(message_type):
    message = ""
    if message_type == "normal":
        message = "Please enter Postcode to validate or enter 'exit' to exit from this loop: "
    elif message_type == "error":
        message = "Please check your response!"
    return message

def infoMessage():
    while True:
        try:
            user_selection = int(input(display_message('normal')))

        except ValueError:
            print(display_message('error'))
            continue

        else:
            valid_user_selection = [1, 2, 3]
            if user_selection not in valid_user_selection:
                print("Please select correct option")
                continue
            if user_selection == 3:
                print("Thank you!")
                break

            if user_selection == 1:
                for i in pn.print_numbers(100):
                    print(i)
            else:
                while True:
                    user_entered_postcode = input(display_message_postcode("normal"))

                    if user_entered_postcode.strip().lower() == 'exit':
                        break

                    try:
                        pc = ValidatePostcode(user_entered_postcode.strip())
                        pc.func_validate_postcode()
                    except ValueError:
                        print("Please enter correct Postcode !")
                    except InvalidInward:
                        print("There might be an issue with Inward part of the post code!")
                    except InvalidOutward:
                        print("There might be an issue with Outward part of the post code!")
                    except InvalidPostcode:
                        # print("Invalid Postcode!")
                        pass
                    else:
                        print(f"Entered Postcode '{Postcode.formatted_postcode}' is/can be a valid one!")


if __name__ == '__main__':
    infoMessage()
