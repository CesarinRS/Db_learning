import sqlite3

class DatabaseManager:
    """Class to manage the purchase database and related operations."""
    
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def connect_db(self):
        """Connects to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def create_table(self):
        """Creates the 'purchase' table if it doesn't exist."""
        with self.connect_db() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS purchase (id INTEGER PRIMARY KEY, product TEXT, price REAL, date TEXT, shop TEXT)") 

    def add_purchases(self, product, price, date, shop):
        """Adds a new purchase to the database."""
        with self.connect_db() as conn:
            conn.execute("INSERT INTO purchase (product, price, date, shop) VALUES (?, ?, ?, ?)", (product, price, date, shop))

    def view_purchases(self):
        """Displays all purchases from the database."""
        with self.connect_db() as conn:
            cursor = conn.execute("SELECT * FROM purchase")
            purchases = cursor.fetchall()
        for purchase in purchases:
            print(purchase)

    def date_filter(self, date):
        """Filters purchases by the specified date."""
        with self.connect_db() as conn:
            cursor = conn.execute("SELECT * FROM purchase WHERE date = ?", (date,))
            purchases = cursor.fetchall()

        for purchase in purchases:
            print(purchase)

    def delete_purchase(self, purchase_id):
        """Deletes a purchase from the database by its ID."""
        with self.connect_db() as conn:
            conn.execute("DELETE FROM purchase WHERE id = ?", (purchase_id,))
            print(f"The purchase with id {purchase_id} has been deleted")

    def edit_purchases(self, purchase_id, product, price, date, shop):
        """Edits an existing purchase in the database."""
        with self.connect_db() as conn:
            conn.execute("UPDATE purchase SET product = ?, price = ?, date = ?, shop = ? WHERE id = ?",
                         (product, price, date, shop, purchase_id))
            print(f"Refactored the purchase with id {purchase_id}")

    def get_totally(self):
        """Calculates the total amount spent on purchases."""
        with self.connect_db() as conn:
            cursor = conn.execute("SELECT SUM(price) FROM purchase")
            total = cursor.fetchone()[0]  # Get the first value from the result
        return total

    def add_category_column(self):
        """Adds a 'category' column to the 'purchase' table."""
        with self.connect_db() as conn:
            conn.execute("ALTER TABLE purchase ADD COLUMN category TEXT")

    def products_category(self, purchase_id, category):
        """Assigns a category to a purchase."""
        with self.connect_db() as conn:
            conn.execute("UPDATE purchase SET category = ? WHERE id = ?", (category, purchase_id))
            print(f"The purchase with id {purchase_id} has been recategorized as {category}")

    def save_and_load(self):
        """Ensures the database is ready at the start of the program."""
        self.create_table()
        print("Database has been initialized")

    def create_history_table(self):
        """Creates the history table to track database actions."""
        with self.connect_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def log_action(self, action, details):
        """Logs an action in the history table."""
        with self.connect_db() as conn:
            conn.execute("INSERT INTO history (action, details) VALUES (?, ?)", (action, details))

    def view_history(self):
        """Displays the history of changes in the database."""
        with self.connect_db() as conn:
            cursor = conn.execute("SELECT * FROM history ORDER BY timestamp DESC")
            history = cursor.fetchall()

        for entry in history:
            print(entry)
