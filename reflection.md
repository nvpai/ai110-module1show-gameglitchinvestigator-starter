# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

When I first ran the game, it looked fine but it was impossible to play correctly. The hints were backwards: I entered a number below the secret (33) and it told me to "Go LOWER" when it should have said "Go HIGHER." The history list was also wrong — when I submitted a number, the history showed the previous number instead of the one I just entered. On top of that, the "Attempts allowed" said 8 in Normal mode but I could only guess 7 times, and the "New Game" button did nothing.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `2` (secret = 33) | Hint says "Go HIGHER" | Hint said "Go LOWER" | None |
| Guess `10` after guessing `5` | History shows `[5, 10]` | History showed only `[5]` (lagged one guess) | None |
| Make 8 guesses in Normal mode | 8 attempts allowed | Game ended after 7 guesses | "Out of attempts! The secret was 33." |
| Switch difficulty to Easy (range 1–20) | Secret is between 1 and 20 | Secret was 63 (out of range) | None |
| Enter `104` in Normal mode | Rejected (out of range 1–100) | Accepted as a normal guess | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude (Claude Code) for this project. It acted like a debugging partner — I described what I saw in the game and it explained the cause and suggested fixes.

**A correct suggestion:** When the hints were still wrong on every other guess, Claude explained that the code was converting the secret to a string (`str(secret)`) on even-numbered attempts, so it was comparing a number to text. That comparison raised a `TypeError` and fell into a broken fallback. It suggested keeping the secret as an integer every turn. I verified this by playing several rounds — the hints were finally correct on every guess — and by writing a pytest case (`test_string_secret_below_guess_still_correct`) that passed.

**An incorrect/misleading suggestion:** The first time I reported the backwards hints, the AI said swapping the two hint messages in `check_guess` would fully fix it. I made that change, but the hints were still wrong on alternate guesses. The first explanation was incomplete — it missed the separate string-conversion bug. I caught this by testing again instead of trusting the fix, which is how the second, deeper bug was found.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To know if a bug was really fixed, I did two things. First, I played the game again and repeated the exact steps that caused the bug to make sure it was gone. Second, I wrote a pytest test for that bug so it would warn me if it ever came back. For example, I ran `test_guess_below_secret_says_go_higher`, which guesses 5 when the secret is 33 and checks the hint says "HIGHER" — it passed, so I knew the hint direction was finally right. AI helped me write the tests by suggesting one test per bug and explaining what each one was checking. In the end, all 23 tests passed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-runs the entire script from top to bottom every time you click a button or type something. So any normal variable gets created fresh each run — that is why the secret number kept changing until it was stored in `st.session_state`, which is the one place that survives between reruns. The history bug taught me that order matters too: the history was being displayed near the top of the script before the new guess was added lower down, so it always showed one step behind. Once I understood reruns, most of the "weird" bugs made sense — they were really about when code runs and where data is stored.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing a pytest case for every bug right after I fix it, so the bug can never quietly come back. Next time I would test an AI's fix before moving on, because the very first fix here looked right but only solved half the problem. This project taught me that AI-generated code can look clean and confident while still being wrong, so I now treat AI suggestions as a starting point to verify, not a final answer to trust.
