import customtkinter as ctk
from tkinter import messagebox
import re 
import os
import random
import string
from Database_Connection import DatabaseConnection 

class PasswordResetPage(ctk.CTk):
    def __init__(self, email):
        super().__init__()

        self.email = email  # Email passed from the login page

        # Set the appearance mode to "Light" or "Dark"
        ctk.set_appearance_mode("Light")
        self.title("Password Reset")
        self.geometry("400x600")
        self.configure(bg="#f4f4f4")

        # Main Frame (Centered)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Password Reset",
            font=("Helvetica", 20, "bold"),
            text_color="#333"
        )
        self.title_label.grid(row=0, column=0, pady=(10, 20), sticky="n")

        # Reset Code Label and Entry
        self.code_label = ctk.CTkLabel(
            self.main_frame,
            text="Enter Reset Code",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.code_label.grid(row=1, column=0, pady=(10, 0))

        self.code_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter the code",
            width=250
        )
        self.code_entry.grid(row=2, column=0, pady=(5, 10))

        # OK Button to Verify Code
        self.ok_button = ctk.CTkButton(
            self.main_frame,
            text="OK",
            font=("Helvetica", 12),
            width=200,
            height=30,
            fg_color="#4CAF50",
            hover_color="#45a049",  # Hover effect
            command=self.verify_code
        )
        self.ok_button.grid(row=3, column=0, pady=(5, 10))

        # New password fields for reset
        self.new_password_label = ctk.CTkLabel(
            self.main_frame,
            text="New Password",
            font=("Helvetica", 12),
            text_color="#555"
        )
        self.confirm_password_label = ctk.CTkLabel(
            self.main_frame,
            text="Confirm Password",
            font=("Helvetica", 12),
            text_color="#555"
        )

        self.new_password_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Enter new password",
            show="*",
            width=250
        )
        self.confirm_password_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Helvetica", 12),
            placeholder_text="Confirm new password",
            show="*",
            width=250
        )
        
        # Store the generated reset code for validation
        self.generated_code = None

    def generate_reset_code(self):
        """
        Generate and send a reset code to the user's email.
        """
        self.generated_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        # For simplicity, show the code on the interface (in real-world use, you would send it via email)
        messagebox.showinfo("Password Reset", f"Your password reset code is: {self.generated_code}")

    def verify_code(self):
        """
        Verify the code entered by the user for password reset.
        """
        entered_code = self.code_entry.get()
        if entered_code == self.generated_code:
            # Remove reset code widgets
            self.code_label.grid_forget()
            self.code_entry.grid_forget()
            self.ok_button.grid_forget()

            # Display the new password input fields
            self.new_password_label.grid(row=1, column=0, pady=(10, 0))
            self.new_password_entry.grid(row=2, column=0, pady=(5, 10))
            self.confirm_password_label.grid(row=3, column=0, pady=(5, 0))
            self.confirm_password_entry.grid(row=4, column=0, pady=(5, 10))

            # Add OK Button below Confirm Password
            self.ok_button = ctk.CTkButton(
                self.main_frame,
                text="OK",
                font=("Helvetica", 12),
                width=200,
                height=30,
                fg_color="#4CAF50",
                hover_color="#45a049",
                command=self.change_password  # Attach change_password method to OK button
            )
            self.ok_button.grid(row=5, column=0, pady=(10, 10))
        else:
            messagebox.showerror("Error", "Invalid reset code.")


    def change_password(self):
        """
        Update the password in the database and validate the new password.
        """
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not new_password or not confirm_password:
            messagebox.showwarning("Error", "Please fill in both password fields.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Update the password in the database
        db = DatabaseConnection()
        if db.update_driver_password(self.email, new_password):
            messagebox.showinfo("Success", "Your password has been successfully changed.")
            self.destroy()  # Close the reset page after successful update
            from Driver_Login_Page import DriverLoginPage  # Re-import the login page
            app = DriverLoginPage()  # Redirect to the login page
            app.mainloop()
        else:
            messagebox.showerror("Error", "Failed to update the password. Please try again.")

class DriverLoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Light")
        self.title("Driver Login")
        self.geometry("400x500")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main Frame (Centered)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Adjust the grid inside the main_frame for proper alignment
        self.main_frame.grid_rowconfigure((0, 8), weight=1)  # Add padding at top and bottom
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Welcome To Driver Login",
            font=("Helvetica", 20, "bold"),
            text_color="#333"
        )
        self.title_label.grid(row=1, column=0, pady=(10, 20))

        # Email Label and Entry
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

        # Forgot Password Button
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
        self.forgot_password_button.grid(row=7, column=0, pady=(5, 10))

        # Logout Button
        self.logout_button = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            width=200,
            height=40,
            fg_color="#FF0000",  # Default red
            hover_color="#FF6347",  # Tomato hover color
            command=self.Exit
        )
        self.logout_button.grid(row=8, column=0, pady=(10, 20))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Error", "Please enter both email and password.")
            return

        # Validate credentials using DatabaseConnection
        db = DatabaseConnection()
        success, driver_info_or_message = db.validate_driver(email, password)

        if success:
            # Assuming the database returns a dictionary containing 'driver_id' and 'full_name'
            driver_id = driver_info_or_message['driver_id']  # driver_id
            driver_name = driver_info_or_message['full_name']  # driver_name

            # Redirect to Driver Dashboard
            self.destroy()  # Close the login page
            from Driver_Dashboard import DriverDashboard  # Import your dashboard
            taxi = ctk.CTk()  # Create a new window for Driver Dashboard
            app = DriverDashboard(taxi, driver_name, driver_id)  # Pass both driver_name and driver_id
            taxi.mainloop()
        else:
            messagebox.showerror("Login Failed", driver_info_or_message)  # Show the error message

    def forgot_password(self):
        """
        Open the password reset page for the user.
        """
        email = self.email_entry.get()
        if not email:
            messagebox.showwarning("Error", "Please enter your email.")
            return
        
        # Open the Password Reset Page
        reset_page = PasswordResetPage(email)
        reset_page.generate_reset_code()  # Generate the reset code when opening the page
        reset_page.mainloop()

    def Exit(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()

