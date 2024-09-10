"""
    Name: geocode_geopy.py
    Author: William A Loring
    Created: 07/10/2021
    Purpose: Geocode using Nominatim from geopy
"""

# pip install geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# For testing
# LAT = 41.8666
# LON = -103.6672


def main():
    # For testing
    geocode()
    # reverse_geocode(LAT, LON)


# ---------------------- GEOCODE ARG ------------------------------------- #
def geocode_arg(city, state, country):
    """
    Geocodes given location information using the Nominatim geocode service.
    Args:
        city (str): The name of the city.
        state (str): The name of the state.
        country (str): The name of the country.
    Returns:
        tuple: A tuple containing the latitude, longitude, and 
        address of the location.
    Raises:
        ValueError: If the location is not found.
        Exception: If the geocoding service is unavailable.
    """
    try:
        # Create geolocator object with Nominatim geocode service
        geolocator = Nominatim(user_agent="location_practice")
        # Create location dictionary for request
        location = {
            "city": city,
            "state": state,
            "country": country
        }
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude, loc.address)
        else:
            raise ValueError("Location not found")

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise Exception(f"Geocoding service unavailable: {str(e)}")
    except Exception as e:
        print(f"An error occurred while geocoding: {str(e)}")


# ---------------------- GEOCODE ----------------------------------------- #
def geocode():
    """
    Geocodes a location using the Nominatim geocode service.
    Returns:
        tuple: A tuple containing the latitude, longitude, 
        and address of the geocoded location.
    Raises:
        ValueError: If the location is not found.
        Exception: If the geocoding service is unavailable.
    """
    try:
        # Create geolocator object with Nominatim geocode service
        # Nominatim is a free geolocater that uses openstreetmaps.org
        geolocator = Nominatim(user_agent="location_practice")

        # Get location input from user
        city = input("Enter city: ")
        state = input("Enter state: ")
        country = input("Enter country: ")

        # Create location dictionary for request
        location = {
            "city": city,
            "state": state,
            "country": country
        }

        loc = geolocator.geocode(location)
        if location:
            return loc.latitude, loc.longitude, loc.address
        else:
            raise ValueError("Location not found")

        # For testing purposes
        # print(geo_location.raw)
        # print(geo_location.address)
        # print((geo_location.latitude, geo_location.longitude))

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise Exception(f"Geocoding service unavailable: {str(e)}")
    except:
        print("An error occured while geocoding.")


# ---------------------- REVERSE GEOCODE --------------------------------- #
def reverse_geocode(lat, lon):
    """
    Reverse geocodes the given latitude and longitude coordinates.
    Parameters:
    - lat (float): The latitude coordinate.
    - lon (float): The longitude coordinate.
    Returns:
    - address (str): The address corresponding to the given coordinates.
    Raises:
    - Exception: If an error occurs while reverse geocoding.
    """
    try:
        # Create geolocator object
        geolocator = Nominatim(user_agent="location_practice")

        # Create location tuple
        location = (lat, lon)

        # Get address with resolution of town
        address = geolocator.reverse(location, zoom=10)

        return address
    except:
        print("An error occured while reverse geocoding.")


# If a standalone program, call the main function
# Else, use as a module
if __name__ == '__main__':
    main()
