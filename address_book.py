"""
@Author: Naveen Madev Naik
@Date: 2024-09-08
@Last Modified by: Naveen Madev Naik
@Last Modified time: 2024-09-08
@Title: Ability to add new Contacts in Address Book using OOP with first and last names, address, city, state, zip, phone number, and email
"""

import re
import mylogging

logger = mylogging.logger_init("address_book.py")


class Contact:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone_number, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.email = email

    def display(self):

        """
        Description:
            Displays the contact details.

        Parmater:
            self:intance of the class

        Return:
            None
        """

        logger.info(f"Name: {self.first_name} {self.last_name}\n"
                    f"Address: {self.address}\n"
                    f"City: {self.city}\n"
                    f"State: {self.state}\n"
                    f"Zip Code: {self.zip_code}\n"
                    f"Phone Number: {self.phone_number}\n"
                    f"Email: {self.email}\n")


class AddressBook:

    @staticmethod
    def get_valid_input(prompt, regex_pattern=None, error_message="Invalid input. Please try again."):

        """
        Description:
            Prompts the user for input and validates it against a regex pattern if provided.

        Parameters:
            prompt (str): The prompt message to display.
            regex_pattern (str): The regular expression pattern to validate the input (optional).
            error_message (str): Error message if the input is invalid.

        Return:
            (str): The valid input from the user.
        """

        while True:
            value = input(prompt)
            if regex_pattern:
                if re.match(regex_pattern, value):
                    return value
                else:
                    logger.info(error_message)
            else:
                if value.strip():
                    return value
                else:
                    logger.info("Input cannot be empty. Please try again.")


    def add_contact(self):

        """
        Description:
            Adds a new contact to the address book by taking input and validating it.

        Parameter:
            self:Instance of the class

        Return:
            contact (Contact): A contact object containing the user's information.
        """

        first_name = self.get_valid_input("First Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")
        last_name = self.get_valid_input("Last Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")
        address = self.get_valid_input("Address: ")
        city = self.get_valid_input("City: ")
        state = self.get_valid_input("State: ")
        zip_code = self.get_valid_input("ZIP Code: ", r'^\d{6}$', "Invalid ZIP Code. Please enter a 6-digit number.")
        phone_number = self.get_valid_input("Phone Number: ", r'^\d{10}$', "Invalid Phone Number. Please enter a 10-digit number.")
        email = self.get_valid_input("Email: ", r'^\w+@\w+\.\w+$', "Invalid Email. Please enter a valid email address.")

        return Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)


def main():
    try:
        address_book = AddressBook()
        contact = address_book.add_contact()

        print("\n--------------Contact Details:---------------")
        contact.display()

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
