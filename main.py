import requests

def get_country_coordinates(place: str = 'Accra', country: str = 'Ghana') -> tuple:
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


def get_responses(coordinates: tuple):
    url = 'https://api.open-meteo.com/v1/forecast?latitude=5.6916&longitude=-0.2&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max&current=temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,relative_humidity_2m&timezone=GMT'

    lat, long = coordinates



def display_weather_data():
    pass

def main():
    user_input = input('Enter the town and country in the format(town,country): ')
    user_input_list = user_input.split(',')
    if len(user_input_list) != 2:
        print('Invalid input')
        return
    place = user_input_list[0]
    country = user_input_list[1]
    val = get_country_coordinates(place, country)
    print(val)

if __name__ == '__main__':
    main()