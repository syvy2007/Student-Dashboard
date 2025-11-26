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

        # Maroon/red  color scheme () MMIS logo)
        self._bg = "#f5f5f5"         # light gray background
        self._header_bg = "#8b2c2c"  # maroon/dark red
        self._accent = "#c84545"     # bright red accent
        self._text_dark = "#333333"  # dark text
        self._text_light = "#ffffff" # white text

        self.title("MMIS Dashboard - Login")
        self.geometry("480x480")
        self.configure(bg=self._bg)

        # Header frame with logo and title
        header = tk.Frame(self, bg=self._header_bg, height=100)
        header.pack(fill='x')
        header.pack_propagate(False)

        # Try to load and display logo
        try:
            logo_path = os.path.join(os.path.dirname(__file__), 'images', 'mmiscebu_logo.jpg')
            if os.path.exists(logo_path):
                logo_img = tk.PhotoImage(file=logo_path)
                logo_lbl = tk.Label(header, image=logo_img, bg=self._header_bg)
                logo_lbl.image = logo_img
                logo_lbl.pack(side='left', padx=16, pady=12)
        except Exception:
            pass

        # Title and subtitle in header
        title_frame = tk.Frame(header, bg=self._header_bg)
        title_frame.pack(side='left', padx=12, expand=True, fill='both')
        tk.Label(title_frame, text='MMIS Dashboard', bg=self._header_bg, fg=self._text_light,
                 font=('Segoe UI', 16, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Maria Montessori International School', bg=self._header_bg, fg='#e8c8c8',
                 font=('Segoe UI', 9)).pack(anchor='w')

        # Main login panel
        main_panel = tk.Frame(self, bg=self._bg)
        main_panel.pack(fill='both', expand=True, padx=32, pady=24)

        # Login form
        form_title = tk.Label(main_panel, text='Sign In', bg=self._bg, fg=self._text_dark,
                              font=('Segoe UI', 14, 'bold'))
        form_title.pack(anchor='w', pady=(0, 16))

        # Username
        tk.Label(main_panel, text='Username', bg=self._bg, fg=self._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.username_entry = tk.Entry(main_panel, bg='#ffffff', fg=self._text_dark, relief='solid', bd=1,
                                       font=('Segoe UI', 10))
        self.username_entry.pack(fill='x', pady=(0, 12), ipady=8)

        # Password
        tk.Label(main_panel, text='Password', bg=self._bg, fg=self._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.password_entry = tk.Entry(main_panel, show='*', bg='#ffffff', fg=self._text_dark, relief='solid', bd=1,
                                       font=('Segoe UI', 10))
        self.password_entry.pack(fill='x', pady=(0, 20), ipady=8)

        # Buttons frame
        btn_frame = tk.Frame(main_panel, bg=self._bg)
        btn_frame.pack(fill='x', pady=8)

        login_btn = tk.Button(btn_frame, text='Login', bg=self._header_bg, fg=self._text_light,
                              activebackground=self._accent, relief='flat', font=('Segoe UI', 11, 'bold'),
                              padx=20, pady=10, command=self.login)
        login_btn.pack(side='left', padx=6)

        register_btn = tk.Button(btn_frame, text='Register', bg=self._accent, fg=self._text_light,
                                 activebackground=self._header_bg, relief='flat', font=('Segoe UI', 11, 'bold'),
                                 padx=20, pady=10, command=self.open_register)
        register_btn.pack(side='left', padx=6)

        # Footer
        footer = tk.Label(self, text='New user? Click Register to create an account', bg=self._bg, fg='#999999',
                          font=('Segoe UI', 9))
        footer.pack(pady=12)

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
        self.title('MMIS Dashboard - Register')
        self.geometry('480x520')
        self.parent = parent
        self.configure(bg=parent._bg)
        self.transient(parent)

        # Header (matching parent)
        header = tk.Frame(self, bg=parent._header_bg, height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=parent._header_bg)
        title_frame.pack(side='left', padx=16, expand=True, fill='both', pady=12)
        tk.Label(title_frame, text='Create Account', bg=parent._header_bg, fg=parent._text_light,
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='MMIS Dashboard', bg=parent._header_bg, fg='#e8c8c8',
                 font=('Segoe UI', 9)).pack(anchor='w')

        # Main form panel
        form_panel = tk.Frame(self, bg=parent._bg)
        form_panel.pack(fill='both', expand=True, padx=32, pady=20)

        # Full name
        tk.Label(form_panel, text='Full name', bg=parent._bg, fg=parent._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.name_entry = tk.Entry(form_panel, bg='#ffffff', fg=parent._text_dark, relief='solid', bd=1,
                                   font=('Segoe UI', 10))
        self.name_entry.pack(fill='x', pady=(0, 12), ipady=8)

        # Username
        tk.Label(form_panel, text='Username', bg=parent._bg, fg=parent._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.username_entry = tk.Entry(form_panel, bg='#ffffff', fg=parent._text_dark, relief='solid', bd=1,
                                       font=('Segoe UI', 10))
        self.username_entry.pack(fill='x', pady=(0, 12), ipady=8)

        # Password
        tk.Label(form_panel, text='Password', bg=parent._bg, fg=parent._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.password_entry = tk.Entry(form_panel, show='*', bg='#ffffff', fg=parent._text_dark, relief='solid', bd=1,
                                       font=('Segoe UI', 10))
        self.password_entry.pack(fill='x', pady=(0, 12), ipady=8)

        # Confirm password
        tk.Label(form_panel, text='Confirm password', bg=parent._bg, fg=parent._text_dark,
                 font=('Segoe UI', 10)).pack(anchor='w', pady=(8, 2))
        self.confirm_entry = tk.Entry(form_panel, show='*', bg='#ffffff', fg=parent._text_dark, relief='solid', bd=1,
                                      font=('Segoe UI', 10))
        self.confirm_entry.pack(fill='x', pady=(0, 20), ipady=8)

        # Create account button
        create_btn = tk.Button(form_panel, text='Create Account', bg=parent._accent, fg=parent._text_light,
                               activebackground=parent._header_bg, relief='flat', font=('Segoe UI', 11, 'bold'),
                               padx=20, pady=10, command=self.register)
        create_btn.pack(fill='x', pady=10)

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


