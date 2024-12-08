import customtkinter as ctk
from tkinter import messagebox

class DriverDashboard:
    def __init__(self, root, driver_name, driver_id):
        self.root = root
        self.driver_name = driver_name
        self.driver_id = driver_id

        # Set window title and size
        self.root.title(f"Driver Dashboard - {self.driver_name}")
        self.root.geometry("600x400")
        ctk.set_appearance_mode("Light")  # Set the appearance mode (Light or Dark)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Heading label
        label = ctk.CTkLabel(self.root, text=f"Welcome, {self.driver_name}!", font=("Arial", 18))
        label.pack(pady=20)

        # View Profile Button
        view_profile_button = ctk.CTkButton(self.root, text="View Profile", font=("Arial", 14), width=200, command=self.view_profile, fg_color="#4CAF50", hover_color="#45a049")
        view_profile_button.pack(pady=10)

        # View Bookings Button
        view_bookings_button = ctk.CTkButton(self.root, text="View Bookings", font=("Arial", 14), width=200, command=self.view_bookings, fg_color="#2196F3", hover_color="#1e88e5")
        view_bookings_button.pack(pady=10)

        # Payment History Button
        payment_history_button = ctk.CTkButton(self.root, text="Payment History", font=("Arial", 14), width=200, command=self.view_payment_history, fg_color="#FF5722", hover_color="#e64a19")
        payment_history_button.pack(pady=10)

        # Earnings Button
        earnings_button = ctk.CTkButton(self.root, text="View Earnings", font=("Arial", 14), width=200, command=self.view_earnings, fg_color="#FFC107", hover_color="#ffb300")
        earnings_button.pack(pady=10)

        # Logout Button
        logout_button = ctk.CTkButton(self.root, text="Logout", font=("Arial", 14), width=200, command=self.logout, fg_color="#F44336", hover_color="#d32f2f")
        logout_button.pack(pady=20)

    def view_profile(self):
        # Placeholder for profile information
        profile_info = f"Driver ID: {self.driver_id}\nName: {self.driver_name}\nEmail: driver@example.com"
        self.show_popup("Profile Information", profile_info)

    def view_bookings(self):
        # Placeholder for booking data
        bookings_info = "Booking 1: Pickup - Location A, Drop-off - Location B\nBooking 2: Pickup - Location C, Drop-off - Location D"
        self.show_popup("Booking History", bookings_info)

    def view_payment_history(self):
        # Placeholder for payment history
        payment_history_info = "Payment 1: $50\nPayment 2: $70\nPayment 3: $60"
        self.show_popup("Payment History", payment_history_info)

    def view_earnings(self):
        # Placeholder for earnings data
        earnings_info = "Total Earnings: $180"
        self.show_popup("Earnings", earnings_info)

    def show_popup(self, title, message):
        # Simple pop-up window to display information
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 12))
        label.pack(pady=20)
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy, fg_color="#4CAF50", hover_color="#45a049")
        close_button.pack(pady=10)

    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            self.root.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    driver_name = "John Doe"  # Example driver name
    driver_id = 12345  # Example driver ID
    dashboard = DriverDashboard(root, driver_name, driver_id)

    # Run the main loop
    root.mainloop()
