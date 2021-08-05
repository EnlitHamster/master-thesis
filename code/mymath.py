def add(x, y):
    return x + y


def sub(x, y):
    return x - y;


def mul(x, y):
    return x * y;


def div(x, y):
    return x / y;


def fib(n):
    fib_1 = 0
    fib_2 = 1

    fib_list = [fib_1, fib_2]

    for _ in range(0, n-2):
        next_fib = fib_1 + fib_2
        fib_list.append(next_fib)
        fib_1, fib_2 = fib_2, next_fib

    return fib_list


class Calc:

    
    def __init__(self, name):
        self.__name = name
        self.__val = 0


    def __init__(self, name, val):
        self.__name = name
        self.__val = val


    def name(self):
        return self.__name


    def value(self):
        return self.__val


    def add(self, x):
        self.__val += x
        return self.__val


    def sub(self, x):
        self.__val -= x
        return self.__val


    def mul(self, x):
        self.__val *= x
        return self.__val


    def div(self, x):
        self.__val /= x
        return self.__val


    def __secret(self):
        self.__val = 0