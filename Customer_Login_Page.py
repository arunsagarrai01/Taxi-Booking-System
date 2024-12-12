import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
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
        if db.update_customer_password(self.email, new_password):
            messagebox.showinfo("Success", "Your password has been successfully changed.")
            self.destroy()  # Close the reset page after successful update
            from Customer_Login_Page import CustomerLoginPage  # Re-import the login page
            app = CustomerLoginPage()  # Redirect to the login page
            app.mainloop()
        else:
            messagebox.showerror("Error", "Failed to update the password. Please try again.")

class CustomerLoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the appearance mode to "Light" or "Dark"
        ctk.set_appearance_mode("Light")
        self.title("Customer Login")
        self.geometry("400x600")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)

        # Configure grid layout to center the main frame
        self.grid_rowconfigure(0, weight=1)  # Center vertically
        self.grid_columnconfigure(0, weight=1)  # Center horizontally

        # Main Frame (Centered with fixed size)
        self.main_frame = ctk.CTkFrame(self, width=300, height=450)  # Specify fixed dimensions
        self.main_frame.grid(row=0, column=0, sticky="")  # No stretching
        self.main_frame.grid_propagate(False)  # Prevent resizing based on children

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

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("Error", "Please enter both email and password.")
            return

        try:
            db = DatabaseConnection()
            success, customer_info_or_message = db.validate_customer(email, password)

            if success:
                if isinstance(customer_info_or_message, dict):
                    customer_id = customer_info_or_message.get("customer_id", None)
                    if not customer_id:
                        raise ValueError("Customer ID is missing.")

                    self.destroy()  # Close login page
                    from Customer_Dashboard import CustomerPanel

                    taxi = ctk.CTk()
                    app = CustomerPanel(taxi, customer_id)
                    taxi.mainloop()
                else:
                    messagebox.showerror("Error", "Unexpected data format received from the database.")
            else:
                messagebox.showerror("Login Failed", customer_info_or_message)

        except ImportError as e:
            messagebox.showerror("Import Error", f"Module error: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")




 # Show the error message

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
