# SPRINT 2: Project Progress Summary

## Overview
Following the completion of SPRINT 1, we focused on enhancing the core functionality of our Case Management API project. This involved connecting team members to the centralized database, building a robust connection manager, adjusting the database schema, and developing comprehensive REST API endpoints.

## Accomplishments

### 1. Establishing Database Connectivity for All Team Members
- Successfully configured and connected all team members to the **AWS RDS MySQL database**.
- Ensured that each member could access the database through **PyCharm** and other SQL clients by setting up appropriate security group rules and connection details.

### 2. Developing a Connection Manager
- Implemented a `ConnectionManager` class to streamline database connections for the project:
  ```python
  import mysql.connector
  import os
  from mysql.connector import pooling
  from dotenv import load_dotenv

  class ConnectionManager:
      def __init__(self):
          self.db_config = {
              "host": os.getenv("DB_HOST"),
              "port": int(os.getenv("DB_PORT")),
              "user": os.getenv("DB_USER"),
              "password": os.getenv("DB_PASSWORD"),
              "database": os.getenv("DB_NAME")
          }

          # Create a connection pool
          self.pool = pooling.MySQLConnectionPool(
              pool_name="mypool",
              pool_size=5,
              **self.db_config
          )

      # Get a connection
      def get_connection(self):
          return self.pool.get_connection()

      # Close the connection
      def close_connection(self, connection):
          if connection.is_connected():
              connection.close()

This manager ensures efficient connection handling using a pool to maintain stability and optimize performance.
### 3. Adjusting the Database Schema
   - Updated the clients table schema to match the PredictionInput model. This involved creating a schema that accurately reflects the data structure needed for client information.
   - Sample schema adjustment included:
   - Modifying column data types to align with the PredictionInput requirements.
   - Adding or updating fields to store client-specific data effectively.
### 4. Developing REST API Endpoints
   - Implemented the core REST API functionalities for client data management:
   - GET endpoint to retrieve client information.
   - POST endpoint to add new client data.
   - DELETE endpoint to remove client data.
   - PUT endpoint to update existing client information.

## Next Steps
   Moving forward, we will:

  - Perform thorough testing and validation of the new REST API endpoints.
  - Implement security measures, such as user authentication and data encryption.
  - Integrate advanced data processing or analytics features to enhance API capabilities.
## Conclusion
SPRINT 2 has solidified the core infrastructure of our project by ensuring database connectivity for all team members, creating a connection manager for efficient data handling, adjusting the database schema for proper client data storage, and developing essential REST API functionalities. This progress lays a strong foundation for further development and upcoming sprints.