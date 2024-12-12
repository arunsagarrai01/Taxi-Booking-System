import customtkinter as ctk
from tkinter import messagebox  # Import messagebox
from Database_Connection import DatabaseConnection  # Replace with your database connection module


class AdminReportViewer:
    def __init__(self, app):
        self.app = app
        self.db = DatabaseConnection()
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

        # Table headers
        headers = ["Report ID", "Customer ID", "Report Content", "Report Date"]
        for col_num, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.content_frame, text=header_text, font=("Arial", 12, "bold"), anchor="w"
            )
            header_label.grid(row=0, column=col_num, padx=10, pady=5, sticky="w")

        # Fetch and display reports
        self.fetch_reports()

    def fetch_reports(self):
        # Clear existing widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Recreate headers
        headers = ["Report ID", "Customer ID", "Report Content", "Report Date"]
        for col_num, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                self.content_frame, text=header_text, font=("Arial", 12, "bold"), anchor="w"
            )
            header_label.grid(row=0, column=col_num, padx=10, pady=5, sticky="w")

        # Query to fetch reports
        query = "SELECT report_id, customer_id, report_content, report_date FROM customer_reports"
        reports = self.db.fetch_query(query)

        # Display each report
        for row_num, report in enumerate(reports, start=1):
            for col_num, value in enumerate(report):
                value_label = ctk.CTkLabel(self.content_frame, text=str(value), anchor="w")
                value_label.grid(row=row_num, column=col_num, padx=10, pady=5, sticky="w")

    def refresh_reports(self):
        # Refresh the reports by fetching them again
        self.fetch_reports()

        # Show a success message box
        messagebox.showinfo("Success", "Reports refreshed successfully!")

