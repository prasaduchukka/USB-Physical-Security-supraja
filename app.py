import os
import subprocess
import random
import string
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk  # Required for images

# Set user email
USER_EMAIL = "testprasadwork@gmail.com"  # Replace with actual registered email

# Paths to images
PROJECT_IMAGE_PATH = r"C:\form\pprojectimg.png"
ENABLE_IMAGE_PATH = r"C:\form\enableimg.jpg"
DISABLE_IMAGE_PATH = r"C:\form\disableimg.jpg"

# Function to generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Function to send password via email
def send_email(to_email, password):
    sender_email = "testprasadwork@gmail.com"  # Replace with your email
    sender_password = "anvvsmscvzejtrqn"  # Replace with your email app password
    subject = "USB Control Access Password"
    body = f"Your password to enable/disable USB ports is: {password}"

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Function to store password temporarily
def save_password(password):
    with open("usb_password.txt", "w") as f:
        f.write(password)

# Function to load stored password
def load_password():
    if os.path.exists("usb_password.txt"):
        with open("usb_password.txt", "r") as f:
            return f.read().strip()
    return None

# Function to run batch file (Enable or Disable USB)
def run_batch_file(action):
    try:
        batch_files = {
            "enable": r"C:\form\scripts\enable_usb.bat",
            "disable": r"C:\form\scripts\disable_usb.bat"
        }
        batch_file_path = batch_files.get(action)

        if not os.path.exists(batch_file_path):
            messagebox.showerror("Error", f"Batch file not found: {batch_file_path}")
            return

        subprocess.run([batch_file_path], text=True, check=True)
        messagebox.showinfo("Success", f"USB Ports {action.capitalize()}d Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to request and send OTP when Enable/Disable USB is clicked
def request_password(action):
    generated_password = generate_password()
    save_password(generated_password)

    if send_email(USER_EMAIL, generated_password):
        messagebox.showinfo("Success", "A password has been sent to your email.")
        verify_password(action)
    else:
        messagebox.showerror("Error", "Failed to send password. Check email settings.")

# Function to verify password before executing the action
def verify_password(action):
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_window.geometry("300x150")

    tk.Label(password_window, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
    password_entry = tk.Entry(password_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def check_password():
        stored_password = load_password()
        if password_entry.get() == stored_password:
            password_window.destroy()
            run_batch_file(action)
        else:
            messagebox.showerror("Error", "Incorrect Password. Please try again.")
            password_entry.delete(0, tk.END)

    tk.Button(password_window, text="OK", command=check_password).pack(pady=10)

# Function to check USB connection status
def check_usb_connection():
    try:
        result = subprocess.run(["wmic", "path", "Win32_USBHub", "get", "DeviceID"], 
                                stdout=subprocess.PIPE, text=True)
        if "DeviceID" in result.stdout:
            messagebox.showinfo("USB Devices", "USB devices are currently connected.")
        else:
            messagebox.showinfo("USB Devices", "No USB devices connected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking USB devices: {str(e)}")

# Function to show detailed project information in a larger window
def show_project_info():
    info_window = Toplevel(root)
    info_window.title("Project & Team Information")
    info_window.geometry("600x400")
    info_window.configure(bg="lightgray")

    project_info = (
        "PROJECT NAME: USB Physical Security\n\n"
        
        "==> Developed by:\n"
        "  - CHUKKA PRASADU                     [ST#IS#7014]\n"
        "  - JAMPANA AAMUKTHA                [ST#IS#7013]\n"
        "  - KARASANI AJAY KUMAR            [ST#IS#7011]\n"
        "  - DEVU BALA BRAHMAJI              [ST#IS#7012]\n"
        "  - GUDIPATI VENKATESWARLU   [ST#IS#7006]\n"
        "  - VUNNAM ANITHA                        [ST#IS#7010]\n\n"
        "==> Project Details:\n"
        "   - This application allows administrators to enable or disable USB ports.\n"
        "   - Provides security against unauthorized USB access.\n"
        "   - Uses email authentication for security.\n"
        "   - Developed using Python (Tkinter) and batch scripts for USB control.\n"
    )

    tk.Label(info_window, text="Project & Team Information", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)
    tk.Label(info_window, text=project_info, font=("Arial", 12), bg="lightgray", justify="left").pack(padx=20, pady=10)

# Create Fullscreen Window
root = tk.Tk()
root.title("USB Control Panel")
# root.geometry("900x600")  # Fixed size instead of fullscreen
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}") 
root.configure(bg="white")

# Load Images
project_img = Image.open(PROJECT_IMAGE_PATH).resize((750, 350))  # Smaller project image
project_img = ImageTk.PhotoImage(project_img)

# Project Image (at the top, centered)
tk.Label(root, image=project_img).pack(pady=10)

# Center Frame for UI Elements
center_frame = tk.Frame(root, bg="white")
center_frame.pack(expand=True)

# Enable USB Section
enable_img = ImageTk.PhotoImage(Image.open(ENABLE_IMAGE_PATH).resize((350, 200)))
disable_img = ImageTk.PhotoImage(Image.open(DISABLE_IMAGE_PATH).resize((350, 200)))

tk.Label(center_frame, image=enable_img).grid(row=0, column=0, padx=20)
tk.Label(center_frame, image=disable_img).grid(row=0, column=1, padx=20)

tk.Button(center_frame, text="Enable USB", font=("Arial", 14), bg="#4CAF50", fg="white",
          command=lambda: request_password("enable")).grid(row=1, column=0, pady=10)
tk.Button(center_frame, text="Disable USB", font=("Arial", 14), bg="#F44336", fg="white",
          command=lambda: request_password("disable")).grid(row=1, column=1, pady=10)

# Other Buttons (Centered Below)
tk.Button(root, text="Project Info", font=("Arial", 14), bg="#FFC107", fg="black",
          command=show_project_info).pack(pady=10)
tk.Button(root, text="Check USB Connection", font=("Arial", 14), bg="#2196F3", fg="white",
          command=check_usb_connection).pack(pady=10)

# Run Tkinter GUI
root.mainloop()
