# Week 1, Subject 1: variables, input, if-statements, functions
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

print("2 + 3 =", add(2, 3))
print("10 / 4 =", divide(10, 4))
print("10 / 0 =", divide(10, 0))
