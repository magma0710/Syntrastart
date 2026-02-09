"""
MovieRating class implementation using PredefinedFlyweight pattern.
"""

from typing import Dict, List


class MovieRating:
    """
    Represents a movie content rating using the PredefinedFlyweight pattern.
    Ratings can be compared and sorted: NR < G < PG < PG-13 < R < NC17
    """

    # Class variable to store all rating instances (flyweight pattern)
    _ratings: Dict[str, 'MovieRating'] = {}

    # Predefined rating order for comparison
    _rating_order = ["NR", "G", "PG", "PG-13", "R", "NC17"]

    def __init__(self, code: str, description: str) -> None:
        """
        Initialize a MovieRating object.

        Args:
            code: Rating code (e.g., "PG-13")
            description: Human-readable description

        Raises:
            ValueError: If code or description is empty
        """
        if not code or not description:
            raise ValueError("Code and description cannot be empty")

        self._code = code
        self._description = description

        # Store in flyweight registry
        if code in MovieRating._ratings:
            raise ValueError(f"Rating with code '{code}' already exists")
        MovieRating._ratings[code] = self

    @property
    def code(self) -> str:
        """Get the rating code."""
        return self._code

    @property
    def description(self) -> str:
        """Get the rating description."""
        return self._description

    def __repr__(self) -> str:
        """String representation: Rating(code)."""
        return f"Rating({self.code})"

    def __str__(self) -> str:
        """String representation: Rating(code)."""
        return f"Rating({self.code})"

    def __eq__(self, other: object) -> bool:
        """Two ratings are equal if their codes match."""
        if not isinstance(other, MovieRating):
            return NotImplemented
        return self.code == other.code

    def __hash__(self) -> int:
        """Hash based on code."""
        return hash(self.code)

    def __lt__(self, other: 'MovieRating') -> bool:
        """
        Compare ratings based on predefined order.
        NR < G < PG < PG-13 < R < NC17
        """
        if not isinstance(other, MovieRating):
            return NotImplemented

        try:
            self_index = MovieRating._rating_order.index(self.code)
            other_index = MovieRating._rating_order.index(other.code)
            return self_index < other_index
        except ValueError:
            # If code not in predefined order, fall back to string comparison
            return self.code < other.code

    def __le__(self, other: 'MovieRating') -> bool:
        """Less than or equal comparison."""
        return self < other or self == other

    def __gt__(self, other: 'MovieRating') -> bool:
        """Greater than comparison."""
        return not self <= other

    def __ge__(self, other: 'MovieRating') -> bool:
        """Greater than or equal comparison."""
        return not self < other


def get_rating(code: str) -> MovieRating:
    """
    Get a MovieRating object based on the rating code.

    Args:
        code: Rating code to look up

    Returns:
        Existing MovieRating object if found

    Raises:
        ValueError: If rating code doesn't exist
    """
    if code not in MovieRating._ratings:
        raise ValueError(f"Rating with code '{code}' does not exist")
    return MovieRating._ratings[code]


# Create the 6 predefined rating objects (PredefinedFactory)
# This will execute when the module is imported
NR = MovieRating("NR", "Not Rated")
G = MovieRating("G", "General Audiences")
PG = MovieRating("PG", "Parental Guidance Suggested")
PG13 = MovieRating("PG-13", "Parents Strongly Cautioned")
R = MovieRating("R", "Restricted")
NC17 = MovieRating("NC-17", "Adults Only")


