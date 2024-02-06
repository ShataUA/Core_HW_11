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
    def __init__(self, value):
        self._value = None
        self.value = value
        # self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        """Return the value"""
        return self._value

    @value.setter
    def value(self, value):
        if value and not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain 10 digits.")
        self._value = value


class Birthday(Field):
    """Birthday class"""
    def __init__(self, value):
        self._value = None
        self.value = value
        super().__init__(self._value)

    @property
    def value(self):
        """Return the value"""
        return self._value

    @value.setter
    def value(self, value):
        try:
            if isinstance(value, str):
                self._value = datetime.strptime(value, '%d-%m-%Y')
                # self._value = parse
            else:
                self._value = value
        except ValueError:
            raise ValueError ('Invalid birthday format. Try "dd-mm-yyyy"')


class Record:
    """Record class"""
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        """Days to birthday"""
        if self.birthday:
            today = datetime.now()
            birthday_this_year = self.birthday.value.replace(today.year)
            if today < birthday_this_year:
                return print((birthday_this_year - today).days)
            else:
                return print((birthday_this_year.replace(today.year + 1) - today).days)
        else:
            return print(f'No birthday specified for contact {self.name}')

    def add_phone(self, phone):
        """Add phone"""
        if phone and phone not in self.phones:
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
    def __init__(self):
        super().__init__()
        self.count = 0
        self.data = {}

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
        while self.count < len(self.data):
            key_list = list(self.data.keys())[self.count: self.count + value]
            for key in key_list:
                yield self.data[key]
            self.count += value
            break
