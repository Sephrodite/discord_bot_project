"""
Examples for future bot features.

"""

import json
import os
import random
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Example 1: Loading dynamic options from another JSON file
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Example: Loading autocomplete values from separate JSON files
# ---------------------------------------------------------------------------

EXAMPLE_LIST_A_FILE = os.getenv("EXAMPLE_LIST_A_FILE", "example_list_a.json")
EXAMPLE_LIST_B_FILE = os.getenv("EXAMPLE_LIST_B_FILE", "example_list_b.json")


def load_string_list(file_path: str) -> list[str]:
    """
    Load a simple JSON file that contains a list of strings.

    This pattern is useful when a command option should autocomplete
    from data stored outside the command itself.
    """

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        return []

    return [str(item) for item in data]


def get_example_list_a_values() -> list[str]:
    """
    Load values from the first example list file.
    """

    return load_string_list(EXAMPLE_LIST_A_FILE)


def get_example_list_b_values() -> list[str]:
    """
    Load values from the second example list file.
    """

    return load_string_list(EXAMPLE_LIST_B_FILE)


def filter_autocomplete_values(values: list[str], current: str, limit: int = 27) -> list[str]:
    """
    Filter autocomplete values based on what the user has typed.

    Discord autocomplete can return at most 25 choices, so we always limit
    the result.
    """

    current = current.lower().strip()

    if not current:
        return values[:limit]

    matches = [
        value for value in values
        if current in value.lower()
    ]

    return matches[:limit]


# ---------------------------------------------------------------------------
# Example 1: Weighted random table
# ---------------------------------------------------------------------------

# Example table:
# - each top-level key is a group/category
# - each item inside the group is a tuple: (value, weight)
# - higher weight means that value is more likely to be selected
#
# For example:
# In group_one, "alpha" has weight 40 and "delta" has weight 10,
# so "alpha" is more likely to be selected than "delta".

EXAMPLE_TABLE = {
    "group_one": [
        ("alpha", 40),
        ("beta", 30),
        ("charlie", 20),
        ("delta", 10),
    ],
    "group_two": [
        ("alpha", 10),
        ("beta", 20),
        ("charlie", 30),
        ("delta", 40),
    ],
}


def pick_weighted_value(group_name: str) -> str:
    """
    Pick one value from EXAMPLE_TABLE using weighted odds.

    Example:
        result = pick_weighted_value("group_one")

    Later, this pattern can be adapted by replacing EXAMPLE_TABLE with
    whatever real table is needed.
    """

    options = EXAMPLE_TABLE[group_name]

    values = [value for value, weight in options]
    weights = [weight for value, weight in options]

    return random.choices(values, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# Example 2: Small JSON state file
# ---------------------------------------------------------------------------

# This follows the same general idea as saving/loading character data,
# but uses a separate file so unrelated state does not get mixed into
# characters.json.
#
# In production, this file should usually live outside the repo, just like
# the live characters.json file.

EXAMPLE_STATE_FILE = os.getenv("EXAMPLE_STATE_FILE", "example_state.json")


def load_example_state() -> dict:
    """
    Load a small JSON state file.

    If the file does not exist yet, return an empty dictionary.
    """

    if not os.path.exists(EXAMPLE_STATE_FILE):
        return {}

    with open(EXAMPLE_STATE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_example_state(state: dict) -> None:
    """
    Save a small JSON state file.
    """

    with open(EXAMPLE_STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


# ---------------------------------------------------------------------------
# Example 3: "Only once per day" guard
# ---------------------------------------------------------------------------

def already_ran_today() -> bool:
    """
    Check whether this example action already ran today.

    This is useful for any feature that should happen at most once per day.
    """

    state = load_example_state()
    today = datetime.now(timezone.utc).date().isoformat()

    return state.get("last_run_date") == today


def mark_ran_today() -> None:
    """
    Save today's date as the last run date.
    """

    state = load_example_state()
    today = datetime.now(timezone.utc).date().isoformat()

    state["last_run_date"] = today
    save_example_state(state)


# ---------------------------------------------------------------------------
# Example 4: Putting the pieces together
# ---------------------------------------------------------------------------

def run_example_once_per_day() -> str | None:
    """
    Example flow:
    - If this already ran today, return None
    - Otherwise, pick a weighted value
    - Save that it ran today
    - Return the selected value

    This is deliberately generic. Replace "group_one" with whatever category
    should be used in the real feature.
    """

    if already_ran_today():
        return None

    selected_value = pick_weighted_value("group_one")
    mark_ran_today()

    return selected_value


