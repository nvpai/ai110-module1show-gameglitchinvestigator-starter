# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

I used Claude (Claude Code) as the agent.

**What task did you give the agent?**

I asked the agent to fix the difficulty levels so the game gets harder as you go up, and to recommend good range and attempt values across Easy, Normal, and Hard.

**What did the agent do?**

- Pointed out that the difficulty curve was inverted: Hard's range was `1–50`, smaller than Normal's `1–100`, so Hard was actually easier.
- Suggested a monotonic curve (range goes up, attempts go down): Easy `1–20` / 8 tries, Normal `1–100` / 7 tries, Hard `1–200` / 6 tries.
- Edited `get_range_for_difficulty` in `logic_utils.py` (Hard → `1, 200`).
- Edited `attempt_limit_map` in `app.py` (8 / 7 / 6).
- Updated the matching test in `tests/test_game_logic.py` and added 3 new tests guarding that the range widens with difficulty.
- Ran `pytest` to confirm all 23 tests passed.

**What did you have to verify or fix manually?**

I checked the new numbers actually made sense by playing each difficulty. I also reviewed the agent's note that Hard (6 tries for 1–200) is below the binary-search optimum, meaning Hard isn't always winnable even with perfect play — I decided to keep it that way on purpose so Hard feels hard.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** "For each bug found and fixed so far, create a test case for each — generate a pytest case in tests/test_game_logic.py that specifically targets the bug you just fixed."

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Non-numeric input | (above) | `test_parse_non_number_rejected` — `parse_guess("abc")` returns not-ok with an error | ✅ Yes | The game should reject letters instead of crashing. |
| Empty / `None` input | (above) | `test_parse_empty_and_none_rejected` — both return `ok = False` | ✅ Yes | Pressing submit with nothing typed shouldn't break the game. |
| Decimal string | (above) | `test_parse_float_string_truncates_to_int` — `"42.9"` becomes `42` | ✅ Yes | Confirms how the game handles a typed decimal. |
| Out-of-range / negative | (above) | `test_out_of_range_guess_is_outside_difficulty_bounds` — `104` and `-1` fall outside `1–100` | ✅ Yes | These were wrongly accepted before, so this guards the range check. |
| Hint direction (inverted-hint bug) | (above) | `test_guess_below_secret_says_go_higher` / `test_guess_above_secret_says_go_lower` | ✅ Yes | Locks in the fix for the backwards hints. |
| Secret as text (string-secret bug) | (above) | `test_string_secret_below_guess_still_correct` and 2 more | ✅ Yes | Catches the `str(secret)` type-mismatch bug if it returns. |
| Difficulty curve | (above) | `test_range_widens_with_difficulty` / `test_hard_is_not_narrower_than_normal` | ✅ Yes | Guards against Hard being easier than Normal again. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Move all the logic functions to logic_utils.py with professional docstrings,
and check the code for style issues.
```

**Linting output before:**

```
$ python3 -m pyflakes logic_utils.py app.py
pyflakes: no issues
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
