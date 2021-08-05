import mymath

# Introspection capabilities
from inspect import getmembers, isfunction, isclass, ismethod


def get_functions(module):
    return getmembers(module, isfunction)


def get_classes(module):
    return getmembers(module, isclass)


def get_methods(module):
    return getmembers(module, ismethod)


function_routing = dict(get_functions(mymath))
class_table = dict(get_classes(mymath))

print('Add 1 and 2:', function_routing['add'](1, 2))
print('Sub 1 and 2:', function_routing['sub'](1, 2))
print('Mul 1 and 2:', function_routing['mul'](1, 2))
print('Div 1 and 2:', function_routing['div'](1, 2))
print('Fib of 10:', function_routing['fib'](10))

calculator = class_table['Calc']('example calculator', 9)
calc_routing = get_methods(calculator)

print('This is', calculator.name())
print('And it is a Calc:', (type(calculator) == class_table['Calc']))

i = 0

for name, method in calc_routing:
    if name != 'name' and name != 'value' and name != '__init__' and name != '_Calc__secret':
        print(name, i, '=', method(i))
        i += 1

# You can also call private methods
dict(calc_routing)['_Calc__secret']()

print('Final value', dict(calc_routing)['value']())