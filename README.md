# Background WPM Calculator

A small program that watches what you type to calculate your actual average words per minute typing speed. Should be more accurate than normal typing tests as it allows you to type anything you'd like, rather than trying to read their text and retype it. 

Lots of work to still do, stay tuned!

## Methodology
- Alpha (letter) characters and timestamps are counted up until a non-alpha character is detected.
- If the next character is a space or punctuation, these will end the word, but be counted as part of the word for WPM calculation purposes. 
  - This is because the program is more focused on measuring sentences during normal typing, rather than testing individual word typing speeds.
- Numbers and other special characters will end and discard any in-progress word.
- Backspace will end and discard any in-progress word. This program (currently) does not make any attempt to measure typing accuracy. 

## Setup Info
This script was written for Windows environments, but as long as your system can run `Python 3`, any OS will probably work just fine. You also need to install the required packages using `pip install -r requirements.txt`. Afterward, you can use Python 3 to run the script, such as via `python main.py`. 

Feel free to open an issue if you have any questions or if something isn't working right!

