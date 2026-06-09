import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import hashlib
import os

USER_FILE = "user.txt"
TASK_FILE = "tasks.txt"

# ---------------- PASSWORD ENCRYPTION ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- LOGIN SYSTEM ----------------
def register():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    hashed = hash_password(password)

    with open(USER_FILE, "w") as f:
        f.write(username + "," + hashed)

    messagebox.showinfo("Success", "Registered Successfully")

def login():
    username = user_entry.get()
    password = pass_entry.get()

    try:
        with open(USER_FILE, "r") as f:
            data = f.read().split(",")
            if username == data[0] and hash_password(password) == data[1]:
                login_window.destroy()
                open_todo()
            else:
                messagebox.showerror("Error", "Invalid Login")
    except:
        messagebox.showerror("Error", "No user found, please register")

# ---------------- TODO FUNCTIONS ----------------
def load_tasks():
    listbox.delete(0, tk.END)
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            for line in f:
                listbox.insert(tk.END, line.strip())

def save_tasks():
    tasks = listbox.get(0, tk.END)
    with open(TASK_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def add_task():
    task = task_entry.get()
    due = cal.get_date()

    if task == "":
        messagebox.showwarning("Warning", "Enter task")
        return

    full_task = f"{task} (Due: {due})"
    listbox.insert(tk.END, full_task)
    save_tasks()
    task_entry.delete(0, tk.END)

def delete_task():
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def mark_done():
    try:
        selected = listbox.curselection()[0]
        task = listbox.get(selected)
        listbox.delete(selected)
        listbox.insert(tk.END, "✔ " + task)
        save_tasks()
    except:
        messagebox.showwarning("Warning", "Select a task")

def clear_all():
    confirm = messagebox.askyesno("Confirm", "Delete all tasks?")
    if confirm:
        listbox.delete(0, tk.END)
        save_tasks()

def search_task():
    keyword = search_entry.get().lower()
    listbox.delete(0, tk.END)

    with open(TASK_FILE, "r") as f:
        for line in f:
            if keyword in line.lower():
                listbox.insert(tk.END, line.strip())

def logout(root):
    root.destroy()
    main()

# ---------------- TODO UI ----------------
def open_todo():
    global listbox, task_entry, search_entry, cal

    root = tk.Tk()
    root.title("✨ Smart To-Do App")
    root.geometry("520x650")
    root.config(bg="#1e272e")

    tk.Label(root, text="📝 My Tasks", font=("Arial", 22, "bold"),
             bg="#1e272e", fg="#00cec9").pack(pady=10)

    task_entry = tk.Entry(root, font=("Arial", 12), width=30)
    task_entry.pack(pady=5)

    cal = DateEntry(root, width=20, background="darkblue",
                    foreground="white", borderwidth=2)
    cal.pack(pady=5)

    btn_frame = tk.Frame(root, bg="#1e272e")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add", bg="#00b894", fg="white",
              width=10, command=add_task).grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Delete", bg="#d63031", fg="white",
              width=10, command=delete_task).grid(row=0, column=1, padx=5)

    tk.Button(btn_frame, text="Done", bg="#0984e3", fg="white",
              width=10, command=mark_done).grid(row=0, column=2, padx=5)

    tk.Button(btn_frame, text="Clear All", bg="#6c5ce7", fg="white",
              width=10, command=clear_all).grid(row=1, column=0, columnspan=3, pady=5)

    search_entry = tk.Entry(root, font=("Arial", 12))
    search_entry.pack(pady=5)

    tk.Button(root, text="Search", bg="#fdcb6e", command=search_task).pack()
    tk.Button(root, text="Show All", bg="#55efc4", command=load_tasks).pack(pady=5)

    listbox = tk.Listbox(root, width=50, height=15,
                         font=("Arial", 12), bg="#2d3436", fg="white")
    listbox.pack(pady=20)

    tk.Button(root, text="Logout", bg="#636e72", fg="white",
              command=lambda: logout(root)).pack()

    load_tasks()
    root.mainloop()

# ---------------- LOGIN UI ----------------
def main():
    global login_window, user_entry, pass_entry

    login_window = tk.Tk()
    login_window.title("🔐 Login System")
    login_window.geometry("300x300")
    login_window.config(bg="#2d3436")

    tk.Label(login_window, text="Login", font=("Arial", 18, "bold"),
             bg="#2d3436", fg="white").pack(pady=10)

    tk.Label(login_window, text="Username", bg="#2d3436", fg="white").pack()
    user_entry = tk.Entry(login_window)
    user_entry.pack()

    tk.Label(login_window, text="Password", bg="#2d3436", fg="white").pack()
    pass_entry = tk.Entry(login_window, show="*")
    pass_entry.pack()

    tk.Button(login_window, text="Login", bg="#00b894",
              fg="white", command=login).pack(pady=5)

    tk.Button(login_window, text="Register", bg="#0984e3",
              fg="white", command=register).pack()

    login_window.mainloop()

# ---------------- START ----------------
main()