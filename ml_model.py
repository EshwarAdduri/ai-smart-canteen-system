import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os
from datetime import datetime, timedelta
from models import db, Reservation, Meal, Prediction, RushHour

class DemandPredictor:
    def __init__(self, model_path='models/demand_prediction_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"✓ Loaded model from {self.model_path}")
        else:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            print("✓ Created new RandomForest model")

    def save_model(self):
        """Save trained model"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✓ Model saved to {self.model_path}")

    def prepare_training_data(self, days_back=60):
        """Prepare training data from historical reservations"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)

        # Get historical reservations
        reservations = Reservation.query.filter(
            Reservation.created_at >= cutoff_date,
            Reservation.status.in_(['completed', 'confirmed'])
        ).all()

        if len(reservations) < 50:
            print(f"⚠ Insufficient data: only {len(reservations)} reservations found")
            return None, None

        # Create features
        data = []
        for res in reservations:
            meal = Meal.query.get(res.meal_id)
            if not meal:
                continue

            pickup_time = res.pickup_time

            features = {
                'meal_id': res.meal_id,
                'day_of_week': pickup_time.weekday(),  # 0=Monday, 6=Sunday
                'hour': pickup_time.hour,
                'is_weekend': 1 if pickup_time.weekday() >= 5 else 0,
                'price': meal.price,
                'category_breakfast': 1 if meal.category == 'breakfast' else 0,
                'category_lunch': 1 if meal.category == 'lunch' else 0,
                'category_dinner': 1 if meal.category == 'dinner' else 0,
                'quantity': res.quantity
            }
            data.append(features)

        df = pd.DataFrame(data)

        # Aggregate by meal_id, day_of_week, hour
        aggregated = df.groupby(['meal_id', 'day_of_week', 'hour']).agg({
            'quantity': 'sum',
            'is_weekend': 'first',
            'price': 'first',
            'category_breakfast': 'first',
            'category_lunch': 'first',
            'category_dinner': 'first'
        }).reset_index()

        aggregated.rename(columns={'quantity': 'demand'}, inplace=True)

        X = aggregated[['meal_id', 'day_of_week', 'hour', 'is_weekend', 
                        'price', 'category_breakfast', 'category_lunch', 'category_dinner']]
        y = aggregated['demand']

        return X, y

    def train(self):
        """Train the demand prediction model"""
        X, y = self.prepare_training_data()

        if X is None or len(X) < 50:
            print("⚠ Not enough data to train model")
            return False

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"✓ Model trained successfully")
        print(f"  MAE: {mae:.2f}")
        print(f"  R² Score: {r2:.2f}")

        # Save model
        self.save_model()

        return True

    def predict_demand(self, meal_id, day_of_week, hour):
        """Predict demand for a specific meal at a specific time"""
        meal = Meal.query.get(meal_id)
        if not meal:
            return 0

        is_weekend = 1 if day_of_week >= 5 else 0

        features = pd.DataFrame([{
            'meal_id': meal_id,
            'day_of_week': day_of_week,
            'hour': hour,
            'is_weekend': is_weekend,
            'price': meal.price,
            'category_breakfast': 1 if meal.category == 'breakfast' else 0,
            'category_lunch': 1 if meal.category == 'lunch' else 0,
            'category_dinner': 1 if meal.category == 'dinner' else 0
        }])

        try:
            prediction = self.model.predict(features)[0]
            return max(0, int(prediction))
        except:
            # Fallback: return average demand
            return self._get_average_demand(meal_id)

    def _get_average_demand(self, meal_id):
        """Fallback: calculate average historical demand"""
        reservations = Reservation.query.filter_by(
            meal_id=meal_id,
            status='completed'
        ).limit(100).all()

        if not reservations:
            return 10  # Default

        total = sum(r.quantity for r in reservations)
        return max(5, int(total / len(reservations)))

    def predict_rush_hours(self, target_date=None):
        """Predict rush hours for a given date"""
        if target_date is None:
            target_date = datetime.utcnow().date()

        # Get historical rush hour data for same day of week
        day_of_week = target_date.weekday()

        # Get past reservations for this day of week
        rush_data = {}
        for hour in range(8, 21):  # 8 AM to 8 PM
            # Count reservations for this hour on similar days
            count = Reservation.query.filter(
                db.func.strftime('%w', Reservation.pickup_time) == str((day_of_week + 1) % 7),
                db.func.strftime('%H', Reservation.pickup_time) == f'{hour:02d}'
            ).count()

            rush_data[hour] = {
                'hour': hour,
                'count': count,
                'level': self._classify_rush_level(count)
            }

        return rush_data

    def _classify_rush_level(self, count):
        """Classify rush level based on count"""
        if count < 5:
            return 'low'
        elif count < 15:
            return 'medium'
        else:
            return 'high'

    def get_quiet_time_suggestions(self, target_date=None):
        """Suggest quiet times to visit canteen"""
        rush_hours = self.predict_rush_hours(target_date)

        quiet_times = []
        for hour, data in sorted(rush_hours.items()):
            if data['level'] == 'low':
                time_str = f"{hour:02d}:00 - {(hour+1):02d}:00"
                quiet_times.append({
                    'time': time_str,
                    'hour': hour,
                    'traffic': 'Light',
                    'recommended': True
                })

        return quiet_times[:3]  # Return top 3 quiet times


# Initialize predictor
predictor = DemandPredictor()
