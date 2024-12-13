import customtkinter as ctk
from tkinter import messagebox
from Database_Connection import DatabaseConnection  # Replace with your actual DatabaseConnection import

class AdminReportViewer:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()  # Make sure the DB connection is correct
        self.setup_ui()

    def setup_ui(self):
        self.app.title("Admin Report Viewer")
        self.app.geometry("800x600")

        # Header
        header = ctk.CTkLabel(self.app, text="Customer Reports", font=("Arial", 24, "bold"))
        header.pack(pady=10)

        # Refresh Button
        refresh_button = ctk.CTkButton(
            self.app,
            text="Refresh Reports",
            command=self.refresh_reports,
            fg_color="#4CAF50",
            font=("Arial", 12, "bold")
        )
        refresh_button.pack(pady=10)

        # Content frame
        self.content_frame = ctk.CTkFrame(self.app, corner_radius=10)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table headers (this should only be set up once)
        self.headers = ["Report ID", "Customer ID", "Report Content", "Report Date"]
        self.create_table_headers()

        # Fetch and display reports
        self.fetch_reports()

    def create_table_headers(self):
        """Create headers in the content frame."""
        for col_num, header_text in enumerate(self.headers):
            header_label = ctk.CTkLabel(
                self.content_frame, text=header_text, font=("Arial", 12, "bold"), anchor="w"
            )
            header_label.grid(row=0, column=col_num, padx=10, pady=5, sticky="w")

    def fetch_reports(self):
        # Clear existing widgets in the content frame, excluding headers
        for widget in self.content_frame.winfo_children():
            if widget.grid_info()['row'] != 0:  # Skip headers on row 0
                widget.destroy()

        try:
            # Query to fetch reports
            query = "SELECT report_id, customer_id, report_content, report_date FROM customer_reports"
            reports = self.db.fetch_query(query)  # Fetch data from the database

            # Debugging: Print fetched reports
            print("Fetched reports:", reports)

            # Check if reports is a valid list with data
            if reports and isinstance(reports, list):
                # Display each report
                for row_num, report in enumerate(reports, start=1):
                    # Assuming each report is a dictionary
                    for col_num, key in enumerate(self.headers):
                        # Map headers to dictionary keys
                        dict_key = key.lower().replace(" ", "_")  # Convert header to dictionary key format
                        value = report.get(dict_key, "")  # Get value from the dictionary
                        value_label = ctk.CTkLabel(
                            self.content_frame,
                            text=str(value),
                            anchor="w",
                            font=("Arial", 12)
                        )
                        value_label.grid(row=row_num, column=col_num, padx=10, pady=5, sticky="w")
            else:
                # No reports found
                no_reports_label = ctk.CTkLabel(
                    self.content_frame,
                    text="No reports found.",
                    anchor="w",
                    font=("Arial", 12)
                )
                no_reports_label.grid(
                    row=1, column=0, columnspan=len(self.headers), padx=10, pady=5, sticky="w"
                )

        except Exception as e:
            # Print and display the error message
            print(f"Error in fetch_reports: {str(e)}")
            error_label = ctk.CTkLabel(
                self.content_frame,
                text=f"Error: {str(e)}",
                anchor="w",
                font=("Arial", 12),
                fg_color="#FFCCCC"
            )
            error_label.grid(
                row=1, column=0, columnspan=len(self.headers), padx=10, pady=5, sticky="w"
            )



    def refresh_reports(self):
        """Refresh the reports by fetching them again."""
        self.fetch_reports()

        # Show a success message box after fetching reports
        messagebox.showinfo("Success", "Reports refreshed successfully!")

