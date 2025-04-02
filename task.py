from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, number):
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(number)

class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        phone = self.find_phone(number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone number {number} not found")

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone:
            self.remove_phone(old_number)
            self.add_phone(new_number)
        else:
            raise ValueError(f"Phone number {old_number} not found")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()
        
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                
                if birthday_this_year < today:
                    birthday_this_year = record.birthday.value.replace(year=today.year + 1)
                
                if 0 <= (birthday_this_year - today).days <= 7:
                    if birthday_this_year.weekday() >= 5:
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))
                    upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})
        
        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), args

def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added."

def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    return "Contact not found."

def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return str(record) if record else "Contact not found."

def show_all(book):
    return "\n".join(str(record) for record in book.data.values()) if book.data else "No contacts found."

def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    return "Contact not found."

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}" if record and record.birthday else "Birthday not found."

def birthdays(book):
    return book.get_upcoming_birthdays()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
