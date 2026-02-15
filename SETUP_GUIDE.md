# SETUP AND INSTALLATION GUIDE
## AI-Powered Smart Canteen System

---

## TABLE OF CONTENTS

1. [System Requirements](#1-system-requirements)
2. [Installation Steps](#2-installation-steps)
3. [Initial Configuration](#3-initial-configuration)
4. [Running the Application](#4-running-the-application)
5. [Database Setup](#5-database-setup)
6. [Troubleshooting Installation](#6-troubleshooting-installation)
7. [Development Setup](#7-development-setup)

---

## 1. SYSTEM REQUIREMENTS

### 1.1 Hardware Requirements

**Minimum:**
- CPU: Dual-core processor 2.0 GHz
- RAM: 4 GB
- Storage: 500 MB free space
- Network: Internet connection

**Recommended:**
- CPU: Quad-core processor 2.5 GHz or better
- RAM: 8 GB or more
- Storage: 2 GB free space
- Network: Stable broadband connection

### 1.2 Software Requirements

**Operating System:**
- Windows 10/11
- macOS 10.15 (Catalina) or later
- Ubuntu 20.04 LTS or later
- Any Linux distribution with Python 3.8+

**Required Software:**
- Python 3.8 or higher
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, or Edge)

**Optional Software:**
- Git (for version control)
- VS Code or PyCharm (for development)
- SQLite Browser (for database inspection)

---

## 2. INSTALLATION STEPS

### 2.1 Extract Project Files

**Step 1**: Locate the downloaded ZIP file
```
smart-canteen-system.zip
```

**Step 2**: Extract to your preferred location

**Windows:**
- Right-click → Extract All
- Choose destination folder
- Click Extract

**macOS:**
- Double-click the ZIP file
- Files extract automatically

**Linux:**
```bash
unzip smart-canteen-system.zip -d /path/to/destination
cd smart-canteen-system
```

### 2.2 Verify Python Installation

**Check Python version:**

**Windows:**
```cmd
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

**Expected output:**
```
Python 3.8.x or higher
```

**If Python is not installed:**
- Windows: Download from python.org
- macOS: `brew install python3` (requires Homebrew)
- Linux: `sudo apt-get install python3 python3-pip`

### 2.3 Create Virtual Environment

**Why?** Isolates project dependencies from system Python.

**Windows:**
```cmd
cd smart-canteen-system
python -m venv venv
```

**macOS/Linux:**
```bash
cd smart-canteen-system
python3 -m venv venv
```

**Verify creation:**
You should see a new `venv` folder in your project directory.

### 2.4 Activate Virtual Environment

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
*If you get an execution policy error:*
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Verification:**
Your terminal prompt should show `(venv)` prefix:
```
(venv) C:\Users\YourName\smart-canteen-system>
```

### 2.5 Install Dependencies

**Step 1**: Ensure virtual environment is activated

**Step 2**: Install all required packages
```bash
pip install -r requirements.txt
```

**Expected output:**
```
Installing collected packages: Flask, Flask-Login, SQLAlchemy...
Successfully installed Flask-2.3.3 Flask-Login-0.6.2 ...
```

**If installation fails:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list
```

You should see:
- Flask (2.3.3)
- Flask-Login (0.6.2)
- Flask-SQLAlchemy (3.0.5)
- pandas (2.0.3)
- scikit-learn (1.3.0)
- And others...

---

## 3. INITIAL CONFIGURATION

### 3.1 Environment Variables (Optional)

**Create .env file** (optional for development):

```bash
# Copy example file
cp .env.example .env

# Edit with your values
SECRET_KEY=your-unique-secret-key-here
FLASK_DEBUG=True
```

**Note:** System works with defaults if you skip this.

### 3.2 Directory Permissions

**Ensure write permissions for:**
- `models/` folder (for ML model)
- `data/` folder (for CSV files)
- Project root (for database file)

**Linux/macOS:**
```bash
chmod -R 755 models/ data/
```

---

## 4. RUNNING THE APPLICATION

### 4.1 First Run

**Step 1**: Ensure virtual environment is activated
```
(venv) appears in prompt
```

**Step 2**: Start the application
```bash
python app.py
```

**Expected output:**
```
* Serving Flask app 'app'
* Debug mode: on
✓ Default admin created (username: admin, password: admin123)
✓ Loaded model from models/demand_prediction_model.pkl
WARNING: This is a development server. Do not use it in production.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**Step 3**: Open web browser and navigate to:
```
http://localhost:5000
```
or
```
http://127.0.0.1:5000
```

**Step 4**: You should see the Smart Canteen homepage! 🎉

### 4.2 Stopping the Application

Press `Ctrl + C` in the terminal

### 4.3 Restarting

```bash
# Make sure you're in project directory and venv is active
python app.py
```

---

## 5. DATABASE SETUP

### 5.1 Automatic Database Creation

**On first run**, the system automatically:
- Creates `canteen.db` SQLite database
- Creates all tables (users, meals, reservations, etc.)
- Creates default admin account
  - Username: `admin`
  - Password: `admin123`

**Verify database creation:**
You should see `canteen.db` file in project root.

### 5.2 Populating Sample Data

**Why?** To test the system and train ML model.

**Step 1**: Ensure app is NOT running (press Ctrl+C)

**Step 2**: Run sample data script
```bash
python init_sample_data.py
```

**Expected output:**
```
Initializing sample data...
✓ Created 10 sample students
✓ Created 13 sample meals
✓ Created 300 historical reservations for ML training

✓✓✓ Sample data initialization complete! ✓✓✓

You can now:
1. Login as admin (username: admin, password: admin123)
2. Login as any student (username: student1-10, password: password123)
3. Train the ML model from the Analytics page

Run the application: python app.py
```

**Step 3**: Restart the application
```bash
python app.py
```

### 5.3 Sample Accounts

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Student Accounts:**
- Username: `student1` to `student10`
- Password: `password123` (all have same password)

**Sample Meals:**
- English Breakfast (£5.99)
- Chicken Curry (£6.99)
- Pizza (£7.50)
- Fish and Chips (£8.99)
- And 9 more...

### 5.4 Resetting Database

**Warning:** This deletes ALL data!

**Step 1**: Stop the application (Ctrl+C)

**Step 2**: Delete database file

**Windows:**
```cmd
del canteen.db
```

**macOS/Linux:**
```bash
rm canteen.db
```

**Step 3**: Restart application
```bash
python app.py
```

Fresh database with only default admin is created.

**Step 4**: (Optional) Run sample data script again
```bash
python init_sample_data.py
```

---

## 6. TROUBLESHOOTING INSTALLATION

### 6.1 Python Not Found

**Symptom:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
- Install Python from python.org
- During installation, check "Add Python to PATH"
- Restart terminal/command prompt
- Try `python3` instead of `python`

### 6.2 pip Not Found

**Symptom:**
```
'pip' is not recognized...
```

**Solution:**
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

### 6.3 Virtual Environment Issues

**Symptom:** Cannot activate venv

**Solution:**

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**General:**
```bash
# Delete venv folder
rm -rf venv  # or rmdir /s venv on Windows

# Recreate
python -m venv venv

# Activate again
```

### 6.4 Module Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### 6.5 Port Already in Use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**

**Option 1:** Kill existing process

**Windows:**
```cmd
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

**macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill -9
```

**Option 2:** Use different port

Edit `app.py`, change last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then access at `http://localhost:5001`

### 6.6 Database Permission Errors

**Symptom:**
```
OperationalError: unable to open database file
```

**Solution:**

**Check write permissions:**
```bash
# macOS/Linux
ls -la canteen.db
chmod 666 canteen.db

# Windows
# Right-click canteen.db → Properties → Security
# Ensure your user has write permission
```

### 6.7 CSS/JS Not Loading

**Symptom:** Page looks unstyled

**Solutions:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Check browser console for errors (F12)
4. Verify `static/` folder has `css/` and `js/` subfolders

---

## 7. DEVELOPMENT SETUP

### 7.1 IDE Configuration

**VS Code:**
1. Install Python extension
2. Select interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

**PyCharm:**
1. Open project folder
2. Settings → Project → Python Interpreter
3. Add → Existing environment
4. Select `venv/bin/python`

### 7.2 Git Configuration (Optional)

```bash
# Initialize git
git init

# Add .gitignore (already provided)
# Commit initial version
git add .
git commit -m "Initial commit"
```

### 7.3 Debug Mode

**Already enabled by default** in `app.py`:
```python
app.run(debug=True)
```

**Benefits:**
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

**For production:** Set `debug=False`

### 7.4 Development Tools

**Install optional dev tools:**
```bash
pip install pytest  # For testing
pip install black   # For code formatting
pip install pylint  # For linting
```

---

## QUICK START CHECKLIST

Use this checklist to ensure proper setup:

- [ ] Python 3.8+ installed
- [ ] Project extracted to desired location
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application runs (`python app.py`)
- [ ] Can access http://localhost:5000 in browser
- [ ] Homepage loads correctly
- [ ] Can login as admin (admin/admin123)
- [ ] (Optional) Sample data loaded (`python init_sample_data.py`)
- [ ] (Optional) Can train ML model from Analytics page

---

## POST-SETUP STEPS

### First Time Admin Tasks:

1. **Login as admin** (admin/admin123)
2. **Change default password** (via database or wait for feature)
3. **Add real meals** (or use sample data)
4. **Train ML model** (Analytics → Train Model Now)
5. **Test student registration** (create test account)
6. **Test meal reservation flow** (book and cancel)
7. **Verify all features work**

### First Time Student Tasks:

1. **Register a student account**
2. **Login successfully**
3. **Browse menu**
4. **Check rush hour predictions**
5. **Make a test reservation**
6. **View your reservations**
7. **Cancel a reservation**

---

## NEXT STEPS

**Now that setup is complete:**

1. 📖 Read the **USER_MANUAL.md** for detailed usage
2. 📊 Review **PROJECT_REPORT.md** for system understanding
3. 🎨 Explore **UML diagrams** in `docs/uml_diagrams/`
4. 🧪 Test all features thoroughly
5. 📝 Customize for your institution's needs
6. 🚀 Deploy to production server (when ready)

---

## SUPPORT

**If you encounter issues during setup:**

- Check troubleshooting section above
- Review error messages carefully
- Ensure all steps were followed
- Verify system requirements
- Contact: support@university.com

**Common Resources:**
- Python Docs: https://docs.python.org/3/
- Flask Docs: https://flask.palletsprojects.com/
- SQLite Docs: https://www.sqlite.org/docs.html

---

**Project developed by**: Eshwar Adduri
**Contact**: addurieshwar6@gmail.com
**Last Updated**: February 2026 
**Version**: 1.0
