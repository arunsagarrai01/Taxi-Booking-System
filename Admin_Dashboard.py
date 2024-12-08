import customtkinter as ctk
from tkinter import messagebox

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Taxi Booking System")
        self.root.geometry("600x400")  # Set the window size
        ctk.set_appearance_mode("Light")  # Set the appearance mode
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self.root, text="Admin Dashboard", font=("Arial", 20), pady=10)
        self.title_label.grid(row=0, column=0, columnspan=2)

        # Buttons for features
        self.assign_button = ctk.CTkButton(self.root, text="Assign Trip", width=20, height=2, command=self.assign_trip, fg_color="#4CAF50", hover_color="#45a049")
        self.assign_button.grid(row=1, column=0, padx=10, pady=10)

        self.view_passenger_button = ctk.CTkButton(self.root, text="View Passengers", width=20, height=2, command=self.view_passengers, fg_color="#2196F3", hover_color="#1e88e5")
        self.view_passenger_button.grid(row=1, column=1, padx=10, pady=10)

        self.view_report_button = ctk.CTkButton(self.root, text="View Report", width=20, height=2, command=self.view_report, fg_color="#FF5722", hover_color="#e64a19")
        self.view_report_button.grid(row=2, column=0, padx=10, pady=10)

        self.show_history_button = ctk.CTkButton(self.root, text="Show History", width=20, height=2, command=self.show_history, fg_color="#FFC107", hover_color="#ffb300")
        self.show_history_button.grid(row=2, column=1, padx=10, pady=10)

        # Logout button
        self.logout_button = ctk.CTkButton(self.root, text="Logout", width=20, height=2, command=self.logout, fg_color="#F44336", hover_color="#d32f2f")
        self.logout_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Status bar
        self.status_label = ctk.CTkLabel(self.root, text="Ready", font=("Arial", 10), anchor="w", padx=10)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

    # Feature Methods
    def assign_trip(self):
        self.status_label.config(text="Assigning trip...")
        messagebox.showinfo("Assign Trip", "Feature to assign trips will be implemented here!")

    def view_passengers(self):
        self.status_label.config(text="Viewing passengers...")
        messagebox.showinfo("View Passengers", "Feature to view passengers will be implemented here!")

    def view_report(self):
        self.status_label.config(text="Viewing report...")
        messagebox.showinfo("View Report", "Feature to view reports will be implemented here!")

    def show_history(self):
        self.status_label.config(text="Showing history...")
        messagebox.showinfo("Show History", "Feature to show history will be implemented here!")

    # Logout method
    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            self.root.destroy()   
            from Index_Page import IndexPage
            app = IndexPage()  
            app.mainloop()

# Driver Code
if __name__ == "__main__":
    root = ctk.CTk()  # Use CTk instead of Tk
    app = AdminDashboard(root)
    root.mainloop()
