# UML DIAGRAMS - Smart Canteen System

## Overview
This document contains all UML diagrams for the AI-Powered Smart Canteen System, designed following standard UML notation.

---

## 1. USE CASE DIAGRAM

### Description
Shows the interactions between actors (Student and Administrator) and the system's main use cases.

### Actors
- **Student**: End user who reserves meals
- **Administrator**: Manages menu, inventory, and views analytics

### Use Cases

**Student Use Cases:**
- Register / Login
- View Daily Menu
- View Rush Prediction (AI)
- Reserve Meal
- View My Reservations
- Cancel Reservation

**Administrator Use Cases:**
- Register / Login (Admin credentials)
- Manage Menu Items
- View Popularity Analytics
- Manage Inventory
- Train AI Model
- View All Reservations

### Mermaid Code
```mermaid
graph TD
    subgraph Smart Canteen System
        UC1[Register / Login]
        UC2[View Daily Menu]
        UC3[View Rush Prediction AI]
        UC4[Reserve Meal]
        UC5[Manage Menu Items]
        UC6[View Popularity Analytics]
        UC7[Manage Inventory]
    end

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4

    Administrator --> UC1
    Administrator --> UC5
    Administrator --> UC6
    Administrator --> UC7

    class Student,Administrator actor;
```

---

## 2. SEQUENCE DIAGRAM - Meal Reservation Flow

### Description
Illustrates the step-by-step interaction between components during a meal reservation.

### Participants
- **Student**: User initiating reservation
- **Web Interface**: Frontend layer
- **Flask Backend**: Application logic
- **Database**: SQLite database

### Flow
1. Student selects meal and pickup time
2. Frontend sends POST request to backend
3. Backend checks stock availability
4. If stock available: creates reservation and updates inventory
5. If stock unavailable: returns error message
6. System generates pickup token
7. Confirmation displayed to student

### Mermaid Code
```mermaid
sequenceDiagram
    participant Student
    participant WebInterface as Web Interface
    participant FlaskBackend as Flask Backend
    participant Database as Database (SQLite)

    Student->>WebInterface: Selects Meal & Pickup Time
    WebInterface->>FlaskBackend: POST /reserve_meal (MealID, Time)
    activate FlaskBackend

    FlaskBackend->>Database: Check Stock Availability
    activate Database
    Database-->>FlaskBackend: Return Stock Count
    deactivate Database

    alt Stock > 0
        FlaskBackend->>Database: Create Reservation Record
        FlaskBackend->>Database: Decrement Inventory
        FlaskBackend-->>WebInterface: Reservation Successful + Token
        WebInterface-->>Student: Show Success & Pickup Token
    else Stock == 0
        FlaskBackend-->>WebInterface: Error: Meal Sold Out
        WebInterface-->>Student: Show Error + Suggest Alternatives
    end
    deactivate FlaskBackend
```

---

## 3. ACTIVITY DIAGRAM - End-to-End Workflow

### Description
Shows the complete user journey for both students and administrators from login to goal completion.

### Student Flow
1. Login/Register
2. View daily menu
3. Check AI rush predictions
4. Select meal
5. Check stock availability
6. Choose pickup time
7. Confirm reservation
8. Receive pickup token
9. Pick up meal

### Admin Flow
1. Login as admin
2. Access dashboard
3. Choose action:
   - Manage menu items
   - View analytics
   - Update inventory

### Mermaid Code
```mermaid
flowchart TD
    Start([Start]) --> Login{Log In?}

    Login -- No --> Register[Register Account]
    Register --> Login
    Login -- Yes --> Role{Check User Role}

    %% Student Flow
    Role -- Student --> ViewMenu[View Daily Menu]
    ViewMenu --> CheckAI[Check AI Rush Prediction]
    CheckAI --> SelectMeal[Select Meal Item]
    SelectMeal --> CheckStock{Stock Available?}
    CheckStock -- No --> SelectAnother[Select Different Meal]
    SelectAnother --> SelectMeal
    CheckStock -- Yes --> ChooseTime[Choose Pickup Time]
    ChooseTime --> Confirm[Confirm Reservation]
    Confirm --> GenToken[Generate Pickup Token]
    GenToken --> Pickup[Pick Up Meal]
    Pickup --> EndStudent([End])

    %% Admin Flow
    Role -- Admin --> Dashboard[View Admin Dashboard]
    Dashboard --> Option{Choose Action}
    Option -- Manage Menu --> ManageMenu[Update Menu Items]
    Option -- View Analytics --> ViewAnalytics[View AI Sales Predictions]
    Option -- Inventory --> ManageInventory[Update Inventory]

    ManageMenu --> EndAdmin([End])
    ViewAnalytics --> EndAdmin
    ManageInventory --> EndAdmin

    classDef student fill:#e1f5fe
    classDef admin fill:#f3e5f5
    class ViewMenu,CheckAI,SelectMeal,CheckStock,ChooseTime,Confirm,GenToken,Pickup student
    class Dashboard,Option,ManageMenu,ViewAnalytics,ManageInventory admin
```

---

## 4. CLASS DIAGRAM - System Architecture

