import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess
from Database_Connection import DatabaseConnection


class AdminLoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Light")
        self.title("Admin Login")
        self.geometry("400x500")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.grid_rowconfigure((0, 7), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome To Admin Login",
            font=("Helvetica", 20, "bold"),
            text_color="#333"
        )
        self.title_label.grid(row=1, column=0, pady=(10, 20))
    
        self.email_label = ctk.CTkLabel(
            self.main_frame,
            text="Email Address",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.email_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter your email",
            width=250
        )
        self.email_entry.grid(row=3, column=0, padx=20, pady=(5, 10))

        # Password Label and Entry
        self.password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.password_label.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter your password",
            show="*",
            width=250
        )
        self.password_entry.grid(row=5, column=0, padx=20, pady=(5, 20))

        # Login Button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            font=("Helvetica", 14, "bold"),
            width=200,
            height=40,
            fg_color="#0000FF",  # Default blue
            hover_color="#87CEEB",  # Sky blue hover
            command=self.login
        )
        self.login_button.grid(row=6, column=0, pady=(10, 10))

        # Logout Button
        self.logout_button = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            width=200,
            height=40,
            fg_color="#FF0000",  # Default red
            hover_color="#FF6347",  # Tomato hover
            command=self.Exit
        )
        self.logout_button.grid(row=7, column=0, pady=(10, 20))

    def login(self):
        """
        Handle the login button click event.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Error", "Please enter both email and password.")
            return

        # Validate credentials using DatabaseConnection
        db = DatabaseConnection()
        success, message = db.validate_admin(email, password)
        db.close_connection()

        if success:
            messagebox.showinfo("Success", message)

            # Close the login window (destroy it)
            self.destroy()

            # Import AdminDashboard after successful login and create an instance
            from Admin_Dashboard import AdminDashboard
            root = ctk.CTk()  # Create a new Tkinter window for the Admin Dashboard
            admin_dashboard = AdminDashboard(root)  # Initialize the Admin Dashboard
            root.mainloop()  # Start the Tkinter event loop for the Admin Dashboard
        else:
            messagebox.showerror("Login Failed", message)




    def Exit(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()

