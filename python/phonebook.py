from typing import Dict, List, Optional


class PhoneBook:
    """
    Created by leon on 1/23/18.
    Made WAY better by kristofer 6/16/24
    Python version for beginner coders

    """
    def __init__(self, phonebook_dict: Optional[Dict[str, List[str]]] = None):
        """
        Constructor for PhoneBook
        :param phonebook_dict: Optional dictionary to initialize the phonebook with
        """
        self.phonebook = phonebook_dict if phonebook_dict is not None else {}

    def add(self, name: str, phone_number: str) -> None:
        """
        Add a phone number for a contact
        :param name: Contact name
        :param phone_number: Phone number to add
        """
        if self.phonebook is None:
            self.phonebook = {}
        if name not in self.phonebook:
            self.phonebook[name] = []
        self.phonebook[name].append(phone_number)

    def add_all(self, name: str, *phone_numbers: str) -> None:
        """
        Add multiple phone numbers for a contact
        :param name: Contact name
        :param phone_numbers: Variable number of phone numbers to add
        """
        if self.phonebook is None:
            self.phonebook = {}
        if name not in self.phonebook:
            self.phonebook[name] = []
        self.phonebook[name].extend(phone_numbers)

    def remove(self, name: str) -> None:
        """
        Remove a contact from the phonebook
        :param name: Contact name to remove
        """
        if self.phonebook is not None and name in self.phonebook:
            del self.phonebook[name]

    def has_entry(self, name: str, phone_number: str = None) -> bool:
        """
        Check if a contact exists, optionally with a specific phone number
        :param name: Contact name to check
        :param phone_number: Optional phone number to check
        :return: True if contact exists (with phone number if specified), False otherwise
        """
        if self.phonebook is None:
            return False
        if phone_number is None:
            return name in self.phonebook
        return name in self.phonebook and phone_number in self.phonebook[name]

    def lookup(self, name: str) -> List[str]:
        """
        Look up all phone numbers for a contact
        :param name: Contact name to look up
        :return: List of phone numbers for the contact
        """
        if self.phonebook is None or name not in self.phonebook:
            return []
        return self.phonebook[name]

    def reverse_lookup(self, phone_number: str) -> str:
        """
        Find the contact name for a given phone number
        :param phone_number: Phone number to look up
        :return: Contact name associated with the phone number
        """
        if self.phonebook is None:
            return None
        for name, numbers in self.phonebook.items():
            if phone_number in numbers:
                return name
        

    def get_all_contact_names(self) -> List[str]:
        """
        Get all contact names in the phonebook
        :return: List of all contact names
        """
        if self.phonebook is None:
            return []
        return list(self.phonebook.keys())

    def get_map(self) -> Dict[str, List[str]]:
        """
        Get the underlying dictionary representation of the phonebook
        :return: Dictionary mapping names to lists of phone numbers
        """
        if self.phonebook is None:
            return {}
        return self.phonebook
    
    def run_menu(self):
        """
        Run a simple menue to interact with the phonebook
        """
        while True:
            print("\nPhone Book Menu:")
            print("1. Add Contact")
            print("2. Add Multiple Numbers")
            print("3. Remove Contact")
            print("4. Check Entry")
            print("5. Lookup Contact")
            print("6. Reverse Lookup")
            print("7. Get All Contact Names")
            print("8. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter contact name: ")
                phone_number = input("Enter phone number: ")
                self.add(name, phone_number)
                print(f"Added {name} with number {phone_number}.")
            elif choice == '2':
                name = input("Enter contact name: ")
                phone_numbers = input("Enter phone numbers (comma separated): ").split(',')
                self.add_all(name, *[num.strip() for num in phone_numbers])
                print(f"Added {name} with numbers {', '.join(phone_numbers)}.")
            elif choice == '3':
                name = input("Enter contact name to remove: ")
                self.remove(name)
                print(f"Removed contact {name}.")
            elif choice == '4':
                name = input("Enter contact name to check: ")
                phone_number = input("Enter phone number to check (optional): ")
                if self.has_entry(name, phone_number):
                    print(f"{name} has the entry {phone_number}.")
                else:
                    print(f"{name} does not have the entry {phone_number}.")
            elif choice == '5':
                name = input("Enter contact name to look up: ")
                numbers = self.lookup(name)
                if numbers:
                    print(f"{name}'s numbers: {', '.join(numbers)}.")
                else:
                    print(f"No entries found for {name}.")
            elif choice == '6':
                phone_number = input("Enter phone number to reverse look up: ")
                name = self.reverse_lookup(phone_number)
                if name:
                    print(f"The number {phone_number} belongs to {name}.")
                else:
                    print(f"No contact found for number {phone_number}.")
            elif choice == '7':
                names = self.get_all_contact_names()
                if names:
                    print(f"All contacts: {', '.join(names)}.")
                else:
                    print("No contacts found.")
            elif choice == '8':
                print("Exiting phone book. Goodbye!")
                break


if __name__ == '__main__':
    phonebook = PhoneBook()
    phonebook.run_menu()
