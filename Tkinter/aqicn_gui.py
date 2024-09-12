"""
    Name: aqicn_gui.py
    Author: William Loring
    Created: 09/07/2024
    Purpose: World Air Quality Index Tkinter GUI
    Claude AI used as a code helper
"""

# pip install requests
import requests
import tkinter as tk
from tkinter import ttk, scrolledtext
import api_key
from geocode_geopy import geocode_arg
import weather_utils

AQICN_ENDPOINT = 'https://api.waqi.info/feed/geo:'


class AQICNGui:
    def __init__(self, master):
        self.master = master
        master.title("World Air Quality Index")
        master.geometry("600x475")
        master.iconbitmap("edit_clear.ico")

        self.create_widgets()

# ---------------------- GET LOCATION ------------------------------------ #
    def get_location(self):
        """
        Retrieves the user input for city, state, and country from GUI entries
            and attempts to geocode the provided location information.
        Returns:
            bool: True if the geocoding is successful 
            and the API request is successful, False otherwise.
        """
        # Get user input for city, state, and country from GUI entries
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        country = self.country_entry.get().strip()

        # Check if at least one location field is filled
        if not any([city, state, country]):
            # If all fields are empty, display an error message and return False
            self.results_display.insert(
                tk.END, "Please enter at least one location field.\n")
            return False

        try:
            # Attempt to geocode the provided location information
            lat, lng, self.address = geocode_arg(city, state, country)

            # Construct API request URL with latitude, longitude, and API key
            response = requests.get(
                AQICN_ENDPOINT + str(lat) + ";" + str(lng)
                + "/?token=" + api_key.API_KEY
            )

            # Check if the API request was successful (status code 200)
            if response.status_code == 200:
                # If API request successful,
                # store the JSON response data and return True
                self.data = response.json()
                return True
            else:
                # If API request failed,
                # display error message and return False
                self.results_display.insert(
                    tk.END, "[-] API unavailable. Please try again.\n")
                return False

        except Exception as e:
            # If any exception occurs during the process,
            # display the error message and return False
            self.results_display.insert(tk.END, f"[-] Error: {str(e)}\n")
            return False

# ---------------------- GET CURRENT AQI --------------------------------- #
    def get_current_aqi(self):
        """
        Retrieves the current Air Quality Index (AQI) and displays it.
        This method clears results display area 
        Checks if the location is available.
        If the location is available, it retrieves the AQI and displays it.
        """
        # Clear the results display area
        self.results_display.delete('1.0', tk.END)

        # Check if the location is available
        if not self.get_location():
            return

        # Retrieve the AQI data and display it
        self.get_aqi()
        self.display_aqi()

# ---------------------- GET AQI FORECAST -------------------------------- #
    def get_aqi_forecast(self):
        """Get the AQI forecast for the given location."""
        # Clear the results display area
        self.results_display.delete('1.0', tk.END)

        # Check if the location is available
        if not self.get_location():
            return

        # Retrieve the AQI forecast data and display it
        self.display_aqi_forecast()

# ---------------------- GET AQI ----------------------------------------- #
    def get_aqi(self):
        """
        Retrieves the Air Quality Index (AQI) data 
        Updates the instance variables with the relevant information.
        """
        # Extract the AQI data from the JSON response
        data = self.data.get("data", {})
        # Extract the sensor location, AQI, and dominant pollutant
        self.sensor_location = data.get("city", {}).get("name", "N/A")
        # Extract the AQI value
        self.aqi = data.get("aqi", "N/A")
        # Convert the AQI value to a string
        self.aqi_string = weather_utils.aqi_to_string(self.aqi)

        iaqi = data.get("iaqi", {})
        self.o3 = iaqi.get("o3", {}).get("v", "NA")
        self.pm25 = iaqi.get("pm25", {}).get("v", "NA")
        self.pm10 = iaqi.get("pm10", {}).get("v", "NA")
        self.co = iaqi.get("co", {}).get("v", "NA")
        self.so2 = iaqi.get("so2", {}).get("v", "NA")
        self.no2 = iaqi.get("no2", {}).get("v", "NA")

        self.dom_pol = data.get("dominentpol", "N/A")

        forecast = data.get("forecast", {}).get("daily", {})
        uvi_data = forecast.get("uvi", [{}])[0]
        self.uvi = uvi_data.get("avg", "NA")
        self.uvi_string = weather_utils.uvi_to_string(self.uvi)

        temp = round(iaqi.get("t", {}).get("v", 0), 1)
        self.temperature = round(((temp * 9.0)/5.0) + 32, 2)

        self.humidity = iaqi.get("h", {}).get("v", "NA")

        wind_speed_kph = iaqi.get("w", {}).get("v", 0)
        self.wind_speed_mph = round(wind_speed_kph * .0621371, 1)

        pressure = iaqi.get("p", {}).get("v", 0)
        self.pressure = round(pressure * .02953, 2)

