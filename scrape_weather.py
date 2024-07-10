import urllib.request
from datetime import datetime, date
import logging
import threading
from html.parser import HTMLParser
from db_operations import DBOperations

class WeatherScraper(HTMLParser):
    """To scrape Winnipeg weather data from the Environment Canada website."""
    def __init__(self, db_operations):
        super().__init__()
        self.th = False
        self.td = False
        self.a = False
        self.td_counter = 0
        self.date = ""
        self.daily_temps = {}
        self.weather = {}
        self.db_operations = db_operations

    def handle_starttag(self, tag, attrs):
        """Handles the start tag and its attributes."""
        if tag == 'th':
            self.th = True
            for attr in attrs:
                if attr[1] != "row":
                    self.th = False

        if tag == 'a':
            self.a = True

        if self.th and self.a and tag == 'abbr':
            for attr in attrs:
                if attr[0] == "title":
                    try:
                        converted_date = datetime.strptime(attr[1], "%B %d, %Y")
                        self.date = converted_date.strftime("%Y-%m-%d")
                    except ValueError:
                        self.th = False

        if tag == 'td':
            self.td = True

    def handle_endtag(self, tag):
        """Handles the end tag and its attributes."""
        if tag == 'td':
            self.td = False

    def handle_data(self, data):
        """Handles the data inside a tag."""
        if self.td and self.th and self.date != "":
            self.td_counter += 1
            if self.td_counter == 1:
                self.daily_temps['Max'] = data
            elif self.td_counter == 2:
                self.daily_temps['Min'] = data
            elif self.td_counter == 3:
                self.daily_temps['Mean'] = data
            else:
                self.weather[self.date] = self.daily_temps
                max_temp = self.daily_temps['Max']
                min_temp = self.daily_temps['Min']
                mean_temp = self.daily_temps['Mean']
                loc = "Winnipeg"
                self.db_operations.save_data(self.date, loc, max_temp, min_temp, mean_temp)
                self.daily_temps = {}
                self.td_counter = 0
                self.th = False
                self.td = False
                self.date = ""

    def scrape_weather_data(self, latest_date=None):
        """Scrapes weather data for the specified range of years."""
        today = date.today()
        start_year = 1990 if latest_date is None else latest_date.year
        for year in range(today.year, start_year, -1):
            for month in range(13, 1, -1):
                if month == 1:
                    new_year = year - 1
                    new_month = 12
                else:
                    new_month = month - 1
                    new_year = year

                date_format = f"Year={new_year}&Month={new_month}"
                input_url = 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?'\
                        'StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&'\
                        + date_format + '#'

                with urllib.request.urlopen(input_url) as response:
                    html = str(response.read())
                    self.feed(html)
        logging.info("Weather data scraped successfully.")
        print("Weather data scraped successfully.")
        return self.scrape_weather_data

def run_thread(db):
    """Using threading to speedup the scraping."""
    threads = []

    for _ in range(30):
        myparser = WeatherScraper(db)
        thread = threading.Thread(target=myparser.scrape_weather_data)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    weather_db = DBOperations("weather_data.sqlite")
    weather_db.purge_data()
    weather_db.initialize_db()
    run_thread(weather_db)
