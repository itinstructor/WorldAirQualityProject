"""
    Name: aqicn_pyside.py
    Author: William Loring
    Created: 09/07/2024
    Purpose: World Air Quality Index PySidew6 GUI
    Claude AI used as a code helper
"""
import sys
# pip install PySide6
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
# pip install requests
import requests
import api_key
# pip install geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import weather_utils
from ui_main import Ui_MainWindow

AQICN_ENDPOINT = 'https://api.waqi.info/feed/geo:'


def geocode(city, state, country):
    """
    Function to get the latitude, longitude, and formatted address for a given location
    """
    # Initialize a geolocator object using the Nominatim service (part of OpenStreetMap)
    geolocator = Nominatim(user_agent="aqicn_app")

    # Create a single address string by joining the city, state, and country,
    # filtering out any None values
    address = ", ".join(filter(None, [city, state, country]))

    try:
        # Use the geolocator to get the location details
        # (latitude, longitude, address) for the given address
        location = geolocator.geocode(address)

        # If location is found, return the latitude, longitude, and address
        if location:
            return location.latitude, location.longitude, location.address
        else:
            # If no location is found, raise a ValueError
            raise ValueError("Location not found")

    # Handle exceptions related to geocoding timeouts or service unavailability
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise Exception(f"Geocoding service unavailable: {str(e)}")

    # Handle any other exceptions that might occur during geocoding
    except Exception as e:
        raise Exception(f"An error occurred during geocoding: {str(e)}")


class AQICNGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        # Set the window icon
        self.setWindowIcon(QIcon("edit_clear.png"))
        self.setup_connections()

# ---------------------------- SETUP CONNECTIONS ------------------------- #
    def setup_connections(self):
        # Connect the currentAQIButton's clicked signal to the
        # get_current_aqi method
        self.currentAQIButton.clicked.connect(self.get_current_aqi)

        # Connect the aqiForecastButton's clicked signal to the
        # get_aqi_forecast method
        self.aqiForecastButton.clicked.connect(self.get_aqi_forecast)

# ---------------------------- GET LOCATION ------------------------------ #
    def get_location(self):
        # Get the city, state, and country input from the UI fields
        # and remove any leading/trailing whitespace
        city = self.cityLineEdit.text().strip()
        state = self.stateLineEdit.text().strip()
        country = self.countryLineEdit.text().strip()

        # If none of the location fields (city, state, country) are filled,
        # prompt the user and stop
        if not any([city, state, country]):
            self.resultsTextEdit.append(
                "Please enter at least one location field.")
            return False

        try:
            # Geocode the input location to get
            # latitude, longitude, and formatted address
            lat, lng, self.address = geocode(city, state, country)

            # Make a request to the AQI (Air Quality Index) API
            # using the geocoded coordinates
            response = requests.get(
                AQICN_ENDPOINT + str(lat) + ";" + str(lng)
                + "/?token=" + api_key.API_KEY
            )

            # Check if the response from the API was successful
            if response.status_code == 200:
                # Parse the response as JSON and store the data
                self.data = response.json()
                return True
            else:
                # If API is unavailable, notify the user
                self.resultsTextEdit.append(
                    "[-] API unavailable. Please try again.")
                return False

        except Exception as e:
            # Catch any exceptions and display an error message
            # in the results text area
            self.resultsTextEdit.append(f"[-] Error: {str(e)}")
            return False

# ---------------------- GET CURRENT AQI --------------------------------- #
    def get_current_aqi(self):
        # Clear the results text area before displaying new results
        self.resultsTextEdit.clear()

        # If the location is not found, return
        if not self.get_location():
            return

        # Get the AQI data and display it
        self.get_aqi()
        self.display_aqi()

# ---------------------- GET AQI FORECAST -------------------------------- #
    def get_aqi_forecast(self):
        # Clear the results text area before displaying new results
        self.resultsTextEdit.clear()

        # If the location is not found, return
        if not self.get_location():
            return

        # Get the AQI forecast data and display it
        self.display_aqi_forecast()

# ---------------------------- GET AQI ----------------------------------- #
    def get_aqi(self):
        data = self.data.get("data", {})
        self.sensor_location = data.get("city", {}).get("name", "N/A")
        self.aqi = data.get("aqi", "N/A")
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

# ---------------------------- DISPLAY AQI ------------------------------- #
    def display_aqi(self):
        result = f"\n {self.address}\n"
        result += f" {'Sensor Location:':<15} {self.sensor_location}\n"
        result += f"{'-'*70}\n"
        result += f" {'AQI:':<27} {self.aqi} {self.aqi_string}\n"
        result += f" {'Dominant Pollutant:':<27} {self.dom_pol}\n"
        result += f" {'Ozone (O₃):':<27} {self.o3}\n"
        result += f" {'Fine Particulates (PM25):':<27} {self.pm25}\n"
        result += f" {'Coarse Particulates (PM10):':<27} {self.pm10}\n"
        result += f" {'Carbon Monoxide (CO):':<27} {self.co}\n"
        result += f" {'Sulfur Dioxide (SO₂):':<27} {self.so2}\n"
        result += f" {'Nitrogen Dioxide (NO₂):':<27} {self.no2}\n"
        result += f" {'UV Index:':<27} {self.uvi} {self.uvi_string}\n"
        result += f" {'Temperature:':<27} {self.temperature}°F\n"
        result += f" {'Humidity:':<27} {self.humidity}%\n"
        result += f" {'Wind Speed:':<27} {self.wind_speed_mph} mph\n"
        result += f" {'Pressure:':<27} {self.pressure} inHg\n"

        self.resultsTextEdit.append(result)

# ---------------------- DISPLAY AQI FORECAST ---------------------------- #
    def display_aqi_forecast(self):
        forecast = self.data.get(
            "data", {}).get(
            "forecast", {}).get("daily", {})
        o3_slice = forecast.get("o3", [])
        pm10_slice = forecast.get("pm10", [])
        pm25_slice = forecast.get("pm25", [])
        uvi_slice = forecast.get("uvi", [])

        result = f"\n {self.address}\n"
        result += f" {'Sensor Location:':<15} {self.data.get(
            'data', {}).get('city', {}).get('name', 'N/A')}\n"
        result += f"{'-'*70}\n"
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

        self.resultsTextEdit.append(result)


def main():
    app = QApplication(sys.argv)
    window = AQICNGui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
