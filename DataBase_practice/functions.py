from data import DatabaseManager
from datetime import datetime
import logging

class MessageHandler:
    """
    Class to handle messages based on platform (console, gui, android, web).
    """
    def __init__(self, platform="console"):
        self.platform = platform
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def display_message(self, message, level="info"):
       levels = {
           "info":logging.info,
           "warning":logging.warning,
           "error":logging.error
       }
       levels.get(level, logging.info)(f"[{self.platform.upper()}] {message}")

class PurchaseManager:
    """
    Class to manage purchase-related actions (add, edit, delete, etc.).
    """
    def __init__(self, message_handler, db_manager):
        self.message_handler = message_handler
        self.db_manager = db_manager

    def add_purchase(self):
        product = input("Product: ")
        price = float(input("Price: "))
        date = input("Date (YYYY-MM-DD): ")
        shop = input("Shop: ")
        self.db_manager.add_purchases(product, price, date, shop)
        self.db_manager.log_action("INSERT", f"Product: {product}, Price: {price}, Date: {date}, Shop: {shop}")
        self.message_handler.display_message(f"Purchase added: {product} at {shop} on {date}")

    def show_purchases(self):
        self.db_manager.view_purchases()
        self.message_handler.display_message("Displayed all purchases.")

    def filter_by_date(self):
        date = input("Filter date (YYYY-MM-DD): ")
        self.db_manager.date_filter(date)
        self.message_handler.display_message(f"Filtered purchases by date: {date}")

    def delete_purchase(self):
        purchase_id = get_input("ID of the purchase to delete: ", int)
        self.db_manager.delete_purchase(purchase_id)
        self.db_manager.log_action("DELETE", f"Purchase with ID {purchase_id} deleted")
        self.message_handler.display_message(f"Purchase with ID {purchase_id} deleted.")

    def edit_purchase(self):
        purchase_id = get_input("ID of the purchase to edit: ", int)
        new_product = input("New product: ")
        price = get_input("Price: ", float)
        date = input("Date of purchase (YYYY-MM-DD): ")
        shop = input("Shop: ")
        self.db_manager.edit_purchases(purchase_id, new_product, price, date, shop)
        self.db_manager.log_action("UPDATE", f"Purchase with ID {purchase_id} updated: {new_product}, {price}, {date}, {shop}")
        self.message_handler.display_message(f"Purchase with ID {purchase_id} updated.")

    def total_expense(self):
        self.db_manager.get_totally()
        self.message_handler.display_message("Displayed total expense.")

    def view_history(self):
        self.db_manager.view_history()
        self.message_handler.display_message("Displayed history.")


def get_input(prompt, type_func=str):
    """
    Gets user input, validating its type.
    """
    while True:
        try:
            return type_func(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")





    
