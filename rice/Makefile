.PHONY: init-db run

# Initialize and seed the local database
init-db:
	PYTHONPATH=. python scripts/init_db.py

# Start the local development server
run:
	uvicorn app.main:app --reload
