'''
Sample Data Initialization Script
Run this after first starting the application to populate with sample data
'''

from app import app, db
from models import User, Meal, Reservation
from datetime import datetime, timedelta
import random

def init_sample_data():
    with app.app_context():
        print("Initializing sample data...")

        # Create sample students
        students = []
        departments = ['Computer Science', 'Engineering', 'Business', 'Arts', 'Science']

        for i in range(1, 11):
            username = f'student{i}'
            if not User.query.filter_by(username=username).first():
                student = User(
                    username=username,
                    email=f'student{i}@university.com',
                    role='student',
                    department=random.choice(departments)
                )
                student.set_password('password123')
                students.append(student)
                db.session.add(student)

        db.session.commit()
        print(f"✓ Created {len(students)} sample students")

        # Create sample meals
        sample_meals = [
            {
                'name': 'English Breakfast',
                'description': 'Full English with eggs, bacon, sausage, beans, and toast',
                'price': 5.99,
                'category': 'breakfast',
                'stock': 50
            },
            {
                'name': 'Avocado Toast',
                'description': 'Smashed avocado on sourdough with cherry tomatoes',
                'price': 4.50,
                'category': 'breakfast',
                'stock': 30
            },
            {
                'name': 'Chicken Curry with Rice',
                'description': 'Spicy chicken curry served with basmati rice',
                'price': 6.99,
                'category': 'lunch',
                'stock': 40
            },
            {
                'name': 'Margherita Pizza',
                'description': 'Classic pizza with tomato sauce, mozzarella, and basil',
                'price': 7.50,
                'category': 'lunch',
                'stock': 35
            },
            {
                'name': 'Caesar Salad',
                'description': 'Fresh romaine lettuce, parmesan, croutons, Caesar dressing',
                'price': 5.50,
                'category': 'lunch',
                'stock': 25
            },
            {
                'name': 'Fish and Chips',
                'description': 'Battered cod with chunky chips and mushy peas',
                'price': 8.99,
                'category': 'dinner',
                'stock': 30
            },
            {
                'name': 'Beef Burger with Fries',
                'description': 'Juicy beef burger with lettuce, tomato, and fries',
                'price': 7.99,
                'category': 'dinner',
                'stock': 45
            },
            {
                'name': 'Vegetable Stir Fry',
                'description': 'Mixed vegetables in soy sauce with noodles',
                'price': 6.50,
                'category': 'dinner',
                'stock': 30
            },
            {
                'name': 'Pasta Carbonara',
                'description': 'Creamy pasta with bacon and parmesan',
                'price': 7.25,
                'category': 'dinner',
                'stock': 35
            },
            {
                'name': 'Chocolate Brownie',
                'description': 'Warm chocolate brownie with ice cream',
                'price': 3.50,
                'category': 'snack',
                'stock': 40
            },
            {
                'name': 'Fresh Fruit Salad',
                'description': 'Mixed seasonal fruits',
                'price': 3.00,
                'category': 'snack',
                'stock': 30
            },
            {
                'name': 'Coffee',
                'description': 'Freshly brewed coffee',
                'price': 2.50,
                'category': 'beverage',
                'stock': 100
            },
            {
                'name': 'Fresh Orange Juice',
                'description': 'Freshly squeezed orange juice',
                'price': 3.00,
                'category': 'beverage',
                'stock': 50
            }
        ]

        meals_created = 0
        for meal_data in sample_meals:
            if not Meal.query.filter_by(name=meal_data['name']).first():
                meal = Meal(**meal_data, is_available=True)
                db.session.add(meal)
                meals_created += 1

        db.session.commit()
        print(f"✓ Created {meals_created} sample meals")

        # Create sample historical reservations for ML training
        all_students = User.query.filter_by(role='student').all()
        all_meals = Meal.query.all()

        if all_students and all_meals:
            reservations_created = 0
            # Create reservations for past 30 days
            for days_ago in range(30, 0, -1):
                # Create 5-15 reservations per day
                num_reservations = random.randint(5, 15)

                for _ in range(num_reservations):
                    student = random.choice(all_students)
                    meal = random.choice(all_meals)

                    # Random time between 8 AM and 7 PM
                    hour = random.randint(8, 19)
                    pickup_time = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
                    pickup_time = pickup_time.replace(hour=hour, minute=random.choice([0, 15, 30, 45]))

                    # Create reservation
                    reservation = Reservation(
                        user_id=student.id,
                        meal_id=meal.id,
                        pickup_time=pickup_time,
                        quantity=random.randint(1, 2),
                        status='completed'
                    )
                    reservation.generate_token()
                    db.session.add(reservation)
                    reservations_created += 1

            db.session.commit()
            print(f"✓ Created {reservations_created} historical reservations for ML training")

        print("\n✓✓✓ Sample data initialization complete! ✓✓✓")
        print("\nYou can now:")
        print("1. Login as admin (username: admin, password: admin123)")
        print("2. Login as any student (username: student1-10, password: password123)")
        print("3. Train the ML model from the Analytics page")
        print("\nRun the application: python app.py")

if __name__ == '__main__':
    init_sample_data()
