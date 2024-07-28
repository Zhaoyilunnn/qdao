"""
Exceptions Module
====================

This module defines exceptions for errors raised by the Quantum Virtual Machine (QVM).

Classes:
    QdaoError: Base class for errors raised by QVM.
"""

class QdaoError(Exception):
    """Base class for errors raised by QVM"""

    def __init__(self, *message):
        """Set the error message"""
        super().__init__(" ".join(message))
        self.message = " ".join(message)

    def __str__(self) -> str:
        """Return the message"""
        return repr(self.message)
