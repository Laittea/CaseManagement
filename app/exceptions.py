"""
This module defines custom exceptions for the application.
"""

class UserNotFoundError(Exception):
    """
        Exception raised when a user is not found in the system.
        Inherits from the built-in Exception class.
    """

    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)
