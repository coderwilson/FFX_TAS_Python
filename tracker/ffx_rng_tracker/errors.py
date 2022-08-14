class SeedNotFoundError(Exception):
    """Raised when no seed is found."""


class InvalidDamageValueError(Exception):
    """Raised when a damage value provided as input is not valid."""


class EventParsingError(Exception):
    """Raised when a string cannot be parsed to instantiate an Event object."""
