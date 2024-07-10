from datetime import datetime
import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations():
    """A class for plotting mean temperatures in a data range."""
    def __init__(self, weather_data):
        """Initialize the PlotOperations class with the specified weather data."""
        self.weather_data = DBOperations(weather_data)

    def plot_boxplot(self, monthly_avg_temps):
        """Create a basic boxplot of mean temperatures in the specified date range."""    
        data = {}
        current_month = 1
        for current_month in range(1, 13):
            month_data = []
            for day, temp in monthly_avg_temps:
                if datetime.strptime(day, "%Y-%m-%d").month == current_month:
                    if temp and temp not in ["LegendM", "M", "LegendE", "E", "\xa0"]:
                        if temp:
                            month_data.append(temp)
                if month_data:
                    data[current_month] = month_data
        plt.boxplot(data.values())
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        title = "Monthly Temperature Distribution"
        plt.title(title)
        plt.show()

    def plot_lineplot(self, daily_temps):
        """A line plot of a particular months mean temperature data based on user input."""
        days = []
        temps = []
        for day, temp in daily_temps:
            if temp not in ["LegendM", "M", "LegendE", "E", " "]:
                days.append(day)
                temps.append(temp)
        plt.plot(days, temps)
        plt.xlabel('Days of the month')
        plt.ylabel('Avg Daily Temperature')
        day = datetime.strptime(days[0], "%Y-%m-%d")
        plt.title('Daily Avg Temperatures of ' + day.strftime("%B,%Y"))
        plt.grid(True)
        plt.xticks(rotation=45, fontsize=10)
        plt.show()
