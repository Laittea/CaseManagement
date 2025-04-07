#!/bin/bash
set -e

# Create data directory if it doesn't exist
mkdir -p /code/data

# Create a Python script to create the database tables
cat > create_tables.py << 'EOF'
from app.database import engine
from app.models import Base

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
EOF

# Create the database tables
python create_tables.py

# Initialize the database with sample data
python initialize_data.py

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
