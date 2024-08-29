from flask import Flask, render_template, request, redirect
from weather_api import fetch_weather_data
from models import db, Weather
from datetime import datetime

app = Flask(__name__)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def show_input():
    if request.method == 'GET':
        return render_template('weather_input.html', show_toast=False)
    else:
        city = request.form['city'].strip()
        forecast_data = fetch_weather_data(city)
        if forecast_data is None or forecast_data == "error":
            return render_template('weather_input.html', show_toast=True)
        else:
            return redirect(f'/{city}')

@app.route('/<city>')
def show_weather(city):
    try:
        forecast_data = fetch_weather_data(city)
        if forecast_data and forecast_data != "error":
            forecast_days = forecast_data['forecast']['forecastday']
            weather_table_data = []
            for day in forecast_days:
                weather_table_data.append({
                    'date': day['date'],
                    'city': forecast_data['location']['name'],
                    'max_temperature': day['day']['maxtemp_c'],
                    'min_temperature': day['day']['mintemp_c'],
                    'precipitation': day['day']['totalprecip_mm'],
                    'sunrise_hour': day['astro']['sunrise'],
                    'sunset_hour': day['astro']['sunset']
                })
                date_obj = datetime.strptime(day['date'], '%Y-%m-%d').date()
                sunrise_obj = datetime.strptime(day['astro']['sunrise'], '%I:%M %p').time()
                sunset_obj = datetime.strptime(day['astro']['sunset'], '%I:%M %p').time()

                existing_weather = Weather.query.filter_by(date=date_obj, city=forecast_data['location']['name']).first()
                if existing_weather:
                    existing_weather.max_temp = day['day']['maxtemp_c']
                    existing_weather.min_temp = day['day']['mintemp_c']
                    existing_weather.total_precip = day['day']['totalprecip_mm']
                    existing_weather.sunrise = sunrise_obj
                    existing_weather.sunset = sunset_obj
                    existing_weather.log_time = datetime.now()
                else:
                    new_weather = Weather(
                        date=date_obj,
                        city=forecast_data['location']['name'],
                        max_temperature=day['day']['maxtemp_c'],
                        min_temperature=day['day']['mintemp_c'],
                        precipitation=day['day']['totalprecip_mm'],
                        sunrise_hour=sunrise_obj,
                        sunset_hour=sunset_obj,
                        log_time=datetime.now()
                    )
                    db.session.add(new_weather)
            db.session.commit()
            return render_template('weather_table.html', weather_data=weather_table_data, city=city)
        else:
            return render_template('weather_input.html', show_toast=True)
    except Exception as e:
        return render_template('weather_input.html', show_toast=True)

@app.route('/records', methods=['GET', 'POST'])
@app.route('/records', methods=['GET', 'POST'])
def show_records():
    deleted_record = request.args.get('deleted')
    if request.method == 'POST':
        city_filter = request.form['city'].strip()
        weather_records = Weather.query.filter(Weather.city.ilike(f'%{city_filter}%')).all()
    else:
        weather_records = Weather.query.all()
    return render_template('weather_records.html', weather_records=weather_records, deleted_record=deleted_record)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete_record(id):
    record = Weather.query.get_or_404(id)
    city = record.city
    date = record.date
    db.session.delete(record)
    db.session.commit()
    return redirect(f'/records?deleted={city} on {date}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