### Description
Defines the object-oriented structure of the system, showing classes, attributes, methods, and relationships.

### Classes

#### User (Abstract Base)
- **Attributes**: user_id, username, email, password_hash, role
- **Methods**: register(), login(), logout()

#### Student (inherits User)
- **Attributes**: student_id, department
- **Methods**: reserve_meal(), view_menu(), check_rush_hours()

#### Administrator (inherits User)
- **Attributes**: admin_id, permissions
- **Methods**: manage_menu(), view_analytics(), update_inventory()

#### Meal
- **Attributes**: meal_id, name, description, price, stock, category
- **Methods**: update_stock()

#### Reservation
- **Attributes**: reservation_id, student_id, meal_id, pickup_time, status, token
- **Methods**: create_reservation(), cancel_reservation()

#### PredictionModel
- **Attributes**: model_id, training_date, accuracy
- **Methods**: train_model(), predict_demand()

### Relationships
- User ◁─ Student (Inheritance)
- User ◁─ Administrator (Inheritance)
- Student ─── Reservation (1 to many)
- Meal ─── Reservation (1 to many)
- PredictionModel ─── Meal (predicts)

### Mermaid Code
```mermaid
classDiagram
    class User {
        -String user_id
        -String username
        -String email
        -String password_hash
        -String role
        +register()
        +login()
        +logout()
    }

    class Student {
        -String student_id
        -String department
        +reserve_meal()
        +view_menu()
        +check_rush_hours()
    }

    class Administrator {
        -String admin_id
        -String permissions
        +manage_menu()
        +view_analytics()
        +update_inventory()
    }

    class Meal {
        -String meal_id
        -String name
        -String description
        -Float price
        -Integer stock
        -String category
        +update_stock()
    }

    class Reservation {
        -String reservation_id
        -String student_id
        -String meal_id
        -DateTime pickup_time
        -String status
        -String token
        +create_reservation()
        +cancel_reservation()
    }

    class PredictionModel {
        -String model_id
        -DateTime training_date
        -Float accuracy
        +train_model()
        +predict_demand()
    }

    User <|-- Student
    User <|-- Administrator
    Student "1" --> "0..*" Reservation
    Meal "1" --> "0..*" Reservation
    PredictionModel --> Meal : predicts
```

---

## 5. ENTITY-RELATIONSHIP DIAGRAM

### Description
Database schema showing tables and their relationships.

### Entities

**users**
- PK: id
- username (unique)
- email (unique)
- password_hash
- role
- department
- created_at

**meals**
- PK: id
- name
- description
- price
- category
- stock
- is_available
- created_at

**reservations**
- PK: id
- FK: user_id → users(id)
- FK: meal_id → meals(id)
- pickup_time
- status
- token (unique)
- quantity
- created_at

**predictions**
- PK: id
- FK: meal_id → meals(id)
- date
- time_slot
- predicted_demand
- actual_demand
- created_at

**rush_hours**
- PK: id
- date
- hour
- traffic_count
- rush_level
- created_at

### Relationships
- users(1) ──── (N)reservations
- meals(1) ──── (N)reservations
- meals(1) ──── (N)predictions

---

## 6. COMPONENT DIAGRAM

### Description
Shows the high-level organization of the system's components and their dependencies.

### Components

**Presentation Layer**
- HTML Templates
- CSS Stylesheets
- JavaScript Frontend

**Application Layer**
- Flask Routes (Controllers)
- Business Logic
- Form Validation

**Data Layer**
- SQLAlchemy ORM
- Database Models
- Query Handlers

**ML Layer**
- Prediction Module
- Training Module
- Feature Engineering

**External Dependencies**
- Bootstrap Framework
- Font Awesome Icons
- Scikit-learn Library

---

## 7. DEPLOYMENT DIAGRAM

### Description
Physical architecture showing how the system is deployed.

### Nodes

**Client Machine**
- Web Browser
- JavaScript Engine

**Web Server**
- Flask Application
- Python Runtime
- Static File Server

**Database Server**
- SQLite Database
- File System Storage

**ML Model**
- Trained Model File (.pkl)
- Prediction Engine

### Connections
- Client ←→ Web Server (HTTP/HTTPS)
- Web Server ←→ Database (SQLAlchemy)
- Web Server ←→ ML Model (Pickle)

---

## Diagram Usage Guide

### For Developers
- Use these diagrams to understand system architecture
- Reference class diagram when adding new features
- Follow sequence diagrams for API implementation
- Update diagrams when making structural changes

### For Documentation
- Include relevant diagrams in technical reports
- Use activity diagrams for user guides
- Reference use case diagrams in requirements
- Attach class diagrams to design documents

### For Stakeholders
- Use case diagrams show system capabilities
- Activity diagrams demonstrate user workflows
- Component diagrams explain system structure
- Deployment diagrams show infrastructure

---

## Tools Used
- Mermaid.js for diagram rendering
- Draw.io for complex diagrams
- PlantUML for automated generation
- GitHub for diagram versioning

---

**Project developed by**: Eshwar Adduri
**Contact**: addurieshwar6@gmail.com
**Last Updated**: February 2026 
**Version**: 1.0
