"""
Movie classes: Abstract Base Class and genre-specific subclasses.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# Import from our other modules
from module02.movie.rating import MovieRating, get_rating
from module02.person.person import Person, get_person


class Movie(ABC):
    """
    Abstract Base Class for all movies.
    """

    def __init__(
            self,
            rt_link: str,
            title: str,
            rating: MovieRating,
            directors: List[Person],
            release_date: Optional[datetime] = None,
            streaming_date: Optional[datetime] = None,
            length: Optional[int] = None,
            company: Optional[str] = None,
            score: Optional[int] = None,
            count: Optional[int] = None
    ) -> None:
        """
        Initialize a Movie object.

        Args:
            rt_link: Rotten Tomatoes link
            title: Movie title
            rating: MovieRating object
            directors: List of Person objects
            release_date: Original release date
            streaming_date: Streaming release date
            length: Runtime in minutes
            company: Production company
            score: Audience rating (0-100)
            count: Number of votes
        """
        if not rt_link or not title:
            raise ValueError("rt_link and title cannot be empty")
        if rating is None:
            raise ValueError("rating cannot be None")

        self._rt_link = rt_link
        self._title = title
        self._rating = rating
        self._directors = directors if directors is not None else []
        self._release_date = release_date
        self._streaming_date = streaming_date
        self._length = length
        self._company = company
        self._score = score
        self._count = count

    @property
    def rt_link(self) -> str:
        """Get the Rotten Tomatoes link."""
        return self._rt_link

    @property
    def title(self) -> str:
        """Get the movie title."""
        return self._title

    @property
    def rating(self) -> MovieRating:
        """Get the movie rating."""
        return self._rating

    @property
    def directors(self) -> List[Person]:
        """Get the list of directors."""
        return self._directors.copy()  # Return copy to prevent modification

    @property
    def release_date(self) -> Optional[datetime]:
        """Get the release date."""
        return self._release_date

    @property
    def streaming_date(self) -> Optional[datetime]:
        """Get the streaming release date."""
        return self._streaming_date

    @property
    def length(self) -> Optional[int]:
        """Get the movie length in minutes."""
        return self._length

    @property
    def company(self) -> Optional[str]:
        """Get the production company."""
        return self._company

    @property
    def score(self) -> Optional[int]:
        """Get the audience score (0-100)."""
        return self._score

    @property
    def count(self) -> Optional[int]:
        """Get the number of votes."""
        return self._count

    def relevant_score(self) -> bool:
        """
        The score of a film is relevant when there is a score given
        and determined by at least 100 votes.

        Returns:
            True if score is relevant, False otherwise
        """
        return self._score is not None and self._count is not None and self._count >= 100

    def is_classic(self) -> bool:
        """
        A film is a classic if it's at least 20 years old
        and has a relevant score higher than 80.

        Returns:
            True if film is a classic, False otherwise
        """
        if not self.relevant_score() or self._score <= 80:
            return False

        if not self._release_date:
            return False

        # Calculate age
        current_year = datetime.now().year
        release_year = self._release_date.year
        age = current_year - release_year

        return age >= 20

    def is_short(self) -> bool:
        """
        A film is a short film if it's shorter than 30 minutes.

        Returns:
            True if film is a short film, False otherwise
        """
        return self._length is not None and self._length < 30

    def url(self) -> str:
        """
        Get the internet address of the film.

        Returns:
            Full URL: https://www.rottentomatoes.com/ + rt_link
        """
        return f"https://www.rottentomatoes.com/{self._rt_link}"

    def __repr__(self) -> str:
        """String representation of the movie."""
        directors_str = ", ".join([d.full_name for d in self._directors]) if self._directors else "Unknown"
        return f"{self.__class__.__name__}('{self._title}', {self._rating}, Directors: {directors_str})"

    def __str__(self) -> str:
        """String representation of the movie."""
        return f"{self._title} ({self._rating})"


# Genre subclasses
class ActionAdventure(Movie):
    """Action & Adventure genre."""
    pass


class Comedy(Movie):
    """Comedy genre."""

    def is_slapstick(self) -> bool:
        """
        A comedy is slapstick if its relevant score is less than 40.

        Returns:
            True if slapstick comedy, False otherwise
        """
        return self.relevant_score() and self._score is not None and self._score < 40


class Drama(Movie):
    """Drama genre."""
    pass


class Horror(Movie):
    """Horror genre."""

    def is_scary(self) -> bool:
        """
        A horror film is scary if its rating is higher than PG.
        According to rating order: NR < G < PG < PG-13 < R < NC-17
        So rating > PG means: PG-13, R, or NC-17

        Returns:
            True if scary horror film, False otherwise
        """
        from module02.movie.rating import get_rating
        pg_rating = get_rating("PG")
        return self._rating > pg_rating


class Romance(Movie):
    """Romance genre."""

    def is_cosy(self) -> bool:
        """
        A romance film is cosy if its length is between 70 and 100 minutes.

        Returns:
            True if cosy romance film, False otherwise
        """
        return self._length is not None and 70 <= self._length <= 100


class ScienceFictionFantasy(Movie):
    """Science Fiction & Fantasy genre."""
    pass


class Western(Movie):
    """Western genre."""
    pass


# Factory function
def create_movie(movie_info: dict) -> Movie:
    """
    Create a Movie object based on the genre.

    Args:
        movie_info: Dictionary from csv.DictReader

    Returns:
        Movie object of the appropriate genre subclass

    Raises:
        ValueError: If genre doesn't exist or required fields are missing
    """
    # Required fields validation
    rt_link = movie_info.get('rotten_tomatoes_link')
    title = movie_info.get('movie_title')
    rating_code = movie_info.get('content_rating')
    genre = movie_info.get('genre')

    if not rt_link or not title or not rating_code or not genre:
        raise ValueError("Missing required fields")

    # Get rating object
    try:
        rating = get_rating(rating_code)
    except ValueError:
        raise ValueError(f"Invalid rating code: {rating_code}")

    # Parse directors
    directors_str = movie_info.get('directors', '')
    directors = []
    if directors_str:
        # Split by comma and handle multiple directors
        director_names = [name.strip() for name in directors_str.split(",") if name.strip()]
        directors = [get_person(name) for name in director_names]

    # Parse dates
    release_date_str = movie_info.get('original_release_date')
    streaming_date_str = movie_info.get('streaming_release_date')

    release_date = None
    streaming_date = None

    if release_date_str:
        try:
            release_date = datetime.strptime(release_date_str, '%Y-%m-%d')
        except ValueError:
            # If date parsing fails, leave as None
            pass

    if streaming_date_str:
        try:
            streaming_date = datetime.strptime(streaming_date_str, '%Y-%m-%d')
        except ValueError:
            # If date parsing fails, leave as None
            pass

    # Parse length (runtime)
    length_str = movie_info.get('runtime', '')
    length = None
    if length_str:
        try:
            length = int(length_str)
        except ValueError:
            # If conversion fails, leave as None
            pass

    # Parse score and count
    score_str = movie_info.get('audience_rating', '')
    count_str = movie_info.get('audience_count', '')

    score = None
    count = None

    if score_str:
        try:
            score = int(score_str)
        except ValueError:
            pass

    if count_str:
        try:
            count = int(count_str)
        except ValueError:
            pass

    # Get company
    company = movie_info.get('production_company')

    # Create appropriate Movie subclass based on genre
    genre_map = {
        'ACTION & ADVENTURE': ActionAdventure,
        'COMEDY': Comedy,
        'DRAMA': Drama,
        'HORROR': Horror,
        'ROMANCE': Romance,
        'SCIENCE FICTION & FANTASY': ScienceFictionFantasy,
        'WESTERN': Western
    }

    genre_class = genre_map.get(genre.upper() if genre else None)
    if not genre_class:
        raise ValueError(f"Unknown genre: {genre}")

    return genre_class(
        rt_link=rt_link,
        title=title,
        rating=rating,
        directors=directors,
        release_date=release_date,
        streaming_date=streaming_date,
        length=length,
        company=company,
        score=score,
        count=count
    )