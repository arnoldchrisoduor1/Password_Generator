import random
import string

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
        print("Error: Please select at least one character type.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

if __name__ == "__main__":
    print("Password Generator Application")
    print("-------------------------------")

    while True:
        try:
            length = int(input("Enter the desired length of the password: "))
            use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
            use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
            use_digits = input("Include digits? (y/n): ").lower() == 'y'
            use_special = input("Include special characters? (y/n): ").lower() == 'y'

            password = generate_password(length, use_lowercase, use_uppercase, use_digits, use_special)

            if password:
                print("Generated Password:", password)
                break
        except ValueError:
            print("Invalid input. Please enter a valid number for the password length.")
