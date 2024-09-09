"""
    Name: aqicn_cli.py
    Author:
    Created:
    Purpose: OOP console app
"""

import weather_utils
import aqicn_class
import os


# ------------------------------ MENU -------------------------------------#
def menu():
    """Print menu for user, return menu choice"""
    print("", "-"*70)
    print(f" [1] Get current AQI")
    print(f" [2] Get AQI forecast")
    print(f" [3] Get new location")
    menu_choice = input(f" [Enter] to quit. Enter your choice: ")
    return menu_choice


# ---------------------- MAIN PROGRAM -------------------------------------#
def main():
    clear_console()
    print(weather_utils.title("  World Air Quality Project App  "))

    # Create program object
    aqicn = aqicn_class.AQICNClass()

    aqicn.get_location()

    # Menu loop
    while True:
        # Display menu choices
        menu_choice = menu()

        # If the user presses the enter key, exit program
        if menu_choice == "":
            # Exit loop
            break

        # Get and display the current weather and air quality
        elif menu_choice == "1":
            clear_console()
            aqicn.get_aqi()
            aqicn.display_aqi()
        # Get and display 12 hour forecast
        elif menu_choice == "2":
            clear_console()
            aqicn.get_aqi_forecast()
        # Get and display 48 hour forecast
        elif menu_choice == "3":
            clear_console()
            aqicn.get_location()


def clear_console():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')


# Call main method to start the program
main()
