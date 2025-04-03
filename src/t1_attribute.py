"""
Напишите метакласс, который автоматически добавляет атрибут created_at
с текущей датой и временем к любому классу, который его использует.
"""

from datetime import datetime
from time import sleep


class MyMeta(type):
    def __new__(cls, name, bases, namespace):
        namespace["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, namespace)


# Пример
class MyClass1(metaclass=MyMeta):
    pass


sleep(2)


class MyClass2(metaclass=MyMeta):
    pass


print(MyClass1.created_at)
print(MyClass2.created_at)
print(MyClass1.created_at < MyClass2.created_at)
