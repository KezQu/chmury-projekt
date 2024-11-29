import tkinter as tk
import db_driver


class App:
    def __init__(self, title, resolution):
        self.app = tk.Tk()
        self.db_handle = db_driver.Driver()
        self.app.title(title)
        self.app.geometry(resolution)
        self.db_handle.connect_to_database()
        self.initialize_ui()

    def initialize_ui(self):
        tk.Button(self.app, text="Add Employee", command=self.db_handle.add_employee).grid(
            row=0, column=0, padx=10, pady=10)
        tk.Button(self.app, text="Delete Employee", command=self.db_handle.del_employee).grid(
            row=1, column=0, padx=10, pady=10)
        tk.Button(self.app, text="Add Manager", command=self.db_handle.add_manager).grid(
            row=2, column=0, padx=10, pady=10)
        tk.Button(self.app, text="Delete Manager", command=self.db_handle.del_manager).grid(
            row=3, column=0, padx=10, pady=10)
        tk.Button(self.app, text="Add Department", command=self.db_handle.add_department).grid(
            row=4, column=0, padx=10, pady=10)
        tk.Button(self.app, text="Delete Department", command=self.db_handle.del_department).grid(
            row=5, column=0, padx=10, pady=10)

    def run(self):
        self.app.mainloop()
