import customtkinter as ctk
from Database_Connection import DatabaseConnection  # Import the DatabaseConnection class
from pymysql import Error

# Taxi Booking System
class TaxiBookingSystem:
    def __init__(self):
        self.base_fare = 50  # Base fare (for display purposes)
        self.per_km_rate = 10  # Rate per kilometer

    def calculate_fare(self, amount):
        return amount

# Payment System
class PaymentSystem:
    def __init__(self, db_connection):
        self.payment_status = "Pending"
        self.db_connection = db_connection  # Database connection

    def make_payment(self, amount, esewa_id):
        # In a real system, you'd integrate eSewa payment gateway here
        self.payment_status = "Paid"
        payment_method = "eSewa"  # Hardcode the payment method
        booking_id = 1  # You should retrieve a real booking ID here if needed

        # Save payment details to the database
        if self.db_connection.save_payment_details(booking_id, amount, payment_method, self.payment_status):
            return f"Payment of ₹{amount} using eSewa ID {esewa_id} successful!"
        else:
            return "Failed to save payment details."

# GUI Application
class TaxiBookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Taxi Booking and Payment System")
        self.geometry("400x400")

        # Database connection from database.py
        self.db_connection = DatabaseConnection()

        # Instances of the core systems
        self.taxi_system = TaxiBookingSystem()
        self.payment_system = PaymentSystem(self.db_connection)

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # eSewa ID input
        self.esewa_label = ctk.CTkLabel(self, text="Enter eSewa ID:")
        self.esewa_label.pack(pady=10)
        self.esewa_entry = ctk.CTkEntry(self)
        self.esewa_entry.pack(pady=5)

        # Amount input by the user
        self.amount_label = ctk.CTkLabel(self, text="Enter Amount (₹):")
        self.amount_label.pack(pady=10)
        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(pady=5)

        # Pay Button
        self.pay_button = ctk.CTkButton(self, text="Make Payment", command=self.make_payment, state="normal")
        self.pay_button.pack(pady=10)

        # Payment Status
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=10)

    def make_payment(self):
        esewa_id = self.esewa_entry.get()
        amount_str = self.amount_entry.get()

        if not esewa_id:
            self.status_label.configure(text="Please enter a valid eSewa ID!")
            return

        try:
            # Convert the input amount to float
            amount = float(amount_str) if amount_str else 0.0
            if amount <= 0:
                self.status_label.configure(text="Amount must be greater than zero!")
                return
        except ValueError:
            self.status_label.configure(text="Please enter a valid amount!")
            return

        # Make the payment and save to the database
        result = self.payment_system.make_payment(amount, esewa_id)
        self.status_label.configure(text=result)
        self.pay_button.configure(state="disabled")

    def on_closing(self):
        self.db_connection.close_connection()
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Set the theme
    ctk.set_default_color_theme("blue")  # Set the color theme
    app = TaxiBookingApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)  # Close DB connection on window close
    app.mainloop()
