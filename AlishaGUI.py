import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Toplevel
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["AttendanceDB"]
collection = db["students"]

# Main Window
root = tk.Tk()
root.title("557 - Alisha Shaikh | Student Attendance Tracker")
root.geometry("620x450")
root.configure(bg="#f0f4f7")

ttk.Label(root, text="557 - Alisha Shaikh | Student Attendance Tracker", font=("Segoe UI", 16, "bold")).pack(pady=15)

# Form Frame
form = ttk.Frame(root)
form.pack(pady=10)
labels = ["Student ID", "Name", "Status (Present/Absent)"]
entries = {}

for i, label in enumerate(labels):
    ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    ent = ttk.Entry(form, width=30)
    ent.grid(row=i, column=1, pady=5)
    entries[label] = ent

# ------------------ CRUD Functions ------------------

def insert():
    sid = entries["Student ID"].get().strip()
    name = entries["Name"].get().strip()
    status = entries["Status (Present/Absent)"].get().strip().capitalize()

    if not (sid and name and status):
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    if collection.find_one({"student_id": sid}):
        messagebox.showerror("Duplicate", "Student ID already exists.")
        return

    collection.insert_one({"student_id": sid, "name": name, "status": status})
    messagebox.showinfo("Success", "Attendance marked.")
    clear_entries()

def read():
    result.delete(1.0, tk.END)
    for doc in collection.find():
        result.insert(tk.END, f"ID: {doc['student_id']} | Name: {doc['name']} | Status: {doc['status']}\n")

def update():
    win = Toplevel(root)
    win.title("Update Attendance")
    win.geometry("350x250")

    ttk.Label(win, text="Student ID to Update:").pack(pady=5)
    sid_entry = ttk.Entry(win, width=30)
    sid_entry.pack()

    ttk.Label(win, text="New Name:").pack(pady=5)
    name_entry = ttk.Entry(win, width=30)
    name_entry.pack()

    ttk.Label(win, text="New Status:").pack(pady=5)
    status_entry = ttk.Entry(win, width=30)
    status_entry.pack()

    def confirm():
        sid = sid_entry.get().strip()
        name = name_entry.get().strip()
        status = status_entry.get().strip().capitalize()

        if not (sid and name and status):
            messagebox.showwarning("Missing Info", "All fields required.")
            return

        result = collection.update_one({"student_id": sid}, {"$set": {"name": name, "status": status}})
        if result.modified_count > 0:
            messagebox.showinfo("Updated", "Record updated.")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No matching student ID.")

    ttk.Button(win, text="Update", command=confirm).pack(pady=15)

def delete():
    win = Toplevel(root)
    win.title("Delete Record")
    win.geometry("300x180")

    ttk.Label(win, text="Enter Student ID to Delete:").pack(pady=10)
    del_entry = ttk.Entry(win, width=30)
    del_entry.pack()

    def confirm():
        sid = del_entry.get().strip()
        if not sid:
            messagebox.showwarning("Missing Info", "Student ID required.")
            return

        result = collection.delete_one({"student_id": sid})
        if result.deleted_count > 0:
            messagebox.showinfo("Deleted", "Record deleted.")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No matching student ID.")

    ttk.Button(win, text="Delete", command=confirm).pack(pady=15)

def clear_entries():
    for e in entries.values():
        e.delete(0, tk.END)

# ------------------ Buttons ------------------
btns = ttk.Frame(root)
btns.pack(pady=10)

ttk.Button(btns, text="Mark Attendance", command=insert).grid(row=0, column=0, padx=10)
ttk.Button(btns, text="View Records", command=read).grid(row=0, column=1, padx=10)
ttk.Button(btns, text="Update", command=update).grid(row=0, column=2, padx=10)
ttk.Button(btns, text="Delete", command=delete).grid(row=0, column=3, padx=10)

# ------------------ Result Area ------------------
result = scrolledtext.ScrolledText(root, width=75, height=10, font=("Consolas", 10))
result.pack(pady=10)

root.mainloop()
