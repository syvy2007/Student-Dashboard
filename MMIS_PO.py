import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
import json
import hashlib
import secrets
import logging
from pathlib import Path
import socket

# Store the users file next to this script so paths are predictable
USER_DIR = Path(__file__).parent
USERS_FILE = USER_DIR / 'users.json'

# logging
logging.basicConfig(level=logging.INFO)



# HASHING for the PASSWORDS
def _derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 100_000
    key = _derive_key(password, salt, iterations)
    return f"{salt.hex()}${iterations}${key.hex()}"


def verify_password(stored: str, provided: str) -> bool:
    try:
        
        if '$' not in stored:
            
            legacy = hashlib.sha256(provided.encode('utf-8')).hexdigest()
            return secrets.compare_digest(legacy, stored)

        salt_hex, iterations_s, key_hex = stored.split('$')
        salt = bytes.fromhex(salt_hex)
        iterations = int(iterations_s)
        expected = bytes.fromhex(key_hex)
        derived = _derive_key(provided, salt, iterations)
        return secrets.compare_digest(derived, expected)
    except Exception:
        return False


# LOAD USERS
def load_users() -> dict:
    try:
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except json.JSONDecodeError:
        logging.warning("users.json is malformed; starting with empty users")
    except Exception as e:
        logging.exception("Failed to load users file: %s", e)

    # default users if file does not exist or fails to load
    logging.info("Creating default users (first run)")
    return {
        "admin": {
            "name": "Administrator",
            "password": hash_password("admin123"),
            "role": "admin"
        },
        "Vlladolid": {
            "name": "Villadolid",
            "password": hash_password("12345"),
            "role": "student"
        }
    }


def save_users(users: dict):
    try:
        tmp = USERS_FILE.with_suffix('.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
        tmp.replace(USERS_FILE)
    except Exception:
        logging.exception("Failed to save users")



# LOGIN WINDOW 
class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        # colors
        self._bg = "#f5f5f5"
        self._header_bg = "#8b2c2c"
        self._accent = "#c84545"
        self._text_dark = "#333333"
        self._text_light = "#ffffff"
        

        self.title("MMIS Dashboard - Login")
        self.geometry("480x480")
        self.configure(bg=self._bg)

        # Header
        header = tk.Frame(self, bg=self._header_bg, height=100)
        header.pack(fill='x')
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=self._header_bg)
        title_frame.pack(side='left', padx=16, expand=True, fill='both')
        tk.Label(title_frame, text='MMIS Dashboard', bg=self._header_bg, fg=self._text_light,
                 font=('Segoe UI', 16, 'bold')).pack(anchor='w')
        tk.Label(title_frame, text='Maria Montessori International School', bg=self._header_bg, fg='#e8c8c8',
                 font=('Segoe UI', 9)).pack(anchor='w')

        main_panel = tk.Frame(self, bg=self._bg)
        main_panel.pack(fill='both', expand=True, padx=32, pady=24)

        tk.Label(main_panel, text='Sign In', bg=self._bg, fg=self._text_dark,
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 16))

        # Username
        tk.Label(main_panel, text='Username', bg=self._bg).pack(anchor='w')
        self.username_entry = tk.Entry(main_panel)
        self.username_entry.pack(fill='x', ipady=6, pady=6)

        # Password
        tk.Label(main_panel, text='Password', bg=self._bg).pack(anchor='w')
        self.password_entry = tk.Entry(main_panel, show="*")
        self.password_entry.pack(fill='x', ipady=6, pady=6)

        # Buttons
        btn_frame = tk.Frame(main_panel, bg=self._bg)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Login", bg=self._header_bg, fg="white",
                  command=self.login).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="Register", bg=self._accent, fg="white",
                  command=self.open_register).grid(row=0, column=1, padx=8)

        self.users = load_users()
        # UX: press Enter to login
        self.bind('<Return>', self.login)
        self.username_entry.focus_set()

   
    # LOGIN LOGIC (UPDATED)
    def login(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter username and password")
            return

        key = username.lower()
        user = self.users.get(key)
        if user and verify_password(user.get("password", ""), password):
            role = user.get("role", "")
            display = user.get("name", username)
            messagebox.showinfo("Login Success", f"Welcome, {display} ({role})")

            # Pass user info to dashboard (store session next to app)
            try:
                session_file = USER_DIR / 'session.json'
                with open(session_file, 'w', encoding='utf-8') as f:
                    json.dump({"user": key, "role": role}, f)
            except Exception:
                logging.exception("Failed to write session file")

            # Try to open using VS Code Live Server (default port 5500)
            LIVE_PORT = 5500
            live_url = f'http://127.0.0.1:{LIVE_PORT}/index.html'
            try:
                with socket.create_connection(('127.0.0.1', LIVE_PORT), timeout=0.5):
                    webbrowser.open(live_url)
            except OSError:
                # Live Server not running — warn the user and fall back to file://
                messagebox.showwarning(
                    "Live Server Not Running",
                    f"Could not contact Live Server at {LIVE_PORT}.\n\nPlease start Live Server in your editor (default port {LIVE_PORT}) or click OK to open the dashboard using the file:// path (some features may be limited)."
                )
                webbrowser.open(os.path.abspath(str(USER_DIR / 'index.html')))

            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def open_register(self):
        RegisterWindow(self)



# REGISTER WINDOW (UPDATED)
class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Register")
        self.geometry("480x500")
        self.configure(bg=parent._bg)

        form = tk.Frame(self, bg=parent._bg)
        form.pack(padx=30, pady=30, fill="both")

        tk.Label(form, text="Full Name").pack(anchor="w")
        self.name_entry = tk.Entry(form)
        self.name_entry.pack(fill='x', pady=6)

        tk.Label(form, text="Username").pack(anchor="w")
        self.username_entry = tk.Entry(form)
        self.username_entry.pack(fill='x', pady=6)

        tk.Label(form, text="Password").pack(anchor="w")
        self.password_entry = tk.Entry(form, show="*")
        self.password_entry.pack(fill='x', pady=6)

        tk.Label(form, text="Confirm Password").pack(anchor="w")
        self.confirm_entry = tk.Entry(form, show="*")
        self.confirm_entry.pack(fill='x', pady=6)

        tk.Label(form, text="Role").pack(anchor="w")
        self.role_var = tk.StringVar(value="student")
        tk.OptionMenu(form, self.role_var, "student", "admin").pack(fill='x')

        tk.Button(form, text="Create Account", bg=parent._accent, fg="white",
                  command=self.register).pack(pady=20)

 
    # REGISTER LOGIC 
    def register(self):
        name = self.name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        users = load_users()

        key = username.lower()
        if key in users:
            messagebox.showerror("Error", "Username exists")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return

        users[key] = {
            "name": name or username,
            "password": hash_password(password),
            "role": role
        }

        save_users(users)

        messagebox.showinfo("Success", "Account created")
        self.parent.users = users
        self.destroy()


# ==================================================================================================================================
if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()
