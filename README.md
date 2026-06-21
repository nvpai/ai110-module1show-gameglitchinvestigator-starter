# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**The game's purpose:** A simple number guessing game built with Streamlit. The app picks a secret number based on the difficulty you choose, and you try to guess it within a limited number of tries. After each guess it tells you to go higher or lower until you win or run out of attempts.

**Bugs I found:**
1. The hints were backwards — it said "Go LOWER" when it should have said "Go HIGHER" (`check_guess` had the labels and messages swapped).
2. The hints were also wrong on every other guess because the secret was turned into text with `str(secret)` on even attempts, so a number was being compared to text.
3. The history showed the previous guess instead of the one I just entered, because the history was drawn before the new guess was added.
4. Normal mode said 8 attempts but only allowed 7, because the attempts counter started at 1 instead of 0.
5. The "New Game" button did nothing because it never reset the game's status.
6. Out-of-range numbers like 104 or -1 were accepted, and they even used up an attempt.
7. The difficulty was wrong: Hard's range (1–50) was smaller than Normal's (1–100), so Hard was actually easier.

**Fixes I applied:**
1. Made the comparison, label, and hint all agree in `check_guess` so the direction is correct.
2. Removed the `str(secret)` line so the secret stays a number every turn.
3. Moved the debug/history panel to the bottom so it shows the latest guess.
4. Started attempts at 0 and only count valid in-range guesses, so you get the full number of tries.
5. Made "New Game" reset attempts, secret, score, status, and history.
6. Added a range check so out-of-range guesses are rejected without using an attempt.
7. Fixed the difficulty levels: Easy 1–20 (8 tries), Normal 1–100 (7 tries), Hard 1–200 (6 tries).
8. Moved the logic functions into `logic_utils.py` so `app.py` only has the UI code.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the app in your browser.
2. Pick a difficulty in the sidebar (Easy, Normal, or Hard). The range and attempts update to match.
3. Type a number and click **Submit Guess 🚀**. Your guess is added to the history right away.
4. Read the hint ("📈 Go HIGHER!" or "📉 Go LOWER!") and guess again. "Attempts left" only goes down for valid guesses.
5. Guess the secret to win 🎉, or click **New Game 🔁** any time to start a fresh round.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->


## 🧪 Test Results

```
$ python -m pytest tests/
platform darwin -- Python 3.12.7, pytest-9.0.3, pluggy-1.6.0
collected 23 items

tests/test_game_logic.py .......................                         [100%]

============================== 23 passed in 0.01s =============================
```

## 🚀 Stretch Features

- [x] **Difficulty levels:** Three levels with their own range and attempts, tuned so the game gets harder as you go up (see `get_range_for_difficulty` in `logic_utils.py` and `attempt_limit_map` in `app.py`).
- [x] **Edge-case tests:** 23 pytest cases covering non-numeric input, empty/`None` input, negative and out-of-range numbers, and the inverted-hint bugs (see `tests/test_game_logic.py`).
- [x] **UI touches:** Emoji hints (📈/📉), a live "Attempts left" counter, win balloons, and a "Developer Debug Info" panel to inspect game state.
