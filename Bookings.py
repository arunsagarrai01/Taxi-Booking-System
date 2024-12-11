import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import tkintermapview
from Database_Connection import DatabaseConnection  # Import the DatabaseConnection class

# TaxiBooking class to hold details of each booking
class TaxiBooking:
    def __init__(self, pickup_location, dropoff_location, date_time, distance, fare, pickup_coords, dropoff_coords):
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.date_time = date_time
        self.distance = distance  # in kilometers
        self.fare = fare  # calculated fare
        self.pickup_coords = pickup_coords  # Pickup coordinates
        self.dropoff_coords = dropoff_coords  # Drop-off coordinates


# Main application class
class TaxiBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taxi Booking System")
        self.root.geometry("1000x700")
        self.bookings = []

        self.markers = []

        # Set theme for CustomTkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Create Geolocator instance
        self.geolocator = Nominatim(user_agent="taxi_booking_app")

        # Create the map widget
        self.create_widgets()

        # Initialize the DatabaseConnection
        self.db = DatabaseConnection()  # Create an instance of DatabaseConnection

        # Initialize distance and fare variables
        self.distance = 0
        self.fare = 0

    def create_widgets(self):
        # Create the main frame to hold left and right sections
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        # Create the left frame for map
        self.map_frame = tk.Frame(self.main_frame, width=500, height=700)
        self.map_frame.grid(row=0, column=0, padx=20, pady=20)

        # Create the right frame for booking form
        self.form_frame = tk.Frame(self.main_frame, width=400, height=700, bg="#2E2E2E")
        self.form_frame.grid(row=0, column=1, padx=20, pady=20)

        # Create and embed the map
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=500, height=700, corner_radius=15)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(27.6839, 85.3186)  # Default position (Kathmandu)
        self.map_widget.set_zoom(12)

        # Create input fields in the right frame
        self.create_input_fields()

    def create_input_fields(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self.form_frame, text="Book Your Taxi", font=("Arial", 28, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Pickup Location Label and Entry
        self.pickup_label = ctk.CTkLabel(self.form_frame, text="Pickup Location", font=("Arial", 16))
        self.pickup_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.pickup_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter pickup location", font=("Arial", 14))
        self.pickup_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        # Drop-off Location Label and Entry
        self.dropoff_label = ctk.CTkLabel(self.form_frame, text="Drop-off Location", font=("Arial", 16))
        self.dropoff_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.dropoff_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter drop-off location", font=("Arial", 14))
        self.dropoff_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        # Date Label and Entry
        self.date_label = ctk.CTkLabel(self.form_frame, text="Date", font=("Arial", 16))
        self.date_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")
        self.date_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter date (YYYY-MM-DD)", font=("Arial", 14))
        self.date_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")

        # Time Label and Entry
        self.time_label = ctk.CTkLabel(self.form_frame, text="Time", font=("Arial", 16))
        self.time_label.grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.time_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Enter time (HH:MM)", font=("Arial", 14))
        self.time_entry.grid(row=4, column=1, padx=20, pady=10, sticky="w")

        # Distance and Fare Labels
        self.distance_label = ctk.CTkLabel(self.form_frame, text="Distance (km):", font=("Arial", 14))
        self.distance_label.grid(row=5, column=0, padx=20, pady=10, sticky="e")
        self.distance_value_label = ctk.CTkLabel(self.form_frame, text="0", font=("Arial", 14))
        self.distance_value_label.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        self.fare_label = ctk.CTkLabel(self.form_frame, text="Fare:", font=("Arial", 14))
        self.fare_label.grid(row=6, column=0, padx=20, pady=10, sticky="e")
        self.fare_value_label = ctk.CTkLabel(self.form_frame, text="0", font=("Arial", 14))
        self.fare_value_label.grid(row=6, column=1, padx=20, pady=10, sticky="w")

        # Book Button
        self.book_button = ctk.CTkButton(self.form_frame, text="Book Taxi", font=("Arial", 16, "bold"), command=self.book_taxi, fg_color="#4CAF50", hover_color="#45a049")
        self.book_button.grid(row=7, column=1, padx=20, pady=30, sticky="w")

        # Bind entries to update distance and fare when locations are filled
        self.pickup_entry.bind("<FocusOut>", self.update_distance_fare)
        self.dropoff_entry.bind("<FocusOut>", self.update_distance_fare)

        # Bind entries to enable the "Book Taxi" button only when both fields are filled
        self.pickup_entry.bind("<KeyRelease>", self.check_fields)
        self.dropoff_entry.bind("<KeyRelease>", self.check_fields)

    def check_fields(self, event=None):
        # Enable the "Book Taxi" button only if both the pickup and drop-off fields are filled
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()

        if pickup_location and dropoff_location:
            self.book_button.configure(state=tk.NORMAL)  # Enable the button
        else:
            self.book_button.configure(state=tk.DISABLED)  # Disable the button

    def update_distance_fare(self, event=None):
        # This function will update the distance and fare when both locations are provided
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()

        if pickup_location and dropoff_location:
            try:
                # Geocode the pickup and dropoff locations
                pickup_coords = self.geolocator.geocode(pickup_location)
                dropoff_coords = self.geolocator.geocode(dropoff_location)

                # Check if geocoding was successful for both locations
                if pickup_coords and dropoff_coords:
                    # Get the coordinates of both locations
                    pickup_lat = pickup_coords.latitude
                    pickup_lon = pickup_coords.longitude
                    dropoff_lat = dropoff_coords.latitude
                    dropoff_lon = dropoff_coords.longitude

                    # Calculate the distance between the two locations
                    self.distance = geodesic((pickup_lat, pickup_lon), (dropoff_lat, dropoff_lon)).kilometers

                    # Calculate fare (e.g., $1 per kilometer)
                    self.fare = round(self.distance * 40, 2)

                    # Update the UI with the calculated values
                    self.distance_value_label.configure(text=f"{self.distance:.2f}")
                    self.fare_value_label.configure(text=f"Rs{self.fare}")

                    # Update the map with the new pickup and dropoff locations
                    self.update_map(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
                else:
                    # Handle case where geocoding failed (invalid locations)
                    self.distance_value_label.configure(text="N/A")
                    self.fare_value_label.configure(text="N/A")
                    messagebox.showerror("Error", "Could not find the locations. Please check the addresses.")
            except Exception as e:
                # Handle general exceptions (e.g., network errors, other unexpected errors)
                self.distance_value_label.configure(text="Error")
                self.fare_value_label.configure(text="Error")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_map(self, pickup_lat, pickup_lon, dropoff_lat, dropoff_lon):
        try:
            # Clear the map first by deleting existing markers (if any)
            for marker in self.markers:
                self.map_widget.delete_marker(marker)  # Delete each marker in the list

            # Reset the marker list after clearing
            self.markers.clear()

            # Add new markers for pickup and dropoff locations
            pickup_marker = self.map_widget.set_marker(pickup_lat, pickup_lon, text="Pickup")
            dropoff_marker = self.map_widget.set_marker(dropoff_lat, dropoff_lon, text="Dropoff")

            # Add the new markers to the list
            self.markers.append(pickup_marker)
            self.markers.append(dropoff_marker)

            # Adjust the zoom level and center the map between the pickup and dropoff locations
            center_lat = (pickup_lat + dropoff_lat) / 2
            center_lon = (pickup_lon + dropoff_lon) / 2

            self.map_widget.set_position(center_lat, center_lon)
            self.map_widget.set_zoom(12)
        except Exception as e:
            # Handle any errors related to map updates (e.g., invalid coordinates)
            messagebox.showerror("Map Error", f"Error updating the map: {str(e)}")

    def book_taxi(self):
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()
        date_str = self.date_entry.get()  # Date part (YYYY-MM-DD)
        time_str = self.time_entry.get()  # Time part (HH:MM)

        try:
            # Parse the date and time separately
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
            date_time = datetime.combine(date, time)

            # Create taxi booking instance
            taxi_booking = TaxiBooking(pickup_location, dropoff_location, date_time, self.distance, self.fare, None, None)

            # Add the booking to the database
            self.db.insert_booking(taxi_booking)

            # Show confirmation message
            messagebox.showinfo("Booking Confirmed", f"Taxi booked from {pickup_location} to {dropoff_location} on {date_time}. Fare: ${self.fare}")
        except ValueError as e:
            messagebox.showerror("Input Error", "Please ensure all fields are correctly filled.")
