import tkinter as tk
from tkinter import messagebox
import json
import os

# Path to the JSON file where items will be saved
ITEMS_FILE = "items.json"

# Load items from the JSON file if it exists, otherwise use default items
def load_items():
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "r") as f:
            return json.load(f)
    else:
        # Default items if no file exists
        return {
            "Lassi": 50,
            "Coffee": 20,
            "Tea": 10,
            "Juice": 30,
            "Shakes": 50,
            "Milk": 20,
            "Shikanji": 15,
            "Red Bull": 150,
            "Roti": 5,
            "Dal Makhni": 12,
            "Paneer": 100,
            "Naan": 10
        }

# Save items to the JSON file
def save_items():
    with open(ITEMS_FILE, "w") as f:
        json.dump(items, f)

# Load items on startup
items = load_items()

def setup_item_manager(root):
    # Set window background and expand window size
    root.config(bg="#2e2e2e")
    root.geometry("500x500")

    # Frame to manage items with gray background
    item_frame = tk.Frame(root, bg="#3b3b3b")
    item_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title
    tk.Label(item_frame, text="Manage Menu Items", font=("Arial", 16), bg="#3b3b3b", fg="white").pack(pady=10)

    # Entry fields for item name and price with gray background and white text
    tk.Label(item_frame, text="Item Name:", bg="#3b3b3b", fg="white").pack(pady=5)
    item_name_entry = tk.Entry(item_frame, bg="#4a4a4a", fg="white", insertbackground="white", width=30)
    item_name_entry.pack()

    tk.Label(item_frame, text="Item Price:", bg="#3b3b3b", fg="white").pack(pady=5)
    item_price_entry = tk.Entry(item_frame, bg="#4a4a4a", fg="white", insertbackground="white", width=30)
    item_price_entry.pack()

    # Display area for items and prices with gray background
    item_display = tk.Listbox(item_frame, width=40, height=10, bg="#4a4a4a", fg="white", selectbackground="#5c5c5c")
    item_display.pack(pady=10)

    def update_display():
        item_display.delete(0, tk.END)
        for name, price in items.items():
            item_display.insert(tk.END, f"{name}: ${price}")

    # Function to add item
    def add_item():
        name = item_name_entry.get().strip()
        try:
            price = int(item_price_entry.get())
            if name and price >= 0:
                items[name] = price
                update_display()
                save_items()  # Save after modification
                item_name_entry.delete(0, tk.END)
                item_price_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Invalid Input", "Item name and price must be provided.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid price.")

    # Function to delete item
    def delete_item():
        selected = item_display.get(tk.ACTIVE)
        if selected:
            item_name = selected.split(":")[0].strip()
            if item_name in items:
                del items[item_name]
                update_display()
                save_items()  # Save after modification

    # Function to update an existing item's price
    def update_item():
        selected = item_display.get(tk.ACTIVE)
        if selected:
            item_name = selected.split(":")[0].strip()
            try:
                new_price = int(item_price_entry.get())
                if item_name in items and new_price >= 0:
                    items[item_name] = new_price
                    update_display()
                    save_items()  # Save after modification
                    item_price_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Invalid Input", "Enter a valid price.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid price.")

    # Buttons for add, delete, and update operations with gray theme
    add_button = tk.Button(item_frame, text="Add Item", command=add_item, bg="#5a5a5a", fg="white", width=15)
    add_button.pack(pady=5)

    delete_button = tk.Button(item_frame, text="Delete Item", command=delete_item, bg="#5a5a5a", fg="white", width=15)
    delete_button.pack(pady=5)

    update_button = tk.Button(item_frame, text="Update Item", command=update_item, bg="#5a5a5a", fg="white", width=15)
    update_button.pack(pady=5)

    # Initialize the display with existing items
    update_display()

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Item Manager")
    setup_item_manager(root)
    root.mainloop()
