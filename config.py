import os
from datetime import timedelta

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///canteen.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Upload folder
    UPLOAD_FOLDER = 'static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Canteen operating hours
    CANTEEN_OPEN_TIME = "08:00"
    CANTEEN_CLOSE_TIME = "20:00"

    # Reservation settings
    MAX_RESERVATIONS_PER_USER = 3
    RESERVATION_ADVANCE_HOURS = 24

    # ML Model settings
    MODEL_PATH = 'models/demand_prediction_model.pkl'
    TRAINING_DATA_PATH = 'data/historical_data.csv'
    MIN_TRAINING_SAMPLES = 100
