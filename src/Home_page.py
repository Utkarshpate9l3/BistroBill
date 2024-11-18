import tkinter
import customtkinter
from PIL import Image
from window_2_Items_modification import items  # Assuming the file contains a list named `items`
import subprocess  # For opening scripts via subprocess

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


# Paths to required files
Login_page_path = "login_Page\login.py"  # Path to the signup file
Add_Items_Path = "src\window_2_Items_modification.py"
Notepad_Path = "src\window_4_Notepad.py"
Calculator_path = "src\window_3_Calculator.py"
Billeing_path = "src\window_6_Billing_Interface.py"

json_file_path = "users.json"  # JSON file with user data

# Functions for the buttons
def run_script(script_name):
    """Execute a Python script by its relative path."""
    try:
        subprocess.Popen(['python', script_name])
    except Exception as e:
        print(f"Error opening {script_name}: {e}")

def logout(home_window):
    """Close the home page and redirect to the login page."""
    home_window.destroy()
    subprocess.Popen(['python', Login_page_path])  # Replace with the relative path to your login page

# Create the Home Page window
def create_home_page():
    home_window = customtkinter.CTk()
    home_window.geometry("800x600")  # Smaller size
    home_window.title('Home')

    # Configure background color
    home_window.configure(bg="#2C2C2C")  # Dark grey background matching the theme

    # Welcome message
    welcome_label = customtkinter.CTkLabel(
        master=home_window, text="Welcome to BistroBill",
        font=('Century Gothic', 30), text_color="white"  # Smaller font
    )
    welcome_label.pack(pady=10)

    # Frame for left stock list
    left_frame = customtkinter.CTkFrame(master=home_window, width=250, height=450, corner_radius=15, fg_color="#1E1E1E")
    left_frame.pack(side=tkinter.LEFT, padx=10, pady=10, fill=tkinter.Y)

    stock_label = customtkinter.CTkLabel(
        master=left_frame, text="Items in Stock", font=('Century Gothic', 16), text_color="white"
    )
    stock_label.pack(pady=5)

    # Scrollable stock list
    stock_canvas = tkinter.Canvas(left_frame, bg="#1E1E1E", highlightthickness=0)
    scrollbar = tkinter.Scrollbar(left_frame, orient=tkinter.VERTICAL, command=stock_canvas.yview)
    stock_list_frame = customtkinter.CTkFrame(master=stock_canvas, fg_color="#1E1E1E")

    stock_canvas.create_window((0, 0), window=stock_list_frame, anchor="nw")
    stock_canvas.configure(yscrollcommand=scrollbar.set)
    stock_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    # Populate stock list from `items`
    for item in items:  # Replace with actual data from `window_2_Items_modification.py`
        item_label = customtkinter.CTkLabel(
            master=stock_list_frame, text=item, font=('Century Gothic', 12), text_color="white"
        )
        item_label.pack(pady=2)

    # Adjust canvas size dynamically
    def on_configure(event):
        stock_canvas.configure(scrollregion=stock_canvas.bbox("all"))

    stock_list_frame.bind("<Configure>", on_configure)

    # Frame for buttons
    right_frame = customtkinter.CTkFrame(master=home_window, width=500, height=450, corner_radius=15, fg_color="#1E1E1E")
    right_frame.pack(side=tkinter.RIGHT, padx=10, pady=10, fill=tkinter.BOTH)

    # Buttons arranged in two rows
    button_params = {"master": right_frame, "width": 180, "height": 50, "corner_radius": 8}
    button1 = customtkinter.CTkButton(
        text="Calculator", fg_color="#34A853", text_color="white",
        command=lambda: run_script(Calculator_path),  # Replace with the relative path to the calculator script
        **button_params
    )
    button1.grid(row=0, column=0, padx=20, pady=20)

    button2 = customtkinter.CTkButton(
        text="Notepad", fg_color="#4285F4", text_color="white",
        command=lambda: run_script(Notepad_Path),  # Replace with the relative path to the notepad script
        **button_params
    )
    button2.grid(row=0, column=1, padx=20, pady=20)

    button3 = customtkinter.CTkButton(
        text="Add Items", fg_color="#FBBC05", text_color="black",
        command=lambda: run_script(Add_Items_Path),  # Replace with the relative path to the add items script
        **button_params
    )
    button3.grid(row=1, column=0, padx=20, pady=20)

    button4 = customtkinter.CTkButton(
        text="Create Bill", fg_color="#EA4335", text_color="white",
        command=lambda: run_script(Billeing_path),  # Replace with the relative path to the create bill script
        **button_params
    )
    button4.grid(row=1, column=1, padx=20, pady=20)

    # Logout button
    logout_button = customtkinter.CTkButton(
        master=home_window,
        text="Logout",
        fg_color="red",
        text_color="white",
        width=100,
        height=40,
        corner_radius=8,
        command=lambda: logout(home_window)  # Pass home_window to the logout function
    )
    logout_button.place(relx=1.0, rely=1.0, anchor=tkinter.SE, x=-10, y=-10)  # Bottom-right corner

    home_window.mainloop()


# Launch the home page directly
create_home_page()
