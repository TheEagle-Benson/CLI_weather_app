import requests
from weather_codes import weather_codes
from datetime import datetime
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
from rich.table import  Table
console = Console()
table = Table(show_header=True, header_style='bold magenta')
install()


def get_country_coordinates(place: str = 'Accra', country: str = 'Ghana'):
    try:
        geocoding = f'https://geocoding-api.open-meteo.com/v1/search?name={place}&count=100&language=en&format=json'
        lat = None
        long = None
        res = requests.get(geocoding)
        data = res.json()
        if not 'results' in data:
            return console.print('An error occurred, check your input and try again', style='bold italic red')
        for index in range(0, 100):
            for key in data['results'][index]:
                if key == 'country' and country in data['results'][index][key]:
                    lat = data['results'][index]['latitude']
                    long = data['results'][index]['longitude']
            break
        return lat, long
    except requests.exceptions.RequestException:
        return console.print('An error occurred', style='bold italic red')


def get_responses(coordinates: tuple) -> tuple:
    lat, long = coordinates
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max,weather_code&current=temperature_2m,weather_code,wind_speed_10m,wind_direction_10m,relative_humidity_2m&timezone=GMT'

    response = requests.get(url)
    data = response.json()
    current_units = data['current_units']
    current_values = data['current']
    daily_units = data['daily_units']
    daily_values = data['daily']
    return current_units, current_values, daily_units, daily_values


def weather_code_to_text(code: int = 0) -> str:
    description_emoji = list(weather_codes[code])
    return f'[white]{description_emoji[1]}[/] {description_emoji[0]}'

def iso8601_to_everyday(time: str) -> str:
    dt = datetime.fromisoformat(time)
    readable_time = dt.strftime('%B %d, %Y %I:%M %p')
    return readable_time


def display_weather_info(response: tuple):
    if not response:
        return
    current_units, current_values, daily_units, daily_values = response

    console.print(
        Panel(
            f'Current Temperature: [bold green]{current_values["temperature_2m"]}{current_units["temperature_2m"]}\n[/]'
            f'Current Weather: [bold green]{weather_code_to_text(current_values["weather_code"])}\n[/]'
            f'Current Wind Speed: [bold green]{current_values["wind_speed_10m"]} {current_units["wind_speed_10m"]}\n[/]'
            f'Current Wind Direction: [bold green]{current_values["wind_direction_10m"]}{current_units["wind_direction_10m"]}\n[/]'
            f'Current Humidity: [bold green]{current_values["relative_humidity_2m"]}{current_units["relative_humidity_2m"]}[/]',
            title='Current Weather Information',
            subtitle='Source: Open-Meteo',
            subtitle_align='right',
            border_style='blue',
            style='bold',
            highlight=True
        )
    )

    print('')
    print('Daily Weather Information')
    print('')
    table.add_column('Time', style='cyan', no_wrap=True)
    table.add_column('Max Temperature(°C)', style='magenta')
    table.add_column('Min Temperature(°C)', style='magenta')
    table.add_column('Precipitation Probability(%)', style='magenta')
    table.add_column('Sunrise(h:m)', style='magenta')
    table.add_column('Sunset(h:m)', style='magenta')
    table.add_column('UV Index', style='magenta')
    table.add_column('Weather Condition', style='magenta')
    for index in range(0, 7):
        table.add_row(f'{daily_values["time"][index]}', f'{daily_values["temperature_2m_max"][index]}', f'{daily_values["temperature_2m_min"][index]}', f'{daily_values["precipitation_probability_max"][index]}', f'{iso8601_to_everyday(daily_values["sunrise"][index])}', f'{iso8601_to_everyday(daily_values["sunset"][index])}', f'{daily_values["uv_index_max"][index]}', f'{weather_code_to_text(daily_values["weather_code"][index])}')
        print(f'{daily_values["time"][index]}    | {daily_values["temperature_2m_max"][index]}    | {daily_values["temperature_2m_min"][index]}    | {daily_values["precipitation_probability_max"][index]}    | {iso8601_to_everyday(daily_values["sunrise"][index])}    | {iso8601_to_everyday(daily_values["sunset"][index])}    | {daily_values["uv_index_max"][index]}    | {weather_code_to_text(daily_values["weather_code"][index])}')
    console.print(table)



def main():
    user_input = console.input('Enter the [italic magenta]town[/] and [italic magenta]country[/] in the [italic magenta]format town,country[/]: ')
    user_input_list = user_input.split(',')
    if len(user_input_list) != 2:
        console.print('Invalid input', style='bold red italic')
        return
    place = user_input_list[0].capitalize()
    country = user_input_list[1].lstrip().capitalize()
    if place == ''  or country == '':
        console.print('Not Found, try again', style='bold red italic')
        return
    search_query = get_country_coordinates(place, country)
    print(search_query)
    if not search_query:
        return
    response = get_responses(search_query)
    display_weather_info(response)

if __name__ == '__main__':
    main()