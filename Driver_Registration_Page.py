import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry  # Import for calendar widget
import re  # For email and phone number validation
from Database_Connection import DatabaseConnection  # Import the class

class DriverRegistrationPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Driver Registration")
        self.geometry("700x900")
        self.configure(bg="#f2f2f2")

        # Set appearance mode
        ctk.set_appearance_mode("System")  # or "Dark" or "Light"
        ctk.set_default_color_theme("blue")

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Driver Registration",
            font=("Helvetica", 24, "bold"),
            text_color="#333333"
        )
        self.title_label.grid(row=0, column=0, pady=(10, 30), columnspan=2)

        # Full Name
        self.create_label_and_entry("Full Name", 1)
        self.name_entry = self.create_entry(1)

        # Address
        self.create_label_and_entry("Address", 2)
        self.address_entry = self.create_entry(2)

        # Phone Number
        self.create_label_and_entry("Phone Number", 3)
        self.phone_entry = self.create_entry(3)

        # Gender
        self.gender_label = ctk.CTkLabel(self.main_frame, text="Gender", font=("Helvetica", 14))
        self.gender_label.grid(row=4, column=0, sticky="w", pady=(10, 5))
        self.gender_var = ctk.StringVar(value="Male")

        self.male_button = ctk.CTkRadioButton(self.main_frame, text="Male", variable=self.gender_var, value="Male")
        self.male_button.grid(row=4, column=1, sticky="w", pady=5)

        self.female_button = ctk.CTkRadioButton(self.main_frame, text="Female", variable=self.gender_var, value="Female")
        self.female_button.grid(row=5, column=1, sticky="w", pady=5)

        self.other_button = ctk.CTkRadioButton(self.main_frame, text="Other", variable=self.gender_var, value="Other")
        self.other_button.grid(row=6, column=1, sticky="w", pady=5)

        # Date of Birth
        self.create_label("Date of Birth", 7)
        self.dob_entry = DateEntry(
            self.main_frame,
            width=20,
            background='darkblue',
            foreground='white',
            date_pattern='dd/MM/yyyy',
            font=("Helvetica", 12)
        )
        self.dob_entry.grid(row=7, column=1, pady=(0, 10))

        # Email
        self.create_label_and_entry("Email Address", 8)
        self.email_entry = self.create_entry(8)

        # Password
        self.create_label_and_entry("Password", 9)
        self.password_entry = self.create_entry(9, show="*")

        # Vehicle Model
        self.create_label_and_entry("Vehicle Model", 10)
        self.vehicle_model_entry = self.create_entry(10)

        # Vehicle Registration Number
        self.create_label_and_entry("Vehicle Registration Number", 11)
        self.vehicle_reg_entry = self.create_entry(11)

        # License Number
        self.create_label_and_entry("License Number", 12)
        self.license_number_entry = self.create_entry(12)

        # Register and Cancel Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=10)
        self.button_frame.grid(row=13, column=0, columnspan=2, pady=20)

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

    def create_label_and_entry(self, label_text, row):
        label = ctk.CTkLabel(self.main_frame, text=label_text, font=("Helvetica", 14))
        label.grid(row=row, column=0, sticky="w", pady=(10, 5))

    def create_label(self, label_text, row):
        label = ctk.CTkLabel(self.main_frame, text=label_text, font=("Helvetica", 14))
        label.grid(row=row, column=0, sticky="w", pady=(10, 5))

    def create_entry(self, row, **kwargs):
        entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter here", width=300, font=("Helvetica", 12), **kwargs)
        entry.grid(row=row, column=1, pady=(0, 10))
        return entry

    def register(self):
        full_name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        gender = self.gender_var.get()
        dob = self.dob_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        vehicle_model = self.vehicle_model_entry.get().strip()
        vehicle_reg_number = self.vehicle_reg_entry.get().strip()
        license_number = self.license_number_entry.get().strip()

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

        if not dob:
            messagebox.showerror("Validation Error", "Date of Birth is required.")
            return

        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror("Validation Error", "Enter a valid email address.")
            return

        if not password or len(password) < 6:
            messagebox.showerror("Validation Error", "Password must be at least 6 characters.")
            return

        if not vehicle_reg_number.isdigit():
            messagebox.showerror("Validation Error", "Vehicle Registration Number must be numeric.")
            return

        if not license_number.isdigit():
            messagebox.showerror("Validation Error", "License Number must be numeric.")
            return

        try:
            # Create an instance of the DatabaseConnection class
            db_connection = DatabaseConnection()

            # Insert into the database if validation passes
            success, message = db_connection.insert_driver(
                full_name, address, phone_number, gender, dob, email, password, vehicle_model, vehicle_reg_number, license_number
            )

            if success:
                messagebox.showinfo("Success", "Driver registration successful!")
            else:
                messagebox.showerror("Database Error", f"Error: {message}")

        except Exception as e:
            # Handle any unforeseen exceptions during database interaction
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def cancel(self):
        self.destroy()
