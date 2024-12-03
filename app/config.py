"""
This module contains the configuration settings for the application.
It uses Pydantic's BaseSettings to load settings from environment variables.
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Explicitly load the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../app/', '.env')
load_dotenv(dotenv_path)

public class Settings(BaseSettings):
    """
    Settings class to manage application configuration.

    Attributes:
        MONGODB_URI (str): MongoDB connection URI.
        MONGODB_NAME (str): MongoDB database name.
    """
    MONGODB_URI: str
    MONGODB_NAME: str

    class Config:
        """
        Config class to specify Pydantic settings behavior.

        Attributes:
            env_file (str): Path to the .env file.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate the settings object to be used throughout the application
settings = Settings()
