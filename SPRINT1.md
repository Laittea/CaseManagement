# Project: Case Management API Development SPRINT1
## OCT. 9th - OCT. 23rd
## Contributors
- Han Yang, Hao Luo, Ruiyi Li, Ruimeng
## Overview
This project aims to create a RESTful API to manage and analyze client data in a case management service. The backend is developed using **FastAPI** and connected to a cloud-based **MySQL** database hosted on **AWS RDS**. The system facilitates CRUD operations and predictive analytics to assist in making informed decisions for clients’ employment outcomes.

## Team Collaboration

### 1. Database Service Selection
As a team, we discussed and evaluated several options for hosting the database. After considering various factors like scalability, security, and ease of use, we decided to use **Amazon RDS (AWS Relational Database Service)** for hosting our **MySQL** database. This choice was driven by the need for an online, centralized database solution that would allow all team members to connect remotely and collaborate effectively.

### 2. REST API Knowledge Sharing
To ensure that all team members were on the same page, we conducted a series of discussions and knowledge-sharing sessions about REST API concepts. This was crucial in helping everyone understand the following:
- How to structure API endpoints for CRUD operations.
- Best practices for data validation using **Pydantic** models.
- Implementation of asynchronous processing with **FastAPI**.

These sessions enabled team members to independently develop API functions, ensuring consistency in design and implementation across the project.

### 3. Development Plan
To manage the project effectively, we outlined a comprehensive development plan that included the following stages:

#### Phase 1: Setup & Initialization
- Create a virtual environment and install dependencies from `requirements.txt`.
- Initialize the FastAPI project structure and set up the database schema using **MySQL Workbench**.

#### Phase 2: Database Configuration
- Register for AWS services and create an RDS instance with MySQL.
- Set up security groups and VPC configuration to allow external access to the database.
- Establish the connection between FastAPI and the AWS-hosted MySQL database.

#### Phase 3: API Development
- Develop core API endpoints for CRUD operations on client data:
    - **POST /clients/predictions**: Accepts client data and returns prediction results.
    - **GET /clients/{id}**: Retrieves client information by ID.
    - **PUT /clients/{id}**: Updates client information by ID.
    - **DELETE /clients/{id}**: Deletes client data by ID.
- Implement data validation using Pydantic models.
- Write unit tests for each endpoint to ensure functionality and reliability.

#### Phase 4: Testing & Documentation
- Conduct end-to-end testing using **Postman** and manual verification of database changes.
- Document API endpoints using FastAPI’s interactive Swagger documentation.
- Create user guides and detailed instructions for API usage, including connection setup and deployment.

#### Phase 5: Final Review & Deployment
- Perform final testing to ensure all components work together seamlessly.
- Deploy the API on a cloud server, ensuring continuous integration and delivery.

### 4. AWS Registration & Database Connection
We successfully registered for AWS, created an RDS instance, and configured it for public access. This involved:
- Setting up inbound rules in the security group to allow access to port **3306** from our IP addresses.
- Modifying VPC settings to enable public accessibility.
- Establishing the connection between MySQL Workbench and the RDS instance, allowing us to manage the database and import CSV data.

With the database setup complete, the backend is now fully functional, providing efficient API access to case management data.

## Future Work
- Enhance predictive analytics by integrating additional ML models.
- Implement OAuth2 for user authentication.
- Add logging and monitoring for improved error handling and performance tracking.

