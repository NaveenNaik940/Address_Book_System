"""

@Author: Naveen Madev Naik
@Date: 2024-09-08
@Last Modified by: Naveen Madev Naik
@Last Modified time: 2024-09-09
@Title: Ability to add, display, edit and delete contacts in an Address Book using OOP

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

        Parameter:
            self:Instance of the class

        Return:
            None
        """

        print("----------------------------------------------------")
        logger.info(f"Name: {self.first_name} {self.last_name}\n"
                    f"Address: {self.address}\n"
                    f"City: {self.city}\n"
                    f"State: {self.state}\n"
                    f"Zip Code: {self.zip_code}\n"
                    f"Phone Number: {self.phone_number}\n"
                    f"Email: {self.email}\n")

    def update_contact(self, **kwargs):

        """
        Description:
            Updates contact details with the provided values.

        Parameter:
            self:Instance of the class
        
        Return:
            None
        """

        for key, value in kwargs.items():
            setattr(self, key, value)
        logger.info(f"Contact {self.first_name} {self.last_name} updated successfully.")


class AddressBook:

    def __init__(self):
        self.contacts = []

    @staticmethod
    def get_valid_input(prompt, regex_pattern=None, error_message="Invalid input. Please try again."):

        """
        Description:
            Prompts the user for input and validates it against a regex pattern if provided.

        Parameter:
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
            Adds a new contact to the address book.

        Parameter:
            self:Instance of the class

        Return:
            None
        """

        first_name = self.get_valid_input("First Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")
        last_name = self.get_valid_input("Last Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")
        address = self.get_valid_input("Address: ")
        city = self.get_valid_input("City: ")
        state = self.get_valid_input("State: ")
        zip_code = self.get_valid_input("ZIP Code: ", r'^\d{6}$', "Invalid ZIP Code. Please enter a 6-digit number.")
        phone_number = self.get_valid_input("Phone Number: ", r'^\d{10}$', "Invalid Phone Number. Please enter a 10-digit number.")
        email = self.get_valid_input("Email: ", r'^\w+@\w+\.\w+$', "Invalid Email. Please enter a valid email address.")

        contact = Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
        self.contacts.append(contact)
        logger.info(f"Contact {first_name} {last_name} added successfully.")
        return contact


    def find_contact(self, first_name, last_name):

        """
        Description:
            Finds a contact by first and last name.

        Parameter:
            self:Instance of the class
            first_name(str): first name to check in contact 
            last_name(str): last name to check in contact

        Return:
            None                
        """

        for contact in self.contacts:
            if contact.first_name.lower() == first_name.lower() and contact.last_name.lower() == last_name.lower():
                return contact
        logger.info(f"Contact {first_name} {last_name} not found.")
        return None


    def delete_contact(self, first_name, last_name):

        """
        Description:
            Deletes a contact by first and last name.

        Parameter:
            first_name (str): The first name of the contact.
            last_name (str): The last name of the contact.

        Return:
            None
        """
        contact = self.find_contact(first_name, last_name)
        if contact:
            self.contacts.remove(contact)
            logger.info(f"Contact {first_name} {last_name} deleted successfully.")
        else:
            logger.info(f"Contact {first_name} {last_name} not found.")    


    def edit_contact(self, first_name, last_name):

        """
        Description:
            Edits an existing contact by searching with the name.

        Parameter:
            first_name:based on first name will edit contact 
            last_name:based on last name will edit contact  

        Return:
            None          
        """
        
        contact = self.find_contact(first_name, last_name)
        if contact:
            print("Editing contact details. Leave blank to keep current value.")
            new_first_name = self.get_valid_input(f"First Name ({contact.first_name}): ") or contact.first_name
            new_last_name = self.get_valid_input(f"Last Name ({contact.last_name}): ") or contact.last_name
            new_address = self.get_valid_input(f"Address ({contact.address}): ") or contact.address
            new_city = self.get_valid_input(f"City ({contact.city}): ") or contact.city
            new_state = self.get_valid_input(f"State ({contact.state}): ") or contact.state
            new_zip_code = self.get_valid_input(f"ZIP Code ({contact.zip_code}): ", r'^\d{6}$', "Invalid ZIP Code.") or contact.zip_code
            new_phone_number = self.get_valid_input(f"Phone Number ({contact.phone_number}): ", r'^\d{10}$', "Invalid Phone Number.") or contact.phone_number
            new_email = self.get_valid_input(f"Email ({contact.email}): ", r'^\w+@\w+\.\w+$', "Invalid Email.") or contact.email

            contact.update_contact(
                first_name=new_first_name,
                last_name=new_last_name,
                address=new_address,
                city=new_city,
                state=new_state,
                zip_code=new_zip_code,
                phone_number=new_phone_number,
                email=new_email
            )
        else:
            logger.info(f"Contact {first_name} {last_name} does not exist.")


def main():
    try:
        address_book = AddressBook()
        while True:
            print("\n1. Add Contact\n2. Edit Contact\n3. Delete Contact\n4. Display Contacts\n5. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                address_book.add_contact()
            elif choice == '2':
                first_name = input("Enter the first name of the contact to edit: ")
                last_name = input("Enter the last name of the contact to edit: ")
                address_book.edit_contact(first_name, last_name)
            elif choice == '3':
                first_name = input("Enter the first name of the contact to delete: ")
                last_name = input("Enter the last name of the contact to delete: ")
                address_book.delete_contact(first_name, last_name)
            elif choice == '4':
                for contact in address_book.contacts:
                    contact.display()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
