# Use Python 3.11 image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the rest of your application
COPY . /code/

# Create data directory for SQLite and set permissions
RUN mkdir -p /code/data && \
    chmod 777 /code/data

# Expose the port your app runs on
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./data/sql_app.db

# Copy the startup script
COPY start.sh /code/start.sh
RUN chmod +x /code/start.sh

# Command to run the application
CMD ["/code/start.sh"]