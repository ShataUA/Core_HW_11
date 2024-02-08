from collections import UserDict
from datetime import datetime


class Field:
    """Field class"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Name class"""
    def __init__(self, value):
        if not value:
            raise ValueError("Give me a name")
        super().__init__(value)


class Phone(Field):
    """Phone class"""
    @property
    def value(self):
        """Return the value"""
        return self.__value

    @value.setter
    def value(self, value):
        if value and not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        self.__value = value


class Birthday(Field):
    """Birthday class"""

    @property
    def value(self):
        """Return the value"""
        return self.__value

    @value.setter
    def value(self, value):
        try:
            if isinstance(value, str):
                self.__value = datetime.strptime(value, '%d-%m-%Y')
            else:
                self.__value = value
        except ValueError:
            raise ValueError('Invalid birthday format. Try "dd-mm-yyyy"')



class Record:
    """Record class"""
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        """Days to birthday"""
        if self.birthday is None:
            return None
        today = datetime.now()
        birthday_this_year = self.birthday.value.replace(today.year)
        if today < birthday_this_year:
            return (birthday_this_year - today).days
        return (birthday_this_year.replace(today.year + 1) - today).days

    def add_phone(self, phone):
        """Add phone"""
        phones_list = [p.value for p in self.phones]
        if phone not in phones_list:
            self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Remove phone"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Edit phone"""
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError

    def find_phone(self, phone):
        """Find phone"""
        for i in self.phones:
            if i.value == phone:
                return i
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Address Book"""

    def add_record(self, record):
        """New record in Address Book"""
        self.data[record.name.value] = record

    def find(self, name):
        """Find record data in Address Book"""
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        """Delete record from Address Book"""
        if name in self.data:
            del self.data[name]

    def iterator(self, value):
        """Iterator"""
        count = 0

        while count < len(self.data):
            yield list(self.data.values())[count: count + value]
            count += value
