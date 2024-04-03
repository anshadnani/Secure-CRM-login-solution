from tkinter import ttk, messagebox
import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import re
import datetime
from time import sleep
from threading import Thread
import smtplib
import ssl
from email.message import EmailMessage
import hashlib

sender_email = "adnaniansh@gmail.com"
sender_password = "yxivszgtkppjivul"
port = 465
smtp_server = "smtp.gmail.com"


class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("500x500")
        master.resizable(False, False)

        # Create a background image
        self.bg_image = ImageTk.PhotoImage(
            Image.open("plutologo.png").resize((500, 500)))

        # Connect to the database and create the users table if it doesn't exist
        self.connection = sqlite3.connect("login.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS person (name TEXT, mobile TEXT, email TEXT, address TEXT, dob DATE, passport TEXT PRIMARY KEY)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS ticket (id TEXT, origin TEXT, dest TEXT, datetime REAL, owner TEXT, mail INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (owner) REFERENCES person (passport))")
        self.connection.commit()

        self.create_login_frame()

    def create_background(self, frame):

        # Create a label to display the background image
        self.bg_label = tk.Label(frame, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_login_frame(self):

        self.login_frame = tk.Frame(self.master, width=500, height=500)

        self.create_background(self.login_frame)

        # label to add space at top of form
        tk.Label(self.login_frame).pack(pady=35)

        # Create the username and password labels and entry widgets
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        # Create the login button
        self.login_button = tk.Button(
            self.login_frame, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        # Create the error message label
        self.error_label = tk.Label(self.login_frame, text="", fg="red")
        self.error_label.pack(pady=5)

        tk.Label(self.login_frame, text="Create a new account?").pack(pady=10)
        # Create the signup button
        self.signup_button = tk.Button(
            self.login_frame, text="Signup", command=self._signup)
        self.signup_button.pack(pady=5)

        self.login_frame.pack()
        self.login_frame.pack_propagate(0)

    def destroy_login_frame(self):
        self.login_frame.destroy()

    def create_signup_frame(self):
        self.signup_frame = tk.Frame(self.master, width=500, height=500)

        self.create_background(self.signup_frame)

        # label to add space at top of form
        tk.Label(self.signup_frame).pack(pady=35)

        # Create the username and password labels and entry widgets
        self.username_label = tk.Label(self.signup_frame, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.signup_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.signup_frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.signup_frame, show="*")
        self.password_entry.pack(pady=5)

        # Create the login button
        self.signup_button = tk.Button(
            self.signup_frame, text="Signup", command=self.signup)
        self.signup_button.pack(pady=5)

        # Create the error message label
        self.error_label = tk.Label(self.signup_frame, text="", fg="red")
        self.error_label.pack(pady=5)

        tk.Label(self.signup_frame, text="Login to your account?").pack(pady=10)
        # Create the signup button
        self.login_button = tk.Button(
            self.signup_frame, text="Login", command=self._login)
        self.login_button.pack(pady=5)

        self.signup_frame.pack()
        self.signup_frame.pack_propagate(0)

    def destroy_signup_frame(self):
        self.signup_frame.destroy()

    def _signup(self):
        self.destroy_login_frame()
        self.create_signup_frame()

    def signup(self):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password and len(password) >= 5:
            hashed_password = hashlib.sha256(
                password.encode("utf-8")).hexdigest()
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.connection.commit()
            messagebox.showinfo("Success", "New Account Created Successfully!")
            self._login()
        elif username and password and len(password) < 5:
            messagebox.showerror(
                "Error", "Password should be a minimum of 5 letters!")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def _login(self):
        self.destroy_signup_frame()
        self.create_login_frame()

    def login(self):
        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.config(
                text="Username and password cannot be empty.")
            return

        # Check if the username and password are correct
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        result = self.cursor.fetchone()
        if result:
            self.error_label.config(text="")
            self.show_main_app()
        else:
            self.error_label.config(text="Invalid username or password.")

    def show_main_app(self):
        # Destroy the login page widgets
        self.destroy_login_frame()

        self.main_frame = tk.Frame(self.master, width=500, height=500)

        self.create_background(self.main_frame)

        # Create the main page widgets

        self.main_label = tk.Label(
            self.main_frame, text="Welcome to the main page!")
        self.main_label.pack(pady=5)
        self.logout_button = tk.Button(
            self.main_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=3)

        # Create the table for data entry
        self.table_frame = tk.Frame(self.main_frame)
        self.y_scrollbar = tk.Scrollbar(self.table_frame)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_scrollbar = tk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.table = ttk.Treeview(
            self.table_frame, yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)

        self.table.bind("<<TreeviewSelect>>", self.item_selected)

        self.table.pack(pady=5, padx=3)

        self.y_scrollbar.config(command=self.table.yview)
        self.x_scrollbar.config(command=self.table.xview)

        self.table_frame.pack(pady=5)

        # columns for table

        self.table['columns'] = (
            'client_name', 'mobile', 'email', 'passport_no', 'dob', 'address', 'ticket', 'ticket_id')

        self.table.column("#0", width=0,  stretch=tk.NO)
        self.table.column("client_name", anchor=tk.CENTER, width=80)
        self.table.column("mobile", anchor=tk.CENTER, width=80)
        self.table.column("email", anchor=tk.CENTER, width=80)
        self.table.column("passport_no", anchor=tk.CENTER, width=80)
        self.table.column("dob", anchor=tk.CENTER, width=80)
        self.table.column("address", anchor=tk.CENTER, width=80)
        self.table.column("ticket", anchor=tk.CENTER, width=80)
        self.table.column("ticket_id", width=0, stretch=tk.NO)

        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("client_name", text="Name", anchor=tk.CENTER)
        self.table.heading("mobile", text="Mobile", anchor=tk.CENTER)
        self.table.heading("email", text="Email", anchor=tk.CENTER)
        self.table.heading("passport_no", text="Passport No", anchor=tk.CENTER)
        self.table.heading("dob", text="Date of Birth", anchor=tk.CENTER)
        self.table.heading("address", text="Address", anchor=tk.CENTER)
        self.table.heading("ticket", text="Ticket", anchor=tk.CENTER)
        self.table.heading("ticket_id", text="", anchor=tk.CENTER)

        query = '''select p.name, p.mobile, p.email, p.passport, p.dob, p.address, origin, dest, date(t.datetime) as 'date', time(t.datetime) as 'time', t.id  from ticket t
                    join person p
                    on t.owner = p.passport
                    WHERE t.datetime > julianday('now')
                    order by t.datetime'''
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        if result:
            for i, row in enumerate(result):
                values = list(row[:6])
                values.append(f"{row[6]} to {row[7]} at {row[8]} {row[9]}")
                values.append(row[-1])
                self.table.insert(parent='', index='end',
                                  iid=i, text='', values=values)
        self.remove_selected = tk.Button(
            self.main_frame, text="Remove selected entry", command=self._remove_selected)
        self.remove_selected.pack(pady=5)
        self.add_new_entry = tk.Button(
            self.main_frame, text="Add new entry", command=self.create_new_entry_frame)
        self.add_new_entry.pack(pady=10)

        self.main_frame.pack()
        self.main_frame.pack_propagate(0)

    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            self.selected_data = item['values']

    def _remove_selected(self):

        query = "DELETE FROM ticket WHERE owner=? AND ID=?"

        if self.selected_data:
            passport = self.selected_data[3]
            t_id = self.selected_data[-1]

            self.cursor.execute(query, (passport, t_id))
            self.connection.commit()

            self.selected_data = None

            self.destroy_main_app()
            self.show_main_app()
        else:
            messagebox.showerror("Error", "No entry selected!")

    def destroy_main_app(self):
        self.main_frame.destroy()

    def clear_dob(self, *args):

        if self.dob_entry.get() == "YYYY-MM-DD":
            self.dob_entry.delete(0, tk.END)

    def clear_date(self, *args):

        if self.date_entry.get() == "YYYY-MM-DD":
            self.date_entry.delete(0, tk.END)

    def clear_time(self, *args):

        if self.time_entry.get() == "HH:MM:SS":
            self.time_entry.delete(0, tk.END)

    def leave_dob(self, *args):

        if self.dob_entry.get() == "":
            self.dob_entry.insert(0, "YYYY-MM-DD")

    def leave_date(self, *args):

        if self.date_entry.get() == "":
            self.date_entry.insert(0, "YYYY-MM-DD")

    def leave_time(self, *args):

        if self.time_entry.get() == "":
            self.time_entry.insert(0, "HH:MM:SS")

    def create_new_entry_frame(self):

        self.destroy_main_app()

        self.entry_frame = tk.Frame(self.master, width=500, height=500)
        self.create_background(self.entry_frame)

        self.input_frame = tk.Frame(self.entry_frame)

        tk.Label(self.input_frame, text="Add new Entry").grid(
            row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.input_frame, text="Client Name").grid(
            row=1, column=0, pady=5)
        self.name_entry = tk.Entry(self.input_frame)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Mobile Number").grid(
            row=2, column=0, pady=5)
        self.mobile_entry = tk.Entry(self.input_frame)
        self.mobile_entry.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Email").grid(row=3, column=0, pady=5)
        self.email_entry = tk.Entry(self.input_frame)
        self.email_entry.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Passport Number").grid(
            row=4, column=0, pady=5)
        self.passport_entry = tk.Entry(self.input_frame)
        self.passport_entry.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Date of Birth").grid(
            row=5, column=0, pady=5)
        self.dob_entry = tk.Entry(self.input_frame)
        self.dob_entry.grid(row=5, column=1, pady=5, padx=5)
        self.dob_entry.insert(0, "YYYY-MM-DD")
        self.dob_entry.bind("<Button-1>", self.clear_dob)
        self.dob_entry.bind("<FocusOut>", self.leave_dob)

        tk.Label(self.input_frame, text="Address").grid(
            row=6, column=0, pady=5)
        self.address_entry = tk.Entry(self.input_frame)
        self.address_entry.grid(row=6, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Ticket Number").grid(
            row=7, column=0, pady=5)
        self.ticket_no_entry = tk.Entry(self.input_frame)
        self.ticket_no_entry.grid(row=7, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Origin").grid(row=8, column=0, pady=5)
        self.origin_entry = tk.Entry(self.input_frame)
        self.origin_entry.grid(row=8, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Destination").grid(
            row=9, column=0, pady=5)
        self.dest_entry = tk.Entry(self.input_frame)
        self.dest_entry.grid(row=9, column=1, pady=5, padx=5)

        tk.Label(self.input_frame, text="Date").grid(row=10, column=0, pady=5)
        self.date_entry = tk.Entry(self.input_frame)
        self.date_entry.grid(row=10, column=1, pady=5, padx=5)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.bind("<Button-1>", self.clear_date)
        self.date_entry.bind("<FocusOut>", self.leave_date)

        tk.Label(self.input_frame, text="Time").grid(row=11, column=0, pady=5)
        self.time_entry = tk.Entry(self.input_frame)
        self.time_entry.grid(row=11, column=1, pady=5, padx=5)
        self.time_entry.insert(0, "HH:MM:SS")
        self.time_entry.bind("<Button-1>", self.clear_time)
        self.time_entry.bind("<FocusOut>", self.leave_time)

        self.input_frame.pack()

        self.add_entry = tk.Button(
            self.entry_frame, text="Add", command=self._add_entry)
        self.add_entry.pack(pady=5)

        self.cancel_entry = tk.Button(
            self.entry_frame, text="Cancel", command=self._cancel_entry)
        self.cancel_entry.pack(pady=5)

        self.entry_frame.pack()
        self.entry_frame.pack_propagate(0)

    def destroy_entry_frame(self):

        self.entry_frame.destroy()

    def _add_entry(self):
        # add data to database
        if (not self.name_entry.get() or not self.mobile_entry.get() or not self.email_entry.get() or
            not self.address_entry.get() or not self.passport_entry.get() or self.dob_entry.get() == "YYYY-MM-DD" or
            not self.ticket_no_entry.get() or not self.origin_entry.get() or not self.dest_entry.get() or
                self.date_entry.get() == "YYYY-MM-DD" or self.time_entry.get() == "HH:MM:SS"):

            messagebox.showerror("Error", "All fields are required!")
        else:
            name = self.name_entry.get()
            mobile = self.mobile_entry.get()
            email = self.email_entry.get()
            passport = self.passport_entry.get()
            dob = self.dob_entry.get()
            address = self.address_entry.get()
            ticket_no = self.ticket_no_entry.get()
            origin = self.origin_entry.get()
            dest = self.dest_entry.get()
            date_of_dep = self.date_entry.get()
            time_of_dep = self.time_entry.get()

            # validating email
            if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email):
                messagebox.showerror("Error", "Invalid Email Address!")

            # Validating date of birth
            if not re.match("\d{4}\-[0|1]\d\-[0|1|2]\d", dob):
                messagebox.showerror("Error", "Date of birth is not valid!")
            else:
                year, month, date = dob.split("-")
                today = datetime.datetime.now()
                if int(month) not in range(1, 13) or (int(year) > today.year and int(month) > today.month and int(date) >= today.day):
                    messagebox.showerror(
                        "Error", "Date of birth is not valid!")
                if int(month) in [1, 3, 5, 7, 8, 10, 12] and int(date) not in range(1, 32):
                    messagebox.showerror(
                        "Error", "Date of birth is not valid!")
                elif int(month) in [4, 6, 9, 11] and int(date) not in range(1, 31):
                    messagebox.showerror(
                        "Error", "Date of birth is not valid!")
                elif int(month) == 2 and int(date) not in range(1, 29):
                    messagebox.showerror(
                        "Error", "Date of birth is not valid!")

            # Validating departure date
            if not re.match("\d{4}\-[0|1]\d\-[0|1|2]\d", date_of_dep):
                messagebox.showerror(
                    "Error", "Date of departure is not valid!")
            else:
                year, month, date = date_of_dep.split("-")
                today = datetime.datetime.now()
                if int(month) not in range(1, 13) or (int(year) < today.year and int(month) < today.month and int(date) < today.day):
                    messagebox.showerror(
                        "Error", "Date of departure is not valid!")
                if int(month) in [1, 3, 5, 7, 8, 10, 12] and int(date) not in range(1, 32):
                    messagebox.showerror(
                        "Error", "Date of departure is not valid!")
                elif int(month) in [4, 6, 9, 11] and int(date) not in range(1, 31):
                    messagebox.showerror(
                        "Error", "Date of departure is not valid!")
                elif int(month) == 2 and int(date) not in range(1, 29):
                    messagebox.showerror(
                        "Error", "Date of departure is not valid!")

            # Validating departure time
            if not re.match("\d{2}\:\d{2}\:\d{2}", time_of_dep):
                messagebox.showerror(
                    "Error", "Date of departure is not valid!")
            else:
                hour, minute, second = time_of_dep.split(":")
                today = datetime.datetime.now()
                if int(hour) not in range(1, 25) or int(minute) not in range(60) or int(second) not in range(60):
                    messagebox.showerror(
                        "Error", "Time of departure is not valid!")

            self.cursor.execute(
                "SELECT * FROM person WHERE passport=?", (passport,))
            row = self.cursor.fetchone()

            if not row:
                self.cursor.execute("INSERT INTO person (name, mobile, email, address, dob, passport) VALUES (?,?,?,?,?,?)", (
                    name, mobile, email, address, dob, passport))
                self.connection.commit()

            self.cursor.execute("INSERT INTO ticket (id, origin, dest, datetime, owner) VALUES (?, ?, ?, julianday(?), ?)", (
                ticket_no, origin, dest, f"{date_of_dep} {time_of_dep}", passport))
            self.connection.commit()

            messagebox.showinfo("Success", "Entry added successfully!")
            self.destroy_entry_frame()
            self.show_main_app()

    def _cancel_entry(self):

        self.destroy_entry_frame()
        self.show_main_app()

    def logout(self):
        # Close the database connection and destroy the main page widgets
        self.connection.close()
        self.destroy_main_app()

        self.create_login_frame()

        # Reconnect to the database
        self.connection = sqlite3.connect("login.db")
        self.cursor = self.connection.cursor()


def mailto(mail, msg):
    context = ssl.create_default_context()
    email = EmailMessage()
    email['From'] = sender_email
    email['To'] = mail
    email['Subject'] = "Flight Remainder"
    email.set_content(msg)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        return server.sendmail(sender_email, mail, email.as_string())


def background_task(interval):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    query = """SELECT p.name, p.email, t.origin, t.dest, date(t.datetime) as 'date', time(t.datetime) as 'time', t.id FROM ticket t
            JOIN person p
            ON t.owner = p.passport
            WHERE t.datetime - julianday('now') < 1 AND t.mail = 0"""

    update_query = """UPDATE ticket SET mail=? WHERE id=?"""
    while True:

        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            client_name, email, origin, destination, date, time, id = row
            msg = f"""Hey {client_name},
It is to inform you that you have a flight from {origin} to {destination} at {date} {time}
            
Regards
Pluto Travels"""

            res = mailto(email, msg)
            if not res:
                cursor.execute(update_query, (1, id))
                conn.commit()
        sleep(interval)


daemon = Thread(target=background_task, args=(600,),
                daemon=True, name="background")
daemon.start()

# Create the main window and start the application
root = tk.Tk()
app = LoginApp(root)
root.mainloop()
