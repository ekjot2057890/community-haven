from App import create_app, mongo
import os
import logging
from App.tasks.scheduler import init_scheduler
from datetime import datetime
from werkzeug.security import generate_password_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create app instance
app = create_app()

# Create a CLI command for creating an admin user
@app.cli.command("create-admin")
def create_admin():
    """Create an admin user"""
    import getpass
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = getpass.getpass("Enter admin password: ")
    confirm_password = getpass.getpass("Confirm admin password: ")
    
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
    # Check if user already exists
    existing_user = mongo.db.users.find_one({"$or": [{"username": username}, {"email": email}]})
    if existing_user:
        print("User with this username or email already exists!")
        return
    
    # Create admin user
    admin = {
        "username": username,
        "email": email,
        "full_name": "Admin User",
        "password_hash": generate_password_hash(password),
        "is_admin": True,
        "is_verified_organizer": True,
        "is_banned": False,
        "created_at": datetime.utcnow()
    }
    
    mongo.db.users.insert_one(admin)
    print(f"Admin user {username} created successfully!")

# Create a CLI command for initializing the database
@app.cli.command("init-db")
def init_db():
    """Initialize the database by creating indexes"""
    # Create geospatial index for events
    mongo.db.events.create_index([("location.coordinates", "2dsphere")])
    
    # Create other indexes
    mongo.db.users.create_index("email", unique=True)
    mongo.db.users.create_index("username", unique=True)
    mongo.db.interests.create_index([("event_id", 1), ("user_id", 1)], unique=True)
    
    print("Database initialized with indexes!")

if __name__ == '__main__':
    # Initialize scheduler
    init_scheduler(app)
    
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
