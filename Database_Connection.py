import pymysql
from pymysql import Error

class DatabaseConnection:
    def __init__(self):
        try:
            # Initialize the database connection using PyMySQL
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='sagar@g66',
                database='Taxi_Booking_System'
            )
            print("Database connected successfully")
        except Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def _execute_query(self, query, values):
        if self.connection is None:
            print("No database connection.")
            return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False

    def save_customer_data(self, full_name, address, phone_number, gender, dob, email, password):
        if self.connection is None:
            print("No database connection.")
            return False, "No database connection."

        try:
            query = """
            INSERT INTO customers (full_name, address, phone_number, gender, dob, email, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (full_name, address, phone_number, gender, dob, email, password)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True, "Customer data saved successfully."
        except Error as e:
            print(f"Error saving customer data: {e}")
            return False, str(e)

    def update_customer_password(self, email, new_password):
        """
        Update the password of the customer with the given email.

        :param email: The email of the customer whose password is to be updated.
        :param new_password: The new password to be set for the customer.
        :return: A tuple (success, message)
        """
        if self.connection is None:
            return False, "No database connection."

        try:
            query = """
            UPDATE customers
            SET password = %s
            WHERE email = %s
            """
            values = (new_password, email)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()

            return True, "Password updated successfully."
        except Error as e:
            print(f"Error updating password: {e}")
            return False, str(e)

    def get_payment_history(self, customer_id):
        """
        Retrieve the payment history for a specific customer, including booking details.

        :param customer_id: The ID of the customer whose payment history is being fetched.
        :return: A list of payment records (or empty list if no history) and a message.
        """
        if self.connection is None:
            return [], "No database connection."

        try:
            query = """
            SELECT 
                p.payment_id, p.amount, p.payment_method, p.payment_status, p.created_at, 
                b.booking_id, b.pickup_location, b.dropoff_location, b.date, b.Dtime 
            FROM 
                payments p
            JOIN 
                bookings b ON p.booking_id = b.booking_id
            WHERE 
                b.customer_id = %s
            ORDER BY p.created_at DESC
            """
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (customer_id,))
            result = cursor.fetchall()
            cursor.close()

            if result:
                return result, "Payment history retrieved successfully."
            else:
                return [], "No payment history found."
        except Error as e:
            print(f"Error retrieving payment history: {e}")
            return [], str(e)

    def get_ride_history(self, customer_id):
        """
        Retrieve all bookings for a customer, including booking details and driver information.
        
        :param customer_id: The ID of the customer whose ride history is being fetched.
        :return: A list of booking records (or empty list if no history) and a message.
        """
        if self.connection is None:
            return [], "No database connection."

        try:
            query = """
            SELECT 
                b.booking_id, b.pickup_location, b.dropoff_location, b.date, b.Dtime, 
                b.distance, b.fare, b.status  -- Removed driver information
            FROM 
                bookings b
            WHERE 
                b.customer_id = %s
            ORDER BY b.date DESC, b.Dtime DESC
            """
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (customer_id,))
            result = cursor.fetchall()
            cursor.close()

            if result:
                return result, "Ride history retrieved successfully."
            else:
                return [], "No ride history found."
        except Error as e:
            print(f"Error retrieving ride history: {e}")
            return [], str(e)

    def get_available_drivers(self):
        try:
            # Query to fetch available drivers
            cursor = self.conn.cursor()
            cursor.execute("SELECT driver_id, driver_name, latitude, longitude FROM drivers WHERE status = 'available'")
            drivers = cursor.fetchall()

            # Convert rows into a list of dictionaries
            drivers_list = [{'driver_id': driver[0], 'driver_name': driver[1], 'latitude': driver[2], 'longitude': driver[3]} for driver in drivers]
            return drivers_list
        except Exception as e:
            print(f"Error fetching drivers: {str(e)}")
            return []

    def get_customer_details_by_id(self, customer_id):
        """
        Retrieve customer details from the database using the customer ID.
        """
        if self.connection is None:
            print("No database connection.")
            return None, "No database connection."

        try:
            query = """
            SELECT 
                full_name, address, phone_number, gender, dob, email 
            FROM 
                customers 
            WHERE 
                customer_id = %s
            """
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result, "Customer details retrieved successfully."
            else:
                print(f"No customer found with ID {customer_id}")
                return None, f"No customer found with ID {customer_id}"
        except Error as e:
            print(f"Error retrieving customer details: {e}")
            return None, str(e)
    
    def fetch_query(self, query, values=None):
        """
        Fetch data from the database using a SELECT query.

        :param query: The SQL query string to execute.
        :param values: Optional tuple of values to execute the query with (default is None).
        :return: List of records fetched from the database, or an empty list if no records are found.
        """
        if self.connection is None:
            print("No database connection.")
            return []

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # Using DictCursor to get results as dictionaries
            cursor.execute(query, values or ())  # Use empty tuple if no values
            result = cursor.fetchall()  # Fetch all results
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching query: {e}")
            return []


    def validate_driver(self, email, password):
        """
        Validate the driver's credentials during login.

        :param email: The email of the driver.
        :param password: The password of the driver.
        :return: A tuple (success, message) indicating whether the login was successful.
        """
        if self.connection is None:
            return False, "No database connection."

        try:
            # Updated query to select both driver_id and full_name
            query = "SELECT driver_id, full_name FROM drivers WHERE email = %s AND password = %s"
            values = (email, password)
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()

            if result:
                driver_id = result['driver_id']
                driver_name = result['full_name']  # Extract full_name
                return True, {'driver_id': driver_id, 'full_name': driver_name}  # Return both driver_id and full_name as a dictionary
            else:
                return False, "Invalid email or password."
        except Error as e:
            print(f"Error validating driver: {e}")
            return False, str(e)


    def update_customer_details(self, customer_id, full_name, email, phone_number, gender, dob, address):
        if self.connection is None:
            return False, "No database connection."

        try:
            query = """
            UPDATE customers
            SET full_name = %s, email = %s, phone_number = %s, gender = %s, dob = %s, address = %s
            WHERE customer_id = %s
            """
            values = (full_name, email, phone_number, gender, dob, address, customer_id)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()

            return True, "Customer details updated successfully."
        except pymysql.MySQLError as e:
            print(f"Error updating customer details: {e}")
            return False, str(e)

    def get_driver_data(self, driver_id):
        """Fetch driver data from MySQL database using pymysql."""
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT * FROM drivers WHERE driver_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (driver_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return {
                    'driver_id': result['driver_id'],
                    'full_name': result['full_name'],
                    'email': result['email'],
                    'phone_number': result['phone_number'],
                    'gender': result['gender'],
                    'dob': result['dob'],
                    'license_number': result['license_number'],
                    'address': result['address']
                }, "Driver data retrieved successfully."
            else:
                return None, f"No driver found with ID {driver_id}"

        except Error as e:
            print(f"Error retrieving driver data: {e}")
            return None, str(e)

    def validate_admin(self, email, password):
        """
        Validate the admin's credentials during login.

        :param email: The email of the admin.
        :param password: The password of the admin.
        :return: A tuple (success, message) indicating whether the login was successful.
        """
        if self.connection is None:
            return False, "No database connection."

        try:
            query = "SELECT * FROM admin WHERE email = %s AND password = %s"
            values = (email, password)
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
            if result:
                return True, "Admin login successful."
            else:
                return False, "Invalid email or password."
        except Error as e:
            print(f"Error validating admin: {e}")
            return False, str(e)

    def delete_driver(self, driver_id):
        """Delete a driver from the drivers table by driver_id."""
        if self.connection is None:
            print("No database connection.")
            return False

        try:
            cursor = self.connection.cursor()  # Regular cursor for executing the query
            query = "DELETE FROM drivers WHERE driver_id = %s"
            cursor.execute(query, (driver_id,))
            self.connection.commit()  # Commit the changes to the database
            cursor.close()
            print(f"Driver with ID {driver_id} deleted successfully.")
            return True
        except Error as err:
            print(f"Error deleting driver: {err}")
            return False


    def fetch_drivers(self):
        """Fetch all drivers from the drivers table."""
        if self.connection is None:
            print("No database connection.")
            return []

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # Using DictCursor for dictionary results
            query = "SELECT driver_id, full_name, phone_number, license_number, vehicle_model, vehicle_registration_number FROM drivers"
            cursor.execute(query)
            drivers = cursor.fetchall()
            cursor.close()
            return drivers
        except Error as err:
            print(f"Error fetching drivers: {err}")
            return []

    def fetch_available_drivers(self):
        """Fetch available drivers from the drivers table."""
        if self.connection is None:
            print("No database connection.")
            return []

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # Using DictCursor to get results as dictionaries
            # SQL query to fetch drivers who are available (assuming 'status' field in the driver table indicates availability)
            query = """
                SELECT driver_id, full_name, status
                FROM drivers
                WHERE status = 'Available'
            """
            cursor.execute(query)
            available_drivers = cursor.fetchall()
            cursor.close()
            return available_drivers  # Return the list of available drivers

        except Error as err:
            print(f"Error fetching available drivers: {err}")
            return []

    def assign_driver_to_booking(self, booking_id, driver_id):
        """Assign a driver to a booking and update its status."""
        if self.connection is None:
            print("No database connection.")
            return False

        try:
            cursor = self.connection.cursor()
            # SQL query to update the booking with the new driver_id and status
            query = """
                UPDATE bookings
                SET driver_id = %s, status = 'Assigned'
                WHERE booking_id = %s
            """
            cursor.execute(query, (driver_id, booking_id))
            
            # Commit the transaction
            self.connection.commit()

            # Check if any row was affected (i.e., if the booking was updated)
            if cursor.rowcount > 0:
                return True  # Successful update
            else:
                return False  # No rows were updated (maybe no such booking exists)

        except Error as err:
            print(f"Error assigning driver to booking: {err}")
            return False
        finally:
            cursor.close()


    def fetch_bookings(self):
        """Fetch all bookings from the bookings table."""
        if self.connection is None:
            print("No database connection.")
            return []

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # Using DictCursor to get results as dictionaries
            cursor.execute("SELECT * FROM bookings")
            bookings = cursor.fetchall()
            cursor.close()
            return bookings
        except Error as err:
            print(f"Error fetching bookings: {err}")
            return []

    def fetch_customers(self):
        """Fetch all customers from the customers table."""
        if self.connection is None:
            print("No database connection.")
            return []

        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)  # Using DictCursor to get results as dictionaries
            cursor.execute("SELECT * FROM customers")  # Modify this query if needed
            customers = cursor.fetchall()
            cursor.close()
            return customers
        except pymysql.MySQLError as err:
            print(f"Error fetching customers: {err}")
            return []

    def update_driver_password(self, email, new_password):
        """
        Update the password of the driver with the given email.

        :param email: The email of the driver whose password is to be updated.
        :param new_password: The new password to be set for the driver.
        :return: A tuple (success, message)
        """
        if self.connection is None:
            return False, "No database connection."

        try:
            query = """
            UPDATE drivers
            SET password = %s
            WHERE email = %s
            """
            values = (new_password, email)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()

            return True, "Password updated successfully."
        except Error as e:
            print(f"Error updating driver password: {e}")
            return False, str(e)


    def update_driver_details(self, driver_id, full_name, email, phone_number, gender, dob, license_number, address):
        """
        Update the details of a driver based on the provided driver ID.
        
        :param driver_id: The ID of the driver whose details need to be updated.
        :param full_name: The new full name of the driver.
        :param email: The new email of the driver.
        :param phone_number: The new phone number of the driver.
        :param gender: The new gender of the driver.
        :param dob: The new date of birth of the driver.
        :param license_number: The new license number of the driver.
        :param address: The new address of the driver.
        :return: A tuple (success, message)
        """
        if self.connection is None:
            return False, "No database connection."

        try:
            query = """
            UPDATE drivers
            SET full_name = %s, email = %s, phone_number = %s, gender = %s, dob = %s, license_number = %s, address = %s
            WHERE driver_id = %s
            """
            values = (full_name, email, phone_number, gender, dob, license_number, address, driver_id)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()

            if cursor.rowcount > 0:  # Check if any row was updated
                return True, "Driver details updated successfully."
            else:
                return False, "Driver not found or no changes made."
        except Error as e:
            print(f"Error updating driver details: {e}")
            return False, str(e)       
    
    def validate_customer(self, email, password):
        if self.connection is None:
            return False, "No database connection."

        try:
            query = "SELECT customer_id, full_name FROM customers WHERE email = %s AND password = %s"
            values = (email, password)
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
            
            if result:
                # Return success and customer details as a dictionary
                return True, result  # 'result' is already a dictionary with customer_id and full_name
            else:
                # Return failure and an error message
                return False, "Invalid email or password."
        except Exception as e:
            print(f"Error validating customer: {e}")
            return False, str(e)


    def save_payment_details(self, booking_id, amount, payment_method, payment_status=None):
        if payment_status is None:
            payment_status = 'Pending'  # Default value for payment status

        # Ensure cursor is initialized before using it
        if self.connection is None:
            print("No database connection.")
            return False

        try:
            # Insert the payment details into the payments table
            query = """
            INSERT INTO payments (booking_id, amount, payment_method, payment_status)
            VALUES (%s, %s, %s, %s)
            """
            cursor = self.connection.cursor()  # Create a new cursor here
            cursor.execute(query, (booking_id, amount, payment_method, payment_status))
            self.connection.commit()
            cursor.close()

            print("Payment details saved successfully.")
            return True
        except pymysql.MySQLError as e:
            print(f"Error saving payment details: {e}")
            return False

    def get_booking_status(self, booking_id):
        """
        Retrieve the status of a specific booking.

        :param booking_id: The ID of the booking whose status is to be retrieved.
        :return: A tuple (status, message)
        """
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT status FROM bookings WHERE booking_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (booking_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result['status'], "Booking status retrieved successfully."
            else:
                return None, "No booking found with the provided ID."
        except Error as e:
            print(f"Error retrieving booking status: {e}")
            return None, str(e)

    def get_payment_status(self, payment_id):
        """
        Retrieve the status of a specific payment.

        :param payment_id: The ID of the payment whose status is to be retrieved.
        :return: A tuple (status, message)
        """
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT payment_status FROM payments WHERE payment_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (payment_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result['payment_status'], "Payment status retrieved successfully."
            else:
                return None, "No payment found with the provided ID."
        except Error as e:
            print(f"Error retrieving payment status: {e}")
            return None, str(e)

    def get_driver_status(self, driver_id):
        """
        Retrieve the status of a specific driver (e.g., Active, Inactive).

        :param driver_id: The ID of the driver whose status is to be retrieved.
        :return: A tuple (status, message)
        """
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT status FROM drivers WHERE driver_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (driver_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result['status'], "Driver status retrieved successfully."
            else:
                return None, "No driver found with the provided ID."
        except Error as e:
            print(f"Error retrieving driver status: {e}")
            return None, str(e)

    def get_customer_status(self, customer_id):
        """
        Retrieve the status of a customer (e.g., Active, Suspended).

        :param customer_id: The ID of the customer whose status is to be retrieved.
        :return: A tuple (status, message)
        """
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT status FROM customers WHERE customer_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result['status'], "Customer status retrieved successfully."
            else:
                return None, "No customer found with the provided ID."
        except Error as e:
            print(f"Error retrieving customer status: {e}")
            return None, str(e)
            
    def update_payment_status(self, payment_id, new_status):
        if self.connection is None:
            return False, "No database connection."

        try:
            query = "UPDATE payments SET payment_status = %s WHERE payment_id = %s"
            values = (new_status, payment_id)
            return self._execute_query(query, values)
        except Error as e:
            print(f"Error updating payment status: {e}")
            return False, str(e)

    def retrieve_payment_details(self, booking_id):
        if self.connection is None:
            return None, "No database connection."

        try:
            query = "SELECT * FROM payments WHERE booking_id = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (booking_id,))
            result = cursor.fetchone()
            cursor.close()
            return result, "Payment details retrieved successfully."
        except Error as e:
            print(f"Error retrieving payment details: {e}")
            return None, str(e)

    def save_booking_data(self, customer_id, pickup_location, dropoff_location, date, Dtime, distance, fare, status):
        if self.connection is None:
            print("No database connection.")
            return False, "No database connection."

        try:
            query = """
            INSERT INTO bookings (customer_id, pickup_location, dropoff_location, date, Dtime, distance, fare, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (customer_id, pickup_location, dropoff_location, date, Dtime, distance, fare, status)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True, "Booking data saved successfully."
        except Error as e:
            print(f"Error saving booking data: {e}")
            return False, str(e)



    def insert_driver(self, full_name, address, phone_number, gender, dob, email, password, vehicle_model, vehicle_registration_number, license_number):
        """Insert a new driver into the database."""
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO drivers (full_name, address, phone_number, gender, dob, email, password, vehicle_model, vehicle_registration_number, license_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (full_name, address, phone_number, gender, dob, email, password, vehicle_model, vehicle_registration_number, license_number)
            cursor.execute(query, values)
            self.connection.commit()

            return True, "Driver registration successful!"  # Return success status and message
        except Exception as e:
            print(f"Error: {e}")
            return False, str(e)  # Return failure status and error message

    def fetch_available_drivers(self, pickup_lat, pickup_lon):
        """Fetch available drivers from the database and calculate their distance from the pickup location."""
        try:
            # Query to fetch available drivers
            cursor = self.connection.cursor()
            query = """
                SELECT driver_id, full_name, latitude, longitude 
                FROM drivers 
                WHERE status = 'available'  -- Assuming availability status
            """
            cursor.execute(query)
            available_drivers = cursor.fetchall()

            if not available_drivers:
                return []

            # Create a list to store drivers with their distance to the pickup location
            drivers_with_distance = []

            for driver in available_drivers:
                driver_id = driver['driver_id']
                driver_name = driver['full_name']
                driver_lat = driver['latitude']
                driver_lon = driver['longitude']

                # Calculate the distance from the pickup location
                distance = geodesic((pickup_lat, pickup_lon), (driver_lat, driver_lon)).kilometers

                # Append driver data with distance
                drivers_with_distance.append((driver_id, driver_name, distance))

            # Sort the list of drivers by distance (ascending order)
            drivers_with_distance.sort(key=lambda x: x[2])  # Sort by distance

            # Return the top 3 closest drivers (or all if you prefer)
            return drivers_with_distance[:3]

        except Exception as e:
            print(f"Error fetching available drivers: {str(e)}")
            return []


    def insert_booking(self, taxi_booking):
        customer_id = 1  # Example, replace with actual customer ID logic

        pickup_location = taxi_booking.pickup_location
        dropoff_location = taxi_booking.dropoff_location
        date = taxi_booking.date_time.date()
        Dtime = taxi_booking.date_time.time()
        distance = taxi_booking.distance
        fare = taxi_booking.fare
        status = None  # Status is set to None by default

        return self.save_booking_data(customer_id, pickup_location, dropoff_location, date, Dtime, distance, fare, status)

    def mark_as_done(self, booking_id):
        """Mark a ride as completed."""
        if self.connection is None:
            print("No database connection.")
            return False, "No database connection."

        try:
            # Update the status of the booking to 'Completed'
            query = "UPDATE bookings SET status = 'Completed' WHERE booking_id = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (booking_id,))
            self.connection.commit()  # Commit the changes
            cursor.close()

            print(f"Booking {booking_id} has been marked as completed.")
            return True, f"Booking {booking_id} marked as completed."
        except Error as e:
            print(f"Error updating ride status for booking {booking_id}: {e}")
            return False, f"Error updating ride status: {e}"

    def cancel_book(self, customer_id, booking_id):
        if self.connection is None:
            print("No database connection.")
            return False, "Database connection error."

        try:
            # Update the status of the booking to 'canceled'
            query = "UPDATE bookings SET status = 'cancelled' WHERE customer_id = %s AND booking_id = %s"
            cursor = self.connection.cursor()

            # Execute the query with parameters
            cursor.execute(query, (customer_id, booking_id))
            self.connection.commit()  # Commit the transaction to apply changes

            # Check if any row was affected
            if cursor.rowcount > 0:
                cursor.close()
                print('821')
                return True, "Booking canceled successfully."
            else:
                cursor.close()
                print('825')
                return False, "No booking found with the given ID or already canceled."

        except Error as e:
            print(f"Error canceling booking: {e}")
            return False, f"Error canceling booking: {e}"



    def get_customer_details(self, email):
        if self.connection is None:
            print("No database connection.")
            return None

        try:
            query = "SELECT full_name, email, phone_number, address FROM customers WHERE email = %s"
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result  # Return customer details as a dictionary
            else:
                print(f"No customer found with email {email}")
                return None
        except Error as e:
            print(f"Error retrieving customer details: {e}")
            return None

    def fetch_available_drivers(self):
        """Fetch all drivers from the database."""
        if self.connection is None:
            print("No database connection.")
            return None

        try:
            query = "SELECT driver_id, full_name FROM drivers"  # Removed the 'status' column as you don't need it
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            if result:
                return result  # Return the list of all drivers as a list of dictionaries
            else:
                print("No drivers found.")
                return None
        except Error as e:
            print(f"Error retrieving drivers: {e}")
            return None



    def submit_customer_report(self, customer_id, report_content):
        try:
            # Assuming you have a database cursor and connection
            cursor = self.connection.cursor()

            # Write the SQL query to insert the report into the appropriate table
            query = """
            INSERT INTO customer_reports (customer_id, report_content, report_date)
            VALUES (%s, %s, NOW())
            """
            cursor.execute(query, (customer_id, report_content))
            self.connection.commit()

            return True, "Report submitted successfully."
        except Exception as e:
            return False, str(e)

            db = DatabaseConnection()
            success, message = db.submit_customer_report(1, "This is a test report.")
            print(success, message)

    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
