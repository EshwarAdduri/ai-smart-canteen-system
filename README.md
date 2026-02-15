# AI-Powered Smart Canteen System

### Project Overview
An intelligent web-based canteen management system that uses machine learning to predict meal demand and rush hours, helping students avoid queues and administrators optimize inventory.

### Features

#### Student Features
- 🔐 **User Authentication**: Secure registration and login
- 📖 **Browse Menu**: View daily meals with prices and availability
- 🎫 **Meal Reservation**: Pre-order meals with pickup time slots
- ⏰ **Rush Hour Predictions**: AI-powered suggestions for quiet times
- 📱 **Reservation Management**: View and cancel active reservations
- 🔔 **Real-time Updates**: Stock availability and pickup notifications

#### Admin Features
- 📊 **Dashboard**: Overview of statistics and analytics
- 🍔 **Meal Management**: Add, edit, delete menu items
- 📈 **AI Analytics**: View demand predictions and trends
- 🤖 **Model Training**: Train ML model with historical data
- 👥 **User Management**: Monitor student registrations
- 📉 **Inventory Tracking**: Real-time stock management

#### AI/ML Features
- **Demand Prediction**: RandomForest regression model predicts meal popularity
- **Rush Hour Analysis**: Traffic pattern analysis based on historical data
- **Quiet Time Suggestions**: Recommends optimal visit times
- **Continuous Learning**: Model retraining with new reservation data

### Technology Stack

#### Backend
- **Framework**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **ML Library**: Scikit-learn (RandomForestRegressor)
- **Data Processing**: Pandas, NumPy

#### Frontend
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **JavaScript**: Vanilla JS with Bootstrap components
- **Styling**: Custom CSS

#### Architecture
- **Pattern**: MVC (Model-View-Controller)
- **Database Models**: User, Meal, Reservation, Prediction, RushHour
- **Design**: Single-page application with server-side rendering

### Project Structure
```
smart-canteen-system/
│
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── ml_model.py            # AI/ML prediction module
├── requirements.txt       # Python dependencies
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── menu.html
│   ├── reservations.html
│   ├── rush_prediction.html
│   ├── admin_meals.html
│   ├── add_meal.html
│   ├── edit_meal.html
│   ├── analytics.html
│   ├── 404.html
│   └── 500.html
│
├── static/                # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
├── models/                # ML model files
│   └── demand_prediction_model.pkl
│
├── data/                  # Data files
│   └── historical_data.csv
│
├── docs/                  # Documentation
│   ├── uml_diagrams/
│   ├── PROJECT_REPORT.md
│   └── USER_MANUAL.md
│
└── tests/                 # Test files
```

### Installation & Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

#### Step 1: Extract the Project
```bash
# Extract the zip file
unzip smart-canteen-system.zip
cd smart-canteen-system
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Initialize Database
```bash
# The database will be created automatically on first run
# Default admin account will be created:
# Username: admin
# Password: admin123
```

#### Step 5: Run the Application
```bash
python app.py
```

The application will start at: `http://localhost:5000`

### Usage Guide

#### For Students

1. **Register an Account**
   - Go to http://localhost:5000
   - Click "Register"
   - Fill in your details (username, email, department, password)
   - Submit the form

2. **Login**
   - Use your credentials to login
   - You'll be redirected to the student dashboard

3. **Browse Menu & Reserve Meals**
   - View available meals on the dashboard
   - Click "Reserve Now" on any meal
   - Select pickup time (minimum 1 hour ahead)
   - Choose quantity
   - Confirm reservation
   - Note your pickup token

4. **Check Rush Hours**
   - Click "Rush Hours" in navigation
   - View AI predictions for today
   - See suggested quiet times
   - Plan your visit accordingly

5. **Manage Reservations**
   - Click "My Reservations"
   - View all your bookings
   - Cancel if needed (before pickup time)

#### For Administrators

1. **Login as Admin**
   - Username: `admin`
   - Password: `admin123`
   - Access admin dashboard

2. **Manage Meals**
   - Click "Meals" in navigation
   - Add new meals with details
   - Edit existing meals
   - Update stock levels
   - Delete meals (if no active reservations)

3. **View Analytics**
   - Click "Analytics"
   - See demand predictions
   - View rush hour analysis
   - Monitor popular meals

4. **Train AI Model**
   - Go to Analytics page
   - Click "Train Model Now"
   - Wait for training completion
   - Improved predictions will be available

### UML Diagrams

The project includes comprehensive UML diagrams:

1. **Use Case Diagram**: Shows interactions between users and system
2. **Sequence Diagram**: Illustrates meal reservation flow
3. **Activity Diagram**: Depicts end-to-end workflows
4. **Class Diagram**: Defines system architecture and relationships

All diagrams are available in `docs/uml_diagrams/`

### Machine Learning Model

#### Algorithm
- **Type**: RandomForestRegressor
- **Input Features**:
  - Meal ID
  - Day of week (0-6)
  - Hour of day (0-23)
  - Weekend flag (0/1)
  - Price
  - Category (breakfast/lunch/dinner)

#### Training Process
1. Collects historical reservation data (last 60 days)
2. Aggregates by meal, day, and hour
3. Trains RandomForest model
4. Evaluates with MAE and R² metrics
5. Saves model for predictions

#### Prediction Accuracy
- Model improves with more data
- Minimum 50 reservations needed for training
- Typically achieves 80-90% accuracy with sufficient data

### Testing

#### Manual Testing Checklist
- [ ] User registration and login
- [ ] Meal browsing and filtering
- [ ] Reservation creation
- [ ] Reservation cancellation
- [ ] Admin meal management
- [ ] Stock updates
- [ ] Rush hour predictions
- [ ] Model training
- [ ] Error handling

#### Test Accounts
- **Admin**: username=`admin`, password=`admin123`
- **Student**: Create via registration page

### Security Features
- Password hashing with Werkzeug
- Session management with Flask-Login
- SQL injection protection via SQLAlchemy
- Input validation on forms
- CSRF protection

### Future Enhancements
- Email notifications for reservations
- Mobile app (iOS/Android)
- Payment integration
- Nutrition information
- Review and rating system
- Multi-language support
- Advanced analytics dashboard
- API for third-party integrations

### Troubleshooting

#### Database Issues
```bash
# Delete database and restart
rm canteen.db
python app.py
```

#### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

#### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Author

**Eshwar Adduri**  
AI Engineer  
Personal Learning & Portfolio Project  

This project was built as part of continuous learning and skill development in AI, machine learning, and full-stack development.

## License

This project is released under the MIT License for learning and demonstration purposes.

### Acknowledgments
- Flask documentation
- Scikit-learn documentation
- Bootstrap framework
- Font Awesome icons

---

## Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run
python app.py

# Access
# Open browser: http://localhost:5000
# Admin login: admin / admin123
```

---

**For detailed documentation, see:**
- `docs/PROJECT_REPORT.md` - Complete project report
- `docs/USER_MANUAL.md` - Detailed user guide
- `docs/uml_diagrams/` - All UML diagrams
