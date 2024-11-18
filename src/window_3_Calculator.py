import tkinter as tk
from math import *

def press(key):
    if key == '=':
        try:
            # Evaluate the expression and display the result
            result = str(eval(entry.get()))  # Safely evaluate the expression using eval
            entry.delete(0, tk.END)  # Clear the entry field
            entry.insert(tk.END, result)  # Insert the result
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")  # Handle invalid input
    elif key == 'C':
        entry.delete(0, tk.END)  # Clear the entry field
    else:
        entry.insert(tk.END, key)  # Insert the pressed key into the entry field

def create_calculator():
    root = tk.Tk()
    root.title("Scientific Calculator")
    root.config(bg="#2e2e2e")  # Set background color for the main window

    global entry
    # Set entry field color to dark gray with white text
    entry = tk.Entry(root, width=40, borderwidth=5, font=('Arial', 18), bg="#4a4a4a", fg="white", insertbackground="white")
    entry.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

    # Button text color and background setup
    buttons = [
        '7', '8', '9', '/', 'sqrt(', '(', ')',
        '4', '5', '6', '*', 'log(', 'sin(', 'cos(',
        '1', '2', '3', '-', 'tan(', 'asin(', 'acos(',
        '0', '.', '=', '+', 'C', 'exp(', 'atan('
    ]

    row_value = 1
    col_value = 0

    # Set button style with gray theme
    for button in buttons:
        tk.Button(root, text=button, width=5, height=2, font=('Arial', 14),
                  bg="#5a5a5a", fg="white", activebackground="#6b6b6b", activeforeground="white",
                  command=lambda key=button: press(key)).grid(row=row_value, column=col_value, padx=5, pady=5)
        col_value += 1
        if col_value > 6:
            col_value = 0
            row_value += 1

    root.mainloop()

create_calculator()
