from collections import UserDict
from typing import List, Optional


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    '''
    Обов'язкове поле
    '''
    pass


class Phone(Field):
    def __init__(self, value: str) -> None:
        '''
        Валідація номера телефону (10 цифр)
        '''
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_number: str, new_number: str) -> None:
        phone_obj = self.find_phone(old_number)
        if not phone_obj:
            raise ValueError(f"Phone number {old_number} not found.")
        new_phone = Phone(new_number)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":

    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print("--- All records ---")
    for name, record in book.data.items():
        print(record)

    print("\n--- Editing John's Phone ---")
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
        print(john)

    found_phone = john.find_phone("5555555555")
    print(f"\nFound phone in {john.name}: {found_phone}")

    print("\n--- Validation Error Check ---")
    try:
        john.add_phone("12345") 
    except ValueError as e:
        print(f"Expected error: {e}")
    book.delete("Jane")
    print(f"\nBook after deleting Jane: {len(book.data)} record(s).")