"""
base.py

Defines the base exception class for the Enterprise Knowledge Intelligence Platform (EKIP).

All project-specific exceptions should inherit from EKIPError.
"""


class EKIPError(Exception):
    """
    Base exception for all EKIP-specific errors.
    """

    def __init__(self, message: str):
        super().__init__(message)