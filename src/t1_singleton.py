"""
Реализуйте паттерн синглтон тремя способами:

с помощью метаклассов
с помощью метода __new__ класса
через механизм импортов
"""


# 1 Способ
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MyClass(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


# Проверка
# a = MyClass(10)
# b = MyClass(20)
# print(a is b)
# print(a.value)
# print(b.value)


# 2 Способ
class MySingletonClass:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        if not self._initialized:
            self.value = value
            self._initialized = True


# Проверка
# a = MySingletonClass(10)
# b = MySingletonClass(20)
# print(a is b)
# print(a.value)
# print(b.value)


# 3 Способ
# a = instance
# b = instance
# print(a is b)
# print(a.value)
