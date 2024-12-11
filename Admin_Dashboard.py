import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import subprocess
from Database_Connection import DatabaseConnection  # Import the fetch_bookings function

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Taxi Booking System")
        self.root.geometry("800x600")  # Increased size for the table
        ctk.set_appearance_mode("Light")  # Set the appearance mode
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self.root, text="Admin Dashboard", font=("Arial", 20), pady=10)
        self.title_label.pack(pady=(10, 20))  # Title centered with padding

        button_frame = ctk.CTkFrame(self.root, height=100, corner_radius=15)
        button_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Buttons for features (arranged horizontally in the frame using pack)
        self.assign_button = ctk.CTkButton(button_frame, text="Assign Trip", width=20, height=2, command=self.assign_trip, fg_color="#4CAF50", hover_color="#45a049")
        self.assign_button.pack(pady=10, padx=10, side="left")

        self.view_passenger_button = ctk.CTkButton(button_frame, text="View Customers", width=20, height=2, command=self.view_passengers, fg_color="#2196F3", hover_color="#1e88e5")
        self.view_passenger_button.pack(pady=10, padx=10, side="left")

        self.view_driver_button = ctk.CTkButton(button_frame, text="View Drivers", width=20, height=2, command=self.view_drivers, fg_color="#FF9800", hover_color="#f57c00")
        self.view_driver_button.pack(pady=10, padx=10, side="left")

        self.view_report_button = ctk.CTkButton(button_frame, text="View Report", width=20, height=2, command=self.view_report, fg_color="#FF5722", hover_color="#e64a19")
        self.view_report_button.pack(pady=10, padx=10, side="left")

        # Register Driver button next to View Report
        self.register_driver_button = ctk.CTkButton(button_frame, text="Register Driver", width=20, height=2, command=self.register_driver, fg_color="#8E24AA", hover_color="#7b1fa2")
        self.register_driver_button.pack(pady=10, padx=10, side="left")

        # Logout button at the bottom (outside the frame)
        self.logout_button = ctk.CTkButton(button_frame, text="Logout", width=20, height=2, command=self.logout, fg_color="#F44336", hover_color="#d32f2f")
        self.logout_button.pack(pady=10, padx=10, side="right")


        # Create the Treeview (table) to display bookings
        self.treeview = ttk.Treeview(self.root, columns=("Booking ID", "Customer ID", "Driver ID", "Pickup Location", "Dropoff Location", "Date", "Time", "Distance", "Fare"), show="headings")
        self.treeview.pack(pady=10, padx=10, fill="both", expand=True)

        # Define column headings


    def clear_treeview(self):
        """Clear the contents of the Treeview before displaying new data."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
    
    def assign_trip(self):
        self.clear_treeview()  # Clear previous content

        self.treeview["columns"] = (
            "Booking ID", "Customer ID", "Driver ID", "Pickup Location", "Dropoff Location",
            "Date", "Time", "Distance", "Fare", "Status"  # Include 'Status' here
        )
        # Define the columns including 'Status'
        self.treeview.heading("Booking ID", text="Booking ID")
        self.treeview.heading("Customer ID", text="Customer ID")
        self.treeview.heading("Driver ID", text="Driver ID")
        self.treeview.heading("Pickup Location", text="Pickup Location")
        self.treeview.heading("Dropoff Location", text="Dropoff Location")
        self.treeview.heading("Date", text="Date")
        self.treeview.heading("Time", text="Time")
        self.treeview.heading("Distance", text="Distance (km)")
        self.treeview.heading("Fare", text="Fare ($)")
        self.treeview.heading("Status", text="Status") 

        self.display_bookings()

        # Add the 'Assign Driver' button below the Treeview
        assign_button = ctk.CTkButton(self.root, text="Assign Driver", command=self.assign_driver)
        assign_button.pack()

    def display_bookings(self):
        """Fetch and display all bookings in the Treeview."""
        db = DatabaseConnection()  # Create a connection instance
        bookings = db.fetch_bookings()  # Fetch all bookings from the database

        # Fetch available drivers from the database
        available_drivers = db.fetch_available_drivers()  # This gets all available drivers

        # Insert each booking into the Treeview
        for booking in bookings:
            # Get the status value, defaulting to "Pending" if no status is provided
            status = booking.get("status", "Pending")  

            # Insert the row with the status
            self.treeview.insert(
                "", "end",
                values=(
                    booking["booking_id"],
                    booking["customer_id"],
                    booking["pickup_location"],
                    booking["dropoff_location"],
                    booking["date"],
                    booking["Dtime"],
                    booking["distance"],
                    booking["fare"],
                    status  # Adding status value to the row
                )
            )

    def assign_driver(self):
        """Handle assigning a driver to a selected booking."""
        selected_item = self.treeview.selection()  # Get the selected booking from the Treeview
        
        if not selected_item:
            ctk.CTkMessagebox.showwarning("No Selection", "Please select a booking to assign a driver.")
            return

        # Get the booking ID of the selected booking
        booking_id = self.treeview.item(selected_item, "values")[0]
        
        # Open a dialog or input box to select a driver
        driver_id = self.select_driver()  # Assume a method to get the driver ID from the admin
        
        if driver_id is None:
            ctk.CTkMessagebox.showwarning("No Driver", "Please select a driver.")
            return
        
        # Update the database to assign the driver and change the status
        db = DatabaseConnection()
        success = db.assign_driver_to_booking(booking_id, driver_id)

        if success:
            # Update the Treeview to reflect the new status and driver assignment
            self.treeview.item(selected_item, values=(  # Update selected row in the Treeview
                self.treeview.item(selected_item, "values")[0],  # Booking ID
                self.treeview.item(selected_item, "values")[1],  # Customer ID
                driver_id,  # New Driver ID
                self.treeview.item(selected_item, "values")[3],  # Pickup Location
                self.treeview.item(selected_item, "values")[4],  # Dropoff Location
                self.treeview.item(selected_item, "values")[5],  # Date
                self.treeview.item(selected_item, "values")[6],  # Time
                self.treeview.item(selected_item, "values")[7],  # Distance
                self.treeview.item(selected_item, "values")[8],  # Fare
                "Assigned"  # Status is updated to 'Assigned'
            ))
            messagebox.showinfo("Success", f"Driver {driver_id} assigned to booking {booking_id}.")
        else:
            messagebox.showerror("Error", "Failed to assign driver to booking.")

    def select_driver(self):
        """Show a dialog to select a driver."""
        import customtkinter as ctk
        from tkinter import messagebox

        db = DatabaseConnection()
        # Fetch all available drivers from the database
        drivers = db.fetch_available_drivers()

        if not drivers:
            # Use messagebox.showwarning if no drivers are available
            messagebox.showwarning("No Drivers", "There are no drivers available.")
            return None

        # Prepare driver options list
        driver_options = [f"{driver['driver_id']} - {driver['full_name']}" for driver in drivers]

        # Show the input dialog with the list of available drivers
        dialog_text = "Select a driver:\n" + "\n".join(driver_options)
        driver_selection_dialog = ctk.CTkInputDialog(
            title="Select Driver", 
            text=dialog_text
        )

        # Wait for the user to make a selection, then get the result
        driver_selection = driver_selection_dialog.get_input()  # Ensure the correct method is used to get user input

        if driver_selection:
            # Validate and extract the driver_id from the selected option
            try:
                driver_id = driver_selection.split(" - ")[0]
                return driver_id
            except IndexError:
                messagebox.showerror("Invalid Selection", "Invalid driver selection format.")
                return None

        # If no selection was made, return None
        return None







    def view_passengers(self):
        """Fetch and display all customers in the Treeview."""
        self.clear_treeview()  # Clear previous content

        # Create a connection instance
        db = DatabaseConnection()
        customers = db.fetch_customers()  # Fetch all customers from the database

        # Check if any customers were returned
        if not customers:
            messagebox.showinfo("No Data", "No customers found.")
            return

        # Define column headings for customer data
        self.treeview["columns"] = ("Customer ID", "Full Name", "Phone Number", "Gender", "DOB", "Email", "Address")
        self.treeview["show"] = "headings"

        # Set headings for customer data
        self.treeview.heading("Customer ID", text="Customer ID")
        self.treeview.heading("Full Name", text="Full Name")
        self.treeview.heading("Phone Number", text="Phone Number")
        self.treeview.heading("Gender", text="Gender")
        self.treeview.heading("DOB", text="Date of Birth")
        self.treeview.heading("Email", text="Email")
        self.treeview.heading("Address", text="Address")

        # Insert each customer into the Treeview
        for customer in customers:
            self.treeview.insert(
                "", "end",
                values=(
                    customer["customer_id"],
                    customer["full_name"],
                    customer["phone_number"],
                    customer["gender"],
                    customer["dob"],
                    customer["email"],
                    customer["address"]
                )
            )

    def view_drivers(self):
        """Fetch and display all drivers in the Treeview."""
        # Clear previous content
        self.clear_treeview()

        # Create a connection instance
        db = DatabaseConnection()
        drivers = db.fetch_drivers()  # Fetch all drivers from the database

        # Check if any drivers were returned
        if not drivers:
            messagebox.showinfo("No Data", "No drivers found.")
            return

        # Define column headings for driver data
        self.treeview["columns"] = ("Driver ID", "Full Name", "Phone Number", "License Number", "Vehicle", "Registration Number")
        self.treeview["show"] = "headings"

        # Set headings for driver data
        self.treeview.heading("Driver ID", text="Driver ID")
        self.treeview.heading("Full Name", text="Full Name")
        self.treeview.heading("Phone Number", text="Phone Number")
        self.treeview.heading("License Number", text="License Number")
        self.treeview.heading("Vehicle", text="Vehicle")
        self.treeview.heading("Registration Number", text="Registration Number")

        # Insert each driver into the Treeview
        for driver in drivers:
            self.treeview.insert(
                "", "end",
                values=(
                    driver["driver_id"],
                    driver["full_name"],
                    driver["phone_number"],
                    driver["license_number"],
                    driver["vehicle_model"],
                    driver["vehicle_registration_number"]
                )
            )

        # Add a Delete button below the Treeview
        delete_button = ctk.CTkButton(self.root, text="Delete", command=self.delete_driver)
        delete_button.pack(pady=10)

    def delete_driver(self):
        """Delete the selected driver."""
        selected_item = self.treeview.selection()  # Get the selected item
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a driver to delete.")
            return

        # Get the driver ID from the selected row
        values = self.treeview.item(selected_item, "values")
        driver_id = values[0] if values else None

        if driver_id:
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete driver ID {driver_id}?")
            if confirm:
                db = DatabaseConnection()
                success = db.delete_driver(driver_id)  # Delete the driver from the database
                if success:
                    messagebox.showinfo("Success", f"Driver ID {driver_id} has been deleted.")
                    self.treeview.delete(selected_item)  # Remove the item from the Treeview
                else:
                    messagebox.showerror("Error", "Failed to delete the driver. Please try again.")

    def clear_treeview(self):
        """Clear all items from the Treeview."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)


    def register_driver(self):
        from Driver_Registration_Page import DriverRegistrationPage
        app = DriverRegistrationPage()
        app.mainloop()

    def view_report(self):
        from View_Report import AdminReportViewer
        # Create a new top-level window
        report_window = ctk.CTk()  # This is a new window for the report viewer
        AdminReportViewer(report_window)  # Pass the new window to AdminReportViewer
        report_window.mainloop()  # Start the main loop for this window



    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            self.root.destroy()
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()

