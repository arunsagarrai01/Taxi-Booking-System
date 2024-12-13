import customtkinter as ctk
from tkinter import messagebox
import re  # For email and phone number validation
from Database_Connection import DatabaseConnection  # Import the class
from tkcalendar import DateEntry  # Import for calendar widget

class CustomerRegistrationPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Customer Registration")
        self.geometry("600x800")
        self.configure(bg="#f2f2f2")

        # Set appearance mode
        ctk.set_appearance_mode("System")  # or "Dark" or "Light"
        ctk.set_default_color_theme("blue")

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Customer Registration",
            font=("Helvetica", 24, "bold"),
            text_color="#333333"
        )
        self.title_label.grid(row=0, column=0, pady=(10, 30), columnspan=2)

        # Full Name
        self.name_label = ctk.CTkLabel(self.main_frame, text="Full Name", font=("Helvetica", 14))
        self.name_label.grid(row=1, column=1, sticky="w", pady=(10, 5))
        self.name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your full name", width=300, font=("Helvetica", 12))
        self.name_entry.grid(row=1, column=2, pady=(0, 10))

        # Address
        self.address_label = ctk.CTkLabel(self.main_frame, text="Address", font=("Helvetica", 14))
        self.address_label.grid(row=2, column=1, sticky="w", pady=(10, 5))
        self.address_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your address", width=300, font=("Helvetica", 12))
        self.address_entry.grid(row=2, column=2, pady=(0, 10))

        # Phone Number
        self.phone_label = ctk.CTkLabel(self.main_frame, text="Phone Number", font=("Helvetica", 14))
        self.phone_label.grid(row=3, column=1, sticky="w", pady=(10, 5))
        self.phone_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your phone number", width=300, font=("Helvetica", 12))
        self.phone_entry.grid(row=3, column=2, pady=(0, 10))

        # Gender
        self.gender_label = ctk.CTkLabel(self.main_frame, text="Gender", font=("Helvetica", 14))
        self.gender_label.grid(row=4, column=1, sticky="w", pady=(10, 5))
        self.gender_var = ctk.StringVar(value="Male")

        self.male_button = ctk.CTkRadioButton(self.main_frame, text="Male", variable=self.gender_var, value="Male")
        self.male_button.grid(row=4, column=2, sticky="w", pady=5)

        self.female_button = ctk.CTkRadioButton(self.main_frame, text="Female", variable=self.gender_var, value="Female")
        self.female_button.grid(row=5, column=2, sticky="w", pady=5)

        self.other_button = ctk.CTkRadioButton(self.main_frame, text="Other", variable=self.gender_var, value="Other")
        self.other_button.grid(row=6, column=2, sticky="w", pady=5)

         # Date of Birth
        self.dob_label = ctk.CTkLabel(self.main_frame, text="Date of Birth", font=("Helvetica", 14))
        self.dob_label.grid(row=7, column=1, sticky="w", pady=(10, 5))

        self.dob_entry = DateEntry(
            self.main_frame,
            width=27,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="dd/MM/yyyy",
            font=("Helvetica", 12)
        )
        self.dob_entry.grid(row=7, column=2, pady=(0, 10))


        # Email
        self.email_label = ctk.CTkLabel(self.main_frame, text="Email Address", font=("Helvetica", 14))
        self.email_label.grid(row=8, column=1, sticky="w", pady=(10, 5))
        self.email_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your email", width=300, font=("Helvetica", 12))
        self.email_entry.grid(row=8, column=2, pady=(0, 10))

        # Password
        self.password_label = ctk.CTkLabel(self.main_frame, text="Password", font=("Helvetica", 14))
        self.password_label.grid(row=9, column=1, sticky="w", pady=(10, 5))
        self.password_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your password", width=300, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=9, column=2, pady=(0, 20))

        # Register and Cancel Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=10)
        self.button_frame.grid(row=10, column=1, columnspan=2, pady=20)

        self.register_button = ctk.CTkButton(
            self.button_frame,
            text="Register",
            font=("Helvetica", 14, "bold"),
            fg_color="#4CAF50",
            width=150,
            command=self.register
        )
        self.register_button.grid(row=1, column=0, padx=20)

        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            font=("Helvetica", 14, "bold"),
            fg_color="#f44336",
            width=150,
            command=self.cancel
        )
        self.cancel_button.grid(row=1, column=1, padx=20)

        # Configure grid expansion
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def register(self):
        full_name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_var.get()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validation
        if not full_name:
            messagebox.showerror("Validation Error", "Full Name is required.")
            return

        if not address:
            messagebox.showerror("Validation Error", "Address is required.")
            return

        if not phone_number or not re.match(r'^\d{10}$', phone_number):
            messagebox.showerror("Validation Error", "Enter a valid 10-digit phone number.")
            return

        if gender == "None":
            messagebox.showerror("Validation Error", "Please select your gender.")
            return

        if not dob or not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
            messagebox.showerror("Validation Error", "Enter a valid DOB in the format DD/MM/YYYY.")
            return

        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Validation Error", "Enter a valid email address.")
            return

        if not password or len(password) < 6:
            messagebox.showerror("Validation Error", "Password must be at least 6 characters.")
            return

        # Create an instance of the DatabaseConnection class
        db_connection = DatabaseConnection()

        # Insert into database if validation passes
        success, message = db_connection.save_customer_data(full_name, address, phone_number, gender, dob, email, password)
        
        if success:
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Database Error", f"Error: {message}")

    def cancel(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()
