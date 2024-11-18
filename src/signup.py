import tkinter
import customtkinter
from PIL import Image
import subprocess
import os
import json

# Set the appearance and theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# Initialize the application
app = customtkinter.CTk()
app.geometry("600x500")
app.title('Sign Up')

login_page_path = "src/login.py"  # Path to the login file
json_file_path = "users.json"  # JSON file to store user data

# Function to handle the sign-up process
def handle_sign_up():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()
    fullname = entry_fullname.get()

    # Check for empty fields
    if not username or not password or not email or not fullname:
        error_label.configure(text="All fields are required.")
        return

    # Prepare user data to be saved
    user_data = {
        "username": username,
        "password": password,  # NOTE: In a real application, hash passwords before storing
        "email": email,
        "fullname": fullname
    }

    # Load existing data and append new data
    try:
        # Load existing data if the file exists
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Check if the username already exists
        if any(user['username'] == username for user in data):
            error_label.configure(text="Username already exists. Please choose another.")
            return

        # Append new user data and save
        data.append(user_data)
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Clear input fields and display success message
        entry_username.delete(0, 'end')
        entry_password.delete(0, 'end')
        entry_email.delete(0, 'end')
        entry_fullname.delete(0, 'end')

        success_label.configure(text="Account created successfully! Please go back to login.")
        error_label.configure(text="")  # Clear any previous errors

    except Exception as e:
        error_label.configure(text=f"Error saving data: {e}")

# Function to return to the login page
def return_to_login():
    app.destroy()
    subprocess.Popen(['python', login_page_path])

# Attempt to load the background image
try:
    img1 = customtkinter.CTkImage(Image.open("C:/Users/Asus/Desktop/Python_Project/assets/pattern.png"), size=(600, 500))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()
except Exception as e:
    print(f"Error loading image: {e}")
    l1 = customtkinter.CTkLabel(master=app, text="Sign Up Page")  # Fallback if image fails
    l1.pack()

# Create the sign-up frame
frame = customtkinter.CTkFrame(master=l1, width=320, height=420, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Add the title label
title_label = customtkinter.CTkLabel(master=frame, text="Create a New Account", font=('Century Gothic', 20))
title_label.place(x=50, y=20)

# Full Name entry
entry_fullname = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Full Name')
entry_fullname.place(x=50, y=80)

# Email entry
entry_email = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
entry_email.place(x=50, y=130)

# Username entry
entry_username = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry_username.place(x=50, y=180)

# Password entry
entry_password = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry_password.place(x=50, y=230)

# Error message label (initially empty)
error_label = customtkinter.CTkLabel(master=frame, text="", text_color="red", font=('Century Gothic', 12))
error_label.place(x=50, y=270)

# Success message label (initially empty)
success_label = customtkinter.CTkLabel(master=frame, text="", text_color="green", font=('Century Gothic', 12))
success_label.place(x=50, y=300)

# Sign Up button with handle_sign_up function
button_signup = customtkinter.CTkButton(master=frame, width=220, text="Sign Up", command=handle_sign_up, corner_radius=6)
button_signup.place(x=50, y=330)

# Back to Login button
button_back = customtkinter.CTkButton(master=frame, width=220, text="Back to Login", command=return_to_login, corner_radius=6, fg_color='#AFAFAF')
button_back.place(x=50, y=380)

# Run the application
app.mainloop()
