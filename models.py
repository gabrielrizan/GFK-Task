from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    max_temperature = db.Column(db.Float, nullable=False)
    min_temperature = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=True)
    sunrise_hour = db.Column(db.Time, nullable=True)
    sunset_hour = db.Column(db.Time, nullable=True)
    log_time = db.Column(db.DateTime, nullable=False, default=db.func.now())

    # unique city and date constraint
    __table_args__ = (db.UniqueConstraint('date', 'city', name='_city_date_uc'),)

    def __repr__(self):
        return f'<Weather {self.city} on {self.date}>'
