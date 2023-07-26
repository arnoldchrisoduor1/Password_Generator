import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length=12, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True):
    # Password generation logic (same as previous code)
    pass

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("400x250")
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
                messagebox.showinfo("Generated Password", f"Your password is: {password}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number for the password length.")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
