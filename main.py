import keyboard
import time
import string

# If you want more insight into what the program is doing with your actual key presses, or you want to debug the program,
# turn this to True to enable debug printouts.
debug = False

# Adjust these if desired to modify exactly how words are tracked
# Defines the minimum length of words to count
minWordSize = 2
# Defines the maximum length of words to count
maxWordSize = 16
# After this many seconds without a keypress, a word's progress is reset and not added to the WPM count.
# This was chosen with the assumption that most people will take less than 2 seconds between typing letters.
# If you're a fast typist, you may want to decrease this value to 1.
# If you're a bit slower, you may want to increase it to 3.
wordTimeoutSeconds = 2

# Configure keys that modify the program's behavior
ignoreKeys = ["shift"]
shortcutKeys = ["ctrl", "right ctrl", "alt", "alt gr", "left windows", "right windows"]
additionalValidChars = ["'", "\""]


""" Wrapper function for only doing certain prints if the program is running in debug mode. """
def dPrint(*args):
    if debug:
        print(*args)


""" Helper function to sum up all values in the hashmap """
def sumHashmapValues(h):
    return sum(h.values())


""" Main class that helps to track all information for WPM calculations """
class WPMCalculator:
    # Setup instance vars
    # Handle overall statistic tracking
    # Hashmaps with keys of length and values of number of words / word type times for those lengths
    numWordsByLength = {}
    wordTimeByLength = {}

    # Handle tracking current word progression information
    wordInProgress = False
    wordLength = 0
    shortcutSequenceLockout = False

    # Track various times. Set these times to some placeholder that doesn't matter but isn't None
    wordStartTime = time.time() - wordTimeoutSeconds
    lastLetterTime = time.time() - wordTimeoutSeconds
    lastWordEndTime = time.time() - wordTimeoutSeconds

    """ Calculates and returns the WPM using self.numWords and self.typingTime, or provided values if present """
    def calculateWPM(self, numWords=None, typingTime=None):
        # Can't set self.x variables as a default arguments, so we use these if statements as a workaround
        if numWords is None:
            numWords = sumHashmapValues(self.numWordsByLength)
        if typingTime is None:
            typingTime = sumHashmapValues(self.wordTimeByLength)
        # Calculate the WPM
        return numWords / (typingTime / 60)

    """ Records the last time a letter was typed """
    def recordLastLetterTime(self, event):
        self.lastLetterTime = event.time

    """ Starts a new word by updating word tracking information """
    def startWord(self, event):
        self.wordInProgress = True
        self.wordLength = 1
        # If it's been a very short time since the previous word ended, this time should be counted for better accuracy
        if event.time - self.lastWordEndTime < wordTimeoutSeconds:
            self.wordStartTime = self.lastWordEndTime
        else:
            self.wordStartTime = event.time

    """ Continues a word by adding another letter and time amount to the word tracking information """
    def continueWord(self):
        self.wordLength += 1

    """ Resets word tracking information """
    def resetWord(self):
        self.wordInProgress = False
        self.wordLength = 0

    """ Records information about the current word, then prepares for the next word (resets word tracking information) """
    def recordWord(self, event=None):
        # Validate word size
        if minWordSize <= self.wordLength <= maxWordSize:
            # If valid, add to word count and typing time
            self.numWordsByLength[self.wordLength] = self.numWordsByLength.get(self.wordLength, 0) + 1
            # If an event was provided, use the times from it, otherwise use the last letter time
            if event is not None:
                wordTime = event.time - self.wordStartTime
                self.lastWordEndTime = event.time
            else:
                wordTime = self.lastLetterTime - self.wordStartTime
                self.lastWordEndTime = self.lastLetterTime
            # Update counters and print stats
            self.wordTimeByLength[self.wordLength] = self.wordTimeByLength.get(self.wordLength, 0) + wordTime
            self.printWordStats(wordTime)
            self.printAllStats()
        else:
            dPrint("Word too short, ignoring")
        # Reset counters
        self.resetWord()

    """ Helper function to handle shortcut sequence keys by setting/unsetting tracking values """
    def handleShortcutKeys(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            self.shortcutSequenceLockout = True
            # If a shortcut sequence is started, reset the word for good measure
            self.resetWord()
        elif event.event_type == keyboard.KEY_UP:
            self.shortcutSequenceLockout = False

    """ Function to print out statistics for the current word """
    def printWordStats(self, wordTime):
        print(f'Previous word length: {self.wordLength}, '
              f'time: {wordTime:.5f} seconds, '
              f'WPM: {self.calculateWPM(1, wordTime):.2f}')

    """ Function to print out statistics about all words """
    def printAllStats(self):
        print(f'Total words: {sumHashmapValues(self.numWordsByLength)}, '
              f'time: {sumHashmapValues(self.wordTimeByLength):.2f} seconds, '
              f'WPM: {self.calculateWPM():.2f}')
        # Print stats based around the lengths of words
        for length in sorted(self.numWordsByLength.keys()):
            number = self.numWordsByLength[length]
            typeTime = self.wordTimeByLength[length]
            wpm = self.calculateWPM(number, typeTime)
            print(f'Words of size {length}: {number} typed, took {typeTime:.2f} seconds, {wpm:.2f} average WPM.')
        print("-" * 10)

    """ Handles whenever a keyboard event is received """
    def processEvent(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            dPrint("New Keypress:", event.to_json())

            # Ignore certain keys
            if event.name in ignoreKeys:
                return

            # Reset previous word if it's been too long since the last character has been typed
            # Note that this does not mean a new word can't also start after this
            if self.wordInProgress and event.time - self.lastLetterTime > wordTimeoutSeconds:
                dPrint('Time since last typed character exceeded, saving and resetting word progress.')
                self.recordWord()

            # Shortcut sequences - don't start a word if a shortcut is being used
            if event.name in shortcutKeys:
                self.handleShortcutKeys(event)
            elif self.shortcutSequenceLockout:
                dPrint("Shortcut sequence lockout active, ignoring characters until reset.")

            # Alphanumeric character - start of word or word continuation
            elif event.name in string.ascii_letters or event.name in additionalValidChars:
                if self.wordInProgress:
                    self.continueWord()
                else:
                    self.startWord(event)

            # Space character
            elif event.name == "space":
                if self.wordInProgress:
                    dPrint("Space detected, ending the word.")
                    self.recordWord(event)
                else:
                    dPrint("Space detected, but a word wasn't in progress, therefore ignoring the character.")

            # End of word via the use of any other character
            else:
                dPrint('Non word character typed, ending word')
                # Discard the word if the backspace is used
                if event.name == "backspace":
                    self.resetWord()
                else:
                    self.recordWord(event)

            # Record when the last letter was typed for use later
            self.recordLastLetterTime(event)

        # Check for key_up events to use with shortcut tracking
        elif event.event_type == keyboard.KEY_UP:
            if event.name in shortcutKeys:
                self.handleShortcutKeys(event)


""" Main function that creates the class instance and starts watching for keyboard events """
def main():
    calc = WPMCalculator()

    while True:
        # Wait for the next keypress event and send it for processing.
        event = keyboard.read_event()
        calc.processEvent(event)


if __name__ == '__main__':
    main()
