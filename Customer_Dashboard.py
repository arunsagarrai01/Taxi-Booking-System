import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Database_Connection import DatabaseConnection

class CustomerPanel:
    def __init__(self, app, customer_id):
        self.app = app
        self.customer_id = customer_id
        self.cuspanfeat = DatabaseConnection()

        self.Customer_Panel_UI()
        self.CustomerFunctions()

    def Customer_Panel_UI(self):
        # Header Label
        header = ctk.CTkLabel(self.app, text="Customer Dashboard", text_color="black", font=("Arial", 24, "bold"))
        header.pack(pady=10)

        # Content frame
        self.content_frame = ctk.CTkFrame(self.app, corner_radius=10)
        self.content_frame.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    def Customer_Profile(self):
        self.clearcontent()

        header = ctk.CTkLabel(self.content_frame, text="Profile Settings", font=("Arial", 24, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=10)

        # First Name
        ctk.CTkLabel(self.content_frame, text="Full Name:", anchor="w").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_full_name = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_full_name.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Email
        ctk.CTkLabel(self.content_frame, text="Email:", anchor="w").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_email = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_email.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Phone
        ctk.CTkLabel(self.content_frame, text="Phone Number:", anchor="w").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_phone_number = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_phone_number.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Gender
        ctk.CTkLabel(self.content_frame, text="Gender:", anchor="w").grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_gender = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_gender.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Date of Birth
        ctk.CTkLabel(self.content_frame, text="Date of Birth:", anchor="w").grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_dob = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_dob.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Address
        ctk.CTkLabel(self.content_frame, text="Address:", anchor="w").grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )
        self.entry_address = ctk.CTkEntry(self.content_frame, width=230, textvariable=ctk.StringVar())
        self.entry_address.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        # Update Profile Button
        ctk.CTkButton(
            self.content_frame, text="Update Profile", fg_color="blue", command=self.update_customer
        ).grid(row=9, column=0, columnspan=2, pady=20)

        # Get customer data from the database
        customer_data, message = self.cuspanfeat.get_customer_details_by_id(self.customer_id)

        if customer_data:
            entries = [
                self.entry_full_name, self.entry_email,
                self.entry_phone_number, self.entry_gender, self.entry_dob,
                self.entry_address
            ]

            # Populate the form with customer data
            values = [
                customer_data['full_name'], customer_data['email'],
                customer_data['phone_number'], customer_data['gender'],
                customer_data['dob'], customer_data['address']
            ]

            for entry, value in zip(entries, values):
                entry.delete(0, "end")
                entry.insert(0, value)
        else:
            CTkMessagebox(title="Error", message=message, icon="error")

    def write_report(self):
        # Clear the current content
        self.clearcontent()

        # Header for the Write Report Section
        header = ctk.CTkLabel(self.content_frame, text="Write a Report", font=("Arial", 24, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=10)

        # Report Text Area
        ctk.CTkLabel(self.content_frame, text="Report Details:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.text_report = ctk.CTkTextbox(self.content_frame, width=400, height=200)
        self.text_report.grid(row=1, column=1, padx=10, pady=5)

        # Submit Button
        ctk.CTkButton(self.content_frame, text="Submit Report", fg_color="blue", command=self.submit_report).grid(
            row=2, column=0, columnspan=2, pady=20
        )

    def submit_report(self):
        # Get the report content
        report_content = self.text_report.get("1.0", "end").strip()

        if report_content:
            # Call the method to save the report in the database
            success, message = self.cuspanfeat.submit_customer_report(self.customer_id, report_content)
            if success:
                CTkMessagebox(title="Success", message="Your report has been submitted successfully!", icon="check")
            else:
                CTkMessagebox(title="Error", message=f"Failed to submit the report: {message}", icon="error")
        else:
            CTkMessagebox(title="Error", message="Report content cannot be empty!", icon="warning")

    def CustomerFunctions(self):
        # Sidebar frame
        self.button_frame = ctk.CTkFrame(self.app, height=100, corner_radius=15)
        self.button_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Sidebar buttons (horizontally aligned)
        self.booking_button = ctk.CTkButton(self.button_frame, text="Profile", command=self.Customer_Profile, fg_color="green")
        self.booking_button.pack(pady=10, padx=10, side="left")

        self.history_button = ctk.CTkButton(self.button_frame, text="Booking History", command=self.History)
        self.history_button.pack(pady=10, padx=10, side="left")

        self.payment_button = ctk.CTkButton(self.button_frame, text="Pay Here", command=self.Pay, fg_color="brown")
        self.payment_button.pack(pady=10, padx=10, side="left")

        # Add a Book Taxi Button
        self.book_taxi_button = ctk.CTkButton(self.button_frame, text="Book a Taxi", fg_color="blue", command=self.book_taxi)
        self.book_taxi_button.pack(pady=10, padx=10, side="left")

        self.report_button = ctk.CTkButton(self.button_frame, text="Write Report", fg_color="orange", command=self.write_report)
        self.report_button.pack(pady=10, padx=10, side="left")

        self.logout_button = ctk.CTkButton(self.button_frame, text="Logout", fg_color="#DC143C", command=self.logout)
        self.logout_button.pack(pady=10, padx=10, side="right")

    def update_customer(self):
        # Get updated details from entry widgets
        updated_full_name = self.entry_full_name.get()
        updated_email = self.entry_email.get()
        updated_phone_number = self.entry_phone_number.get()
        updated_gender = self.entry_gender.get()
        updated_dob = self.entry_dob.get()
        updated_address = self.entry_address.get()

        # Update customer details in the database
        update_status, message = self.cuspanfeat.update_customer_details(
            self.customer_id, updated_full_name, updated_email, updated_phone_number,
            updated_gender, updated_dob, updated_address
        )

        if update_status:
            CTkMessagebox(title="Update Successful", message="Customer details updated successfully!", icon="check")
        else:
            CTkMessagebox(title="Update Failed", message=f"Failed to update details: {message}", icon="error")

    def book_taxi(self):
        taxi_booking_window = ctk.CTkToplevel()
        taxi_booking_window.title("Book a Taxi")
        taxi_booking_window.geometry("800x600")  # Adjust window size as needed

        from Bookings import TaxiBookingApp
        TaxiBookingApp(taxi_booking_window)
        self.clearcontent()

    def Pay(self):
        # Clear current content or perform necessary actions before launching Payment UI
        self.clearcontent()  
        from Payment import TaxiBookingApp  # Ensure the Payment interface is defined here
        payment_app = TaxiBookingApp()  # Create an instance of the payment app
        payment_app.mainloop()  # Start the main event loops

    def History(self):
        # Clear current content
        self.clearcontent()

        # Get the ride history for the customer
        ride_history, message = self.cuspanfeat.get_ride_history(self.customer_id)

        if ride_history:
            # Create a table to display the ride history
            header = ctk.CTkLabel(self.content_frame, text="Booking History", font=("Arial", 24, "bold"))
            header.grid(row=0, column=0, columnspan=7, pady=10)  # Adjusted columnspan to 7

            # Column headers for the table (removed "Driver" and "Driver Phone")
            columns = ["Booking ID", "Pickup Location", "Dropoff Location", "Date", "Time", "Fare", "Status"]
            for col_num, col_name in enumerate(columns):
                ctk.CTkLabel(self.content_frame, text=col_name, font=("Arial", 12, "bold")).grid(row=1, column=col_num, padx=10, pady=5)

            # Populate the table with ride history data
            for row_num, ride in enumerate(ride_history, start=2):
                ctk.CTkLabel(self.content_frame, text=ride['booking_id']).grid(row=row_num, column=0, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['pickup_location']).grid(row=row_num, column=1, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['dropoff_location']).grid(row=row_num, column=2, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['date']).grid(row=row_num, column=3, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['Dtime']).grid(row=row_num, column=4, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['fare']).grid(row=row_num, column=5, padx=10, pady=5)
                ctk.CTkLabel(self.content_frame, text=ride['status']).grid(row=row_num, column=6, padx=10, pady=5)  # Display status

        else:
            CTkMessagebox(title="No History", message=message, icon="info")



    def logout(self):
        self.clearcontent()
        self.app.destroy()
        self.show_login_screen()
        

    def show_login_screen(self):
        from Index_Page import IndexPage
        app =  IndexPage()
        app.mainloop()

        
    def clearcontent(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

