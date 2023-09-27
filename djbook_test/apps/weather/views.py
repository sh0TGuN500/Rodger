import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.humanize.templatetags import humanize
from datetime import datetime
from os import getenv


def weather(request):
    return render(request, 'weather/weather_page.html')


API_KEY = getenv('OPENWEATHER_API')
BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast'


def process_forecast_data(data):
    filtered_forecast = []
    last_data = ''

    for item in data['list']:
        date_time_obj = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
        humanized_date = humanize.naturalday(date_time_obj)

        if humanized_date == last_data:
            humanized_date = ''
        else:
            last_data = humanized_date

        element = {
            'day': humanized_date,
            'time': date_time_obj.strftime("%H:%M"),
            'temperature': round(item['main']['temp'], 1),
            'wind': round(item['wind']['speed'], 1),
            'description': item['weather'][0]['description']
        }

        filtered_forecast.append(element)

    return filtered_forecast


def get_weather(request):
    if request.method == 'POST':
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        if not lat or not lng:
            return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)

        params = {
            'lat': lat,
            'lon': lng,
            'appid': API_KEY,
            'units': 'metric'
        }

        forecast_response = requests.get(BASE_URL, params=params)

        if forecast_response.status_code != 200:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

        forecast_data = forecast_response.json()
        filtered_forecast = process_forecast_data(forecast_data)

        location = forecast_data['city'][
                       'name'] or f'{forecast_data["city"]["coord"]["lat"]}, {forecast_data["city"]["coord"]["lon"]}'
        weather_info = f'<h2>Location: {location}</h2>'

        ready_forecast = '<table><colgroup span="4"></colgroup><tr><th>Day</th><th>Time</th><th>Temperature</th><th>Wind</th><th>Weather</th></tr>'

        for item in filtered_forecast:
            info = f'<tr><td>{item["day"]}</td>'
            info += f'<td>{item["time"]}</td>'
            info += f'<td>{item["temperature"]} C</td>'
            info += f'<td>{item["wind"]} m/s</td>'
            info += f'<td>{item["description"]}</td></tr>'
            ready_forecast += info

        ready_forecast += '</table>'

        return JsonResponse({'weather_info': weather_info, 'forecast': ready_forecast})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


'''
def get_weather(request):
    if request.method == 'POST':
        lat = request.POST['lat']
        lng = request.POST['lng']

        # Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key
        api_key = '5e77e8ca1182feec77e14e9ddd677c74'
        forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={api_key}&units=metric'
        forecast_response = requests.get(forecast)
        if forecast_response.status_code != 200:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
        filtered_forecast = list()
        forecast_data = forecast_response.json()
        last_data = ''

        for i in forecast_data['list']:
            element = dict()
            date_format = "%Y-%m-%d %H:%M:%S"
            date_time_str = i['dt_txt']
            date_time_obj = datetime.strptime(date_time_str, date_format)
            humanized_date = humanize.naturalday(date_time_obj)
            if humanized_date == last_data:
                humanized_date = ''
            else:
                last_data = humanized_date
            hour_minute_str = date_time_obj.strftime("%H:%M")
            element['day'] = humanized_date
            element['time'] = hour_minute_str
            element['temperature'] = round(i['main']['temp'], 1)
            element['wind'] = round(i["wind"]["speed"], 1)
            element['description'] = i["weather"][0]["description"]
            # element['icon'] = f'https://openweathermap.org/img/wn/{i["weather"][0]["icon"]}@2x.png'
            filtered_forecast.append(element)

        location = forecast_data["city"]["name"]
        if not location:
            location = f'{forecast_data["city"]["coord"]["lat"]}, {forecast_data["city"]["coord"]["lon"]}'
        weather_info = f'<h2>Location: {location}</h2>'

        ready_forecast = '<table><colgroup span="4"></colgroup><tr><th>Day</th><th>Time</th><th>Temperature</th><th>Wind</th><th>Weather</th></tr>'
        for i in filtered_forecast:
            info = f'<tr><td>{i["day"]}</td>'
            info += f'<td>{i["time"]}</td>'
            info += f'<td>{i["temperature"]} C</td>'
            info += f'<td>{i["wind"]} m/s</td>'
            info += f'<td>{i["description"]}</td></tr>'
            ready_forecast += info
        ready_forecast += '</table>'

        return JsonResponse({'weather_info': weather_info, 'forecast': ready_forecast})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
'''
