"""
Module 1 - Functional Programming
Developer: Christophe Van Heck
Date: November 2025

Description:
------------
This program reads a CSV file (bord.csv) that contains survey data.
It stores all lines in memory and offers 10 analysis options through
a text-based menu.

Each menu item is implemented in its own function, as required.
The code follows PEP8, includes type hints, comments, and handles
errors gracefully.
"""

from typing import List, Dict
import csv
import sys


# ============================================================
# A) Reading the CSV file
# ============================================================
def read_csv_file() -> List[List[str]]:
    """
    Ask the user for the path to a CSV file until a valid one is read.
    If the user types STOP, the program ends.
    The function skips the header line and returns a list of lists
    containing all rows from the file.
    """
    while True:
        path = input("Enter path to CSV file (or type STOP to exit): ").strip()

        # Allow user to stop the program immediately
        if path.lower() == "stop":
            print("Program stopped by user.")
            sys.exit(0)

        try:
            with open(path, encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)  # skip column names
                contents = [row for row in reader if row]
                print(f"✅ File successfully loaded: {len(contents)} records found.")
                return contents
        except FileNotFoundError:
            print("⚠️ File not found. Please try again.")
        except Exception as e:
            print(f"⚠️ Error reading file: {e}")


# ============================================================
# B) Menu item functions
# ============================================================
def print_line_count(contents: List[List[str]]) -> None:
    """1) Print the number of lines in the dataset."""
    print(f"There are {len(contents)} lines in the file.")


def print_contents(contents: List[List[str]]) -> None:
    """
    2) Print all contents line by line, formatted with column values.
    The id column is NOT the same as the line number.
    """
    for i, row in enumerate(contents, start=1):
        try:
            print(
                f"Line {i}, started on {row[1]}, sent on {row[2]}, "
                f"{row[3]}, {row[4]}, {row[5]}, {row[6]}"
            )
        except IndexError:
            print(f"⚠️ Line {i} is incomplete and was skipped.")


def print_unique_dates(contents: List[List[str]]) -> None:
    """
    3) Show all unique start dates (day/month/year).
    Extracts only the date portion before the time.
    """
    unique_dates = set()
    for row in contents:
        if len(row) > 1 and row[1]:
            date = row[1].split(" ")[0]
            unique_dates.add(date)
    print("Unique submission dates:", sorted(unique_dates))


def print_number_stats(contents: List[List[str]]) -> None:
    """
    4) Print average, minimum, and maximum for the 'random number' column.
    Handles both comma and dot decimals, ignores invalid values.
    """
    numbers = []
    for row in contents:
        if len(row) > 3:
            val = row[3].replace(",", ".").strip()
            try:
                numbers.append(float(val))
            except ValueError:
                continue
    if numbers:
        avg = sum(numbers) / len(numbers)
        print(f"Average: {avg}")
        print(f"Lowest: {min(numbers)}")
        print(f"Highest: {max(numbers)}")
    else:
        print("⚠️ No valid numbers found in the file.")


def print_color_stats(contents: List[List[str]]) -> None:
    """
    5) Count how many times each color appears (case-insensitive).
    Also prints which color appears the most.
    """
    color_counts: Dict[str, int] = {}
    for row in contents:
        if len(row) > 5 and row[5].strip():
            color = row[5].strip().upper()
            color_counts[color] = color_counts.get(color, 0) + 1

    # Display all colors with their counts
    for color, count in color_counts.items():
        print(f"{color}: {count}")

    # Identify the most frequent color
    if color_counts:
        most_common = max(color_counts, key=color_counts.get)
        print(f"The most common color is: {most_common}")


def print_places(contents: List[List[str]]) -> None:
    """
    6) Print all unique place names (case-insensitive, no duplicates).
    """
    places = {row[4].strip().title() for row in contents if len(row) > 4 and row[4].strip()}
    print("Unique places:", sorted(places))


def print_participation_stats(contents: List[List[str]]) -> None:
    """
    7) Count the number of complete and incomplete submissions.
    A submission is complete if the 'datestamp' column is filled.
    """
    total = len(contents)
    complete = sum(1 for row in contents if len(row) > 2 and row[2].strip())
    incomplete = total - complete
    print(f"There are {total} submissions: {complete} complete and {incomplete} incomplete.")


def print_id_stats(contents: List[List[str]]) -> None:
    """
    8) Check if the ID column is consistent (consecutive integers).
    Prints which IDs are missing.
    """
    ids = sorted(int(row[0]) for row in contents if row[0].isdigit())
    if not ids:
        print("⚠️ No valid IDs found.")
        return

    missing = [i for i in range(min(ids), max(ids) + 1) if i not in ids]
    if missing:
        print("Missing ID values:", missing)
    else:
        print("All IDs are consecutive and valid.")


def print_q_stats(contents: List[List[str]]) -> None:
    """
    9) Analyze how many words:
       - start with 'Q'
       - contain 'Q' elsewhere
       - contain no 'Q'
    """
    start_q = mid_q = no_q = 0
    for row in contents:
        if len(row) > 6:
            word = row[6].strip().lower()
            if "q" not in word:
                no_q += 1
            elif word.startswith("q"):
                start_q += 1
            else:
                mid_q += 1
    print(f"{start_q} words start with 'Q'")
    print(f"{mid_q} words contain 'Q' but not at the start")
    print(f"{no_q} words contain no 'Q'")


def save_filtered(contents: List[List[str]]) -> None:
    """
    10) Save all rows with:
         - a valid numeric value
         - and a Q-word that starts with 'Q'
    into a new CSV file with columns: id;number;color;q-word
    """
    filename = input("Enter name of output file (e.g. output.csv): ").strip()
    valid_lines = []

    for row in contents:
        try:
            number = float(row[3].replace(",", "."))
            qword = row[6].strip().lower()
            if qword.startswith("q"):
                valid_lines.append([row[0], row[3], row[5], row[6]])
        except (ValueError, IndexError):
            continue

    try:
        with open(filename, "w", encoding="utf-8") as file:
            for line in valid_lines:
                file.write(";".join(line) + "\n")
        print(f"✅ Saved {len(valid_lines)} valid lines to {filename}")
    except Exception as e:
        print(f"⚠️ Error saving file: {e}")


# ============================================================
# C) Main program (menu system)
# ============================================================
def main() -> None:
    """
    The main menu loop.
    Displays all 10 options and lets the user select one.
    Typing STOP ends the program.
    """
    contents = read_csv_file()

    menu_options = {
        "1": print_line_count,
        "2": print_contents,
        "3": print_unique_dates,
        "4": print_number_stats,
        "5": print_color_stats,
        "6": print_places,
        "7": print_participation_stats,
        "8": print_id_stats,
        "9": print_q_stats,
        "10": save_filtered,
    }

    # Infinite menu loop until STOP is typed
    while True:
        print(
            "\n========= MENU ========="
            "\n1) Line count"
            "\n2) Show contents"
            "\n3) Unique dates"
            "\n4) Number stats"
            "\n5) Color stats"
            "\n6) Places"
            "\n7) Participation stats"
            "\n8) ID stats"
            "\n9) Q-word stats"
            "\n10) Save filtered"
            "\nType STOP to exit."
        )

        choice = input("Choose an option: ").strip().lower()

        if choice == "stop":
            print("👋 Program stopped.")
            break
        elif choice in menu_options:
            menu_options[choice](contents)
        else:
            print("⚠️ Invalid option. Please choose a number between 1–10 or type STOP.")


# ============================================================
# D) Run the program
# ============================================================
if __name__ == "__main__":
    main()
