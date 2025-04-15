# Case Management System

## Project Overview
This project provides a backend API for a Case Management System that allows social workers to manage client information and predict client success rates based on various interventions.

### User Story
As a user of the backend API's, I want to call API's that can retrieve, update, and delete information of clients who have already registered with the CaseManagement service so that I more efficiently help previous clients make better decisions on how to be gainfully employed.

### Features
- REST API endpoints for client information management
- Machine learning model for predicting client success rates
- Authentication and authorization system
- SQLite database for data storage
- Docker support for easy deployment
- Continuous Deployment to AWS

## How to Use

### Option 1: Running with Docker (Recommended)

#### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system (optional for docker-compose method)

#### Using Docker Compose (Simplest Method)

1. Clone the repository:
   ```bash
   git clone https://github.com/Laittea/CaseManagement.git
   cd CaseManagement
   ```

2. Run the application using Docker Compose:
   ```bash
   docker-compose up
   ```

   - To run in detached mode (in the background):
   ```bash
   docker-compose up -d
   ```

3. Access the API documentation at [http://localhost:8080/docs](http://localhost:8080/docs)

4. Log in as admin (username: `admin`, password: `admin123`)

5. To stop the application:
   ```bash
   docker-compose down
   ```

#### Using Docker Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Laittea/CaseManagement.git
   cd CaseManagement
   ```

2. Build the Docker image:
   ```bash
   docker build -t case-management .
   ```

3. Run the container:
   ```bash
   docker run -d -p 8080:8000 --name case-management-api case-management
   ```

   This command will:
   - Build and run the container in detached mode
   - Map port 8080 on your host to port 8000 in the container
   - Name the container "case-management-api"
   - Automatically create the database tables and initialize sample data

4. Access the API documentation at [http://localhost:8080/docs](http://localhost:8080/docs)

5. Log in as admin (username: `admin`, password: `admin123`)

6. To stop and remove the container when done:
   ```bash
   docker stop case-management-api
   docker rm case-management-api
   ```

7. To view logs from the container:
   ```bash
   docker logs case-management-api
   ```

8. To access a shell inside the running container:
   ```bash
   docker exec -it case-management-api bash
   ```

### Docker Environment Variables (Optional)

You can customize the application behavior by passing environment variables to the Docker container:

```bash
docker run -d -p 8080:8000 \
  -e DATABASE_URL=sqlite:///./app.db \
  -e SECRET_KEY=your_custom_secret_key \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=30 \
  --name case-management-api case-management
```

### Troubleshooting Docker

1. If you encounter port conflicts:
   ```bash
   docker run -d -p 8081:8000 --name case-management-api case-management
   ```
   Then access the API at [http://localhost:8081/docs](http://localhost:8081/docs)

2. To check if the container is running:
   ```bash
   docker ps
   ```

3. To view container logs:
   ```bash
   docker logs case-management-api
   ```

4. To rebuild the container if you've made changes:
   ```bash
   docker stop case-management-api
   docker rm case-management-api
   docker build -t case-management .
   docker run -d -p 8080:8000 --name case-management-api case-management
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

## AWS EC2 Deployment

This application is automatically deployed to AWS EC2 using GitHub Actions. The deployment process is triggered whenever a new Release is created from the master branch.

### Accessing the Public Endpoint

The application is deployed to an AWS EC2 instance and is accessible through the instance's public IP or DNS. The endpoint URL is added to each GitHub Release description after deployment is complete.

To access the deployed application:
1. Go to the [Releases page](https://github.com/Laittea/CaseManagement/releases) on GitHub
2. Find the latest release
3. The deployment URL will be listed in the release description under "Deployment Info"

### Deployment Process

The deployment process includes the following steps:
1. Connecting to the EC2 instance via SSH
2. Pulling the latest code from the repository
3. Building a Docker image on the EC2 instance
4. Running the Docker container
5. Verifying the deployment
6. Updating the release with the public endpoint URL

For detailed setup instructions, see the [AWS EC2 Deployment Setup Guide](docs/aws-ec2-deployment-setup.md).

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
