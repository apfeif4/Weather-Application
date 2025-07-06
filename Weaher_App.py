# Weather app
# Author Andrew Pfeifer
# 8/11/2023
import requests


def get_city(payload):
    # Unpacking dictionary items to shorten the format length for the url.
    country = payload['country code']
    state = payload['state id']
    city = payload['city name']
    api = payload['api key']
    # Formatting URL with user input to search by city.
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{country}&limit=1&appid={api}'
    try:
        # Response makes call to server to obtain weather datat.
        response = requests.get(url)
        # Weather data loaded to dictionary.
        weather_data = response.json()

    except requests.ConnectionError as e:
        print("A connection error occurred. ", e)
    except requests.HTTPError as e:
        print("An HTTP error occurred. ", e)
    else:

        try:
            # Pulls lat, lon and city from weather data.
            lon = str(weather_data[0]['lon'])
            lat = str(weather_data[0]['lat'])
            city = weather_data[0]['name']

        except KeyError:
            print("Location not found. Please check your input.")
        except IndexError:
            print("Location not found. Please check your input.")
        else:
            # Adding longitude, latitude, and city name to payload dictionary.
            payload['lat'] = lat
            payload['lon'] = lon
            payload['city'] = city
            # The new information that's added is sent to the get weather function. no return needed.
            get_weather(payload)


def get_zip(payload):
    # Unpacking payload items to shorten the formatting for the url.
    zip_code = payload["zip code"]
    country = payload['country code']
    api = payload['api key']
    # URL is formatted for searches by zip code.
    url = f'http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country}&appid={api}'

    try:
        # Makes call to the server to obtain the weather data based on zip code.
        response = requests.get(url)
        # Loads the weather data to a dictionary.
        weather_data = response.json()

    except requests.ConnectionError as e:
        print("A connection error occurred. ", e)
    except requests.HTTPError as e:
        print("An HTTP error occurred. ", e)
    else:

        try:
            # Pulls lat, lon and city from weather data.
            lon = str(weather_data['lon'])
            lat = str(weather_data['lat'])
            city = weather_data['name']

        except KeyError:
            print("Location not found. Please check your input.")
        except IndexError:
            print("Location not found. Please check your input.")
        else:
            # Adding longitude, latitude, and city name to payload dictionary.
            payload['lat'] = lat
            payload['lon'] = lon
            payload['city'] = city
            # The new information that's added is sent to the get weather function. no return needed.
            get_weather(payload)


def get_weather(payload):
    # Gets the unit measurement url based on user input.
    unit_url = get_unit(payload)
    # Unpacks the lat,  lon, api key from the dictionary to shorten URL formatting.
    lat = payload['lat']
    lon = payload['lon']
    api_key = payload['api key']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}{unit_url}'

    try:
        # Sends request to get information from the server.
        response = requests.get(url)
    except requests.ConnectionError as e:
        print("A connection error occurred. ", e)
    except requests.HTTPError as e:
        print("An HTTP error occurred. ", e)
    else:

        weather_data = response.json()
        pretty_print(weather_data, payload['city'], payload['unit'])


def get_unit(payload):

    if payload['unit'] == 'c':
        measure = '&units=metric'
    elif payload['unit'] == 'k':
        measure = ''
    else:
        measure = '&units=imperial'

    return measure


