import math
import tkinter as tk
from tkinter import ttk


# Conversion factors for measurement conversion
CONVERSION_FACTORS = {
    "meters": {"feet": 3.28084},
    "feet": {"meters": 0.3048},
    "kilograms": {"pounds": 2.20462},
    "pounds": {"kilograms": 0.453592},
    "celsius": {"fahrenheit": lambda c: (c * 9/5) + 32},
    "fahrenheit": {"celsius": lambda f: (f - 32) * 5/9}
}

# Exchange rates for price conversion (example rates, not real-time)
EXCHANGE_RATES = {
    "USD": {"EUR": 0.85, "GBP": 0.75, "JPY": 110.00},
    "EUR": {"USD": 1.18, "GBP": 0.88, "JPY": 129.40},
    "GBP": {"USD": 1.33, "EUR": 1.14, "JPY": 146.00},
    "JPY": {"USD": 0.0091, "EUR": 0.0077, "GBP": 0.0068}
}


class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("400x600")
        master.resizable(False, False)
        master.configure(bg="#F0F0F0")

        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.expression_var.set('')
        self.result_var.set('0')
        self.angle_mode = "deg"  # default to degrees

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.general_math_frame = ttk.Frame(self.notebook, style='TFrame')
        self.scientific_frame = ttk.Frame(self.notebook, style='TFrame')
        self.measurement_frame = ttk.Frame(self.notebook, style='TFrame')
        self.price_frame = ttk.Frame(self.notebook, style='TFrame')

        self.notebook.add(self.general_math_frame, text="General Math")
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.notebook.add(self.measurement_frame, text="Measurement")
        self.notebook.add(self.price_frame, text="Price")

        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#F0F0F0')
        style.configure('TButton', font=('Arial', 16), padding=10, relief="flat", background="#E0E0E0", foreground="#333333")
        style.map('TButton', background=[('active', '#D0D0D0')])

        style.configure('Operator.TButton', background="#ADD8E6", foreground="#FFFFFF")
        style.map('Operator.TButton', background=[('active', '#87CEEB')])

        style.configure('Equals.TButton', background="#4682B4", foreground="#FFFFFF")
        style.map('Equals.TButton', background=[('active', '#5F9EA0')])

        style.configure('Clear.TButton', background="#FF6347", foreground="#FFFFFF")
        style.map('Clear.TButton', background=[('active', '#FF4500')])

        style.configure('Scientific.TButton', background="#D3D3D3", foreground="#333333")
        style.map('Scientific.TButton', background=[('active', '#C0C0C0')])

        self.create_general_math_ui(self.general_math_frame)
        self.create_scientific_ui(self.scientific_frame)
        self.create_measurement_conversion_ui(self.measurement_frame)
        self.create_price_conversion_ui(self.price_frame)

    # ------------------ General Math ------------------
    def create_general_math_ui(self, frame):
        display_frame = tk.Frame(frame, bg="#F0F0F0")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        self.expression_label = tk.Label(display_frame, textvariable=self.expression_var, anchor="e", font=('Arial', 16), bg="#F0F0F0", fg="#888888")
        self.expression_label.pack(expand=True, fill="both")

        self.result_label = tk.Label(display_frame, textvariable=self.result_var, anchor="e", font=('Arial', 24, 'bold'), bg="#F0F0F0", fg="#333333")
        self.result_label.pack(expand=True, fill="both")

        buttons = [
            {'text': 'Ac', 'style': 'Clear.TButton', 'col': 0, 'row': 1},
            {'text': '+/-', 'style': 'Scientific.TButton', 'col': 1, 'row': 1},
            {'text': '%', 'style': 'Scientific.TButton', 'col': 2, 'row': 1},
            {'text': '/', 'style': 'Operator.TButton', 'col': 3, 'row': 1},
            {'text': '7', 'style': 'TButton', 'col': 0, 'row': 2},
            {'text': '8', 'style': 'TButton', 'col': 1, 'row': 2},
            {'text': '9', 'style': 'TButton', 'col': 2, 'row': 2},
            {'text': '*', 'style': 'Operator.TButton', 'col': 3, 'row': 2},
            {'text': '4', 'style': 'TButton', 'col': 0, 'row': 3},
            {'text': '5', 'style': 'TButton', 'col': 1, 'row': 3},
            {'text': '6', 'style': 'TButton', 'col': 2, 'row': 3},
            {'text': '-', 'style': 'Operator.TButton', 'col': 3, 'row': 3},
            {'text': '1', 'style': 'TButton', 'col': 0, 'row': 4},
            {'text': '2', 'style': 'TButton', 'col': 1, 'row': 4},
            {'text': '3', 'style': 'TButton', 'col': 2, 'row': 4},
            {'text': '+', 'style': 'Operator.TButton', 'col': 3, 'row': 4},
            {'text': '0', 'style': 'TButton', 'col': 0, 'row': 5, 'columnspan': 2},
            {'text': '.', 'style': 'TButton', 'col': 2, 'row': 5},
            {'text': '=', 'style': 'Equals.TButton', 'col': 3, 'row': 5}
        ]

        for button_data in buttons:
            text = button_data['text']
            style_name = button_data['style']
            col = button_data['col']
            row = button_data['row']
            columnspan = button_data.get('columnspan', 1)
            ttk.Button(frame, text=text, style=style_name, command=lambda b=text: self.button_click(b)).grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=1, pady=1)

        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

    def button_click(self, value):
        if value == "Ac":
            self.expression_var.set("")
            self.result_var.set("0")
        elif value == "=":
            try:
                result = eval(self.expression_var.get())
                self.result_var.set(str(result))
                self.expression_var.set(str(result))
            except Exception:
                self.result_var.set("Error")
        elif value == "+/-":
            try:
                current = self.expression_var.get()
                if current.startswith("-"):
                    self.expression_var.set(current[1:])
                else:
                    self.expression_var.set("-" + current)
            except Exception:
                self.result_var.set("Error")
        else:
            current = self.expression_var.get()
            self.expression_var.set(current + str(value))

    # ------------------ Scientific ------------------
    def create_scientific_ui(self, frame):
        display_frame = tk.Frame(frame, bg="#F0F0F0")
        display_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.scientific_expression_label = tk.Label(display_frame, textvariable=self.expression_var, anchor="e", font=('Arial', 16), bg="#F0F0F0", fg="#888888")
        self.scientific_expression_label.pack(expand=True, fill="both")

        self.scientific_result_label = tk.Label(display_frame, textvariable=self.result_var, anchor="e", font=('Arial', 24, 'bold'), bg="#F0F0F0", fg="#333333")
        self.scientific_result_label.pack(expand=True, fill="both")

        scientific_buttons_data = [
            {'text': 'sin', 'style': 'Scientific.TButton', 'col': 0, 'row': 1},
            {'text': 'cos', 'style': 'Scientific.TButton', 'col': 1, 'row': 1},
            {'text': 'tan', 'style': 'Scientific.TButton', 'col': 2, 'row': 1},
            {'text': 'sqrt', 'style': 'Scientific.TButton', 'col': 3, 'row': 1},
            {'text': '^', 'style': 'Scientific.TButton', 'col': 4, 'row': 1},
            {'text': 'pi', 'style': 'Scientific.TButton', 'col': 0, 'row': 2},
            {'text': 'deg', 'style': 'Scientific.TButton', 'col': 1, 'row': 2},
            {'text': 'rad', 'style': 'Scientific.TButton', 'col': 2, 'row': 2}
        ]

        for button_data in scientific_buttons_data:
            text = button_data['text']
            style_name = button_data['style']
            col = button_data['col']
            row = button_data['row']
            columnspan = button_data.get('columnspan', 1)

            if text in ['deg', 'rad']:
                ttk.Button(frame, text=text, style=style_name, command=lambda m=text: self.toggle_angle_mode(m)).grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=1, pady=1)
            else:
                ttk.Button(frame, text=text, style=style_name, command=lambda b=text: self.button_click(b)).grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=1, pady=1)

        for i in range(3):
            frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            frame.grid_columnconfigure(i, weight=1)

    def toggle_angle_mode(self, mode):
        self.angle_mode = mode
        self.result_var.set(f"Mode: {mode}")

    # ------------------ Measurement Conversion ------------------
    def create_measurement_conversion_ui(self, frame):
        self.measurement_input_var = tk.StringVar()
        self.from_unit = tk.StringVar(value="meters")
        self.to_unit = tk.StringVar(value="feet")

        tk.Entry(frame, textvariable=self.measurement_input_var, font=('Arial', 14)).pack(pady=10)
        ttk.Combobox(frame, textvariable=self.from_unit, values=list(CONVERSION_FACTORS.keys())).pack(pady=5)
        ttk.Combobox(frame, textvariable=self.to_unit, values=list(CONVERSION_FACTORS.keys())).pack(pady=5)

        tk.Button(frame, text="Convert", command=self.perform_measurement_conversion).pack(pady=10)
        self.measurement_result = tk.Label(frame, text="", font=('Arial', 16))
        self.measurement_result.pack(pady=5)

    def perform_measurement_conversion(self):
        try:
            value = float(self.measurement_input_var.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()

            if from_unit == to_unit:
                converted_value = value
            elif from_unit in CONVERSION_FACTORS and to_unit in CONVERSION_FACTORS[from_unit]:
                factor = CONVERSION_FACTORS[from_unit][to_unit]
                converted_value = factor(value) if callable(factor) else value * factor
            else:
                converted_value = "Error"

            self.measurement_result.config(text=f"{converted_value}")
        except Exception:
            self.measurement_result.config(text="Invalid Input")

    # ------------------ Price Conversion ------------------
    def create_price_conversion_ui(self, frame):
        self.price_input_var = tk.StringVar()
        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="EUR")

        tk.Entry(frame, textvariable=self.price_input_var, font=('Arial', 14)).pack(pady=10)
        ttk.Combobox(frame, textvariable=self.from_currency, values=list(EXCHANGE_RATES.keys())).pack(pady=5)
        ttk.Combobox(frame, textvariable=self.to_currency, values=list(EXCHANGE_RATES.keys())).pack(pady=5)

        tk.Button(frame, text="Convert", command=self.perform_price_conversion).pack(pady=10)
        self.price_result = tk.Label(frame, text="", font=('Arial', 16))
        self.price_result.pack(pady=5)

    def perform_price_conversion(self):
        try:
            amount = float(self.price_input_var.get())
            from_currency = self.from_currency.get()
            to_currency = self.to_currency.get()

            if from_currency == to_currency:
                converted_amount = amount
            elif from_currency in EXCHANGE_RATES and to_currency in EXCHANGE_RATES[from_currency]:
                rate = EXCHANGE_RATES[from_currency][to_currency]
                converted_amount = amount * rate
            else:
                converted_amount = "Error"

            self.price_result.config(text=f"{converted_amount}")
        except Exception:
            self.price_result.config(text="Invalid Input")


if __name__ == "__main__":
    root = tk.Tk()
    my_calculator = CalculatorGUI(root)
    root.mainloop()
