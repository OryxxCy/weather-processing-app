import datetime
import logging
import sys
from menu import Menu
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

logging.basicConfig(filename='weather_processor.log',
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)

class WeatherProcessor():
    """Allow the users to download full weather data or to update weather data."""
    def __init__(self):
        """Initialize the WeatherProcessor class with menu options."""
        try:
            self.main_menu = Menu(title="Welcome to Weather Processor, please select:")
            self.weather_db = DBOperations("weather_data.sqlite")
            self.weather_db.initialize_db()
            self.weather_scraper = WeatherScraper(self.weather_db)
            self.plot_operations = PlotOperations("weather_data.sqlite")
        except RuntimeError as e:
            logging.error("Error initializing WeatherProcessor: %s", e)
        except SystemError as e:
            logging.error("Error initializing WeatherProcessor: %s", e)

    def menu(self):
        """Create a menu with three options to the user."""
        try:
            self.main_menu.set_options([
                ("Download full weather data", self.weather_scraper.scrape_weather_data),
                ("Update weather data", self.update_data),
                ("Generate box plot", self.generate_box_plot),
                ("Generate line plot", self.generate_line_plot),
                ("Quit", sys.exit)
            ])

            self.main_menu.open()
        except RuntimeError as e:
            logging.error("Error when opening WeatherProcessor menu: %s", e)
        except SystemError as e:
            logging.error("Error when opening WeatherProcessor menu: %s", e)

    def update_data(self):
        """Update the weather data."""
        try:
            data = self.weather_db.fetch_data()
            dates = [datetime.datetime.strptime(row[1], "%Y-%m-%d") for row in data]
            latest_date = max(dates) if dates else None

            self.weather_scraper.scrape_weather_data(latest_date)
            after_data = self.weather_db.fetch_data()
            if len(after_data) - len(data) > 0:
                print(f"{len(after_data) - len(data)} data was inserted.")
            else:
                print("The data is up to date.")
            input("Please press anything to continue.")
        except RuntimeError as e:
            logging.error("Error when updating weather data: %s", e)
        except SystemError as e:
            logging.error("Error when updating weather data: %s", e)

    def generate_box_plot(self):
        """Generate box plot for a specified year range."""
        try:
            start_year = int(input("Enter the start year: "))
            end_year = int(input("Enter the end year: "))
            monthly_avg_temps = self.weather_db.fetch_monthly_avg_temps(start_year, end_year)

            if start_year > end_year:
                print("Invalid start year")
                return
            if not monthly_avg_temps:
                print(f"No data available between {start_year} to {end_year}")
                return
            self.plot_operations.plot_boxplot(monthly_avg_temps)
            logging.info("Box plot generated successfully.")
        except RuntimeError as e:
            logging.error("Error when generating box plot: %s", e)
        except SystemError as e:
            logging.error("Error when generating box plot: %s", e)
        except ValueError as e:
            print("Invalid input. Please input a whole number.")
            logging.error("Error when generating line plot: %s", e)

        input("Please press anything to continue.")

    def generate_line_plot(self):
        """Generate line plot for a specified month and year."""
        try:
            year = int(input("Enter the year: "))
            month = int(input("Enter the month: "))
            daily_temps = self.weather_db.fetch_monthly_avg_temps(year, year, month)
            if month >= 13:
                input("Invalid month, Please press anything to continue.")
                return
            if not daily_temps:
                input(f"No data available for {month}, {year}. Please press anything to continue.")
                return
            self.plot_operations.plot_lineplot(daily_temps)
            logging.info("Line plot generated successfully.")
        except RuntimeError as e:
            logging.error("Error when generating line plot: %s", e)
        except SystemError as e:
            logging.error("Error when generating line plot: %s", e)
        except ValueError as e:
            print("Invalid input. Please input a whole number.")
            logging.error("Error when generating line plot: %s", e)

        input("Please press anything to continue.")

if __name__ == "__main__":
    weather_processor = WeatherProcessor()
    weather_processor.menu()