def pretty_print(weather_data, city, unit):

    print("\nThe current weather for {} is:".format(city).title())
    print('-' * 39)
    # Formats output based on dict values.
    if unit == 'c':
        print("{:<16} {:>18}\u00b0C".format("Temperature: ", weather_data['main']['temp']))
        print("{:<16} {:>18}\u00b0C".format("Feels like: ", weather_data['main']['feels_like']))
        print("{:<16} {:>13}\u00b0C".format("Minimum temperature: ", weather_data['main']['temp_min']))
        print("{:<16} {:>13}\u00b0C".format("Maximum temperature: ", weather_data['main']['temp_max']))
    elif unit == 'f':
        print("{:<16} {:>18}\u00b0F".format("Temperature: ", weather_data['main']['temp']))
        print("{:<16} {:>18}\u00b0F".format("Feels like: ", weather_data['main']['feels_like']))
        print("{:<16} {:>13}\u00b0F".format("Minimum temperature: ", weather_data['main']['temp_min']))
        print("{:<16} {:>13}\u00b0F".format("Maximum temperature: ", weather_data['main']['temp_max']))
    elif unit == 'k':
        print("{:<16} {:>18} Kelvin".format("Temperature: ", weather_data['main']['temp']))
        print("{:<16} {:>18} Kelvin".format("Feels like: ", weather_data['main']['feels_like']))
        print("{:<16} {:>13} Kelvin".format("Minimum temperature: ", weather_data['main']['temp_min']))
        print("{:<16} {:>13} Kelvin".format("Maximum temperature: ", weather_data['main']['temp_max']))

    if unit == 'f':
        print("{:<16} {:>17} mph".format("Wind speed: ", weather_data['wind']['speed']))
    else:
        print("{:<16} {:>17} m/s".format("Wind speed: ", weather_data['wind']['speed']))

    print("{:<16} {:>17} hPa           ".format("Pressure: ", weather_data['main']['pressure']))
    print("{:<16} {:>18}%".format("Humidity: ", weather_data['main']['humidity']))
    print("{:<16} {:>16}".format("Currently outside: ", weather_data['weather'][0]['main']))
    print("{:<16} {:>17}".format("Conditions outside: ", weather_data['weather'][0]['description']))
    print('-' * 39 + "\n")


def main():

    api_key = 'a0989825ffe2b6082dfecd4faa09ae41'
    print("Welcome to the weather program!")

    while True:  # Starts main program loop.
        unit = str(input("What is the unit of measure you would like to see, enter '-1' to exit? celsius = c, "
                         "kelvin = k, fahrenheit = f\n")).lower().strip()
        if unit == '-1':
            break
        elif unit in ['c', 'k', 'f']:
            while True:  # starts to loop for city or zip.
                search_by = input("Would you like to search for weather by city or zip code? "
                                  "Enter '-1' to go back.\n").lower().strip()
                if search_by == '-1':
                    break
                elif search_by == "zipcode" or search_by == 'zip code' or search_by == 'zip':
                    while True:  # Start country code loop/ zip loop
                        country_code = str(input("Please enter the 2 digit country abbreviation. Enter '-1' to "
                                                 "go back.\n")).lower().strip()
                        if country_code == '-1':
                            break
                        elif len(country_code) != 2:
                            print('An invalid country code was entered.')
                        elif len(country_code) == 2:
                            zip_code = str(input("Please enter the zip code you want to look up.\n")).lower().strip()
                            payload = {"zip code": zip_code, "country code": country_code,  "api key": api_key,
                                       "unit": unit}
                            get_zip(payload)
                            print("Would you like to look up another city by zip code?")

                elif search_by == "city" or search_by == 'city name':
                    while True:  # Start city loop.
                        country_code = input("Please enter the 2 digit country abbreviation. enter '-1' "
                                             "to go back\n").lower().strip()
                        if country_code == '-1':
                            break
                        elif len(country_code) != 2:
                            print("An invalid country code was entered.")
                        elif len(country_code) == 2:
                            state_id = input("Please enter the 2 digit State abbreviation.\n").lower().strip()

                            if len(state_id) != 2:
                                print('An invalid state ID was entered.')
                            else:
                                city_name = input("Please enter the name of the city you "
                                                  "would like to look up.\n").lower().strip()
                                payload = {"city name": city_name, "state id": state_id, "country code": country_code,
                                           "api key": api_key, "unit": unit}
                                get_city(payload)
                                print("Would you like to look up weather by another city in this country?")

                else:
                    print("This is an invalid option.")
        else:
            print("This is an invalid option.")
    print("Thank you for using the weather program.")


if __name__ == "__main__":
    main()
