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
        sensor_location = self.data.get("data").get("city").get("name")
        forecast = self.data.get("data").get("forecast").get("daily")

        o3_slice = forecast.get("o3")[:]
        pm25_slice = forecast.get("pm25")[:]
        # if forecast.get("uvi") != None:
        #     uvi_slice = forecast.get("uvi")[:]
        # else:
        #     uvi_slice = []

        print(f'\n {self.address}')
        print(f' {"Sensor Location:":15} {sensor_location}')
        print("", "-"*70)
        print(f' {"o3":>16} {" pm25":{WIDTH}} {"   uvi":{WIDTH}}')

        # Iterate through list of dictionaries
        # for x, y, z in map(None, o3_slice, pm25_slice, uvi_slice):
        # for x, y, z in zip_longest(o3_slice, pm25_slice, uvi_slice, fillvalue="NA"):
        # for x, y, z in zip(o3_slice, pm25_slice, uvi_slice):
        #     print(
        #         f'{x.get("day")}: {x.get("avg"):{WIDTH}} {y.get("avg"):{WIDTH}} {z.get("avg"):{WIDTH}} {weather_utils.uvi_to_string(z.get("avg"))}')
        for x, y, in zip(o3_slice, pm25_slice):
            print(
                f'{x.get("day")}: {x.get("avg"):{WIDTH}} {y.get("avg"):{WIDTH}}')

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
        print(f'\n {self.address}')
        print(f' {"Sensor Location:":15} {self.sensor_location}')
        print("", "-"*70)
        print(f' {"AQI:":{self.WIDTH}} {self.aqi} {self.aqi_string}')
        print(f' {"Dominant Pollutant:":{self.WIDTH}} {self.dom_pol}')
        print(f' {"Ozone (O₃):":{self.WIDTH}} {self.o3}')
        print(f' {"Fine Particulates (PM25):":{self.WIDTH}} {self.pm25}')
        print(f' {"Coarse Particulates (PM10):":{self.WIDTH}} {self.pm10}')
        print(f' {"Carbon Monoxide (CO):":{self.WIDTH}} {self.co}')
        print(f' {"Sulfur Dioxide (SO₂):":{self.WIDTH}} {self.so2}')
        print(f' {"Nitrogen Dioxide (NO₂):":{self.WIDTH}} {self.no2}')
        print(f' {"UV Index:":{self.WIDTH}} {self.uvi} {self.uvi_string}')
        print(f' {"Temperature:":{self.WIDTH}} {self.temperature}°F')
        print(f' {"Humidity:":{self.WIDTH}} {self.humidity}%')
        print(f' {"Wind Speed:":{self.WIDTH}} {self.wind_speed_mph} mph')
        print(f' {"Pressure:":{self.WIDTH}} {self.pressure} inHg')
