import random
import string
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
import sqlite3
import pyperclip


def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True):
    characters = ''
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def create_table():
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            password TEXT NOT NULL,
            description TEXT
        )
    """)
    connection.commit()
    connection.close()


def insert_password(password, description):
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO passwords (password, description) VALUES (?, ?)", (password, description))
    connection.commit()
    connection.close()


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("600x400")  # Increased size of the GUI
        create_table()  # Create the database table if it doesn't exist
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Password Generator", font=("Helvetica", 20)).pack(pady=10)

        self.length_label = ttk.Label(self, text="Password Length:")
        self.length_label.pack()
        self.length_entry = ttk.Entry(self)
        self.length_entry.insert(0, "12")  # Default password length
        self.length_entry.pack()

        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(self, text="Include lowercase letters", variable=self.use_lowercase_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include uppercase letters", variable=self.use_uppercase_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include digits", variable=self.use_digits_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include special characters", variable=self.use_special_var).pack(anchor="w")

        self.generate_button = ttk.Button(self, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=20)

        # Add a button to copy the generated password to the clipboard
        self.copy_button = ttk.Button(self, text="Copy Password", command=self.copy_password, state=tk.DISABLED)
        self.copy_button.pack(pady=10)

        # Text box to display the generated password and description
        self.password_textbox = tk.Text(self, height=5, wrap="word")
        self.password_textbox.pack(pady=10, padx=5)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            use_lowercase = self.use_lowercase_var.get()
            use_uppercase = self.use_uppercase_var.get()
            use_digits = self.use_digits_var.get()
            use_special = self.use_special_var.get()

            password = generate_password(length, use_lowercase, use_uppercase, use_digits, use_special)

            if password:
                description = tk.simpledialog.askstring("Description", "Enter a description for the account:")
                if description is not None:
                    insert_password(password, description)
                    self.copy_button.configure(state=tk.NORMAL)  # Enable the copy button
                    # Clear the text box before displaying the new password and description
                    self.password_textbox.delete(1.0, tk.END)
                    # Insert the generated password and description into the text box
                    self.password_textbox.insert(tk.END, f"Generated Password: {password}\nDescription: {description}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number for the password length.")

    def copy_password(self):
        # Retrieve the generated password from the text box instead of generating a new one
        password_and_description = self.password_textbox.get(1.0, tk.END)
        password = password_and_description.split("Generated Password: ")[-1].split("\n")[0]
        pyperclip.copy(password)
        messagebox.showinfo("Password Copied", "The generated password has been copied to the clipboard!")


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()

    
