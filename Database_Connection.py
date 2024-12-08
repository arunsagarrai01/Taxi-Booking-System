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


    def validate_customer(self, email, password):
        if self.connection is None:
            return False, "No database connection."

        try:
            query = "SELECT * FROM customers WHERE email = %s AND password = %s"
            values = (email, password)
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
            if result:
                return True, "Login successful."
            else:
                return False, "Invalid email or password."
        except Error as e:
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

    def save_booking_data(self, customer_id, driver_id, pickup_location, dropoff_location, date, Dtime, distance, fare):
        if self.connection is None:
            print("No database connection.")
            return False, "No database connection."

        try:
            query = """
            INSERT INTO bookings (customer_id, driver_id, pickup_location, dropoff_location, date, Dtime, distance, fare)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (customer_id, driver_id, pickup_location, dropoff_location, date, Dtime, distance, fare)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True, "Booking data saved successfully."
        except Error as e:
            print(f"Error saving booking data: {e}")
            return False, str(e)

    def insert_booking(self, taxi_booking):
        customer_id = 1  # Example, replace with actual customer ID logic
        driver_id = 1    # Example, replace with actual driver ID logic

        pickup_location = taxi_booking.pickup_location
        dropoff_location = taxi_booking.dropoff_location
        date = taxi_booking.date_time.date()
        Dtime = taxi_booking.date_time.time()
        distance = taxi_booking.distance
        fare = taxi_booking.fare

        return self.save_booking_data(customer_id, driver_id, pickup_location, dropoff_location, date, Dtime, distance, fare)

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
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
