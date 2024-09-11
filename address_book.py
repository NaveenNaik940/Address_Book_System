"""

Naveen Madev Naik
@Date: 2024-09-10
@Last Modified by: Naveen Madev Naik
@Last Modified time: 2024-09-10
@Title: Ability to create contacts in address book and multiple address book with no duplicate contacts and sort the conctact by name or city and finally stores address book in file(txt,csv,json)

"""

import re
import os
import csv
import json
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
            **kwargs:keyword arguments to take multiple values

        Return:
            None
        """

        for key, value in kwargs.items():
            setattr(self, key, value)
        logger.info(f"Contact {self.first_name} {self.last_name} updated successfully.")


class AddressBook:


    def __init__(self, name):
        self.name = name
        self.contacts = []
        self.load_from_file()

    def save_to_file(self, file_type="txt"):
        
        """
        Description:
            Saves the current address book contacts to either a text file or a CSV file or json file
            depending on the user's choice.

        Parameters:
            file_type (str): Type of file to save ('txt' for text, 'csv' for CSV, 'json' for json)

        Return:
            None
        """

        if file_type == "csv":
            filename = f"{self.name}.csv"
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['First Name', 'Last Name', 'Address', 'City', 'State', 'Zip Code', 'Phone Number', 'Email'])
                for contact in self.contacts:
                    writer.writerow([contact.first_name, contact.last_name, contact.address, contact.city,
                                    contact.state, contact.zip_code, contact.phone_number, contact.email])
            logger.info(f"Address book {self.name} saved to {filename}.")
            print(f"Address book saved to {filename}.")

        elif file_type == 'txt':
            filename = f"{self.name}.txt"
            with open(filename, 'w') as f:
                for contact in self.contacts:
                    contact_info = f"{contact.first_name},{contact.last_name},{contact.address},{contact.city},{contact.state},{contact.zip_code},{contact.phone_number},{contact.email}\n"
                    f.write(contact_info)
            logger.info(f"Address book {self.name} saved to {filename}.")
        
        elif file_type == 'json':
            filename = f"{self.name}.json"
            with open(filename, 'w') as f:
                contacts_data = [contact.__dict__ for contact in self.contacts]
                json.dump(contacts_data, f, indent=4)
            logger.info(f"Address book {self.name} saved to {filename}.")

    


    def load_from_file(self,file_type='txt'):

        """
        Description:
            Loads contacts from a text file if it exists.

        Parmater:
            self:Instance of the class
            file_type (str): Type of file to load ('txt' for text, 'csv' for CSV)

        Return:
            None
        
        """
        
        if file_type == 'csv':
            filename = f"{self.name}.csv"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    for row in reader:
                        if len(row) == 7:
                            contact = Contact(first_name=row[0], last_name=row[1], address=row[2], 
                                            city=row[3], state=row[4], zip_code=row[5], 
                                            phone_number=row[6], email=row[7])
                            self.contacts.append(contact)
                logger.info(f"Address book {self.name} loaded from {filename}.")
                print(f"Address book loaded from {filename}.")

        elif file_type == 'txt':
            filename = f"{self.name}.txt"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    for line in f:
                        # Each line in the file is in the format:
                        # "first_name,last_name,address,city,state,zip_code,phone_number,email"
                        contact_data = line.strip().split(',')
                        if len(contact_data) == 8:  
                            first_name, last_name, address, city, state, zip_code, phone_number, email = contact_data
                            contact = Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
                            self.contacts.append(contact)
                logger.info(f"Address book {self.name} loaded from {filename}.")

        elif file_type == 'json':
            filename = f"{self.name}.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    contacts_data = json.load(f)
                    for contact_data in contacts_data:
                        contact = Contact(**contact_data)
                        self.contacts.append(contact)
                logger.info(f"Address book {self.name} loaded from {filename}.")        


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


    def add_contact(self, multiple=False):

        """
        Description:
            Adds one or more contacts to the address book. Ensures no duplicate entry of the same person.

        Parameter:
            self: Instance of the class
            multiple (bool): If True, the method will allow adding multiple contacts.

        Return:
            None
        """

        while True:
            first_name = self.get_valid_input("First Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")
            last_name = self.get_valid_input("Last Name: ", r'[A-Za-z]{3,}$', "Invalid Name. Enter at least a 3-letter name")

            # Check for duplicate contact
            if self.find_contact(first_name, last_name):
                logger.info(f"Contact {first_name} {last_name} already exists. Please enter a different contact.")
                print(f"Contact {first_name} {last_name} already exists.")
                if not multiple:
                    return  # Exit if adding a single contact
                continue  # Ask for a different contact if adding multiple

            address = self.get_valid_input("Address: ")
            city = self.get_valid_input("City: ")
            state = self.get_valid_input("State: ")
            zip_code = self.get_valid_input("ZIP Code: ", r'^\d{6}$', "Invalid ZIP Code. Please enter a 6-digit number.")
            phone_number = self.get_valid_input("Phone Number: ", r'^\d{10}$', "Invalid Phone Number. Please enter a 10-digit number.")
            email = self.get_valid_input("Email: ", r'^\w+@\w+\.\w+$', "Invalid Email. Please enter a valid email address.")

            contact = Contact(first_name, last_name, address, city, state, zip_code, phone_number, email)
            self.contacts.append(contact)
            logger.info(f"Contact {first_name} {last_name} added successfully.")
            print(f"Contact {first_name} {last_name} added successfully.")

            if not multiple:
                break
            more = input("Do you want to add another contact? (yes/no): ").strip().lower()
            if more != 'yes':
                break


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
            logger.info(f"Contact {first_name} {last_name} not exist.")


    def display_contacts(self,option=None):

        """
        Description:
            Displays all the contacts in the address book, sorted by first name and last name or city

        Parameter:
            self: Instance of the class.
            option(str):sorting the contacts based on the option

        Return:
            None                
        """

        if not self.contacts:
            print(f"No contacts found in {self.name} Address Book.")
            return
        
        # Sort contacts by first and last name
        if option=='name':
            sorted_contacts = sorted(self.contacts, key=lambda contact: (contact.first_name.lower(), contact.last_name.lower()))

        # Display sorted contacts
            for contact in sorted_contacts:
                contact.display()

        elif option == 'city':
            sorted_contacts = sorted(self.contacts, key=lambda contact: (contact.city.lower()))
            for contact in sorted_contacts:
                contact.display()        
        else:
            for contact in self.contacts:
                contact.display()        


    def search_by_city_or_state(self, location):

        """
        Description:
            Searches contacts by city or state in the address book.

        Parameter:
            location (str): The city or state to search by.

        Return:
            None
        """

        found_contacts = [contact for contact in self.contacts if contact.city.lower() == location.lower() or contact.state.lower() == location.lower()]
        if found_contacts:
            for contact in found_contacts:
                contact.display()
        else:
            print(f"No contacts found in {self.name} for the location {location}.")


class AddressBookSystem:

    def __init__(self):
        self.address_books = {}

    def create_address_book(self, name):

        """
        Description:
            Creates a new address book with a unique name.

        Parameter:
            self:Instance of the class
            name:name of the address book needs to be created

        Return:
            None              
        """

        if name in self.address_books:
            logger.info(f"Address book with name {name} already exists.")
            print(f"Address book with name {name} already exists.")
        else:
            self.address_books[name] = AddressBook(name)
            logger.info(f"Address book {name} created successfully.")
            print(f"Address book {name} created successfully.")

    def select_address_book(self):

        """
        Description:
            Selects an existing address book by name.

        Parameter:
            self:Instance of the class

        Return:
            None               
        """

        if not self.address_books:
            print("No address books available.")
            return None

        print("\nAvailable Address Books:")
        for name in self.address_books:
            print(f"- {name}")
        
        name = input("Enter the name of the address book to select: ").strip()
        return self.address_books.get(name)

    def search_across_books(self, location):

        """
        Description:
            Searches across all address books for contacts by city or state.

        Parameter:
            location (str): The city or state to search by.

        Return:
            None
        """

        for name, address_book in self.address_books.items():
            print(f"Searching in {name} Address Book:")
            address_book.search_by_city_or_state(location)


    def get_contact_count_by_city_or_state(self, location):

        """
        Description:
            Counts the number of contacts by city or state across all address books.

        Parameter:
            location (str): The city or state to search for.

        Return:
            (int): The count of contacts found for the given city or state.
        """

        count = 0
        for name, address_book in self.address_books.items():
            found_contacts = [contact for contact in address_book.contacts if contact.city.lower() == location.lower() or contact.state.lower() == location.lower()]
            count += len(found_contacts)
        return count


def main():
    try:
        system = AddressBookSystem()

        while True:
            print("\n===== Address Book Menu =====")
            print("1. Create Address Book")
            print("2. Select Address Book")
            print("3. Search and Count Contacts by City/State")
            print("4. Save as File and Exit")
            print("5. Exit")

            choice = input("Choose an option: ").strip()

            if choice == '1':
                name = input("Enter a unique name for the new Address Book: ").strip()
                system.create_address_book(name)

            elif choice == '2':
                selected_book = system.select_address_book()
                
                if selected_book:
                    while True:
                        print(f"\n===== {selected_book.name} Menu =====")
                        print("1. Add Single Contact")
                        print("2. Add Multiple Contacts")
                        print("3. Edit Contact")
                        print("4. Delete Contact")
                        print("5. Display Contacts")
                        print("6. Search Contact by City/State")
                        print("7. Go Back")

                        book_choice = input("Choose an option: ").strip()

                        if book_choice == '1':
                            selected_book.add_contact()
                        elif book_choice == '2':
                            selected_book.add_contact(multiple=True)
                        elif book_choice == '3':
                            first_name = input("Enter the first name of the contact to edit: ").strip()
                            last_name = input("Enter the last name of the contact to edit: ").strip()
                            selected_book.edit_contact(first_name, last_name)
                        elif book_choice == '4':
                            first_name = input("Enter the first name of the contact to delete: ").strip()
                            last_name = input("Enter the last name of the contact to delete: ").strip()
                            selected_book.delete_contact(first_name, last_name)
                        elif book_choice == '5':
                            print("Sort Contacts By\n")
                            print("1.Sort By Name\n2.sort by City\n3.No sorting")
                            option=input("Enter Your Option: ")
                            if option == '1':
                                selected_book.display_contacts('name')
                            elif option == '2': 
                                selected_book.display_contacts('city') 
                            else:
                                selected_book.display_contacts()    
                        elif book_choice == '6':
                            location = input("Enter the city or state to search: ").strip()
                            system.search_across_books(location)
                        elif book_choice == '7':
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("No address book selected or available.")

            elif choice == '3':
                location = input("Enter the city or state to search for contact count: ").strip()
                count = system.get_contact_count_by_city_or_state(location)
                print(f"Total number of contacts in {location}: {count}")

            elif choice == '4':
                file_type = input("Enter file type to save (txt or csv or json): ").strip().lower()
                if file_type not in ['txt', 'csv','json']:
                    print("Invalid file type. Please enter 'txt' or 'csv' or 'json'.")
                else:
                    for book in system.address_books.values():
                        book.save_to_file(file_type)
                    print("All address books saved. Exiting.")
                break               

            elif choice == '5':
                print("Exiting the Address Book system.")
                break

            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