# ---------------------- DISPLAY AQI ------------------------------------- #
    def display_aqi(self):
        """Display AQI results in the results display area."""
        result = f"\n {self.address}\n"
        result += f" {'Sensor Location:':<15} {self.sensor_location}\n"
        result += f"{'-'*70}\n"
        result += f" {'AQI:':>27} {self.aqi} {self.aqi_string}\n"
        result += f" {'Dominant Pollutant:':>27} {self.dom_pol}\n"
        result += f" {'Ozone (O₃):':>27} {self.o3}\n"
        result += f" {'Fine Particulates (PM25):':>27} {self.pm25}\n"
        result += f" {'Coarse Particulates (PM10):':>27} {self.pm10}\n"
        result += f" {'Carbon Monoxide (CO):':>27} {self.co}\n"
        result += f" {'Sulfur Dioxide (SO₂):':>27} {self.so2}\n"
        result += f" {'Nitrogen Dioxide (NO₂):':>27} {self.no2}\n"
        result += f" {'UV Index:':>27} {self.uvi} {self.uvi_string}\n"
        result += f" {'Temperature:':>27} {self.temperature}°F\n"
        result += f" {'Humidity:':>27} {self.humidity}%\n"
        result += f" {'Wind Speed:':>27} {self.wind_speed_mph} mph\n"
        result += f" {'Pressure:':>27} {self.pressure} inHg\n"

        # Insert the formatted result into the GUI display
        self.results_display.insert(tk.END, result)
        # Set focus to the city entry widget
        self.city_entry.focus()
        # Select the text in the city entry widget
        self.city_entry.select_range(0, tk.END)

# ---------------------- DISPLAY AQI FORECAST ---------------------------- #
    def display_aqi_forecast(self):
        """
        Display the AQI forecast for a given address.
        Retrieves the forecast data from the API response 
        Formats it into a readable string.
        The forecast includes the daily average values for 
        ozone (o3) and particulate matter (pm25).
        """
        # Get sensor location from the API response
        sensor_location = self.data.get(
            "data", {}).get(
            "city", {}).get("name", "N/A")
        
        # Get the forecast data from the API response
        forecast = self.data.get("data", {}).get(
            "forecast", {}).get("daily", {})

        # Extract o3 (ozone) and pm25 (particulate matter) forecast data
        o3_slice = forecast.get("o3", [])
        pm10_slice = forecast.get("pm10", [])
        pm25_slice = forecast.get("pm25", [])
        uvi_slice = forecast.get("uvi", [])

        # Initialize the result string with the address
        result = f"\n {self.address}\n"

        # Extract the sensor location from the API response
        result += f" {'Sensor Location:':<15} {sensor_location}\n"

        # Add a separator line to the result string
        result += f"{'-'*70}\n"

        # Add headers for the forecast data to the result string
        result += f" {'o3':>15} {'pm10':>5} {'pm25':>5} {'uvi':>4}\n"

        # Format the forecast data into a readable string
        for o3, pm10, pm25, uvi in zip(o3_slice, pm10_slice, pm25_slice, uvi_slice):
            day = o3.get('day', 'N/A')
            o3 = o3.get('avg', 'N/A')
            pm10 = pm10.get('avg', 'N/A')
            pm25 = pm25.get('avg', 'N/A')
            uvi = uvi.get('avg', 'N/A')

            # For each day in the forecast, add a line with the
            # date, o3, pm10, pm25 and uvi average
            result += f"{day}: {o3:>4} {pm10:> 4} {pm25:>5} {uvi:>4}\n"

        # Insert the formatted result into the GUI display
        self.results_display.insert(tk.END, result)
        self.city_entry.focus()
        self.city_entry.select_range(0, tk.END)

# ---------------------- CREATE WIDGETS ---------------------------------- #
    def create_widgets(self):
        """Create and place the widgets in the main window."""
        # Location input frame
        location_frame = ttk.Frame(self.master)
        location_frame.pack(pady=10)

        # City input
        ttk.Label(location_frame, text="City:").grid(
            row=0, column=0, padx=5, pady=5, sticky='e')
        self.city_entry = ttk.Entry(location_frame, width=30)
        self.city_entry.insert(0, "Scottsbluff")
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)

        # State input
        ttk.Label(location_frame, text="State:").grid(
            row=1, column=0, padx=5, pady=5, sticky='e')
        self.state_entry = ttk.Entry(location_frame, width=30)
        self.state_entry.insert(0, "NE")
        self.state_entry.grid(row=1, column=1, padx=5, pady=5)

        # Country input
        ttk.Label(location_frame, text="Country:").grid(
            row=2, column=0, padx=5, pady=5, sticky='e')
        self.country_entry = ttk.Entry(location_frame, width=30)
        self.country_entry.insert(0, "US")
        self.country_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Get Current AQI",
                   command=self.get_current_aqi).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Get AQI Forecast",
                   command=self.get_aqi_forecast).pack(side=tk.LEFT, padx=5)

        # Results display
        self.results_display = scrolledtext.ScrolledText(
            self.master, width=70, height=20)
        self.results_display.pack(pady=10)


def main():
    root = tk.Tk()
    app = AQICNGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
