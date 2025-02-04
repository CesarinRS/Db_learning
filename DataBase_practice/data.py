import sqlite3
from datetime import datetime

class DatabaseManager:
    """Class to manage the purchase database and related operations."""
    
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def connect_db(self):
        """Returns a managed database connection."""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Creates the 'purchase' table if it doesn't exist."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS purchase (
                    id INTEGER PRIMARY KEY, 
                    product TEXT, 
                    price REAL, 
                    date TEXT, 
                    shop TEXT
                )
            """)
            conn.commit()

    def add_purchases(self, product, price, date, shop):
        """Adds a new purchase to the database."""
        try:
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO purchase (product, price, date, shop) VALUES (?, ?, ?, ?)", 
                               (product, price, date, shop))
                conn.commit()
            print(f"Purchase {product} added successfully!")
        except sqlite3.DatabaseError as e:
            print(f"Error adding purchase: {e}")

    def view_purchases(self):
        """Displays all purchases from the database."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM purchase")
            purchases = cursor.fetchall()

        for purchase in purchases:
            print(purchase)

    def date_filter(self, start_date, end_date):
        """Filters purchases by the specified date."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM purchase WHERE date BETWEEN ? AND ?", (start_date, end_date))
            purchases = cursor.fetchall()
        return purchases

    def delete_purchase(self, purchase_id):
        """Deletes a purchase from the database by its ID."""
        try:
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM purchase WHERE id = ?", (purchase_id,))
                conn.commit()
            print(f"Purchase {purchase_id} has been deleted successfully")
        except sqlite3.DatabaseError as e:
            print(f"Error deleting purchase: {e}")

    def edit_purchases(self, purchase_id, product, price, date, shop):
        """Edits an existing purchase in the database."""
        try:
            with self.connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE purchase 
                    SET product = ?, price = ?, date = ?, shop = ? 
                    WHERE id = ?
                """, (product, price, date, shop, purchase_id))
                conn.commit()
            print(f"Purchase with ID {purchase_id} updated successfully.")
        except sqlite3.DatabaseError as e:
            print(f"Error editing purchase: {e}")

    def get_total(self):
        """Calculates the total amount spent on purchases."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price) FROM purchase")
            total = cursor.fetchone()[0] or 0  # Default to 0 if no purchases
        return total

    def add_category_column(self):
        """Adds a 'category' column to the 'purchase' table if it doesn't exist."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(purchase)")
            columns = [column[1] for column in cursor.fetchall()]
            if "category" not in columns:
                cursor.execute("ALTER TABLE purchase ADD COLUMN category TEXT")
                conn.commit()

    def products_category(self, purchase_id, category):
        """Assigns a category to a purchase."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE purchase SET category = ? WHERE id = ?", (category, purchase_id))
            conn.commit()
            print(f"The purchase with ID {purchase_id} has been recategorized as {category}.")

    def initialize_and_load_db(self):
        """Ensures the database is ready at the start of the program."""
        self.create_table()
        print("Database has been initialized.")

    def create_history_table(self):
        """Creates the history table to track database actions."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def log_action(self, action, details):
        """Logs an action in the history table."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO history (action, details) VALUES (?, ?)", (action, details))
            conn.commit()

    def view_history(self):
        """Displays the history of changes in the database."""
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history ORDER BY timestamp DESC")
            history = cursor.fetchall()

        for entry in history:
            print(entry)

