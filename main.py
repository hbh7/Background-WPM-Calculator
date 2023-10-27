import keyboard
import time
import string


ignoreKeys = ["shift"]
additionalValidChars = ["'", "\""]
minWordSize = 2
maxWordSize = 16
wordTimeoutSeconds = 5

def calculateWPM(numWords, typingTime):
    return numWords / (typingTime / 60)

def main():

    numWords = 0
    typingTime = 0

    wordLength = 0

    wordInProgress = False
    wordStartTime = time.time()  # Set it to some placeholder that doesn't matter but isn't None
    lastLetterTime = time.time()

    while True:
        # Wait for the next keypress event
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(event.to_json())
            #print(event.time)
            #print(event.name)

            # Ignore certain keys
            if event.name in ignoreKeys:
                continue

            # Reset previous word if it's been too long since the last character has been typed
            # Note that this does not mean a new word can't also start after this
            if event.time - lastLetterTime > wordTimeoutSeconds:
                wordInProgress = False
                # TODO: if a word was in progress, check if it should have been added to the count.

            # Alphanumeric character - start of word or word continuation
            if event.name in string.ascii_letters or event.name in additionalValidChars:
                if wordInProgress:
                    wordLength += 1
                else:
                    wordInProgress = True
                    wordStartTime = event.time
                    wordLength = 1


            # End of word or control sequence abort
            #elif event.name == 'space' or event.name == 'space':
            else:
                print('Non word character typed, ending word')

                # Discard the word if the backspace is used
                if event.name != "backspace":

                    # Validate word size
                    if minWordSize <= wordLength <= maxWordSize:
                        # If valid, add to word count and typing time
                        numWords += 1
                        wordTime = event.time - wordStartTime
                        typingTime += wordTime
                        print(f'Current word length: {wordLength}, time: {wordTime}, WPM: {calculateWPM(1, wordTime)}')
                        print(f'Current words: {numWords}, time: {typingTime}, WPM: {calculateWPM(numWords, typingTime)}')
                    else:
                        print("Word too short, ignoring")

                # Reset vars
                wordLength = 0
                wordInProgress = False

            # Adjust tracking vars
            lastLetterTime = event.time



if __name__ == '__main__':
    main()

