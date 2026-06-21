"""
Regression tests for bugs found and fixed in the Game Glitch Investigator.

Each test documents the specific glitch it guards against.
"""

import os
import sys

import pytest

# Allow importing logic_utils.py from the project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# 
# check_guess returns a (outcome, message) tuple, so the outcome is unpacked.
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# BUG 1: check_guess hints were inverted.
# A guess BELOW the secret used to say "Go LOWER" (and vice versa).
# Correct: guess > secret -> "Too High" + go lower; guess < secret -> "Too Low" + go higher.
# ---------------------------------------------------------------------------

def test_guess_below_secret_says_go_higher():
    outcome, message = check_guess(5, 33)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_guess_above_secret_says_go_lower():
    outcome, message = check_guess(90, 33)
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_exact_guess_wins():
    outcome, message = check_guess(33, 33)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# BUG 2: On even attempts the secret was cast to str(...), so check_guess
# compared int vs str. That raised TypeError and produced backwards hints.
# The fallback branch must now coerce to int and return the correct direction.
# ---------------------------------------------------------------------------

def test_string_secret_below_guess_still_correct():
    # guess (int) is below a stringified secret -> should say go higher
    outcome, message = check_guess(5, "33")
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_string_secret_above_guess_still_correct():
    outcome, message = check_guess(90, "33")
    assert outcome == "Too High"
    assert "LOWER" in message.upper()


def test_string_secret_equal_guess_wins():
    outcome, _ = check_guess(33, "33")
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# BUG 3: Easy mode produced an out-of-range secret because the range mapping
# was wrong / hardcoded. Ranges must match each difficulty.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "difficulty,expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 200)),
        ("Unknown", (1, 100)),  # default fallback
    ],
)
def test_range_for_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


# ---------------------------------------------------------------------------
# BUG 5: difficulty curve was not monotonic. Hard used to be 1-50, which is a
# NARROWER range than Normal's 1-100, making "Hard" actually easier.
# The range must widen as difficulty increases: Easy < Normal < Hard.
# ---------------------------------------------------------------------------

def test_range_widens_with_difficulty():
    easy_high = get_range_for_difficulty("Easy")[1]
    normal_high = get_range_for_difficulty("Normal")[1]
    hard_high = get_range_for_difficulty("Hard")[1]

    assert easy_high < normal_high < hard_high


def test_hard_is_not_narrower_than_normal():
    # Direct guard against the original inversion (Hard 1-50 < Normal 1-100).
    assert get_range_for_difficulty("Hard")[1] > get_range_for_difficulty("Normal")[1]


def test_all_ranges_start_at_one():
    for difficulty in ("Easy", "Normal", "Hard"):
        low, _ = get_range_for_difficulty(difficulty)
        assert low == 1


# ---------------------------------------------------------------------------
# BUG 4 (input validation / parsing): out-of-range and junk input were
# accepted. parse_guess must report bad input rather than crashing.
# Range enforcement itself happens in the UI using get_range_for_difficulty.
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_float_string_truncates_to_int():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_empty_and_none_rejected():
    assert parse_guess("")[0] is False
    assert parse_guess(None)[0] is False


def test_parse_non_number_rejected():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err is not None


def test_out_of_range_guess_is_outside_difficulty_bounds():
    # Demonstrates the check the UI now performs for Normal mode.
    low, high = get_range_for_difficulty("Normal")
    assert not (low <= 104 <= high)
    assert not (low <= -1 <= high)


# ---------------------------------------------------------------------------
# update_score sanity (guards the scoring branches used by the outcomes above).
# ---------------------------------------------------------------------------

def test_win_awards_points_with_floor():
    # Late win still floors at +10.
    assert update_score(0, "Win", attempt_number=20) == 10


def test_too_low_loses_points():
    assert update_score(50, "Too Low", attempt_number=3) == 45
