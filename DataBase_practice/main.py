"""
Main Program to manage purchase records.
"""

from data import DatabaseManager
from functions import MessageHandler, PurchaseManager

# Inicializar manejadores
db_manager = DatabaseManager()
db_manager.create_table()
db_manager.create_history_table()

message_handler = MessageHandler(platform="console")
purchase_manager = PurchaseManager(message_handler, db_manager)

class Console:
    def __init__(self):
        pass

    def console_capture(self):
        while True:
            self.menu()
            option = input("Select option: ")

            if option == "1":
                purchase_manager.add_purchase()

            elif option == "2":
                purchase_manager.show_purchases()

            elif option == "3":
                purchase_manager.filter_by_date()
                
            elif option == "4":
                purchase_manager.delete_purchase()
            
            elif option == "5":
                purchase_manager.edit_purchase()

            elif option == "6":
                purchase_manager.total_expense()

            elif option == "7":
                purchase_manager.view_history()

            elif option == "8":
                print("Exiting...")
                break

            else: 
                print("Invalid option")

    def menu(self):
        message_handler.display_message("\nMenú:")
        message_handler.display_message("1. Add purchase")
        message_handler.display_message("2. View purchases")
        message_handler.display_message("3. Filter by date")
        message_handler.display_message("4. Delete purchase")
        message_handler.display_message("5. Edit purchase")
        message_handler.display_message("6. Total expense")
        message_handler.display_message("7. See history")
        message_handler.display_message("8. Exit")


# Ejecutar el programa en consola
if __name__ == "__main__":
    console_app = Console()
    console_app.console_capture()
