# Case Management System

## Project Overview

This project provides a backend API for a Case Management System that allows social workers to manage client information and predict client success rates based on various interventions.

### User Story

As a user of the backend API's, I want to call API's that can retrieve, update, and delete information of clients who have already registered with the CaseManagment service so that I more efficiently help previous clients make better decisions on how to be gainfully employed.

### Features

- REST API endpoints for client information management
- Machine learning model for predicting client success rates
- Authentication and authorization system
- SQLite database for data storage
- Docker support for easy deployment

## How to Use

### Option 1: Running with Docker (Recommended)

#### Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

#### Using Docker Compose

1. Clone the repository
2. Navigate to the project directory
3. Run the application using Docker Compose:
   ```
   docker-compose up
   ```
4. Access the API documentation at http://localhost:8000/docs
5. Log in as admin (username: admin, password: admin123)

#### Using Docker Run

1. Build the Docker image:
   ```
   docker build -t case-management .
   ```
2. Run the container:
   ```
   docker run -d -p 8080:8000 --name case-management-api case-management
   ```
   This command will:
   - Build and run the container in detached mode
   - Map port 8080 on your host to port 8000 in the container
   - Name the container "case-management-api"
   - Automatically create the database tables and initialize sample data

3. Access the API documentation at http://localhost:8080/docs
4. Log in as admin (username: admin, password: admin123)

5. To stop and remove the container when done:
   ```
   docker stop case-management-api
   docker rm case-management-api
   ```

### Option 2: Running Locally

1. Create a virtual environment for this project
2. Install all dependencies in requirements.txt:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   uvicorn app.main:app --reload
   ```
4. Load data into database:
   ```
   python initialize_data.py
   ```
5. Go to SwaggerUI: http://127.0.0.1:8000/docs
6. Log in as admin (username: admin, password: admin123)

## API Endpoints

After logging in, you can use the following endpoints:

- **Create User**: Only users in admin role can create new users. The role field needs to be either "admin" or "case_worker"
- **Get clients**: Display all the clients that are in the database
- **Get client**: Search for a client by id
- **Update client**: Update a client's basic info by providing client_id and updated values
- **Delete client**: Delete a client by id
- **Get clients by criteria**: Get a list of clients who meet a certain combination of criteria
- **Get Clients by services**: Get a list of clients who meet a certain combination of service statuses
- **Get clients services**: View a client's services' status
- **Get clients by success rate**: Search for clients whose cases have a success rate beyond a certain number
- **Get clients by case worker**: View which clients are assigned to a specific case worker
- **Update client services**: Update the service status of a case
- **Create case assignment**: Create a new case assignment