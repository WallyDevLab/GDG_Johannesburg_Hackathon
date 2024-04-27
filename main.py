from pyzbar.pyzbar import decode
from PIL import Image
import json
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

# def scan_barcode(image_path=None):
#     """
#     Scans a barcode from an image or user input.

#     Args:
#         image_path (str, optional): Path to the image containing the barcode. Defaults to None.

#     Returns:
#         str: Decoded barcode data or None if no barcode is found.
#     """
#     if image_path:
#         img = Image.open(image_path)
#         decoded_data = decode(img)
#     else:
#         barcode_input = input("Enter the barcode number: ")
#         decoded_data = [{"data": barcode_input.encode()}]

#     if decoded_data:
#         barcode_data = decoded_data[0].data.decode("utf-8")
#         return barcode_data
#     else:
#         print("No barcode detected.")
#         return None
    
def input_barcode_number():

    barcode_input = input("Enter the barcode number: ")
    decoded_data = [{"data": barcode_input.encode()}]

    if decoded_data:
        barcode_data = decoded_data[0]["data"].decode("utf-8")
        return barcode_data
    else:
        print("No barcode detected.")
        return None


    pass

def load_inventory():
    """Loads inventory from a JSON file or creates an empty one if it doesn't exist."""
    try:
        with open("inventory.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_inventory(inventory):
    """Saves the inventory to a JSON file."""
    with open("inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)

def add_product(inventory):
    """Adds a new product with expiry date to the inventory."""
    barcode_data = input_barcode_number()
    if barcode_data:
        product_name = input("Enter product name: ")
        while True:
            expiry_date_str = input("Enter expiry date (YYYY-MM-DD): ")
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        inventory[barcode_data] = {"name": product_name, "expiry_date": expiry_date_str}
        print("Product added!")

def remove_product(inventory):
    """Removes a product from the inventory."""
    barcode_data = input_barcode_number()
    if barcode_data in inventory:
        del inventory[barcode_data]
        print("Product removed!")
    else:
        print("Product not found in inventory.")

def view_inventory(inventory):
    """Displays the current inventory."""
    if inventory:
        print("Inventory:")
        for barcode, product in inventory.items():
            print(f"  {barcode}: {product['name']}")
    else:
        print("Inventory is empty.")

# def check_expiry_and_send_alerts(inventory):
#     """Checks for expiring products and sends email alerts."""
#     today = datetime.now().date()
#     alert_threshold = timedelta(days=5)
#     sender_email = "your_email@example.com"
#     sender_password = "your_password"
#     receiver_email = "recipient@example.com"

#     for barcode, product in inventory.items():
#         expiry_date = datetime.strptime(product["expiry_date"], "%Y-%m-%d").date()
#         days_left = expiry_date - today
#         if 0 < days_left <= alert_threshold:
#             subject = f"Product Expiring Soon: {product['name']}"
#             body = f"The product with barcode {barcode} and name '{product['name']}' is expiring on {expiry_date}. Please take necessary action."
#             message = EmailMessage()
#             message["From"] = sender_email
#             message["To"] = receiver_email
#             message["Subject"] = subject
#             message.set_content(body)

#             with smtplib.SMTP_SSL("your_email_server", 465) as server:
#                 server.login(sender_email, sender_password)
#                 server.send_message(message)
#             print(f"Email alert sent for product: {product['name']}")

def main():
    inventory = load_inventory()

    while True:
        print("\nMenu:")
        print("1. Scan and Add Product")
        print("2. Remove Product")
        print("3. View Inventory")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product(inventory)
            # check_expiry_and_send_alerts(inventory)
        elif choice == "2":
            remove_product(inventory)
        elif choice == "3":
            view_inventory(inventory)
        elif choice == "4":
            save_inventory(inventory)
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()  
