import tkinter as tk
from tkinter import messagebox , scrolledtext
import importlib.util
from datetime import datetime
from tkinter import Frame, Label, Entry, LabelFrame, RIDGE, Button
import requests


# Import module directly if it's in the same folder
try:
    import window_2_Items_modification as module
except ModuleNotFoundError:
    print("Error: window_2_Items_modification.py not found in the expected directory.")
    exit(1)

# Get all items
items = module.items

# Define manual categorization for drinks and foods
drinks = {'Lassi', 'Coffee', 'Tea', 'Juice', 'Shakes', 'Milk', 'Shikanj', 'Redbull'}
foods = set(items) - drinks  # Remaining items are categorized as foods

class CheckoutPad:
    def __init__(self, root):
        self.root = root
        self.root.title("Bistro Billing")
        
        # Create frames for layout
        self.drinks_frame = tk.LabelFrame(root, text="Drinks", padx=10, pady=10)
        self.foods_frame = tk.LabelFrame(root, text="Foods", padx=10, pady=10)
        self.bill_frame = tk.LabelFrame(root, text="Bill", padx=10, pady=10)
        
        self.drinks_frame.grid(row=0, column=0, padx=10, pady=10)
        self.foods_frame.grid(row=0, column=1, padx=10, pady=10)
        self.bill_frame.grid(row=0, column=2, padx=10, pady=10)
        
        # Initialize dictionaries for tracking checkboxes and quantities
        self.drink_vars = {}
        self.food_vars = {}
        self.drink_quantities = {}
        self.food_quantities = {}
        
        # Create checkboxes for drinks
        for i, drink in enumerate(drinks):
            var = tk.IntVar()
            chk = tk.Checkbutton(self.drinks_frame, text=drink, variable=var)
            chk.grid(row=i, column=0, sticky="w")
            self.drink_vars[drink] = var
            self.drink_quantities[drink] = tk.Entry(self.drinks_frame, width=5)
            self.drink_quantities[drink].grid(row=i, column=1)
        
        # Create checkboxes for foods
        for i, food in enumerate(foods):
            var = tk.IntVar()
            chk = tk.Checkbutton(self.foods_frame, text=food, variable=var)
            chk.grid(row=i, column=0, sticky="w")
            self.food_vars[food] = var
            self.food_quantities[food] = tk.Entry(self.foods_frame, width=5)
            self.food_quantities[food].grid(row=i, column=1)
        
        # Bill display area
        self.bill_text = tk.Text(self.bill_frame, height=15, width=30)
        self.bill_text.grid(row=0, column=0)
        
        # Footer for total costs and controls
        self.footer_frame = tk.Frame(root)
        self.footer_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # Display fields for total costs
        tk.Label(self.footer_frame, text="Drinks Cost:").grid(row=0, column=0, sticky="e")
        self.drinks_cost_var = tk.StringVar(value="0.00")
        tk.Entry(self.footer_frame, textvariable=self.drinks_cost_var, state="readonly", width=10).grid(row=0, column=1)

        tk.Label(self.footer_frame, text="Foods Cost:").grid(row=0, column=2, sticky="e")
        self.foods_cost_var = tk.StringVar(value="0.00")
        tk.Entry(self.footer_frame, textvariable=self.foods_cost_var, state="readonly", width=10).grid(row=0, column=3)

        # Tax and discount inputs
        tk.Label(self.footer_frame, text="Drinks Tax %:").grid(row=1, column=0, sticky="e")
        self.drinks_tax_entry = tk.Entry(self.footer_frame, width=5)
        self.drinks_tax_entry.grid(row=1, column=1)

        tk.Label(self.footer_frame, text="Foods Tax %:").grid(row=1, column=2, sticky="e")
        self.foods_tax_entry = tk.Entry(self.footer_frame, width=5)
        self.foods_tax_entry.grid(row=1, column=3)

        tk.Label(self.footer_frame, text="Drinks Discount %:").grid(row=2, column=0, sticky="e")
        self.drinks_discount_entry = tk.Entry(self.footer_frame, width=5)
        self.drinks_discount_entry.grid(row=2, column=1)

        tk.Label(self.footer_frame, text="Foods Discount %:").grid(row=2, column=2, sticky="e")
        self.foods_discount_entry = tk.Entry(self.footer_frame, width=5)
        self.foods_discount_entry.grid(row=2, column=3)

        # Total and action buttons
        self.total_button = tk.Button(root, text="Total", command=self.calculate_total)
        self.total_button.grid(row=3, column=0, pady=10)

        self.save_button = tk.Button(root, text="Save", command=self.save_bill)
        self.save_button.grid(row=3, column=1, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.open_send_window)
        self.send_button.grid(row=3, column=2, pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=3, column=3, pady=10)

    def calculate_total(self):
        total_drinks_cost = 0
        total_foods_cost = 0
        self.bill_text.delete('1.0', tk.END)  # Clear previous bill

        # Generate header for bill
        bill_content = f"Bill No - {datetime.now().strftime('%Y%m%d%H%M%S')}\n"
        bill_content += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_content += "=====================\n"
        bill_content += "Items(q)       Amount\n"
        bill_content += "=====================\n"

        # Calculate cost for drinks
        for drink, var in self.drink_vars.items():
            if var.get() == 1:  # If the item is selected
                quantity = int(self.drink_quantities[drink].get() or 0)
                cost = quantity * 50  # Assume each drink costs 50 units
                total_drinks_cost += cost
                bill_content += f"{drink} ({quantity})      {cost}\n"

        # Calculate cost for foods
        for food, var in self.food_vars.items():
            if var.get() == 1:  # If the item is selected
                quantity = int(self.food_quantities[food].get() or 0)
                cost = quantity * 100  # Assume each food item costs 100 units
                total_foods_cost += cost
                bill_content += f"{food} ({quantity})      {cost}\n"

        # Apply tax and discount
        drinks_tax = total_drinks_cost * float(self.drinks_tax_entry.get() or 0) / 100
        foods_tax = total_foods_cost * float(self.foods_tax_entry.get() or 0) / 100
        drinks_discount = total_drinks_cost * float(self.drinks_discount_entry.get() or 0) / 100
        foods_discount = total_foods_cost * float(self.foods_discount_entry.get() or 0) / 100

        # Update costs after tax and discount
        total_drinks_cost = total_drinks_cost + drinks_tax - drinks_discount
        total_foods_cost = total_foods_cost + foods_tax - foods_discount
        final_total = total_drinks_cost + total_foods_cost

        # Update footer fields
        self.drinks_cost_var.set(f"{total_drinks_cost:.2f}")
        self.foods_cost_var.set(f"{total_foods_cost:.2f}")

        # Display bill in the text widget
        bill_content += "=====================\n"
        bill_content += f"Total Drinks Cost:   {total_drinks_cost:.2f}\n"
        bill_content += f"Total Foods Cost:    {total_foods_cost:.2f}\n"
        bill_content += "=====================\n"
        bill_content += f"Grand Total:         {final_total:.2f}\n"
        bill_content += "=====================\n"

        self.bill_text.insert(tk.END, bill_content)

    def save_bill(self):
        # Save the bill to a .txt file
        bill_content = self.bill_text.get('1.0', tk.END).strip()
        if not bill_content:
            messagebox.showwarning("Warning", "No bill to save.")
            return
        
        filename = f"Bill_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(bill_content)
        messagebox.showinfo("Saved", f"Bill saved as {filename}")

    # def send_bill(self):
    #     # Placeholder for sending the bill (e.g., via email or other means)
    #     messagebox.showinfo("Send", "Bill sent successfully (feature not implemented).")
    def open_send_window(self):
    # Create a new window for sending the bill
        send_root = tk.Toplevel(self.root)
        send_root.geometry('400x500')  # Increased the overall window size
        send_root['bg'] = "white"
        
        # Frame for header
        frame4 = Frame(send_root, width=400, height=80, relief=RIDGE, borderwidth=5, bg='#248aa2', highlightbackground="white", highlightcolor="white", highlightthickness=2)
        frame4.place(x=0, y=0)
                
        l2 = Label(frame4, text="Send Bill", font=('roboto', 24, 'bold'), bg='#248aa2', fg="#ffffff")
        l2.place(x=135, y=15)

        # Frame for main content
        frame5 = Frame(send_root, width=400, height=420, relief=RIDGE, borderwidth=5, bg='#248aa2', highlightbackground="white", highlightcolor="white", highlightthickness=2)
        frame5.place(x=0, y=80)

        innerframe5 = Frame(frame5, width=380, height=400, relief=RIDGE, borderwidth=3, bg='#248aa2', highlightbackground="white", highlightcolor="white", highlightthickness=2)        
        innerframe5.place(x=5, y=5)

        # Label and Entry for phone number
        l4 = Label(innerframe5, text="Phone Number", font=('verdana', 10, 'bold'))
        l4.place(x=55, y=30)

        number = Entry(innerframe5, width=40, borderwidth=2)  # Adjusted width to fit new frame size
        number.place(x=55, y=60)
        
        # Label and ScrolledText for bill details
        l5 = Label(innerframe5, text="Bill Details", font=('verdana', 10, 'bold'))
        l5.place(x=55, y=100)

        b_detail = scrolledtext.ScrolledText(innerframe5, width=32, height=12, relief=RIDGE, borderwidth=3)  # Increased width and height to fill frame
        b_detail.place(x=55, y=130)
        
        # Insert the bill details from the main window
        b_detail.insert("1.0", self.bill_text.get("1.0", tk.END))

        # Send function to trigger SMS
        def send_bill():
            ph_number = number.get()
            messages = b_detail.get("1.0", "end-1c")

            if ph_number == "":
                messagebox.showerror("Error", 'Please fill the phone number')
            elif messages == "":
                messagebox.showerror("Error", 'Bill Details is empty')
            else:
                try:
                    url = "https://www.fast2sms.com/dev/bulk"
                    api_key = ""  # Place your Fast2SMS API key here
                    querystring = {
                        "authorization": api_key,
                        "sender_id": "FSTSMS",
                        "message": messages,
                        "language": "english",
                        "route": "p",
                        "numbers": ph_number
                    }
                    headers = {'cache-control': "no-cache"}
                    response = requests.get(url, headers=headers, params=querystring)
                    
                    if response.status_code == 200:
                        messagebox.showinfo("Send SMS", 'Bill has been sent successfully')
                    else:
                        messagebox.showerror("Error", 'Failed to send SMS')

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")
                
        # Button to send the message
        send_msg = Button(innerframe5, text="Send Bill", relief=tk.RAISED, borderwidth=2, font=('verdana', 10, 'bold'), bg='#248aa2', fg="white", padx=20, command=send_bill)
        send_msg.place(x=140, y=350)
# Run the app
root = tk.Tk()
app = CheckoutPad(root)
root.mainloop()
