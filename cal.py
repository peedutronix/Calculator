import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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

def meters_to_feet(m):
    return m * 3.28084

def feet_to_meters(ft):
    return ft / 3.28084

def kilograms_to_pounds(kg):
    return kg * 2.20462

def pounds_to_kilograms(lb):
    return lb / 2.20462

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

# Placeholder for currency exchange rates (for demonstration purposes)
EXCHANGE_RATES = {
    "USD_to_EUR": 0.85,
    "EUR_to_USD": 1.18,
    "USD_to_GBP": 0.73,
    "GBP_to_USD": 1.37,
}

def convert_currency(amount, from_currency, to_currency):
    key = f"{from_currency}_to_{to_currency}"
    if key in EXCHANGE_RATES:
        return amount * EXCHANGE_RATES[key]
    else:
        raise ValueError("Unsupported currency conversion.")


class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("400x600")

        self.equation = tk.StringVar()
        self.entry_value = ''
        self.equation.set('0')

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        self.general_math_frame = ttk.Frame(self.notebook)
        self.scientific_frame = ttk.Frame(self.notebook)
        self.measurement_frame = ttk.Frame(self.notebook)
        self.price_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.general_math_frame, text="General Math")
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.notebook.add(self.measurement_frame, text="Measurement")
        self.notebook.add(self.price_frame, text="Price")

        self.create_general_math_buttons(self.general_math_frame)
        self.create_scientific_buttons(self.scientific_frame)
        self.create_measurement_conversion_ui(self.measurement_frame)
        self.create_price_conversion_ui(self.price_frame)

        # Configure styles for a modern look
        style = ttk.Style()
        style.theme_use('clam') # Use a modern theme
        style.configure('TButton', font=('Arial', 14), padding=10)
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 14), padding=5)
        style.configure('TCombobox', font=('Arial', 12), padding=5)
        style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'), padding=[10, 5])

        # Display for General Math and Scientific sections
        self.display = tk.Entry(self.general_math_frame, textvariable=self.equation, font=('Arial', 24), bd=0, justify='right', bg="#CCCCCC")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def button_click(self, char):
        if char == '=':
            try:
                self.entry_value = str(eval(self.entry_value.replace('^', '**')))
            except Exception as e:
                self.entry_value = "Error"
                messagebox.showerror("Error", e)
        elif char == 'C':
            self.entry_value = ''
        elif char == 'sqrt':
            try:
                self.entry_value = str(square_root(float(self.entry_value)))
            except Exception as e:
                self.entry_value = "Error"
                messagebox.showerror("Error", e)
        elif char == '^':
            self.entry_value += '**'
        elif char == 'sin':
            try:
                self.entry_value = str(sin_val(float(self.entry_value)))
            except Exception as e:
                self.entry_value = "Error"
                messagebox.showerror("Error", e)
        elif char == 'cos':
            try:
                self.entry_value = str(cos_val(float(self.entry_value)))
            except Exception as e:
                self.entry_value = "Error"
                messagebox.showerror("Error", e)
        elif char == 'tan':
            try:
                self.entry_value = str(tan_val(float(self.entry_value)))
            except Exception as e:
                self.entry_value = "Error"
                messagebox.showerror("Error", e)
        else:
            self.entry_value += str(char)
        self.equation.set(self.entry_value)

    def create_general_math_buttons(self, frame):
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        row_val = 1 # Start from row 1 to leave space for display
        col_val = 0
        for button in buttons:
            ttk.Button(frame, text=button, command=lambda b=button: self.button_click(b)).grid(row=row_val, column=col_val, sticky="nsew", padx=1, pady=1)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        frame.grid_rowconfigure(0, weight=1)
        for i in range(1, row_val + 1):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def create_scientific_buttons(self, frame):
        scientific_buttons = [
            'sqrt', '^', 'sin', 'cos',
            'tan', 'C', '='
        ]
        row_val = 1 # Start from row 1 to leave space for display
        col_val = 0
        for button in scientific_buttons:
            ttk.Button(frame, text=button, command=lambda b=button: self.button_click(b)).grid(row=row_val, column=col_val, sticky="nsew", padx=1, pady=1)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        frame.grid_rowconfigure(0, weight=1)
        for i in range(1, row_val + 1):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

        # Add a display for the scientific section
        self.scientific_display = tk.Entry(self.scientific_frame, textvariable=self.equation, font=('Arial', 24), bd=0, justify='right', bg="#CCCCCC")
        self.scientific_display.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def create_measurement_conversion_ui(self, frame):
        self.measurement_input = tk.StringVar()
        self.measurement_output = tk.StringVar()
        self.measurement_input.set('0')
        self.measurement_output.set('0')

        tk.Label(frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.measurement_input, width=15).grid(row=0, column=1, padx=5, pady=5)

        self.from_unit = ttk.Combobox(frame, values=["Meters", "Feet", "Kilograms", "Pounds", "Celsius", "Fahrenheit"])
        self.from_unit.grid(row=1, column=0, padx=5, pady=5)
        self.from_unit.set("Meters")

        self.to_unit = ttk.Combobox(frame, values=["Meters", "Feet", "Kilograms", "Pounds", "Celsius", "Fahrenheit"])
        self.to_unit.grid(row=1, column=1, padx=5, pady=5)
        self.to_unit.set("Feet")

        tk.Button(frame, text="Convert", command=self.perform_measurement_conversion).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Result:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.measurement_output, width=15, state='readonly').grid(row=3, column=1, padx=5, pady=5)

    def perform_measurement_conversion(self):
        try:
            value = float(self.measurement_input.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = 0

            if from_unit == "Meters" and to_unit == "Feet":
                result = meters_to_feet(value)
            elif from_unit == "Feet" and to_unit == "Meters":
                result = feet_to_meters(value)
            elif from_unit == "Kilograms" and to_unit == "Pounds":
                result = kilograms_to_pounds(value)
            elif from_unit == "Pounds" and to_unit == "Kilograms":
                result = pounds_to_kilograms(value)
            elif from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = celsius_to_fahrenheit(value)
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = fahrenheit_to_celsius(value)
            elif from_unit == to_unit:
                result = value
            else:
                messagebox.showerror("Error", "Unsupported conversion.")
                return

            self.measurement_output.set(str(round(result, 4)))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a numeric value.")
        except Exception as e:
            messagebox.showerror("Error", e)

    def create_price_conversion_ui(self, frame):
        self.price_input = tk.StringVar()
        self.price_output = tk.StringVar()
        self.price_input.set('0')
        self.price_output.set('0')

        tk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.price_input, width=15).grid(row=0, column=1, padx=5, pady=5)

        self.from_currency = ttk.Combobox(frame, values=["USD", "EUR", "GBP"])
        self.from_currency.grid(row=1, column=0, padx=5, pady=5)
        self.from_currency.set("USD")

        self.to_currency = ttk.Combobox(frame, values=["USD", "EUR", "GBP"])
        self.to_currency.grid(row=1, column=1, padx=5, pady=5)
        self.to_currency.set("EUR")

        tk.Button(frame, text="Convert", command=self.perform_price_conversion).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Result:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame, textvariable=self.price_output, width=15, state='readonly').grid(row=3, column=1, padx=5, pady=5)

    def perform_price_conversion(self):
        try:
            amount = float(self.price_input.get())
            from_currency = self.from_currency.get()
            to_currency = self.to_currency.get()

            if from_currency == to_currency:
                result = amount
            else:
                result = convert_currency(amount, from_currency, to_currency)

            self.price_output.set(str(round(result, 2)))
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", e)


if __name__ == '__main__':
    root = tk.Tk()
    my_calculator = CalculatorGUI(root)
    root.mainloop()