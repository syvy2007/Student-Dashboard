import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
import json

USERS_FILE = 'users.json'


def load_users():
    # Load users from JSON file if present, otherwise return default map
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    # default fallback users (kept for compatibility)
    return {
        "Villadolid": "12345",
        "Lumanta": "876543",
        "Son": "123344",
    }


def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print('Failed to save users:', e)


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("360x240")

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Login", width=10, command=self.login).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Register", width=10, command=self.open_register).grid(row=0, column=1, padx=5)

        self.users = load_users()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username and username in self.users and self.users[username] == password:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            # OPEN HTML DASHBOARD
            html_path = os.path.abspath("index.html")
            webbrowser.open(f"file://{html_path}")
            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_register(self):
        RegisterWindow(self)


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Register')
        self.geometry('360x320')
        self.parent = parent

        tk.Label(self, text='Full name:').pack(pady=4)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=4)

        tk.Label(self, text='Username:').pack(pady=4)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=4)

        tk.Label(self, text='Password:').pack(pady=4)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=4)

        tk.Label(self, text='Confirm password:').pack(pady=4)
        self.confirm_entry = tk.Entry(self, show='*')
        self.confirm_entry.pack(pady=4)

        tk.Button(self, text='Create account', command=self.register).pack(pady=10)

    def register(self):
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not username or not password:
            messagebox.showerror('Error', 'Username and password are required')
            return
        if password != confirm:
            messagebox.showerror('Error', 'Passwords do not match')
            return

        users = load_users()
        if username in users:
            messagebox.showerror('Error', 'Username already exists')
            return

        # Save user (password stored in plain text for this demo project)
        users[username] = password
        save_users(users)

        # Update parent login data and prefill fields
        self.parent.users = users
        self.parent.username_entry.delete(0, tk.END)
        self.parent.username_entry.insert(0, username)
        self.parent.password_entry.delete(0, tk.END)
        self.parent.password_entry.insert(0, password)

        messagebox.showinfo('Success', 'Account created — you can now login')
        self.destroy()


if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()


