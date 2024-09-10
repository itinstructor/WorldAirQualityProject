"""
    Name: weather_utils.py
    Author: William A Loring
    Created: 06/20/2021
    Purpose: 
"""
import datetime


# ----------------------- ASCII DECORATED TITLE --------------------------- #
def title(statement):
    """
        Takes in a string argument
        returns a string with ascii decorations
    """
    # Get the length of the statement
    text_length = len(statement)

    # Create the title string
    # Initialize the result string variable
    result = ""
    result = result + "+--" + "-" * text_length + "--+\n"
    result = result + "|  " + statement + "  |\n"
    result = result + "+--" + "-" * text_length + "--+"

    # Return the contatenated title string
    return result


# --------------------------- AQI TO STRING ------------------------------ #
def aqi_to_string(aqi):
    aqi_string = "None"
    if aqi <= 50:
        aqi_string = "Good"
    elif aqi <= 100:
        aqi_string = "Moderate"
    elif aqi <= 150:
        aqi_string = "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        aqi_string = "Unhealthy"
    elif aqi <= 300:
        aqi_string = "Very Unhealthy"
    elif aqi > 301:
        aqi_string = "Hazardous"
    else:
        aqi_string = "None"
    return aqi_string


# --------------------------- UV INDEX STRING ------------------------------#
def uvi_to_string(uvi):
    if uvi >= 11:
        uvi_string = "Extreme"
    elif uvi >= 8:
        uvi_string = "Very High"
    elif uvi >= 6:
        uvi_string = "High"
    elif uvi >= 3:
        uvi_string = "Moderate"
    elif uvi >= 0:
        uvi_string = "Low"

    return uvi_string


# ------------------- CONVERT TO CELSIUS TO FAHRENHEIT ------------------- #
def celsius_to_fahrenheit(celsius):
    return round((((celsius * 9) / 5) + 32), 1)


# --------------------------- CONVERT TIME ------------------------------- #
def convert_day_time(unix_time):
    """
        Convert GMT Unix timestamp to local day, month, year
    """
    # Convert Unix timestamp to Python datetime
    local_time = datetime.datetime.fromtimestamp(unix_time)

    # Format the date to hours, AM PM
    local_time = local_time.strftime("%m/%d/%Y")

    # Strip out the leading 0's
    local_time = local_time.lstrip("0")
    return local_time


# --------------------------- CONVERT TIME ------------------------------- #
def convert_hourly_time(time):
    """
        Convert GMT Unix time to local hourly time
    """
    # Convert Unix timestamp to Python datetime
    time = datetime.datetime.fromtimestamp(time)

    # Format the date to hours, AM PM
    time = time.strftime("%I:%S %p")

    # Strip out the leading 0's
    time = time.lstrip("0")
    return time


# ----------------------------- CONVERT TIME --------------------------------#
def convert_time(time):
    """
        Convert GMT Unix time to local time
    """
    # Convert Unix timestamp to local Python datetime
    time = datetime.datetime.fromtimestamp(time)
    # Format the date to hours, minutes, seconds, AM PM
    time = f"{time:%I:%M:%S %p}"
    # Strip out the leading 0's: 01 becomes 1
    time = time.lstrip("0")
    # Return GMT Unix as local Python time object
    return time
