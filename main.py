import keyboard
import time
import string

# If you want more insight into what the program is doing with your actual key presses, or you want to debug the program,
# turn this to True to enable debug printouts.
debug = True

ignoreKeys = ["shift"]
additionalValidChars = ["'", "\""]
minWordSize = 2
maxWordSize = 16

# After this many seconds without a keypress, a word's progress is reset and not added to the WPM count.
# This was chosen with the assumption that most people will take less than 3 seconds between typing letters.
wordTimeoutSeconds = 3

""" Wrapper function for only doing certain prints if the program is running in debug mode. """
def dPrint(*args):
    if debug:
        print(args)


class WPMCalculator:
    # Setup instance vars
    # Handle overall statistic tracking
    numWords = 0
    typingTime = 0

    # Handle tracking word progression information
    wordLength = 0

    wordInProgress = False
    wordStartTime = time.time()  # Set it to some placeholder that doesn't matter but isn't None
    lastLetterTime = time.time()

    def calculateWPM(self, numWords=None, typingTime=None):
        # Can't set self.x variables as a default arguments, so we use these if statements as a workaround
        if numWords is None:
            numWords = self.numWords
        if typingTime is None:
            typingTime = self.typingTime
        return numWords / (typingTime / 60)

    def processEvent(self, event):

        if event.event_type == keyboard.KEY_DOWN:
            dPrint("New Keypress:", event.to_json())

            # Ignore certain keys
            if event.name in ignoreKeys:
                return

            # Reset previous word if it's been too long since the last character has been typed
            # Note that this does not mean a new word can't also start after this
            if event.time - self.lastLetterTime > wordTimeoutSeconds:
                dPrint('Time since last typed character exceeded, resetting word progress.')
                self.wordLength = 0
                self.wordInProgress = False
                # TODO: if a word was in progress, check if it should have been added to the count.

            # Alphanumeric character - start of word or word continuation
            if event.name in string.ascii_letters or event.name in additionalValidChars:
                if self.wordInProgress:
                    self.wordLength += 1
                else:
                    self.wordInProgress = True
                    self.wordStartTime = event.time
                    self.wordLength = 1

            # Space character
            elif event.name == "space":
                if self.wordInProgress:
                    dPrint("Space detected, adding to the word length but ending the word.")
                    self.wordLength += 1
                    self.wordInProgress = False
                else:
                    dPrint("Space detected, but a word wasn't in progress, therefore ignoring the character.")

            # End of word or control sequence abort
            else:
                dPrint('Non word character typed, ending word')

                # Discard the word if the backspace is used
                if event.name != "backspace":

                    # Validate word size
                    if minWordSize <= self.wordLength <= maxWordSize:
                        # If valid, add to word count and typing time
                        self.numWords += 1
                        wordTime = event.time - self.wordStartTime
                        self.typingTime += wordTime
                        dPrint(f'Current word length: {self.wordLength}, time: {wordTime}, WPM: {self.calculateWPM(1, wordTime)}')
                        print(f'Current words: {self.numWords}, time: {self.typingTime}, WPM: {self.calculateWPM()}')
                    else:
                        dPrint("Word too short, ignoring")

                # Reset vars
                self.wordLength = 0
                self.wordInProgress = False

            # Adjust tracking vars
            self.lastLetterTime = event.time


def main():
    calc = WPMCalculator()

    while True:
        # Wait for the next keypress event
        event = keyboard.read_event()
        calc.processEvent(event)


if __name__ == '__main__':
    main()

