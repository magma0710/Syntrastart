"""
This is the main module of the test for module 2: Object Oriented Programming
"""

# python imports
import csv
import os
from typing import List

# custom imports
from module02.movie import Movie, create_movie

# Constants
MOVIE_FILE = "reviews.csv"  # Update for your system
EXPORT_FILE = "export.csv"  # Update for your system


def load_movies(file_location: str) -> List[Movie] | None:
    """
    Load all movies from a csv file into a list of Movie objects.
    :param file_location: Location of the csv file
    :raise FileNotFoundError: When the file cannot be found
    :return: List of Movie objects or None in case of error
    """
    if not os.path.exists(file_location):
        raise FileNotFoundError(f"Bestand niet gevonden: {file_location}")
    try:
        errors = 0
        movies = []
        with open(file_location, 'r', encoding="UTF-8") as file:
            reader = csv.DictReader(file, delimiter=",")
            for i, row in enumerate(reader):
                try:
                    movie = create_movie(row)
                    movies.append(movie)
                except ValueError as e:
                    errors += 1
                    print(f"Probleem met Lijn {i} : '{e}' => {row}")
        if errors:
            print(f"{errors} films konden niet geladen worden")
    except Exception as e:
        # Exception is a good choice
        print(f"Probleem bij het inlezen van bestand: {file_location} => {e}")
        return None
    return movies


# =========== HELPER FUNCTIONS FOR MENU ===========
def print_number_of_movies(movies: List[Movie]) -> None:
    """Print the number of movies in the input file."""
    print(f"\nNumber of movies: {len(movies)}")


