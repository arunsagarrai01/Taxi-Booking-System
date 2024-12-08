import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from Database_Connection import DatabaseConnection

class CustomerLoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the appearance mode to "Light" or "Dark"
        ctk.set_appearance_mode("Light")  # You can change to "Dark" if you prefer
        self.title("Customer Login")
        self.geometry("400x600")
        self.configure(bg="#f4f4f4")

        # Centering the main frame in the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main Frame (Centered)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Centering elements within the main frame
        self.main_frame.grid_rowconfigure((0, 8), weight=1)  # Top and bottom spacing
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome To Customer Login",
            font=("Helvetica", 20, "bold"),
            text_color="#333"
        )
        self.title_label.grid(row=0, column=0, pady=(10, 20), sticky="n")

        # Email Label and Entry
        self.email_label = ctk.CTkLabel(
            self.main_frame,
            text="Email Address",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.email_label.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))

        self.email_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter your email",
            width=250
        )
        self.email_entry.grid(row=2, column=0, pady=(5, 10))

        # Password Label and Entry
        self.password_label = ctk.CTkLabel(
            self.main_frame,
            text="Password",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.password_label.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter your password",
            show="*",
            width=250
        )
        self.password_entry.grid(row=4, column=0, pady=(5, 20))

        # Login Button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            font=("Helvetica", 14, "bold"),
            width=200,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",  # Change color on hover
            command=self.login
        )
        self.login_button.grid(row=5, column=0, pady=(10, 20))

        # Forget Password Button
        self.forgot_password_button = ctk.CTkButton(
            self.main_frame,
            text="Forgot Password?",
            font=("Helvetica", 10),
            width=200,
            height=30,
            fg_color="white",
            text_color="#1E90FF",  # Default text color (dodger blue)
            hover_color="#87CEEB",  # Sky blue hover
            border_width=0,
            command=self.forgot_password
        )
        self.forgot_password_button.grid(row=6, column=0, pady=(5, 10))

        # Separator
        self.separator = ctk.CTkLabel(
            self.main_frame,
            text="────────────────────────",
            font=("Helvetica", 10),
            text_color="#aaa"
        )
        self.separator.grid(row=7, column=0, pady=10)

        # Sign Up Label and Button
        self.sign_up_label = ctk.CTkLabel(
            self.main_frame,
            text="Don't have an account?",
            font=("Helvetica", 10),
            text_color="#555"
        )
        self.sign_up_label.grid(row=8, column=0, pady=(5, 0))

        self.sign_up_button = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            font=("Helvetica", 10, "bold"),
            width=200,
            height=40,
            fg_color="#2196F3",
            hover_color="#1e88e5",
            command=self.sign_up
        )
        self.sign_up_button.grid(row=9, column=0, pady=10)

        # Logout Button with Transition from Red to Light Red
        self.logout_button = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            width=200,
            height=40,
            fg_color="#FF0000",  # Default orange
            hover_color="#FF7F7F",  # Red hover first
            command=self.Exit
        )
        self.logout_button.bind("<Enter>", self.set_hover_light_red)
        self.logout_button.grid(row=10, column=0, pady=10)

    # Change hover color for Logout Button to Light Red
    def set_hover_light_red(self, event):
        self.logout_button.hover_color = "#FFA07A"  # Light red

    # Placeholder methods for button actions
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
        customer = db.validate_customer(email, password)  # Assuming this returns customer details or None

        if customer:
            customer_id = customer[0]
            # Redirect to CustomerPanel
            self.destroy()  # Close the login page
            from Customer_Dashboard import CustomerPanel  # Import your dashboard
            taxi = ctk.CTk()  # Create a new window for CustomerPanel
            app = CustomerPanel(taxi, customer_id)  # Pass the parent window and customer ID
            taxi.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")



    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Redirecting to Forgot Password Page.")

    def sign_up(self):
        self.destroy()
        from Customer_Registration_Page import CustomerRegistrationPage
        app = CustomerRegistrationPage()
        app.mainloop()

    def Exit(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()


if __name__ == "__main__":
    app = CustomerLoginPage()
    app.mainloop()
