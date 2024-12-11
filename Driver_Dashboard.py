import customtkinter as ctk
from tkinter import messagebox
from Database_Connection import DatabaseConnection

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


        # Logout Button
        logout_button = ctk.CTkButton(self.root, text="Logout", font=("Arial", 14), width=200, command=self.logout, fg_color="#F44336", hover_color="#d32f2f")
        logout_button.pack(pady=20)

    def clearcontent(self):
        # This function clears the content on the screen (you might want to implement it)
        for widget in self.root.winfo_children():
            widget.destroy()

    def view_profile(self):
        self.clearcontent()

        # Header Label
        header = ctk.CTkLabel(self.root, text="Driver Profile Settings", font=("Arial", 24, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=10)

        # Full Name
        ctk.CTkLabel(self.root, text="Full Name:", anchor="w").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_full_name = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_full_name.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Email
        ctk.CTkLabel(self.root, text="Email:", anchor="w").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_email = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_email.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Phone Number
        ctk.CTkLabel(self.root, text="Phone Number:", anchor="w").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_phone_number = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_phone_number.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Gender
        ctk.CTkLabel(self.root, text="Gender:", anchor="w").grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_gender = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_gender.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Date of Birth
        ctk.CTkLabel(self.root, text="Date of Birth:", anchor="w").grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_dob = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_dob.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # License Number
        ctk.CTkLabel(self.root, text="License Number:", anchor="w").grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_license_number = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_license_number.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Address
        ctk.CTkLabel(self.root, text="Address:", anchor="w").grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_address = ctk.CTkEntry(self.root, width=230, textvariable=ctk.StringVar())
        self.entry_address.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        # Update Profile Button
        ctk.CTkButton(
            self.root, text="Update Profile", fg_color="blue", command=self.update_driver
        ).grid(row=9, column=0, columnspan=2, pady=20)

        ctk.CTkButton(
            self.root, text="Cancel", fg_color="red", command=self.go_to_dashboard
        ).grid(row=9, column=1, pady=20, sticky="e", padx=10)
        # Get driver data from the database
        db = DatabaseConnection()
        driver_data, message = db.get_driver_data(self.driver_id)

        if driver_data:
            # Set the fields using the returned dictionary
            self.entry_full_name.delete(0, "end")
            self.entry_full_name.insert(0, driver_data['full_name'])

            self.entry_email.delete(0, "end")
            self.entry_email.insert(0, driver_data['email'])

            self.entry_phone_number.delete(0, "end")
            self.entry_phone_number.insert(0, driver_data['phone_number'])

            self.entry_gender.delete(0, "end")
            self.entry_gender.insert(0, driver_data['gender'])

            self.entry_dob.delete(0, "end")
            self.entry_dob.insert(0, driver_data['dob'])

            self.entry_license_number.delete(0, "end")
            self.entry_license_number.insert(0, driver_data['license_number'])

            self.entry_address.delete(0, "end")
            self.entry_address.insert(0, driver_data['address'])

        else:
            messagebox.showerror("Error", message)

    def update_driver(self):
        # Get updated driver data from the form
        updated_info = {
            "full_name": self.entry_full_name.get(),
            "email": self.entry_email.get(),
            "phone_number": self.entry_phone_number.get(),
            "gender": self.entry_gender.get(),
            "dob": self.entry_dob.get(),
            "license_number": self.entry_license_number.get(),
            "address": self.entry_address.get()
        }

        db = DatabaseConnection()

        # Pass the updated_info dictionary directly to the method
        success, message = db.update_driver_details(
            self.driver_id,  # Ensure driver_id is correctly passed
            updated_info["full_name"], 
            updated_info["email"], 
            updated_info["phone_number"], 
            updated_info["gender"], 
            updated_info["dob"], 
            updated_info["license_number"], 
            updated_info["address"]
        )

        # Display success or error message
        if success:
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.go_to_dashboard()
        else:
            messagebox.showerror("Error", message)
        
    def view_bookings(self):
        self.clearcontent()

        # Get the ride history for the driver
        db = DatabaseConnection()
        ride_history, message = db.get_ride_history(self.driver_id)

        if ride_history:
            # Create a table to display the ride history
            header = ctk.CTkLabel(self.root, text="Assigned Trips", font=("Arial", 24, "bold"))
            header.grid(row=0, column=0, columnspan=7, pady=10)

            # Column headers for the table, including "Status"
            columns = ["Booking ID", "Pickup Location", "Dropoff Location", "Date", "Time", "Fare", "Status", "Actions"]
            for col_num, col_name in enumerate(columns):
                ctk.CTkLabel(self.root, text=col_name, font=("Arial", 12, "bold")).grid(row=1, column=col_num, padx=10, pady=5)

            # Populate the table with ride history data
            for row_num, ride in enumerate(ride_history, start=2):
                ctk.CTkLabel(self.root, text=ride['booking_id']).grid(row=row_num, column=0, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=ride['pickup_location']).grid(row=row_num, column=1, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=ride['dropoff_location']).grid(row=row_num, column=2, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=ride['date']).grid(row=row_num, column=3, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=ride['Dtime']).grid(row=row_num, column=4, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=ride['fare']).grid(row=row_num, column=5, padx=10, pady=5)
                
                ctk.CTkLabel(self.root, text=ride['status']).grid(row=row_num, column=6, padx=10, pady=5)

                # "Mark as Done" Button
                mark_done_button = ctk.CTkButton(
                    self.root,
                    text="Mark as Done",
                    command=lambda ride_id=ride['booking_id'], status_label=status_label: db.mark_as_done(ride_id, status_label)
                )
                mark_done_button.grid(row=row_num, column=7, padx=10, pady=5)

            # Back button to navigate to the dashboard
            back_button = ctk.CTkButton(self.root, text="Back", command=self.go_to_dashboard)
            back_button.grid(row=row_num + 1, column=0, columnspan=8, pady=20)
        else:
            messagebox.showinfo("No History", message)

    def view_payment_history(self):
        self.clearcontent()

        # Fetch the payment history for the driver
        db = DatabaseConnection()
        payment_history, message = db.get_payment_history(self.driver_id)

        if payment_history:
            # Create a table to display the payment history
            header = ctk.CTkLabel(self.root, text="Payment History", font=("Arial", 24, "bold"))
            header.grid(row=0, column=0, columnspan=6, pady=10)

            # Column headers for the table
            columns = ["Payment ID", "Date", "Amount", "Payment Method", "Status"]
            for col_num, col_name in enumerate(columns):
                ctk.CTkLabel(self.root, text=col_name, font=("Arial", 12, "bold")).grid(row=1, column=col_num, padx=10, pady=5)

            # Populate the table with payment history data
            for row_num, payment in enumerate(payment_history, start=2):
                ctk.CTkLabel(self.root, text=payment['payment_id']).grid(row=row_num, column=0, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=payment['date']).grid(row=row_num, column=1, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=payment['amount']).grid(row=row_num, column=2, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=payment['payment_method']).grid(row=row_num, column=3, padx=10, pady=5)
                ctk.CTkLabel(self.root, text=payment['status']).grid(row=row_num, column=4, padx=10, pady=5)
                back_button = ctk.CTkButton(self.root, text="Back", command=self.go_to_dashboard)
                back_button.grid(row=row_num + 1, column=0, columnspan=6, pady=20)
        else:
            messagebox.showinfo("No History", message)

    def go_to_dashboard(self):
        # Close current profile view
        self.root.destroy()  # Close the current window

        # Reopen the Driver Dashboard
        from Driver_Dashboard import DriverDashboard  # Import your dashboard
        taxi = ctk.CTk()  # Create a new window for Driver Dashboard
        app = DriverDashboard(taxi, self.driver_name, self.driver_id)  # Pass driver_name and driver_id
        taxi.mainloop()  # Start the dashboard

    def show_popup(self, title, message):
        # Simple pop-up window to display information
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("400x200")
        label = ctk.CTkLabel(popup, text=message, font=("Arial", 12))
        label.pack(pady=50)
        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=20)

    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            self.root.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()
