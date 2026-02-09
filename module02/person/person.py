"""
Person class implementation using Flyweight Factory pattern.
"""

from typing import Dict


class Person:
    """
    Represents a person (director) using the Flyweight Factory pattern.
    Only one Person object should exist per unique full name.
    """

    # Class variable to store all person instances (flyweight pattern)
    _persons: Dict[str, 'Person'] = {}

    def __init__(self, full_name: str) -> None:
        """
        Initialize a Person object.

        Args:
            full_name: Full name of the person

        Raises:
            ValueError: If full_name is empty
        """
        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty")

        # Store the normalized name (lowercase for case-insensitive comparison)
        self._full_name = full_name.strip()
        self._normalized_name = self._full_name.lower()

        # Check if a person with this name already exists (case-insensitive)
        if self._normalized_name in Person._persons:
            existing = Person._persons[self._normalized_name]
            raise ValueError(f"Person with name '{full_name}' already exists "
                             f"(existing: '{existing.full_name}')")

        # Store in flyweight registry using normalized name as key
        Person._persons[self._normalized_name] = self

    @property
    def full_name(self) -> str:
        """Get the person's full name (immutable)."""
        return self._full_name

    def __repr__(self) -> str:
        """String representation: Person(full_name)."""
        return f"Person({self.full_name})"

    def __str__(self) -> str:
        """String representation: Person(full_name)."""
        return f"Person({self.full_name})"

    def __eq__(self, other: object) -> bool:
        """
        Two persons are equal if their full names match
        (case-insensitive comparison).
        """
        if not isinstance(other, Person):
            return NotImplemented
        return self._normalized_name == other._normalized_name

    def __hash__(self) -> int:
        """Hash based on normalized name (case-insensitive)."""
        return hash(self._normalized_name)


def get_person(full_name: str) -> Person:
    """
    Get an existing Person or create a new one.

    Args:
        full_name: Full name of the person (case-insensitive)

    Returns:
        Person object

    Raises:
        ValueError: If full_name is empty
    """
    if not full_name or not full_name.strip():
        raise ValueError("Full name cannot be empty")

    full_name = full_name.strip()
    normalized_name = full_name.lower()

    # Check if person already exists
    if normalized_name in Person._persons:
        return Person._persons[normalized_name]

    # Create new person
    return Person(full_name)