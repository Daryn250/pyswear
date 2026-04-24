# pyswear
Minimal Python Library for Swear filters

validate_text(message) -> Validates a message, returns false if profanity found.
- ascii_clean (allow ascii cleaning)
- allow_utf8 (restrict to only ascii characters)
- letter_swap_test (swaps first letters of adjacent words to see if swears are created)
- check_reverse (reverse string and then check profanity
- debug (print statements)
- profanity_percent (sensitivity of the detector. defaults at 0.85. can go higher than 1)