def print_movies_per_genre(movies: List[Movie]) -> None:
    """Print a list of genres and how many times each occurs, sorted by count."""
    from collections import Counter

    genre_count = Counter()
    for movie in movies:
        # Get the class name (e.g., 'Comedy', 'Horror')
        genre_name = movie.__class__.__name__
        genre_count[genre_name] += 1

    print("\nMovies per genre (sorted by count):")
    print("-" * 40)
    for genre, count in sorted(genre_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{genre:25} : {count}")


def count_person_objects() -> None:
    """Print how many Person objects have been created."""
    from module02.person.person import Person
    # Person._persons is the class variable storing all persons
    print(f"\nNumber of Person objects created: {len(Person._persons)}")


def print_highest_scoring_movies(movies: List[Movie]) -> None:
    """Print the movie(s) with the highest relevant score."""
    # Filter movies with relevant scores
    relevant_movies = [m for m in movies if m.relevant_score()]

    if not relevant_movies:
        print("\nNo movies with relevant scores found.")
        return

    # Find highest score
    highest_score = max(m.score for m in relevant_movies if m.score is not None)

    # Find all movies with that score
    top_movies = [m for m in relevant_movies if m.score == highest_score]

    print(f"\nHighest score: {highest_score}%")
    print(f"Number of movies with this score: {len(top_movies)}")
    print("-" * 40)
    for movie in top_movies:
        print(f"{movie.title} (Score: {movie.score}%, Votes: {movie.count})")


def print_most_active_directors(movies: List[Movie]) -> None:
    """Print the director(s) who directed the most films."""
    from collections import Counter

    director_count = Counter()
    for movie in movies:
        for director in movie.directors:
            director_count[director.full_name] += 1

    if not director_count:
        print("\nNo directors found.")
        return

    # Find max count
    max_count = max(director_count.values())

    # Find all directors with that count
    top_directors = [name for name, count in director_count.items() if count == max_count]

    print(f"\nMost active director(s) directed {max_count} films:")
    print("-" * 40)
    for director_name in sorted(top_directors):
        print(director_name)


def print_shortest_longest_movies(movies: List[Movie]) -> None:
    """Print the shortest and longest movie(s)."""
    # Filter movies with known length
    movies_with_length = [m for m in movies if m.length is not None]

    if not movies_with_length:
        print("\nNo movies with length information found.")
        return

    # Find min and max length
    min_length = min(m.length for m in movies_with_length)
    max_length = max(m.length for m in movies_with_length)

    # Find all movies with those lengths
    shortest_movies = [m for m in movies_with_length if m.length == min_length]
    longest_movies = [m for m in movies_with_length if m.length == max_length]

    print(f"\nSHORTEST movies ({min_length} minutes):")
    print("-" * 40)
    for movie in shortest_movies:
        print(f"{movie.title} ({movie.length} min)")

    print(f"\nLONGEST movies ({max_length} minutes):")
    print("-" * 40)
    for movie in longest_movies:
        print(f"{movie.title} ({movie.length} min)")


def print_scary_horror_movies(movies: List[Movie]) -> None:
    """Print all horror films that are scary."""
    from module02.movie.movie import Horror

    horror_movies = [m for m in movies if isinstance(m, Horror)]

    if not horror_movies:
        print("\nNo horror movies found.")
        return

    scary_movies = [m for m in horror_movies if m.is_scary()]

    print(f"\nScary horror movies: {len(scary_movies)} out of {len(horror_movies)} horror movies")
    print("-" * 40)
    for movie in scary_movies:
        print(f"{movie.title} (Rating: {movie.rating})")


def print_score_distribution(movies: List[Movie]) -> None:
    """Print all scores from 0 to 100 and how many movies have each score."""
    from collections import Counter

    # Count scores for movies with scores
    score_count = Counter()
    for movie in movies:
        if movie.score is not None:
            score_count[movie.score] += 1

    print("\nScore distribution (0-100%):")
    print("-" * 40)
    for score in range(101):
        count = score_count.get(score, 0)
        print(f"{score:3}%: {count}")


def export_movies_without_relevant_score(movies: List[Movie], export_file: str) -> None:
    """
    Create a CSV file with movie information of films without relevant score,
    in alphabetical order.
    """
    # Filter movies without relevant score
    movies_to_export = [m for m in movies if not m.relevant_score()]

    if not movies_to_export:
        print("\nNo movies without relevant score found.")
        return

    # Sort alphabetically by title
    movies_to_export.sort(key=lambda m: m.title.lower())

    try:
        with open(export_file, 'w', encoding='UTF-8', newline='') as file:
            # Create CSV writer
            import csv
            writer = csv.writer(file)

            # Write header
            writer.writerow([
                'Title', 'Genre', 'Rating', 'Directors',
                'Release Date', 'Length', 'Company', 'Score', 'Votes'
            ])

            # Write movie data
            for movie in movies_to_export:
                # Format directors as comma-separated string
                directors_str = ', '.join(d.full_name for d in movie.directors) if movie.directors else ''

                # Format release date
                release_date_str = movie.release_date.strftime('%Y-%m-%d') if movie.release_date else ''

                writer.writerow([
                    movie.title,
                    movie.__class__.__name__,
                    str(movie.rating),
                    directors_str,
                    release_date_str,
                    str(movie.length) if movie.length is not None else '',
                    movie.company if movie.company else '',
                    str(movie.score) if movie.score is not None else '',
                    str(movie.count) if movie.count is not None else ''
                ])

        print(f"\nExported {len(movies_to_export)} movies to: {export_file}")

    except Exception as e:
        print(f"\nError exporting to {export_file}: {e}")


# =========== MAIN FUNCTION ===========
def main():
    """
    Load movies and present a menu until the user chooses to stop
    """
    print("Movie Analysis System")
    print("=====================")

    # Step 1: Load movies
    try:
        movies = load_movies(MOVIE_FILE)
        if movies is None:
            print("Error loading movies. Exiting.")
            return

        print(f"Successfully loaded {len(movies)} movies")

        # Step 2: Menu loop
        while True:
            print("\n" + "=" * 50)
            print("MOVIE ANALYSIS MENU")
            print("=" * 50)
            print("1) Print number of movies")
            print("2) Print movies per genre")
            print("3) Count Person objects")
            print("4) Print highest scoring movie(s)")
            print("5) Print most active director(s)")
            print("6) Print shortest and longest movie(s)")
            print("7) Print scary horror movies")
            print("8) Print score distribution")
            print("9) Export movies without relevant score to CSV")
            print("10) Stop program")
            print("11) Print all movies between 1/4/2000 and 1/4/2005; shorter than 120 minutes")
            print("=" * 50)

            choice = input("Enter your choice (1-11): ").strip()

            if choice == "1":
                print_number_of_movies(movies)
            elif choice == "2":
                print_movies_per_genre(movies)
            elif choice == "3":
                count_person_objects()
            elif choice == "4":
                print_highest_scoring_movies(movies)
            elif choice == "5":
                print_most_active_directors(movies)
            elif choice == "6":
                print_shortest_longest_movies(movies)
            elif choice == "7":
                print_scary_horror_movies(movies)
            elif choice == "8":
                print_score_distribution(movies)
            elif choice == "9":
                export_movies_without_relevant_score(movies, EXPORT_FILE)
            elif choice == "10":
                print("Goodbye!")
                break
            elif choice == "11":
                option_11_filter_movies(movies)
            else:
                print("Invalid choice. Please enter a number between 1 and 11.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Please check that the file exists at: {MOVIE_FILE}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Alle films uitgebracht tussen 1/4/2000 en 1/4/2005 korter dan 120 minuten.
from datetime import datetime

def option_11_filter_movies(movies):
    start_date = datetime(2000, 4, 1)
    end_date = datetime(2005, 4, 1)

    print("\n--- Option 11: Movies released between 1/4/2000 and 1/4/2005 shorter than 120 minutes ---")

    found = False
    for movie in movies:

        # release_date may already be a datetime object
        if isinstance(movie.release_date, datetime):
            release = movie.release_date
        else:
            release = datetime.strptime(movie.release_date, "%Y-%m-%d")

        if start_date <= release <= end_date and movie.length < 120:
            print(f"- {movie.title} ({movie.length} min, {release.date()})")
            found = True

    if not found:
        print("No movies found that match these criteria.")

if __name__ == "__main__":
    main()