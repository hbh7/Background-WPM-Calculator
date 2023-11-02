# Background WPM Calculator

A small program that watches what you type to calculate your actual average words per minute typing speed. Should be more accurate than normal typing tests as it allows you to type anything you'd like, rather than trying to read their text and retype it. 

## Example Output:
```text
Previous word length: 4, time: 0.42801 seconds, WPM: 140.18
Total words: 82, time: 40.87 seconds, WPM: 120.39
Words of size 2: 15 typed, took 4.19 seconds, 214.74 average WPM.
Words of size 3: 21 typed, took 10.56 seconds, 119.33 average WPM.
Words of size 4: 20 typed, took 7.19 seconds, 166.96 average WPM.
Words of size 5: 10 typed, took 6.20 seconds, 96.80 average WPM.
Words of size 6: 7 typed, took 5.29 seconds, 79.36 average WPM.
Words of size 7: 4 typed, took 2.10 seconds, 114.56 average WPM.
Words of size 8: 1 typed, took 0.64 seconds, 93.60 average WPM.
Words of size 9: 4 typed, took 4.70 seconds, 51.03 average WPM.
----------
```

## Methodology
- Alpha (letter) characters and timestamps are counted up until a non-alpha character is detected.
- If the next character is a space or punctuation, these will end the word, but be counted as part of the word for WPM calculation purposes. 
  - This is because the program is more focused on measuring sentences during normal typing, rather than testing individual word typing speeds.
  - Assuming you start the next sentence (as defined by ending with a period and followed by a space or two) within the word timeout period, then it should record the time between words.  
- Numbers and other special characters will end and discard any in-progress word.
- Backspace will end and discard any in-progress word.  
  - A side effect of this behavior is that any further revisions to the word after the backspace might be counted as a new word.
  - This program (currently) does not make any attempt to measure typing accuracy.
- Shortcut sequences and related should be discarded. 
  - Examples: control+c, alt+f4, etc.
- Average WPM is calculated based on the summation words typed and time taken. Words of different lengths are not weighted differently.
  - A possible future expansion might be to remove outliers to improve average accuracy. 
- No compiled build is provided, and the program is written in an interpreted language. This is to make it easier for you to verify that the program is not maliciously key-logging you. 

## Setup Info
This script was written for Windows environments, but as long as your system can run `Python 3`, any OS will probably work just fine. You also need to install the required packages using `pip install -r requirements.txt`. Afterward, you can use Python 3 to run the script, such as via `python main.py`. If desired, you can edit `main.py` and tweak the variables near the top of the file to modify the program's behavior. 

Feel free to open an issue if you have any questions or if something isn't working right!

