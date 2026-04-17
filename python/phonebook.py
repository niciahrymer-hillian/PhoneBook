from ast import literal_eval
from pathlib import Path
from typing import Dict, List, Optional


CONTACT_LIST_FILE = Path(__file__).resolve().parent.parent / "contactlist.py"


class PhoneBook:
    def __init__(
        self,
        phonebook_dict: Optional[Dict[str, List[str]]] = None,
        persist_to_file: bool = False,
    ):
        self.persist_to_file = persist_to_file
        self.phonebook = (
            phonebook_dict
            if phonebook_dict is not None
            else self._load_contacts_from_file() if persist_to_file else {}
        )

    def _load_contacts_from_file(self) -> Dict[str, List[str]]:
        if not CONTACT_LIST_FILE.exists():
            return {}

        text = CONTACT_LIST_FILE.read_text(encoding="utf-8").strip()
        if not text or "=" not in text:
            return {}

        try:
            raw_contacts = literal_eval(text.split("=", 1)[1].strip())
        except (SyntaxError, ValueError):
            return {}

        phonebook: Dict[str, List[str]] = {}
        for entry in raw_contacts:
            if isinstance(entry, str) and " " in entry:
                name, phone_number = entry.rsplit(" ", 1)
                phonebook.setdefault(name, []).append(phone_number)
        return phonebook

    def _save_contacts_to_file(self) -> None:
        if not self.persist_to_file:
            return

        contacts = [
            f'    "{name} {number}",'
            for name in sorted(self.phonebook)
            for number in self.phonebook[name]
        ]
        content = "CONTACTS = [\n" + "\n".join(contacts) + "\n]\n"
        CONTACT_LIST_FILE.write_text(content, encoding="utf-8")

    def _refresh_from_file(self) -> None:
        if self.persist_to_file:
            self.phonebook = self._load_contacts_from_file()

    def _add_numbers(self, name: str, phone_numbers: List[str]) -> None:
        self._refresh_from_file()
        numbers = self.phonebook.setdefault(name, [])
        for phone_number in phone_numbers:
            phone_number = phone_number.strip()
            if phone_number and phone_number not in numbers:
                numbers.append(phone_number)
        self._save_contacts_to_file()

    def add(self, name: str, phone_number: str) -> None:
        self._add_numbers(name, [phone_number])

    def add_all(self, name: str, *phone_numbers: str) -> None:
        self._add_numbers(name, list(phone_numbers))

    def remove(self, name: str) -> None:
        self._refresh_from_file()
        self.phonebook.pop(name, None)
        self._save_contacts_to_file()

    def has_entry(self, name: str, phone_number: str = None) -> bool:
        self._refresh_from_file()
        if not phone_number:
            return name in self.phonebook
        return phone_number in self.phonebook.get(name, [])

    def lookup(self, name: str) -> List[str]:
        self._refresh_from_file()
        return self.phonebook.get(name, [])

    def reverse_lookup(self, phone_number: str) -> Optional[str]:
        self._refresh_from_file()
        for name, numbers in self.phonebook.items():
            if phone_number in numbers:
                return name
        return None

    def get_all_contact_names(self) -> List[str]:
        self._refresh_from_file()
        return list(self.phonebook.keys())

    def get_map(self) -> Dict[str, List[str]]:
        self._refresh_from_file()
        return self.phonebook

    def run_menu(self):
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
                name = input("Enter first and last name: ")
                phone_number = input("Enter phone number: ")
                self.add(name, phone_number)
                print(f"Added {name} with number {phone_number} and saved it to the shared contact list.")
            elif choice == '2':
                name = input("Enter first and last name: ")
                phone_numbers = input("Enter phone numbers (comma separated): ").split(',')
                cleaned_numbers = [num.strip() for num in phone_numbers if num.strip()]
                self.add_all(name, *cleaned_numbers)
                print(f"Added {name} with numbers {', '.join(cleaned_numbers)} and saved them to the shared contact list.")
            elif choice == '3':
                name = input("Enter contact name to remove: ")
                self.remove(name)
                print(f"Removed contact {name} from the phone book and shared contact list.")
            elif choice == '4':
                name = input("Enter contact name to check: ")
                phone_number = input("Enter phone number to check (optional): ")
                if self.has_entry(name, phone_number):
                    print(f"{name} was found in the shared contact list.")
                else:
                    print(f"{name} was not found.")
            elif choice == '5':
                name = input("Enter contact name to look up: ")
                numbers = self.lookup(name)
                if numbers:
                    print(f"Found in the shared contact list: {name} -> {', '.join(numbers)}.")
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
    PhoneBook(persist_to_file=True).run_menu()
