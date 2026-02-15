# USER MANUAL
## AI-Powered Smart Canteen System

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Student Guide](#3-student-guide)
4. [Administrator Guide](#4-administrator-guide)
5. [Troubleshooting](#5-troubleshooting)
6. [FAQ](#6-faq)
7. [Support](#7-support)

---

## 1. INTRODUCTION

### 1.1 Welcome
Welcome to the AI-Powered Smart Canteen System! This platform revolutionizes how you experience canteen services by eliminating queues, providing intelligent predictions, and ensuring your favorite meals are always available.

### 1.2 System Requirements
- **Web Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Internet Connection**: Stable connection required
- **Screen Resolution**: Minimum 1280x720 (mobile compatible)
- **JavaScript**: Must be enabled

### 1.3 Key Features
- ✅ Pre-order meals and skip queues
- ✅ AI-powered rush hour predictions
- ✅ Real-time stock availability
- ✅ Instant reservation confirmation
- ✅ Pickup token system
- ✅ Mobile-friendly interface

---

## 2. GETTING STARTED

### 2.1 Accessing the System

**Step 1**: Open your web browser

**Step 2**: Navigate to: `http://localhost:5000` (or your institution's URL)

**Step 3**: You'll see the landing page with system overview

### 2.2 Creating an Account

**For Students:**

1. Click **"Register"** button on the homepage
2. Fill in the registration form:
   - **Username**: Your unique identifier (letters, numbers, underscores)
   - **Email**: Your university email address
   - **Department**: Select from dropdown
   - **Password**: Minimum 6 characters
3. Click **"Register"** button
4. You'll see a success message
5. Proceed to login

**Important Notes:**
- Username must be unique
- Email must be valid and unique
- Remember your password (no recovery yet!)
- Use your institutional email

### 2.3 Logging In

**Step 1**: Click **"Login"** on homepage

**Step 2**: Enter your credentials:
- Username
- Password

**Step 3**: Click **"Login"** button

**Step 4**: You'll be redirected to your dashboard

---

## 3. STUDENT GUIDE

### 3.1 Dashboard Overview

After logging in, you'll see your **Student Dashboard** with:

**Top Section:**
- Rush Hours Panel (left)
- Quiet Time Suggestions (right)

**Middle Section:**
- Your Active Reservations

**Bottom Section:**
- Available Meals Grid

### 3.2 Checking Rush Hours

**Purpose**: Avoid crowds by visiting during quiet times

**How to Use:**

1. **Rush Hours Panel** shows hourly predictions:
   - 🔴 **HIGH** - Very busy, expect queues
   - 🟡 **MEDIUM** - Moderate traffic
   - 🟢 **LOW** - Quiet time, recommended

2. **Quiet Time Suggestions**:
   - Shows top 3 recommended time slots
   - Based on AI analysis of historical data
   - Updates daily

**Pro Tips:**
- Check predictions before making reservation
- Book during green (low) times for best experience
- Predictions are most accurate for lunch/dinner

### 3.3 Browsing the Menu

**Method 1: From Dashboard**
- Scroll down to see available meals
- View price, stock, and category

**Method 2: From Menu Page**
- Click **"Menu"** in navigation
- Use category filters:
  - All
  - Breakfast
  - Lunch
  - Dinner
  - Snacks

**Meal Information:**
- **Name**: Meal title
- **Description**: Details about the dish
- **Price**: Cost in £
- **Category**: Meal type
- **Stock**: Available portions

### 3.4 Reserving a Meal

**Step-by-Step Process:**

1. **Find Your Meal**:
   - Browse dashboard or menu
   - Check stock availability (must be > 0)

2. **Click "Reserve Now"**:
   - A modal (popup) appears

3. **Fill Reservation Form**:
   - **Pickup Time**: Select date and time
     - Must be at least 1 hour ahead
     - Within canteen operating hours (8 AM - 8 PM)
   - **Quantity**: Number of portions (1 to available stock)

4. **Confirm Reservation**:
   - Review details
   - Click **"Confirm Reservation"**

5. **Receive Confirmation**:
   - Success message appears
   - **Pickup Token** is generated (e.g., "A7B3C9")
   - Token shown at top of page

**Important:**
- ⚠️ Write down or screenshot your pickup token!
- ⚠️ Stock is deducted immediately
- ⚠️ Pickup time cannot be changed after booking

**Example:**
```
Meal: Chicken Curry with Rice
Pickup Time: Today, 1:00 PM
Quantity: 1
Token: F8E2A1
Status: Confirmed ✅
```

### 3.5 Viewing Your Reservations

**Access**: Click **"My Reservations"** in navigation

**Information Displayed:**
- **Token**: Your unique pickup code
- **Meal Name**: What you ordered
- **Quantity**: Number of portions
- **Pickup Time**: When to collect
- **Status**: Current state
  - **PENDING**: Awaiting processing
  - **CONFIRMED**: Ready for pickup ✅
  - **COMPLETED**: Already collected
  - **CANCELLED**: Was cancelled
- **Created**: When you made the reservation

**Actions Available:**
- **Cancel**: Only for pending/confirmed reservations
  - Stock will be returned
  - Click Cancel button
  - Confirm in popup dialog

### 3.6 Picking Up Your Meal

**At the Canteen Counter:**

1. **Go to pickup counter** at your reserved time

2. **Show your token**:
   - Display token number from app
   - Or show printed/screenshot token

3. **Staff verifies** and prepares your meal

4. **Collect your meal** - enjoy!

**Tips:**
- Arrive within 15 minutes of pickup time
- Have token ready
- If late, contact canteen staff

### 3.7 Cancelling a Reservation

**When You Can Cancel:**
- Status is PENDING or CONFIRMED
- Before pickup time

**How to Cancel:**

1. Go to **"My Reservations"**
2. Find the reservation
3. Click **"Cancel"** button (red)
4. Confirm in dialog box
5. Stock is returned automatically
6. Status changes to CANCELLED

**Note**: Cancelled reservations cannot be restored

---

## 4. ADMINISTRATOR GUIDE

### 4.1 Admin Login

**Credentials** (default):
- **Username**: `admin`
- **Password**: `admin123`

**⚠️ SECURITY**: Change default password immediately!

### 4.2 Admin Dashboard

**Statistics Cards** (top row):
- 📊 Total Meals
- 👥 Total Students
- 🛒 Today's Orders
- ⏳ Pending Reservations

**Recent Reservations Table**:
- Last 10 reservations
- Shows token, student, meal, time, status

**Popular Meals Chart**:
- Top 5 most ordered meals
- Order count and progress bar

**Quick Actions**:
- Add New Meal
- View All Meals
- View Analytics
- Train AI Model

### 4.3 Managing Meals

#### 4.3.1 Viewing All Meals

1. Click **"Meals"** in navigation
2. See table with all meals:
   - ID
   - Name
   - Category
   - Price
   - Stock (color-coded)
   - Availability status
   - Actions (Edit/Delete)

#### 4.3.2 Adding a New Meal

**Step-by-Step:**

1. Click **"Add New Meal"** button

2. Fill in the form:
   - **Meal Name** *: e.g., "Chicken Tikka Masala"
   - **Description**: Details about the dish
   - **Category** *: Select from dropdown
     - Breakfast
     - Lunch
     - Dinner
     - Snack
     - Beverage
   - **Price** *: In £ (e.g., 6.99)
   - **Initial Stock** *: Number of portions (e.g., 50)

3. Click **"Add Meal"**

4. Confirmation message appears

5. Meal is now available for students

**Validation:**
- * = Required fields
- Price must be ≥ 0
- Stock must be ≥ 0

#### 4.3.3 Editing a Meal

**Purpose**: Update details or stock

**Steps:**

1. Go to **Meals** page
2. Click **Edit** button (yellow) for the meal
3. Modify fields as needed:
   - Name
   - Description
   - Category
   - Price
   - Stock
   - Availability toggle
4. Click **"Update Meal"**

**Use Cases:**
- Replenish stock
- Change price
- Update description
- Temporarily disable meal
- Fix incorrect information

#### 4.3.4 Deleting a Meal

**⚠️ Caution**: This action cannot be undone!

**When You Can Delete:**
- Meal has no active reservations (pending/confirmed)

**Steps:**

1. Go to **Meals** page
2. Click **Delete** button (red)
3. Confirm in dialog
4. Meal is permanently removed

**If Unable to Delete:**
- Check for active reservations
- Wait for them to complete
- Or cancel them first

### 4.4 Viewing Analytics

**Access**: Click **"Analytics"** in navigation

**Section 1: Demand Predictions**
- Shows predicted demand for top meals
- Based on ML model
- For lunch time period
- Helps with inventory planning

**Section 2: Rush Hour Analysis**
- Expected traffic by hour
- High/medium rush times highlighted
- Use to plan staffing

**Section 3: Model Management**
- Train AI model button
- Status messages
- Training progress

### 4.5 Training the AI Model

**Purpose**: Improve prediction accuracy with new data

**When to Train:**
- After significant new reservation data (50+ bookings)
- Weekly or monthly
- When predictions seem inaccurate

**How to Train:**

1. Go to **Analytics** page
2. Click **"Train Model Now"**
3. System processes historical data:
   - Collects last 60 days of reservations
   - Extracts features
   - Trains RandomForest model
   - Evaluates accuracy
   - Saves model
4. Wait for completion (5-30 seconds)
5. Success or warning message appears

**Success Message**:
```
✅ Model trained successfully
   MAE: 1.82
   R² Score: 0.84
```

**Warning Message**:
```
⚠️ Insufficient data to train model
   Need at least 50 completed reservations
```

**What Happens:**
- Predictions become more accurate
- Rush hour analysis improves
- Quiet time suggestions refine

---

## 5. TROUBLESHOOTING

### 5.1 Cannot Login

**Problem**: "Invalid username or password"

**Solutions:**
- ✓ Check username spelling (case-sensitive)
- ✓ Verify password (no extra spaces)
- ✓ Ensure you registered first
- ✓ Try different browser
- ✓ Clear browser cache and cookies

### 5.2 Cannot Register

**Problem**: "Username already exists"
- **Solution**: Choose different username

**Problem**: "Email already registered"
- **Solution**: Use different email or login if you already have account

**Problem**: "Password too short"
- **Solution**: Use at least 6 characters

### 5.3 Cannot Reserve Meal

**Problem**: "Meal sold out"
- **Solution**: Choose different meal or check back later

**Problem**: "Pickup time must be at least 1 hour from now"
- **Solution**: Select later time

**Problem**: "Insufficient stock"
- **Solution**: Reduce quantity or select different meal

### 5.4 Lost Pickup Token

**Solution:**
1. Go to "My Reservations"
2. Find your reservation
3. Token is displayed in first column
4. Screenshot or write it down

### 5.5 Page Not Loading

**Solutions:**
- ✓ Check internet connection
- ✓ Refresh page (F5 or Ctrl+R)
- ✓ Clear browser cache
- ✓ Try incognito/private mode
- ✓ Update browser to latest version
- ✓ Try different browser

### 5.6 Model Training Fails

**Problem**: "Insufficient data"

**Solution:**
- Wait for more reservations (need 50+)
- System will work with default predictions meanwhile

### 5.7 Stock Not Updating

**Solution:**
- Refresh the page
- Check admin panel for actual stock
- Verify reservation was confirmed

---

## 6. FAQ

### General Questions

**Q1: Is this system free to use?**
A: Yes, for students and staff of the institution.

**Q2: Do I need to download an app?**
A: No, it's a web-based system. Use any browser.

**Q3: Can I use it on mobile?**
A: Yes! The system is mobile-responsive.

**Q4: How accurate are the rush hour predictions?**
A: Typically 80-90% accurate with sufficient historical data.

**Q5: Can I reserve meals for someone else?**
A: No, one account per person.

### Student Questions

**Q6: How far in advance can I reserve?**
A: Minimum 1 hour, maximum 24 hours ahead.

**Q7: Can I modify my reservation?**
A: No, but you can cancel and create new one.

**Q8: What if I'm late for pickup?**
A: Contact canteen staff. Meal may be given away after 15 minutes.

**Q9: Can I reserve multiple meals at once?**
A: No, but you can make multiple reservations.

**Q10: What if my preferred meal is unavailable?**
A: Check back later or use rush predictions to find best times.

### Admin Questions

**Q11: How often should I train the model?**
A: Weekly or monthly, after significant new data.

**Q12: Can I delete completed reservations?**
A: They're kept for historical analysis. No need to delete.

**Q13: How do I change admin password?**
A: Currently via database. Feature coming soon.

**Q14: What's the maximum stock I can set?**
A: Technically unlimited, but be realistic (e.g., 100-200).

**Q15: Can I add meal images?**
A: Future feature. Currently shows placeholder icons.

---

## 7. SUPPORT

### 7.1 Getting Help

**Technical Issues:**
- Email: addurieshwar6@gmail.com
- Phone: +44 XXX XXX XXXX
- Hours: Monday-Friday, 9 AM - 5 PM

**Canteen Operations:**
- Counter Staff during operating hours
- Canteen Manager: manager@university.com

### 7.2 Feedback & Suggestions

We value your input!

**Submit Feedback:**
- Online form: [URL]
- Email: addurieshwar6@gmail.com
- In-person: Canteen feedback box

### 7.3 Reporting Bugs

**If you find a bug:**
1. Note what you were doing
2. Take screenshot if possible
3. Email support with details:
   - Your username (not password!)
   - Date and time
   - What happened vs. what you expected
   - Browser and device info

### 7.4 Feature Requests

**Want a new feature?**
- Submit via feedback form
- Include:
  - Feature description
  - Why it's useful
  - How it should work

**Popular Requested Features:**
- ✅ Email notifications (planned)
- ✅ Meal ratings (planned)
- ✅ Loyalty points (under consideration)
- ✅ Diet filters (planned)

---

## QUICK REFERENCE CARD

### Student Quick Guide
```
Login → View Menu → Check Rush Hours →
Select Meal → Reserve → Get Token → Pick Up
```

### Admin Quick Guide
```
Login → Dashboard → Manage Meals →
View Analytics → Train Model
```

### Important Links
- **Homepage**: http://localhost:5000
- **Login**: http://localhost:5000/login
- **Register**: http://localhost:5000/register
- **Dashboard**: Auto-redirect after login

---

**Project developed by**: Eshwar Adduri
**Contact**: addurieshwar6@gmail.com
**Last Updated**: February 2026 
**Version**: 1.0
