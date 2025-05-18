# Community Pulse

A location-aware platform designed to facilitate interaction, visibility, and participation within defined geographic communities.

## Project Overview

Community Pulse is a web application that helps people discover and participate in local events. It provides features for creating, managing, and attending events within geographic communities.

### Features

- **User Authentication**: Register, login, and manage user profiles
- **Event Management**: Create, edit, and delete events
- **Event Discovery**: Find events by location, category, or search terms
- **RSVP System**: Register interest in events and track attendance
- **Comments**: Discuss events with other community members
- **Admin Panel**: Manage users, events, and content

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **API Serialization**: Marshmallow with Flask-Marshmallow

## Setup Instructions

### Prerequisites

- Python 3.6+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/community-pulse.git
   cd community-pulse
   ```

2. **Run the setup script** (Unix/macOS):
   ```
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Initialize the database
   flask init-db
   
   # Run the application
   flask run
   ```

3. **Access the application**:
   Open your browser and navigate to http://localhost:5000

### Configuration

Environment variables can be set in a `.env` file:
- `SECRET_KEY`: Flask session encryption key
- `JWT_SECRET_KEY`: JWT token encryption key
- `DATABASE_URL`: Database connection string
- `ADMIN_EMAIL`: Default admin user email
- `ADMIN_PASSWORD`: Default admin user password

## Project Structure

```
community-pulse/
├── app.py                  # Application entry point
├── __init__.py             # Application factory and setup
├── models.py               # Database models
├── schemas.py              # Serialization schemas
├── utils.py                # Utility functions
├── routes/                 # API routes and controllers
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── events.py           # Event endpoints
│   ├── users.py            # User endpoints
│   └── admin.py            # Admin endpoints
├── static/                 # Static files (CSS, JS, images)
│   ├── CSS/                # CSS stylesheets
│   └── JS/                 # JavaScript files
├── templates/              # HTML templates
├── requirements.txt        # Package dependencies
└── README.md               # Project documentation
```

## API Documentation

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create a new event
- `GET /api/events/<id>` - Get event details
- `PUT /api/events/<id>` - Update an event
- `DELETE /api/events/<id>` - Delete an event
- `POST /api/events/<id>/rsvp` - RSVP to an event
- `GET /api/events/<id>/rsvp` - Get event RSVPs
- `GET /api/events/<id>/comments` - Get event comments
- `POST /api/events/<id>/comments` - Comment on an event
- `GET /api/events/categories` - Get event categories
- `GET /api/events/my-events` - Get your created events
- `GET /api/events/attending` - Get events you're attending

### Users
- `GET /api/users/profile` - Get your profile
- `PUT /api/users/profile` - Update your profile
- `PUT /api/users/password` - Change your password
- `GET /api/users/<id>` - Get a user's profile
- `GET /api/users/notifications` - Get your notifications
- `POST /api/users/notifications/read` - Mark notifications as read

### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/users/<id>` - Get user details
- `PUT /api/admin/users/<id>/verify` - Verify/unverify user as organizer
- `PUT /api/admin/users/<id>/ban` - Ban/unban user
- `PUT /api/admin/users/<id>/admin` - Add/remove admin privileges
- `GET /api/admin/events` - Get all events
- `PUT /api/admin/events/<id>/status` - Update event status
- `GET /api/admin/categories` - Get all categories
- `POST /api/admin/categories` - Create category
- `PUT /api/admin/categories/<id>` - Update category
- `DELETE /api/admin/categories/<id>` - Delete category
- `GET /api/admin/dashboard` - Get admin dashboard stats

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-new-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
