from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os
import requests
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {'q': 'zadar', 'appid': OPEN_WEATHER_API_KEY, 'units': 'metric', 'lang': 'hr'}
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather)
