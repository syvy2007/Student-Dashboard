import tkinter as tk
from tkinter import messagebox, ttk
import random


# LOGIN CREDENTIALS & GRADES
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

# LOGIN SCREEN
def show_login():
    def generate_code():
        code = str(random.randint(1000, 9999))
        lbl_code.config(text=f"Verification Code: {code}")
        return code

    def check_login():
        username = entry_username.get()
        password = entry_password.get()
        code_input = entry_code.get()

        if username in USERS and USERS[username] == password:
            if code_input == current_code[0]:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                login_window.destroy()
                show_dashboard(username)
            else:
                messagebox.showerror("Login Failed", "Incorrect verification code")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Student Login")
    login_window.geometry("300x250")

    tk.Label(login_window, text="Username").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    current_code = [generate_code()]
    lbl_code = tk.Label(login_window, text=f"Verification Code: {current_code[0]}")
    lbl_code.pack(pady=5)

    entry_code = tk.Entry(login_window)
    entry_code.pack(pady=5)

    tk.Button(login_window, text="New Code", command=lambda: current_code.__setitem__(0, generate_code())).pack(pady=5)
    tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

    login_window.mainloop()



#============================DASHBOARD=============================

def show_dashboard(username):
    dashboard = tk.Tk()
    dashboard.title("Student Grades Dashboard")
    dashboard.geometry("500x400")

    tk.Label(dashboard, text=f"Welcome, {username}!").pack(pady=10)

    # Student selector
    selected_student = tk.StringVar(value=username)
    tk.Label(dashboard, text="Select Student:").pack()
    student_menu = ttk.OptionMenu(dashboard, selected_student, username, *STUDENT_GRADES.keys())
    student_menu.pack(pady=5)

    # Grades display frame
    grades_frame = tk.Frame(dashboard)
    grades_frame.pack(pady=10)

    def display_grades(student):
        for widget in grades_frame.winfo_children():
            widget.destroy()
        for subject, grade in STUDENT_GRADES[student].items():
            tk.Label(grades_frame, text=f"{subject}: {grade}").pack(anchor="w")

    # Initial display
    display_grades(username)

    # Update grades when selection changes
    selected_student.trace_add("write", lambda *args: display_grades(selected_student.get()))

    # Logout button
    tk.Button(dashboard, text="Logout", command=lambda: [dashboard.destroy(), show_login()]).pack(pady=10)

    dashboard.mainloop()


# START PROGRAM
show_login()
