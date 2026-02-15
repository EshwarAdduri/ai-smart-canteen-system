from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os

from config import Config
from models import db, User, Meal, Reservation, Prediction, RushHour
from ml_model import predictor

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

    # Create default admin if not exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@canteen.com',
            role='admin',
            department='Administration'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin created (username: admin, password: admin123)")

# ==================== ROUTES ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

# ==================== AUTHENTICATION ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        department = request.form.get('department')

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Create new user
        user = User(
            username=username,
            email=email,
            role='student',
            department=department
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# ==================== STUDENT ROUTES ====================

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    min_booking_time = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
    if current_user.is_admin():
        return redirect(url_for('admin_dashboard'))

    # Get available meals
    meals = Meal.query.filter_by(is_available=True).all()

    # Get user's active reservations
    reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).filter(
        Reservation.status.in_(['pending', 'confirmed'])
    ).order_by(Reservation.pickup_time).all()

    # Get rush hour predictions for today
    rush_hours = predictor.predict_rush_hours()
    quiet_times = predictor.get_quiet_time_suggestions()

    return render_template(
        'student_dashboard.html',
        meals=meals,
        reservations=reservations,
        rush_hours=rush_hours,
        quiet_times=quiet_times,
        min_booking_time=min_booking_time
    )

@app.route('/student/menu')
@login_required
def view_menu():
    category = request.args.get('category', 'all')

    if category == 'all':
        meals = Meal.query.filter_by(is_available=True).all()
    else:
        meals = Meal.query.filter_by(category=category, is_available=True).all()

    return render_template('menu.html', meals=meals, category=category)

