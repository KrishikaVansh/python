import json
import hashlib
import os

FILE_NAME = "users.json"

# Load existing users or create new file
def load_users():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(FILE_NAME, "w") as f:
        json.dump(users, f, indent=4)

# Hash password using SHA256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register user
def register():
    users = load_users()
    username = input("Enter username: ")

    if username in users:
        print("❌ Username already exists! Try another.")
        return
    
    password = input("Enter password: ")
    hashed = hash_password(password)
    users[username] = hashed
    save_users(users)

    print("✅ Registration successful!")

# Login user
def login():
    users = load_users()
    username = input("Enter username: ")

    if username not in users:
        print("❌ Username not found!")
        return

    password = input("Enter password: ")
    hashed = hash_password(password)

    if users[username] == hashed:
        print("✅ Login successful! Welcome,", username)
    else:
        print("❌ Incorrect password!")

# Main menu
def main():
    while True:
        print("\n===== USER MANAGEMENT SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main()
