from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'


@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {'q': 'zadar', 'appid': 'e0fc4312cb583fa27eb794af4c75f574', 'units': 'metric', 'lang': 'hr'}
    response = requests.get(url, parameters)
    weather = response.json()
    return render_template('index.html', weather = weather)
