import tkinter as tk
from tkinter import messagebox, ttk

# ==============================
# LOGIN CREDENTIALS & GRADES
# ==============================
USERS = {
    "Villadolid": "12345",
    "Lumanta": "876543",
    "Son": "123344",
}

STUDENT_GRADES = {
    "Villadolid": {
        "General Physics": 89,
        "Contemporary Philippine Arts from the Regions": 92,
        "General Biology": 85,
        "Practical Research": 88,
        "Personal Development": 95,
        "General Chemistry": 94,
        "Empowerment Technology": 95,
        "Media Information Literacy": 99,
        "Rhythmic Activities": 96,
    },
    "Lumanta": {
        "General Physics": 89,
        "Contemporary Philippine Arts from the Regions": 92,
        "General Biology": 96,
        "Practical Research": 99,
        "Personal Development": 95,
        "General Chemistry": 96,
        "Empowerment Technology": 99,
        "Media Information Literacy": 96,
        "Rhythmic Activities": 95,
    },
    "Son": {
        "General Physics": 99,
        "Contemporary Philippine Arts from the Regions": 92,
        "General Biology": 96,
        "Practical Research": 99,
        "Personal Development": 95,
        "General Chemistry": 96,
        "Empowerment Technology": 99,
        "Media Information Literacy": 96,
        "Rhythmic Activities": 95,
    }
}

# ==============================
# DESIGN COLORS
# ==============================
BG_COLOR = "#F9F5FF"       # soft lavender background
CARD_COLOR = "#FFFFFF"      # white card
ACCENT_COLOR = "#A084DC"    # soft violet
TEXT_COLOR = "#4A4A4A"      # dark gray
FONT_TITLE = ("Poppins", 16, "bold")
FONT_TEXT = ("Poppins", 12)


# ==============================
# LOGIN SCREEN
# ==============================
def show_login():
    def check_login():
        username = entry_username.get()
        password = entry_password.get()

        if username in USERS and USERS[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            login_window.destroy()
            show_grades(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Student Login")
    login_window.geometry("400x350")
    login_window.config(bg=BG_COLOR)

    # Aesthetic login frame (card)
    frame = tk.Frame(login_window, bg=CARD_COLOR, bd=3, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

    # Title
    tk.Label(frame, text="Welcome Student", font=FONT_TITLE, fg=ACCENT_COLOR, bg=CARD_COLOR).pack(pady=10)

    # Username input
    tk.Label(frame, text="Username", font=FONT_TEXT, bg=CARD_COLOR).pack(pady=(10, 0))
    entry_username = tk.Entry(frame, font=FONT_TEXT, bg="#F0EFFF", relief="flat", justify="center")
    entry_username.pack(pady=5, ipady=4)

    # Password input
    tk.Label(frame, text="Password", font=FONT_TEXT, bg=CARD_COLOR).pack(pady=(10, 0))
    entry_password = tk.Entry(frame, font=FONT_TEXT, show="*", bg="#F0EFFF", relief="flat", justify="center")
    entry_password.pack(pady=5, ipady=4)

    # Login Button
    tk.Button(
        frame, text="Login", font=FONT_TEXT, bg=ACCENT_COLOR, fg="white",
        relief="flat", cursor="hand2", command=check_login
    ).pack(pady=15, ipadx=15, ipady=5)

    login_window.mainloop()


# ==============================
# GRADES DASHBOARD
# ==============================
def show_grades(username):
    grades_window = tk.Tk()
    grades_window.title("Student Grades Dashboard")
    grades_window.geometry("700x450")
    grades_window.config(bg=BG_COLOR)

    # Sidebar
    sidebar = tk.Frame(grades_window, bg=ACCENT_COLOR, width=160)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="Dashboard", bg=ACCENT_COLOR, fg="white", font=("Poppins", 15, "bold")).pack(pady=20)
    tk.Label(sidebar, text=f"{username}", bg=ACCENT_COLOR, fg="#EDE7F6", font=("Poppins", 11)).pack(pady=5)

    # Logout button
    def logout():
        grades_window.destroy()
        show_login()

    tk.Button(sidebar, text="Logout", bg="#8668CC", fg="white", font=("Poppins", 11),
              relief="flat", cursor="hand2", command=logout).pack(pady=15, ipadx=10, ipady=3)

    # Main area
    main_frame = tk.Frame(grades_window, bg=CARD_COLOR, bd=3, relief="ridge")
    main_frame.place(relx=0.58, rely=0.5, anchor="center", width=460, height=370)

    tk.Label(main_frame, text="Student Grades", font=FONT_TITLE, fg=ACCENT_COLOR, bg=CARD_COLOR).pack(pady=10)

    # Dropdown to select student
    selected_student = tk.StringVar(value=username)

    def display_grades(student):
        for widget in grades_frame.winfo_children():
            widget.destroy()
        for subject, grade in STUDENT_GRADES[student].items():
            tk.Label(grades_frame, text=f"{subject}: {grade}", font=FONT_TEXT, bg=CARD_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=10, pady=3)

    tk.Label(main_frame, text="Select Student:", font=FONT_TEXT, bg=CARD_COLOR).pack()
    student_menu = ttk.OptionMenu(main_frame, selected_student, username, *STUDENT_GRADES.keys(), command=display_grades)
    student_menu.pack(pady=5)

    # Grades display frame
    grades_frame = tk.Frame(main_frame, bg=CARD_COLOR)
    grades_frame.pack(pady=10)
    display_grades(username)

    grades_window.mainloop()


# ==============================
# START PROGRAM
# ==============================
show_login()
