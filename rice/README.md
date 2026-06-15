## 🌾 Rice (Backend) Setup

This is the FastAPI backend service for `bento-box`. 

### Prerequisites
* Python 3.10+
* Virtual Environment tool (`venv`)

### 1. Installation

Navigate to the backend directory and set up your Python virtual environment:

```bash
# Navigate to the backend
cd rice

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment (macOS)
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

## 💾 Database Setup & Local Testing

This project runs on an asynchronous SQLite database engine (`sqlite+aiosqlite`), meaning it requires zero external service installations to run locally. The database schema is generated automatically from your application models.

### 1. Initialize and Seed the Database

Before starting up the API web server, run the built-in database setup script. This will generate your local database file (`bento.db`) and inject initial placeholder data (mock members and inventory items) so you can test endpoints immediately:

```bash
# Ensure you are in the /rice directory and your virtual environment is active
make init-db

# Start the local development server
make run
