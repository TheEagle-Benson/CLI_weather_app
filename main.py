import requests
from weather_codes import weather_codes

def get_country_coordinates(place: str = 'Accra', country: str = 'Ghana') -> tuple:
    try:
        geocoding = f'https://geocoding-api.open-meteo.com/v1/search?name={place}&count=100&language=en&format=json'
        lat = None
        long = None
        res = requests.get(geocoding)
        for index in range(0, 100):
            for key in res.json()['results'][index]:
                if key == 'country' and country in res.json()['results'][index][key]:
                    lat = res.json()['results'][index]['latitude']
                    long = res.json()['results'][index]['longitude']
            break
        return lat, long
    except requests.exceptions.RequestException:
        print('An error occurred:')
        return None, None


def get_responses(coordinates: tuple) -> tuple:
    lat, long = coordinates
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max&current=temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,relative_humidity_2m&timezone=GMT'

    response = requests.get(url)
    data = response.json()
    current_units = data['current_units']
    current_values = data['current']
    daily_units = data['daily_units']
    daily_values = data['daily']
    return current_units, current_values, daily_units, daily_values


def weather_code_to_text(code: int = 0) -> str:
    description_emoji = list(weather_codes[code])
    return f'{description_emoji[1]} {description_emoji[0]}'


def display_weather_info(response: tuple):
    current_units, current_values, daily_units, daily_values = response
    print(f'daily_units: {daily_units}')
    print(f'daily_values: {daily_values}')


    print(f'Current Temperature: {current_values["temperature_2m"]} {current_units["temperature_2m"]}')
    print(f'Current Weather: {weather_code_to_text(current_values["weather_code"])}')
    print(f'Current Wind Speed: {current_values["wind_speed_10m"]} {current_units["wind_speed_10m"]}')
    print(f'Current Wind Direction: {current_values["wind_direction_10m"]} {current_units["wind_direction_10m"]}')
    print(f'Current Humidity: {current_values["relative_humidity_2m"]} {current_units["relative_humidity_2m"]}')













def main():
    user_input = input('Enter the town and country in the format(town,country): ')
    user_input_list = user_input.split(',')
    if len(user_input_list) != 2:
        print('Invalid input')
        return
    place = user_input_list[0].capitalize()
    country = user_input_list[1].capitalize()
    search_query = get_country_coordinates(place, country)
    if not search_query[0]  or not search_query[1] :
        print('Not Found, try again')
        return
    print(search_query)
    response = get_responses(search_query)
    display_weather_info(response)

if __name__ == '__main__':
    main()