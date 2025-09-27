import math
import tkinter as tk
from tkinter import ttk, messagebox


# Conversion factors for measurement conversion
CONVERSION_FACTORS = {
    "meters": {"feet": 3.28084},
    "feet": {"meters": 0.3048},
    "kilograms": {"pounds": 2.20462},
    "pounds": {"kilograms": 0.453592},
    "celsius": {"fahrenheit": lambda c: (c * 9/5) + 32},
    "fahrenheit": {"celsius": lambda f: (f - 32) * 5/9}
}

# Exchange rates (demo, not real-time)
EXCHANGE_RATES = {
    "USD": {"EUR": 0.85, "GBP": 0.75, "JPY": 110.00},
    "EUR": {"USD": 1.18, "GBP": 0.88, "JPY": 129.40},
    "GBP": {"USD": 1.33, "EUR": 1.14, "JPY": 146.00},
    "JPY": {"USD": 0.0091, "EUR": 0.0077, "GBP": 0.0068}
}


# Safe eval environment
SAFE_ENV = {
    "sqrt": math.sqrt,
    "pow": math.pow,
    "pi": math.pi,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "__builtins__": {}
}


class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Calculator")
        master.geometry("420x650")
        master.resizable(False, False)

        # Variables
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.expression_var.set("")
        self.result_var.set("0")
        self.angle_mode = "deg"
        self.history = []

        # Notebook (tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.general_math_frame = ttk.Frame(self.notebook)
        self.scientific_frame = ttk.Frame(self.notebook)
        self.measurement_frame = ttk.Frame(self.notebook)
        self.price_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.general_math_frame, text="General")
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.notebook.add(self.measurement_frame, text="Measurement")
        self.notebook.add(self.price_frame, text="Currency")
        self.notebook.add(self.history_frame, text="History")

        # Create UIs
        self.create_general_math_ui(self.general_math_frame)
        self.create_scientific_ui(self.scientific_frame)
        self.create_measurement_conversion_ui(self.measurement_frame)
        self.create_price_conversion_ui(self.price_frame)
        self.create_history_ui(self.history_frame)

        # Dark/Light mode toggle
        menu = tk.Menu(master)
        master.config(menu=menu)
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)

        self.dark_mode = False

    # ------------------ General Math ------------------
    def create_general_math_ui(self, frame):
        display_frame = tk.Frame(frame, bg="#F0F0F0")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        self.expression_label = tk.Label(display_frame, textvariable=self.expression_var,
                                         anchor="e", font=('Arial', 16), bg="#F0F0F0", fg="#555")
        self.expression_label.pack(expand=True, fill="both")

        self.result_label = tk.Label(display_frame, textvariable=self.result_var,
                                     anchor="e", font=('Arial', 24, 'bold'), bg="#F0F0F0", fg="#000")
        self.result_label.pack(expand=True, fill="both")

        buttons = [
            ['Ac', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', 'Copy']
        ]

        for r, row in enumerate(buttons, 1):
            for c, text in enumerate(row):
                ttk.Button(frame, text=text, command=lambda b=text: self.button_click(b)).grid(
                    row=r, column=c, sticky="nsew", padx=2, pady=2)

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
                expr = self.expression_var.get()
                result = eval(expr, SAFE_ENV)
                self.result_var.set(str(result))
                self.expression_var.set(str(result))
                self.history.append(f"{expr} = {result}")
                self.update_history()
            except Exception:
                self.result_var.set("Error")
        elif value == "+/-":
            current = self.expression_var.get()
            if current.startswith("-"):
                self.expression_var.set(current[1:])
            else:
                self.expression_var.set("-" + current)
        elif value == "Copy":
            self.master.clipboard_clear()
            self.master.clipboard_append(self.result_var.get())
            messagebox.showinfo("Copied", "Result copied to clipboard")
        else:
            self.expression_var.set(self.expression_var.get() + str(value))

    # ------------------ Scientific ------------------
    def create_scientific_ui(self, frame):
        sci_buttons = [
            ['sin', 'cos', 'tan', 'sqrt', '^'],
            ['pi', 'deg', 'rad', '(', ')']
        ]

        for r, row in enumerate(sci_buttons):
            for c, text in enumerate(row):
                ttk.Button(frame, text=text, command=lambda b=text: self.button_click(b)).grid(
                    row=r, column=c, sticky="nsew", padx=2, pady=2)

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

    # ------------------ Currency Conversion ------------------
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

    # ------------------ History ------------------
    def create_history_ui(self, frame):
        self.history_listbox = tk.Listbox(frame, font=('Arial', 12))
        self.history_listbox.pack(expand=True, fill="both", padx=5, pady=5)

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history[-20:]:  # last 20
            self.history_listbox.insert(tk.END, item)

    # ------------------ Theme ------------------
    def toggle_theme(self):
        if self.dark_mode:
            self.master.configure(bg="#F0F0F0")
            self.dark_mode = False
        else:
            self.master.configure(bg="#222")
            self.dark_mode = True


if __name__ == "__main__":
    root = tk.Tk()
    my_calculator = CalculatorGUI(root)
    root.mainloop()
