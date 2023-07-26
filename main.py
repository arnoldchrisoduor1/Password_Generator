import random
import string
import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
import pandas as pd
import sqlite3
import os


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


def save_to_excel(password, description):
    data = {"Password": [password], "Description": [description]}
    df = pd.DataFrame(data)

    file_path = os.path.join(os.getcwd(), "liked_passwords.xlsx")

    if not os.path.exists(file_path):
        # If the file doesn't exist, create a new Excel file with the data
        try:
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            messagebox.showinfo("Saved to Excel", f"Password and description saved to '{file_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving to Excel: {e}")
    else:
        # If the file already exists, append the new data to it
        try:
            with pd.ExcelWriter(file_path, engine="openpyxl", mode="a") as writer:
                df.to_excel(writer, index=False, header=not writer.sheets)
            messagebox.showinfo("Saved to Excel", f"Password and description saved to '{file_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving to Excel: {e}")


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
        self.geometry("400x250")
        create_table()  # Create the database table if it doesn't exist
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Password Generator", font=("Helvetica", 20)).pack(pady=10)

        self.length_label = tk.Label(self, text="Password Length:")
        self.length_label.pack()
        self.length_entry = tk.Entry(self)
        self.length_entry.insert(0, "12")  # Default password length
        self.length_entry.pack()

        self.use_lowercase_var = tk.BooleanVar(value=True)
        self.use_uppercase_var = tk.BooleanVar(value=True)
        self.use_digits_var = tk.BooleanVar(value=True)
        self.use_special_var = tk.BooleanVar(value=True)

        tk.Checkbutton(self, text="Include lowercase letters", variable=self.use_lowercase_var).pack(anchor="w")
        tk.Checkbutton(self, text="Include uppercase letters", variable=self.use_uppercase_var).pack(anchor="w")
        tk.Checkbutton(self, text="Include digits", variable=self.use_digits_var).pack(anchor="w")
        tk.Checkbutton(self, text="Include special characters", variable=self.use_special_var).pack(anchor="w")

        self.generate_button = tk.Button(self, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=20)

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
                    save_to_excel(password, description)
                    messagebox.showinfo("Generated Password", f"Your password is: {password}\nDescription: {description}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number for the password length.")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
