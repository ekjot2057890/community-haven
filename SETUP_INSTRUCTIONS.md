# Community Pulse - Setup Instructions

## Frontend Setup

The frontend is a static website that can be served using any web server. For development purposes, you can use Python's built-in HTTP server:

```bash
# Start the frontend server
python3 -m http.server 8000
```

Then access the site at http://localhost:8000

## Backend Setup

The backend requires:
1. Python 3.8+
2. MongoDB

### 1. Install MongoDB

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

#### Using Docker:
If you have Docker installed, you can use the provided docker-compose.yml file:

```bash
docker-compose up -d
```

### 2. Set up Python environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize the database

```bash
cd backend
export FLASK_APP=App/run.py
python -m flask init-db
```

### 4. Create an admin user

```bash
export FLASK_APP=App/run.py
python -m flask create-admin
```

### 5. Start the backend

```bash
export FLASK_APP=App/run.py
export FLASK_ENV=development
export MONGO_URI="mongodb://localhost:27017/community_pulse"
export JWT_SECRET_KEY="development-secret-key"
cd backend
python -m flask run --host=0.0.0.0
```

The backend API will be available at http://localhost:5000

## Accessing the Admin Interface

Once both the frontend and backend are running, you can access the admin interface at:

http://localhost:8000/admin/dashboard.html

You'll need to log in using the admin credentials you created in step 4.

## Path Fixes

If you encounter any issues with file paths not being found, run the fix_paths.sh script:

```bash
chmod +x fix_paths.sh
./fix_paths.sh
```

This script ensures all CSS and JavaScript file paths use the correct case (CSS/styles.css, JS/script.js) across all HTML files. 