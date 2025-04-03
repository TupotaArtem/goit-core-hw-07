from collections import UserDict
from datetime import datetime, timedelta, date

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {e}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, number):
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(number)

class Birthday(Field):
    def __init__(self, value):
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
            if date_obj > date.today():
                raise ValueError("Birthday cannot be in the future")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)
    
    def __str__(self):
        return self.value

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
            raise ValueError(f"Phone number {number} not found")

    def edit_phone(self, old_number, new_number):
       
        phone = self.find_phone(old_number) 
            
        if phone:  
            self.add_phone(new_number)  
            self.remove_phone(old_number) 
            return "phone changed"
        else:
            raise ValueError(f"Phone number {old_number} not found")             
            
    def find_phone (self,number:str): 
        for phone in self.phones:
           if phone.value == number:  
               return phone
        return None

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "No birthday set"

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones) if self.phones else "No phones"
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")

    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

                birthday_this_year = birthday_date.replace(year=today.year)
                
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                if 0 <= (birthday_this_year - today).days <= days:
                    congratulation_date = self.adjust_for_weekend(birthday_this_year)
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays
               
    @staticmethod
    def adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return birthday + timedelta(days=(7 - birthday.weekday()))
        return birthday

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return "Contact added or updated."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        return record.edit_phone(old_phone, new_phone)
    
    return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return '; '.join(p.value for p in record.phones) if record else "Contact not found."

@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.data.values()) if book.data else "No contacts found."

@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added successfully."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return record.show_birthday() if record else "Contact not found."

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()

def parse_input(user_input):
    parts = user_input.split()
    if not parts: 
        return "", [] 
    return parts[0].strip().lower(), parts[1:]


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        if not command:continue

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
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
