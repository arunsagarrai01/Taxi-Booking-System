import customtkinter as ctk
from tkinter import messagebox
from tkinter import Canvas
from PIL import Image, ImageTk  # Import the required modules for working with images

class IndexPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set the appearance mode to "Dark" or "Light"
        ctk.set_appearance_mode("Light")  # You can change to "Dark"
        self.title("Taxi Booking System")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)


        # Load background image
        self.bg_image = Image.open("Image/Taxi.jpg")  # Replace with your image path
        self.bg_image = self.bg_image.resize((1000, 1000))  # Resize to fit the window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a Canvas and add the background image
        self.canvas = Canvas(self, width=600, height=400)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.canvas.place(relwidth=1, relheight=1)  # Make the canvas cover the entire window

        # Title Label (Fix: Using text_color instead of fg)
        self.title_label = ctk.CTkLabel(
            self,
            text="Welcome to Taxi Booking System",
            font=("Helvetica", 18, "bold"),
            text_color="#333"  # Corrected text color argument
        )
        self.title_label.pack(pady=20)

        # Buttons for Roles
        self.customer_button = ctk.CTkButton(
            self,
            text="Customer",
            font=("Helvetica", 14),
            width=200,
            height=50,
            fg_color="#4CAF50",
            hover_color="#45a049",  # Change color on hover
            command=self.open_customer_page
        )
        self.customer_button.pack(pady=10)

        self.driver_button = ctk.CTkButton(
            self,
            text="Driver",
            font=("Helvetica", 14),
            width=200,
            height=50,
            fg_color="#2196F3",
            hover_color="#1e88e5",
            command=self.open_driver_page
        )
        self.driver_button.pack(pady=10)

        self.admin_button = ctk.CTkButton(
            self,
            text="Admin",
            font=("Helvetica", 14),
            width=200,
            height=50,
            fg_color="#FF5722",
            hover_color="#e64a19",
            command=self.open_admin_page
        )
        self.admin_button.pack(pady=10)

        # Exit Button
        self.exit_button = ctk.CTkButton(
            self,
            text="Exit",
            font=("Helvetica", 12),
            width=200,
            height=50,
            fg_color="#f44336",
            hover_color="#d32f2f",
            command=self.exit_app
        )
        self.exit_button.pack(side="bottom", pady=20)

    # Placeholder methods for different pages
    def open_customer_page(self):
        self.destroy()
        from Customer_Login_Page import CustomerLoginPage  # Make sure the module is available
        app = CustomerLoginPage()  # Instantiate the page
        app.mainloop()  # Start the mainloop for the passenger login page

    def open_driver_page(self):
        self.destroy()
        from Driver_Login_Page import DriverLoginPage  # Make sure the module is available
        app = DriverLoginPage()  # Instantiate the page
        app.mainloop()  

    def open_admin_page(self):
        self.destroy()
        from Admin_Login_Page import AdminLoginPage
        app = AdminLoginPage()  # Instantiate the page
        app.mainloop()  

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = IndexPage()
    app.mainloop()
