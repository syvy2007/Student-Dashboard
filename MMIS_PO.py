import tkinter as tk
from tkinter import messagebox
import webbrowser
import os

USERS = {
    "Lumanta": "876543",
}

class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("350x250")
        self.configure(bg="#f3e9ff")  

        # Title Label
        tk.Label(
            self,
            text="MMIS Login",
            font=("Arial", 18, "bold"),
            bg="#f3e9ff",
            fg="#53008f"
        ).pack(pady=10)

        # Username
        tk.Label(self, text="Username:", bg="#f3e9ff", fg="black").pack()
        self.username_entry = tk.Entry(self, width=25)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(self, text="Password:", bg="#f3e9ff", fg="black").pack()
        self.password_entry = tk.Entry(self, width=25, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_btn = tk.Button(
            self,
            text="Login",
            bg="#8b5cf6",
            fg="white",
            width=15,
            height=1,
            activebackground="#7c3aed",
            activeforeground="white",
            command=self.login
        )
        self.login_btn.pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in USERS and USERS[username] == password:
            messagebox.showinfo("Login Success", "Welcome!")

            # OPEN HTML DASHBOARD
            html_path = os.path.abspath("index.html")
            webbrowser.open(f"file://{html_path}")

            self.destroy()
        else:
            messagebox.showerror("Error", "Invalid username or password")


if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()


