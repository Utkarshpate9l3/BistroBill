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
app.geometry("600x440")
app.title('Login')

# Paths to required files
Home_page_path = "src\Home_page.py"
signup_page_path = "src\signup.py"  # Path to the signup file
json_file_path = "users.json"  # JSON file with user data

# Function to authenticate user
def open_home_page():
    username = entry1.get()
    password = entry2.get()

    # Check for empty fields
    if not username or not password:
        error_label.configure(text="Username and password are required.")
        return

    # Verify credentials from JSON
    try:
        with open(json_file_path, 'r') as file:
            users = json.load(file)

        # Check if username and password match any user in JSON
        user_found = any(user['username'] == username and user['password'] == password for user in users)

        if user_found:
            error_label.configure(text="")  # Clear any error
            subprocess.Popen(['python', Home_page_path])  # Open home page
        else:
            error_label.configure(text="Invalid username or password.")

    except FileNotFoundError:
        error_label.configure(text="No user data found. Please sign up first.")
    except Exception as e:
        error_label.configure(text=f"Error: {e}")

# Function to open the sign-up page
def open_signup_page():
    subprocess.Popen(['python', signup_page_path])

# Load background image
try:
    img1 = customtkinter.CTkImage(Image.open("C:/Users/Asus/Desktop/Python_Project/assets/pattern.png"), size=(600, 440))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()
except Exception as e:
    print(f"Error loading image: {e}")
    l1 = customtkinter.CTkLabel(master=app, text="Login Page")  # Fallback if image fails
    l1.pack()

# Create the login frame
frame = customtkinter.CTkFrame(master=l1, width=320, height=375, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Add title label
l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
l2.place(x=50, y=45)

# Username and Password entries
entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=165)

# "Forgot password?" label
l3 = customtkinter.CTkLabel(master=frame, text="Forget password?", font=('Century Gothic', 12))
l3.place(x=155, y=195)

# Error message label (initially empty)
error_label = customtkinter.CTkLabel(master=frame, text="", text_color="red", font=('Century Gothic', 12))
error_label.place(x=50, y=215)

# Login button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=open_home_page, corner_radius=6)
button1.place(x=50, y=240)

# Sign Up button
button_signup = customtkinter.CTkButton(master=frame, width=220, text="Sign Up", command=open_signup_page, corner_radius=6)
button_signup.place(x=50, y=290)

# Load social media icons
try:
    img2 = customtkinter.CTkImage(Image.open("C:/Users/Asus/Desktop/Python_Project/assets/Google__G__Logo.svg.webp").resize((20, 20), Image.LANCZOS))
    img3 = customtkinter.CTkImage(Image.open("C:/Users/Asus/Desktop/Python_Project/assets/124010.png").resize((20, 20), Image.LANCZOS))
    pass
except Exception as e:
    print(f"Error loading social icons: {e}")
    img2 = img3 = None

# Google and Facebook buttons
button2 = customtkinter.CTkButton(master=frame, image=img2, text="Google", width=100, height=20, compound="left",
                                  fg_color='white', text_color='black', hover_color='#AFAFAF')
button2.place(x=50, y=340)

button3 = customtkinter.CTkButton(master=frame, image=img3, text="Facebook", width=100, height=20, compound="left",
                                  fg_color='white', text_color='black', hover_color='#AFAFAF')
button3.place(x=170, y=340)

# Run the application
app.mainloop()
