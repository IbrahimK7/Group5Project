# Group 5 Project - Game Platform

A Flask-based web application for a gaming community platform with user authentication, game discovery, leaderboards, parties, and messaging features.

## Project Overview

This application provides a comprehensive gaming community platform where users can:
- Create accounts and authenticate securely
- Discover and browse games
- View leaderboards and player rankings
- Create and join parties
- Send messages to other players
- Manage user profiles and settings
- Check what's trending in the community

## Project Structure

```
Group5Project/
├── models/                          # Data models and database interactions
│   ├── CreateAccountModel.py       # Account creation logic
│   ├── login_model.py              # Authentication and login
│   ├── PlayerStatsModel.py         # Player statistics
│   ├── games_model.py              # Game data management
│   ├── leaderboard_model.py        # Leaderboard rankings
│   ├── parties.py                  # Party/group management
│   ├── messages_model.py           # Messaging system
│   └── whats_hot.py                # Trending games/content
├── routes/                          # API endpoints and views
│   ├── auth.py                     # Authentication routes (login/signup)
│   ├── home.py                     # Home page and main routes
│   ├── inbox_routes.py             # Messaging routes
│   ├── party_routes.py             # Party management routes
│   └── routes.py                   # Additional routes
├── templates/                       # HTML templates
│   ├── login.html                  # Login page
│   ├── CreateAccount.html          # Account creation page
│   ├── home.html                   # Home/dashboard page
│   ├── playerprofiles.html         # Player profiles
│   ├── messages.html               # Messaging interface
│   ├── conversation.html           # Conversation view
│   ├── party_routes.html           # Party management
│   ├── joinparty.html              # Party join interface
│   ├── Leaveparty.html             # Party leave interface
│   ├── editprofile.html            # Profile editing
│   ├── Profile.html                # User profile page
│   ├── settings.html               # User settings
│   ├── host.html                   # Hosting interface
│   ├── Rate.html                   # Rating system
│   └── Search.html                 # Search functionality
├── static/                          # Static assets
│   ├── style.css                   # Main stylesheet
│   ├── style1.css                  # Alternative stylesheet
│   ├── newstyle.css                # Modern stylesheet
│   └── js/                         # JavaScript files
│       ├── home_panels.js          # Home page functionality
│       ├── conversation.js         # Conversation interactions
│       ├── messages.js             # Messaging functionality
│       ├── parties.js              # Party management JS
│       └── whats_hot.js            # Trending content JS
├── utils/                           # Utility functions
├── tests/                           # Unit tests
├── config.py                        # Application configuration
├── run.py                           # Application entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Technology Stack

- **Backend Framework:** Flask 3.0.3
- **Database:** MongoDB (via PyMongo 4.6.0)
- **Testing:** pytest 7.1.2
- **Environment Management:** python-dotenv 1.0.0
- **Frontend:** HTML5, CSS3, Vanilla JavaScript

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- MongoDB installed and running
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Group5Project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   Create a `.env` file in the root directory with your MongoDB connection settings:
   ```
   MONGODB_URI=mongodb://localhost:27017/
   DATABASE_NAME=game_platform
   ```

## Running the Application

Start the development server:
```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000/`

### Default Routes
- `/` - Redirects to login
- `/login` - User login page
- `/home` - Main dashboard (requires authentication)
- `/api/games` - Games API endpoint
- `/whats-hot` - Trending content API

## Features

### Authentication
- User registration and account creation
- Secure login/logout
- Session management

### Games & Discovery
- Browse available games
- Game ratings and reviews
- "What's Hot" trending section

### Social Features
- Player profiles and statistics
- Leaderboards and rankings
- Party creation and management
- Join/leave party functionality
- In-game messaging and conversations
- Player search

### User Management
- Profile editing
- Settings customization
- Player statistics tracking

## Testing

Run the test suite:
```bash
pytest
```

Tests are located in the `tests/` directory.

## Development Notes

- The application uses Flask sessions for user authentication
- MongoDB stores all user data, game data, and messaging records
- Frontend uses vanilla JavaScript for interactive features
- CSS is organized across multiple stylesheets for different components

## Project Team

Ibrahim Khokher, Tyler Rop, Marin Baloshi
