from flask import Flask, request, render_template, jsonify
import requests
import os
import sys
from datetime import datetime

app = Flask(__name__)

PORT = 5001
AUTHOR = "Hubert Kaproń"
INDEX = 99565

CITIES = {
    'Polska': ['Warszawa', 'Kraków', 'Gdańsk'],
    'Francja': ['Paryż', 'Lyon', 'Marsylia'],
    'Niemcy': ['Berlin', 'Monachium', 'Hamburg']
}

@app.route('/')
def index():
    print(f"Aplikacja uruchomiona przez {AUTHOR} o indeksie {INDEX} w dniu {datetime.now()}, nasłuchuje na porcie {PORT}")
    sys.stdout.flush()
    return render_template('index.html', countries=CITIES.keys())

@app.route('/get_cities/<country>')
def get_cities(country):
    return jsonify({'cities': CITIES.get(country, [])})

@app.route('/get_weather', methods=['POST'])
def get_weather():
        country = request.form.get('country')
        city = request.form.get('city')
        weather_data = get_weather_data(city, country)
        return render_template('index.html',
                               countries=CITIES.keys(),
                               weather=weather_data,
                               selected_country=country)

def get_weather_data(city, country):
    API_KEY = os.environ["WEATHER_API_KEY"]
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric&lang=pl"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if data.get('cod') != 200:
            raise ValueError(f"Błąd API: {data.get('message', 'Nieznany błąd')}")

        return {
            'city': city,
            'country': country,
            'temperature': f"{data['main']['temp']}°C",
            'conditions': data['weather'][0]['description'],
            'humidity': f"{data['main']['humidity']}%",
            'icon': data['weather'][0]['icon']
        }
    except Exception as e:
        print(f"Błąd API: {str(e)}")
        return {
            'city': city,
            'country': country,
            'temperature': 'B/d',
            'conditions': 'Nie można pobrać danych',
            'humidity': 'B/d',
            'icon': None
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)