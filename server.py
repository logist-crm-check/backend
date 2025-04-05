from flask import Flask,request
from weather import weather_by_city
app = Flask(__name__)


@app.post('/')
def index():
    body = request.get_json()
    city = body["city"]
    weather = weather_by_city(city)
    if weather:
       weather_text = f"Сейчас {weather['temp_C']}, ощущается как {weather['FeelsLikeC']}"
    else:
       weather_text = "Прогноз сейчас недоступен"

    return {"temp_c": weather['temp_C'], "feels": weather['FeelsLikeC']}

if __name__=="__main__":
    app.run()