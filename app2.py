from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index1():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            api_key = '8437c87af477a14403844356b1207dd5'  # Replace with your API key
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                weather_data = {'error': 'City not found or API error'}
    return render_template('index1.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
