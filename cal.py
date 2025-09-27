import math

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    else:
        return x / y

def power(x, y):
    return math.pow(x, y)

def square_root(x):
    if x < 0:
        return "Error! Cannot calculate square root of a negative number."
    return math.sqrt(x)

def sin_val(x):
    return math.sin(math.radians(x)) # Convert degrees to radians

def cos_val(x):
    return math.cos(math.radians(x)) # Convert degrees to radians

def tan_val(x):
    if math.cos(math.radians(x)) == 0:
        return "Error! Tangent is undefined."
    return math.tan(math.radians(x)) # Convert degrees to radians

while True:
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. Sine")
    print("8. Cosine")
    print("9. Tangent")
    print("10. Exit")

    choice = input("Enter choice(1/2/3/4/5/6/7/8/9/10): ")

    if choice in ('1', '2', '3', '4'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            result = divide(num1, num2)
            print(num1, "/", num2, "=", result)
    elif choice == '5':
        try:
            num1 = float(input("Enter base number: "))
            num2 = float(input("Enter exponent: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue
        print(num1, "^", num2, "=", power(num1, num2))
    elif choice == '6':
        try:
            num1 = float(input("Enter number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        print("sqrt(", num1, ") =", square_root(num1))
    elif choice == '7':
        try:
            num1 = float(input("Enter angle in degrees: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        print("sin(", num1, ") =", sin_val(num1))
    elif choice == '8':
        try:
            num1 = float(input("Enter angle in degrees: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        print("cos(", num1, ") =", cos_val(num1))
    elif choice == '9':
        try:
            num1 = float(input("Enter angle in degrees: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        print("tan(", num1, ") =", tan_val(num1))
    elif choice == '10':
        print("Exiting calculator.")
        break
    else:
        print("Invalid Input")