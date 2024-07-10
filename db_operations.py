import logging
from dbcm import DBCM

class DBOperations():
    """Create, read, update and delete and data in a SQLite database."""
    def __init__(self, file):
        """Initialize the DBOperations class with the specified file."""
        self.file = file

    def initialize_db(self):
        """Creates weather_data table."""
        with DBCM(self.file) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS weather_data
                                (id INTEGER PRIMARY KEY,
                                date TEXT NOT NULL,
                                location TEXT NOT NULL,
                                min_temp REAL NOT NULL,
                                max_temp REAL NOT NULL,
                                avg_temp REAL NOT NULL,
                                CONSTRAINT unique_date_location UNIQUE (date, location));""")
        logging.info("Table created successfully.")

    def save_data(self, date_data, location, max_data, min_data, mean_data):
        """Inserts data to the weather_data table, ignoring duplicates."""
        with DBCM(self.file) as cursor:
            sql = """INSERT OR IGNORE INTO weather_data
                    (date, location, min_temp, max_temp, avg_temp)
                    VALUES (?, ?, ?, ?, ?)"""
            data = (date_data, location, max_data, min_data, mean_data)
            cursor.execute(sql, data)
        logging.info("Data saved successfully %s", data)
        print("Data saved successfully.")

    def fetch_data(self):
        """Return all rows of the weather_data table."""
        with DBCM(self.file) as cursor:
            cursor.execute("SELECT * FROM weather_data;")
            logging.info("Data was fetched successfully.")
            return cursor.fetchall()

    def fetch_monthly_avg_temps(self, start_year, end_year, month=None):
        """Return the monthly avg_temp between the specified date range."""
        with DBCM(self.file) as cursor:
            if month is None:
                cursor.execute("SELECT date, avg_temp "
                                "FROM weather_data "
                                "WHERE date BETWEEN ? AND ?;", (start_year, end_year + 1))
            else:
                cursor.execute("SELECT date, avg_temp "
                                "FROM weather_data "
                                "WHERE date LIKE ?;",(f"{start_year}-{month:02}%",))
            logging.info("Monthly avg_temp data was fetched successfully.")
            return cursor.fetchall()

    def purge_data(self):
        """Delete all data from the weather_data table."""
        with DBCM(self.file) as cursor:
            cursor.execute("DROP TABLE weather_data")
        logging.info("Rows deleted successfully.")
