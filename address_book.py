"""

@Author: Naveen Madev Naik
@Date: 2024-09-08
@Last Modified by: Naveen Madev Naik
@Last Modified time: 2024-09-08
@Title: Ability to create a Contacts in Address Book with first and last names, address, city, state, zip, phone number and email

"""

import re
import mylogging

logger=mylogging.logger_init("address_book.py")


def get_valid_input(prompt, regex_pattern=None, error_message="Invalid input. Please try again."):

    """
    Description:
        Prompts the user for input and validates it against a regex pattern if provided.

    Parameters: 
        prompt (str) - The prompt message to display.
        regex_pattern (str) - The regular expression pattern to validate the input (optional).
        error_message (str) - Error message if the input is invalid.

    Return: 
        (str) - The valid input from the user.
    """

    while True:
        value = input(prompt)
        if regex_pattern:
            if re.match(regex_pattern, value):
                return value
            else:
                logger.info(error_message)
        else:
            if value.strip():  # Ensure input is not empty
                return value
            else:
                logger.info("Input cannot be empty. Please try again.")


def display_contact(contact):

    """
    Description:
        Display the contact details stored in the dictionary.

    Parameters: 
        contact (dict) - Dictionary containing the contact's details.

    Return: 
        None
    """
    
    logger.info(f"Name: {contact['first_name']} {contact['last_name']}\n"
          f"Address: {contact['address']}\n"
          f"City: {contact['city']}\n"
          f"State: {contact['state']}\n"
          f"Zip Code: {contact['zip_code']}\n"
          f"Phone Number: {contact['phone_number']}\n"
          f"Email: {contact['email']}\n")


def main():
    try:
        first_name = get_valid_input("First Name: ",r'[A-Za-z]{3,}$',"Invalid Name. Enter atleast letter name")
        last_name = get_valid_input("Last Name: ",r'[A-Za-z]{3,}$',"Invalid Name. Enter atleast letter name")
        address = get_valid_input("Address: ")
        city = get_valid_input("City: ")
        state = get_valid_input("State: ")
        zip_code = get_valid_input("ZIP Code: ", r'^\d{6}$', "Invalid ZIP Code. Please enter a 6-digit number.")
        phone_number = get_valid_input("Phone Number: ", r'^\d{10}$', "Invalid Phone Number. Please enter a 10-digit number.")
        email = get_valid_input("Email: ", r'^\w+@\w+\.\w+$', "Invalid Email. Please enter a valid email address.")

        contact = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "phone_number": phone_number,
            "email": email
        }

        print("\n--------------Contact Details:---------------")
        display_contact(contact)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
