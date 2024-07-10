import sqlite3

class DBCM:
    """Creates a context manager for a SQLite database."""
    def __init__(self, file):
        """Initialize the DBCM class with the specified file."""
        self.file = file
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Opens the connection to a database and returns a cursor for sql queries"""
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()

        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        """Saves all changes and closes the cursor and connection."""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
