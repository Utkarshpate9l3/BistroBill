import tkinter
import os 
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:
    __root = Tk()

    # Default window width and height
    __thisWidth = 600
    __thisHeight = 400
    __thisTextArea = Text(__root, bg="#2e2e2e", fg="white", insertbackground="white", font=("Arial", 14))
    __thisMenuBar = Menu(__root, bg="#3b3b3b", fg="white", tearoff=0)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0, bg="#3b3b3b", fg="white")
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0, bg="#3b3b3b", fg="white")
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0, bg="#3b3b3b", fg="white")

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea, bg="#4a4a4a")	 
    __file = None

    def __init__(self, **kwargs):
        # Set window icon and title
        try:
            self.__root.wm_iconbitmap("Notepad.ico") 
        except:
            pass
        self.__root.title("Untitled - Notepad")
        self.__root.config(bg="#2e2e2e")

        # Set window size and center it on screen
        self.__thisWidth = kwargs.get("width", 600)
        self.__thisHeight = kwargs.get("height", 400)
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__root.geometry(f"{self.__thisWidth}x{self.__thisHeight}+{int(left)}+{int(top)}")

        # Make textarea auto-resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # File menu options
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # Edit menu options
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
        self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
        self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # Help menu options
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        # Configure menu bar
        self.__root.config(menu=self.__thisMenuBar)

        # Configure scrollbar
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Custom Notepad Application")

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt",
         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)
            with open(self.__file, "r") as file:
                self.__thisTextArea.insert(1.0, file.read())

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):
        if not self.__file:
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if not self.__file:
                return
        with open(self.__file, "w") as file:
            file.write(self.__thisTextArea.get(1.0, END))
        self.__root.title(os.path.basename(self.__file) + " - Notepad")

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

# Run main application
notepad = Notepad(width=600, height=400)
notepad.run()
