import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import requests
import api_key
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import weather_utils
from ui_main import Ui_MainWindow

AQICN_ENDPOINT = 'https://api.waqi.info/feed/geo:'


def geocode(city, state, country):
    geolocator = Nominatim(user_agent="aqicn_app")
    address = ", ".join(filter(None, [city, state, country]))

    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude, location.address
        else:
            raise ValueError("Location not found")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise Exception(f"Geocoding service unavailable: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred during geocoding: {str(e)}")


class AQICNGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.load_ui()
        self.setupUi(self)
        self.setup_connections()

    def load_ui(self):
        loader = QUiLoader()
        ui_file = QFile("main.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def setup_connections(self):
        self.currentAQIButton.clicked.connect(self.get_current_aqi)
        self.aqiForecastButton.clicked.connect(self.get_aqi_forecast)

    def get_location(self):
        city = self.cityLineEdit.text().strip()
        state = self.stateLineEdit.text().strip()
        country = self.countryLineEdit.text().strip()

        if not any([city, state, country]):
            self.resultsTextEdit.append(
                "Please enter at least one location field.")
            return False

        try:
            lat, lng, self.address = geocode(city, state, country)
            response = requests.get(
                AQICN_ENDPOINT + str(lat) + ";" + str(lng)
                + "/?token=" + api_key.API_KEY
            )

            if response.status_code == 200:
                self.data = response.json()
                return True
            else:
                self.resultsTextEdit.append(
                    "[-] API unavailable. Please try again.")
                return False
        except Exception as e:
            self.resultsTextEdit.append(f"[-] Error: {str(e)}")
            return False

    def get_current_aqi(self):
        self.resultsTextEdit.clear()
        if not self.get_location():
            return

        self.get_aqi()
        self.display_aqi()

    def get_aqi_forecast(self):
        self.resultsTextEdit.clear()
        if not self.get_location():
            return

        self.display_aqi_forecast()

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

    def display_aqi_forecast(self):
        forecast = self.data.get("data", {}).get(
            "forecast", {}).get("daily", {})
        o3_slice = forecast.get("o3", [])
        pm25_slice = forecast.get("pm25", [])

        result = f"\n {self.address}\n"
        result += f" {'Sensor Location:':<15} {self.data.get(
            'data', {}).get('city', {}).get('name', 'N/A')}\n"
        result += f"{'-'*70}\n"
        result += f" {'o3':>16} {'pm25':>5}\n"

        for o3, pm25 in zip(o3_slice, pm25_slice):
            result += f"{o3.get('day', 'N/A')}: {o3.get('avg', 'N/A')
                                :>4} {pm25.get('avg', 'N/A'):>5}\n"

        self.resultsTextEdit.append(result)


def main():
    app = QApplication(sys.argv)
    window = AQICNGui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
