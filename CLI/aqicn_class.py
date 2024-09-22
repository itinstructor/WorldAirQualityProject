"""
    Name: aqicn_class.py
    Author: William Loring
    Created: 08/06/2021
    Purpose: World Air Quality Index class for AQICN API
"""

# pip install requests
import requests
import api_key
import geocode_geopy
import weather_utils

# Set this to False to only display the final results
IS_DEBUGGING = False

# URL for World Air Quality Index
AQICN_ENDPOINT = 'https://api.waqi.info/feed/geo:'


class AQICNClass:
    def __init__(self):
        self.WIDTH = 27

# ------------------------ GET LOCATION ----------------------------------- #
    def get_location(self):
        # Get location input from user
        try:
            # Return lat, lng, and address from geopy Nominatum
            lat, lng, self.address = geocode_geopy.geocode()

            # Use the requests.get() function
            # with the parameter of the url
            response = requests.get(
                AQICN_ENDPOINT + str(lat) + ";" + str(lng)
                + "/?token=" + api_key.API_KEY
            )

            # If the status_code is 200, successful connection and data
            if (response.status_code == 200):

                # Convert JSON data into a Python dictionary with key value pairs
                self.data = response.json()

                # Let user know the connection was successful
                print("\n [+] The connection to AQICN was successful.")

                # Used to debug process
                if (IS_DEBUGGING == True):

                    # Display the status code
                    print(
                        f'\n Status code: {response.status_code} \n')

                    # Display the raw JSON data
                    print(' Raw API data:')
                    print(response.text)

                    # Display the Python dictionary
                    print('\nThe JSON data converted to a Python dictionary:')
                    print(self.data)
            else:
                print('[-] API unavailable. You may want to try again')
                self.get_location()
        except Exception as e:
            print('[-] There was an error. You may want to try again')
            print(e)
            self.get_location()

# ------------------------ GET AQI FORECAST ------------------------------ #
    def get_aqi_forecast(self):
        WIDTH = 4
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

        print(f'\n {self.address}')
        print(f' {"Sensor Location:":15} {sensor_location}')
        print("", "-"*70)
        print(f" {'o3':>15} {'pm10':>5} {'pm25':>5} {'uvi':>4}")

        # Iterate through list of dictionaries
        # for x, y, z in map(None, o3_slice, pm25_slice, uvi_slice):
        # for x, y, z in zip_longest(o3_slice, pm25_slice, uvi_slice, fillvalue="NA"):
        # for x, y, z in zip(o3_slice, pm25_slice, uvi_slice):
        #     print(
        #         f'{x.get("day")}: {x.get("avg"):{WIDTH}} {y.get("avg"):{WIDTH}} {z.get("avg"):{WIDTH}} {weather_utils.uvi_to_string(z.get("avg"))}')
        for o3, pm10, pm25, uvi in zip(o3_slice, pm10_slice, pm25_slice, uvi_slice):

            day = o3.get('day', 'N/A')
            o3 = o3.get('avg', 'N/A')
            pm10 = pm10.get('avg', 'N/A')
            pm25 = pm25.get('avg', 'N/A')
            uvi = uvi.get('avg', 'N/A')

            # For each day in the forecast, add a line with the
            # date, o3, pm10, pm25 and uvi average
            result = f"{day}: {o3:>4} {pm10:> 4} {pm25:>5} {uvi:>4}"
            print(result)

# ------------------------ GET CURRENT AQI ------------------------------- #
    def get_aqi(self):
        self.sensor_location = self.data.get("data").get("city").get("name")
        self.aqi = self.data.get("data").get("aqi")
        self.aqi_string = weather_utils.aqi_to_string(self.aqi)

        # Ozone
        if "o3" in self.data.get("data").get("iaqi"):
            self.o3 = self.data.get("data").get("iaqi").get("o3").get("v")
        else:
            self.o3 = "NA"
        # Fine particulates PM25
        self.pm25 = self.data.get("data").get("iaqi").get("pm25").get("v")

        # Coarse particulates PM10
        if "pm10" in self.data.get("data").get("iaqi"):
            self.pm10 = self.data.get("data").get("iaqi").get("pm10").get("v")
        else:
            self.pm10 = "NA"

        # Carbon Monoxide
        if "co" in self.data.get("data").get("iaqi"):
            self.co = self.data.get("data").get("iaqi").get("co").get("v")
        else:
            self.co = "NA"

        # Sulphur Dioxide
        if "so2" in self.data.get("data").get("iaqi"):
            self.so2 = self.data.get("data").get("iaqi").get("so2").get("v")
        else:
            self.so2 = "NA"

        # Nitrogen Dioxide
        if "no2" in self.data.get("data").get("iaqi"):
            self.no2 = self.data.get("data").get("iaqi").get("no2").get("v")
        else:
            self.no2 = "NA"

        # ------- Dominant pollutant
        self.dom_pol = self.data.get("data").get("dominentpol")

        # ------- UV Index
        if "uvi" in self.data.get("data").get("forecast").get("daily"):
            self.uvi = self.data.get("data").get("forecast").get(
                "daily").get("uvi")[0].get("avg")
            self.uvi_string = weather_utils.uvi_to_string(self.uvi)
        else:
            self.uvi = "NA"
            self.uvi_string = "NA"

        # Celsius temperature
        temp = round(self.data.get("data").get("iaqi").get("t").get("v"), 1)
        # Convert to fahrenheit
        self.temperature = round(((temp * 9.0)/5.0) + 32, 2)

        self.humidity = self.data.get("data").get("iaqi").get("h").get("v")

        # Wind in kph
        wind_speed_kph = self.data.get("data").get("iaqi").get("w").get("v")
        # Convert to mph
        self.wind_speed_mph = round(wind_speed_kph * .0621371, 1)

        # Barometric pressure in mmHg
        pressure = self.data.get("data").get("iaqi").get("p").get("v")
        # Convert to mph
        self.pressure = round(pressure * .02953, 2)

# ------------------------ DISPLAY AQI ----------------------------------- #
    def display_aqi(self):
        """Print the data from dictionary created from the API data"""
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
        print(result)
