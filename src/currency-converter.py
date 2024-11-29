import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
import requests
from PIL import ImageTk, Image
from tkinter import messagebox

# Define the root window
root = tk.Tk()
root.geometry("600x270")
root.title("Currency Converter")
root.iconbitmap('assets/icon.ico')
root.maxsize(600, 270)
root.minsize(600, 270)

# Set dark background color
root.configure(bg="#2D2D2D")

# Load image for the label
image = Image.open('assets/currency.png')
zoom = 0.5
pixels_x, pixels_y = tuple([int(zoom * x) for x in image.size])
img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))

# Define API key and base URL
API_KEY = "f8994c8458e3d7d513b600b42ca9eec1"
BASE_URL = "http://api.currencylayer.com/live"
CURRENCY_LIST_URL = "http://api.currencylayer.com/list"

# Fetch available currencies
def fetch_currencies():
    try:
        response = requests.get(CURRENCY_LIST_URL, params={"access_key": API_KEY})
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return list(data["currencies"].keys())
        else:
            messagebox.showerror("Error", "Failed to fetch currency list. Check your API key or internet connection.")
            return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

# Fetch currency list dynamically
currency_list = fetch_currencies()

def show_data():
    amount = E1.get()
    from_currency = c1.get()
    to_currency = c2.get()
    
    if amount == '':
        messagebox.showerror("Currency Converter", "Please fill the amount.")
    elif not from_currency or not to_currency:
        messagebox.showerror("Currency Converter", "Please choose both currencies.")
    else:
        try:
            response = requests.get(BASE_URL, params={"access_key": API_KEY, "currencies": to_currency, "source": from_currency, "format": 1})
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                conversion_rate = data["quotes"].get(f"{from_currency}{to_currency}")
                if conversion_rate:
                    amount = float(amount)
                    converted_amount = conversion_rate * amount
                    E2.delete(0, 'end')
                    E2.insert(0, f"{converted_amount:.2f}")
                    text.insert('end', f'{amount} {from_currency} Equals {converted_amount:.2f} {to_currency} \n\n Last Updated: {datetime.now()}\n')
                else:
                    messagebox.showerror("Currency Converter", f"Conversion rate for {from_currency} to {to_currency} not found!")
            else:
                messagebox.showerror("Currency Converter", "Failed to fetch conversion rate. Check your API key or internet connection.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def clear():
    E1.delete(0, 'end')
    E2.delete(0, 'end')
    text.delete(1.0, 'end')

# Define labels and inputs
l1 = Label(root, text="Currency Converter Using Python", font=('verdana', '10', 'bold'), bg="#2D2D2D", fg="white")
l1.place(x=150, y=15)

amt = Label(root, text="Amount", font=('roboto', 10, 'bold'), bg="#2D2D2D", fg="white")
amt.place(x=20, y=15)

E1 = Entry(root, width=20, borderwidth=1, font=('roboto', 10, 'bold'), bg="#404040", fg="white", insertbackground="white")
E1.place(x=20, y=40)

c1 = tk.StringVar()
c2 = tk.StringVar()

currencychoose1 = ttk.Combobox(root, width=20, textvariable=c1, state='readonly', font=('verdana', 10, 'bold'))
currencychoose1['values'] = currency_list
currencychoose1.place(x=300, y=40)
currencychoose1.current(0)

E2 = Entry(root, width=20, borderwidth=1, font=('roboto', 10, 'bold'), bg="#404040", fg="white", insertbackground="white")
E2.place(x=20, y=80)

currencychoose2 = ttk.Combobox(root, width=20, textvariable=c2, state='readonly', font=('verdana', 10, 'bold'))
currencychoose2['values'] = currency_list
currencychoose2.place(x=300, y=80)
currencychoose2.current(0)

text = Text(root, height=7, width=52, font=('verdana', '10', 'bold'), bg="#404040", fg="white", insertbackground="white")
text.place(x=100, y=120)

B = Button(root, text="Search", command=show_data, font=('verdana', '10', 'bold'), borderwidth=2, bg="#FF5733", fg="white")
B.place(x=20, y=120)

clear_btn = Button(root, text="Clear", command=clear, font=('verdana', '10', 'bold'), borderwidth=2, bg="#2874A6", fg="white")
clear_btn.place(x=20, y=170)

panel = Label(root, image=img, bg="#2D2D2D")
panel.place(x=190, y=35)

root.mainloop()