@app.route('/student/reserve', methods=['POST'])
@login_required
def reserve_meal():
    meal_id = request.form.get('meal_id', type=int)
    pickup_time_str = request.form.get('pickup_time')
    quantity = request.form.get('quantity', 1, type=int)

    meal = Meal.query.get(meal_id)
    if not meal:
        flash('Meal not found', 'danger')
        return redirect(url_for('student_dashboard'))

    # Check stock
    if meal.stock < quantity:
        flash('Insufficient stock available', 'danger')
        return redirect(url_for('student_dashboard'))

    # Parse pickup time
    try:
        pickup_time = datetime.strptime(pickup_time_str, '%Y-%m-%dT%H:%M')
    except:
        flash('Invalid pickup time', 'danger')
        return redirect(url_for('student_dashboard'))

    # Create reservation
    reservation = Reservation(
        user_id=current_user.id,
        meal_id=meal_id,
        pickup_time=pickup_time,
        quantity=quantity,
        status='confirmed'
    )
    reservation.generate_token()

    # Update stock
    meal.update_stock(-quantity)

    db.session.add(reservation)
    db.session.commit()

    flash(f'Reservation confirmed! Your pickup token is: {reservation.token}', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/student/reservations')
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(
        user_id=current_user.id
    ).order_by(Reservation.created_at.desc()).all()

    return render_template('reservations.html', reservations=reservations)

@app.route('/student/cancel/<int:reservation_id>', methods=['POST'])
@login_required
def cancel_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if not reservation or reservation.user_id != current_user.id:
        flash('Reservation not found', 'danger')
        return redirect(url_for('my_reservations'))

    if reservation.cancel():
        flash('Reservation cancelled successfully', 'success')
    else:
        flash('Cannot cancel this reservation', 'danger')

    return redirect(url_for('my_reservations'))

@app.route('/student/rush-prediction')
@login_required
def rush_prediction():
    rush_hours = predictor.predict_rush_hours()
    quiet_times = predictor.get_quiet_time_suggestions()

    return render_template('rush_prediction.html', rush_hours=rush_hours, quiet_times=quiet_times)

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    # Statistics
    total_meals = Meal.query.count()
    total_users = User.query.filter_by(role='student').count()
    today_reservations = Reservation.query.filter(
        db.func.date(Reservation.created_at) == datetime.utcnow().date()
    ).count()
    pending_reservations = Reservation.query.filter_by(status='pending').count()

    # Recent reservations
    recent_reservations = Reservation.query.order_by(
        Reservation.created_at.desc()
    ).limit(10).all()

    # Popular meals
    popular_meals = db.session.query(
        Meal.name,
        db.func.count(Reservation.id).label('count')
    ).join(Reservation).group_by(Meal.id).order_by(db.desc('count')).limit(5).all()

    stats = {
        'total_meals': total_meals,
        'total_users': total_users,
        'today_reservations': today_reservations,
        'pending_reservations': pending_reservations
    }

    return render_template(
        'admin_dashboard.html',
        stats=stats,
        recent_reservations=recent_reservations,
        popular_meals=popular_meals
    )

@app.route('/admin/meals')
@login_required
def manage_meals():
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    meals = Meal.query.all()
    return render_template('admin_meals.html', meals=meals)

@app.route('/admin/meals/add', methods=['GET', 'POST'])
@login_required
def add_meal():
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        stock = int(request.form.get('stock'))

        meal = Meal(
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
            is_available=True
        )

        db.session.add(meal)
        db.session.commit()

        flash('Meal added successfully', 'success')
        return redirect(url_for('manage_meals'))

    return render_template('add_meal.html')

@app.route('/admin/meals/edit/<int:meal_id>', methods=['GET', 'POST'])
@login_required
def edit_meal(meal_id):
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    meal = Meal.query.get_or_404(meal_id)

    if request.method == 'POST':
        meal.name = request.form.get('name')
        meal.description = request.form.get('description')
        meal.price = float(request.form.get('price'))
        meal.category = request.form.get('category')
        meal.stock = int(request.form.get('stock'))
        meal.is_available = 'is_available' in request.form

        db.session.commit()
        flash('Meal updated successfully', 'success')
        return redirect(url_for('manage_meals'))

    return render_template('edit_meal.html', meal=meal)

@app.route('/admin/meals/delete/<int:meal_id>', methods=['POST'])
@login_required
def delete_meal(meal_id):
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    meal = Meal.query.get_or_404(meal_id)

    # Check if meal has active reservations
    active_reservations = Reservation.query.filter_by(
        meal_id=meal_id,
        status='pending'
    ).count()

    if active_reservations > 0:
        flash('Cannot delete meal with active reservations', 'danger')
        return redirect(url_for('manage_meals'))

    db.session.delete(meal)
    db.session.commit()

    flash('Meal deleted successfully', 'success')
    return redirect(url_for('manage_meals'))

@app.route('/admin/analytics')
@login_required
def analytics():
    if not current_user.is_admin():
        flash('Access denied', 'danger')
        return redirect(url_for('student_dashboard'))

    # Get predictions for popular meals
    meals = Meal.query.limit(10).all()
    predictions = []

    for meal in meals:
        pred = predictor.predict_demand(meal.id, datetime.now().weekday(), 12)
        predictions.append({
            'meal': meal.name,
            'predicted_demand': pred
        })

    rush_hours = predictor.predict_rush_hours()

    return render_template('analytics.html', predictions=predictions, rush_hours=rush_hours)

@app.route('/admin/train-model', methods=['POST'])
@login_required
def train_model():
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'}), 403

    success = predictor.train()

    if success:
        return jsonify({'success': True, 'message': 'Model trained successfully'})
    else:
        return jsonify({'success': False, 'message': 'Insufficient data to train model'})

# ==================== API ROUTES ====================

@app.route('/api/meals')
def api_meals():
    meals = Meal.query.filter_by(is_available=True).all()
    return jsonify([meal.to_dict() for meal in meals])

@app.route('/api/rush-hours')
def api_rush_hours():
    rush_hours = predictor.predict_rush_hours()
    return jsonify(rush_hours)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== RUN ====================

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
