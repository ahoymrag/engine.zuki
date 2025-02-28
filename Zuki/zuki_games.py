# zuki_games.py

import random
import speech

def magic_trick():
    """
    A quick 'guess-the-number' magic trick where Zuki tries to read your mind.
    You (the user) pick a number in your head, Zuki asks a few questions.
    """

    # Greet the user
    print("\n🪄 Zuki's Magic Trick!")
    speech.speak("Welcome to my magic show. Think of a number between 1 and 100.")

    # We can ask the user to pick a number, but Zuki will "guess" it
    # using a simple binary search approach or random guesses.
    low, high = 1, 100
    guess_count = 0
    while low <= high:
        guess_count += 1
        guess = (low + high) // 2
        print(f"\nZuki guesses: {guess}")
        speech.speak(f"I guess your number is {guess}. Am I right?")

        response = input("(yes / higher / lower): ").strip().lower()
        if response == "yes":
            print(f"🎉 Hooray! I got it in {guess_count} guesses!")
            speech.speak("Hooray! I read your mind!")
            return
        elif response == "higher":
            low = guess + 1
        elif response == "lower":
            high = guess - 1
        else:
            print("❓ Please respond with 'yes', 'higher', or 'lower'.")

    # If we exit the loop, something went wrong
    print("I couldn't guess your number. You might have tricked me!")
    speech.speak("I'm stumped. Better luck next time.")


def twenty_questions():
    """
    A very basic '20 Questions' style game.
    Zuki has a tiny knowledge base. The user thinks of an item,
    and Zuki asks yes/no questions until it tries to guess.
    """

    print("\n❓ Zuki's 20 Questions Game!")
    speech.speak("Let's play 20 Questions! Think of an item, and I'll try to guess it.")

    # A tiny knowledge base to show how it might work
    # Each dictionary item: 'object': [list of yes/no Q&A pairs]
    knowledge_base = {
        "apple": [
            "Is it something you can eat?",
            "Is it a fruit?",
            "Is it typically red or green?"
        ],
        "banana": [
            "Is it something you can eat?",
            "Is it a fruit?",
            "Is it long and yellow?"
        ],
        "dog": [
            "Is it an animal?",
            "Does it bark?",
            "Is it a common household pet?"
        ],
        "cat": [
            "Is it an animal?",
            "Does it meow?",
            "Is it a common household pet?"
        ]
        # You can add more objects...
    }

    # We ask yes/no questions for each item in the knowledge base and see if it matches
    possible_answers = []  # keep track of possible matches
    for item, questions in knowledge_base.items():
        # We'll ask all the questions in 'questions'
        all_yes = True
        for q in questions:
            print("\nZuki asks:", q)
            speech.speak(q)
            answer = input("(yes/no): ").strip().lower()

            # If user says no, item doesn't match
            if answer not in ("yes", "no"):
                print("Please answer yes or no.")
                speech.speak("Please answer yes or no.")
                # Just ask again (simple approach)
                answer = input("(yes/no): ").strip().lower()

            if answer == "no":
                all_yes = False
                break

        if all_yes:
            # All questions matched a 'yes' for this item
            possible_answers.append(item)

    # Now let's guess
    if not possible_answers:
        print("Hmm... I couldn't figure out what you're thinking of!")
        speech.speak("I couldn't guess it. I'm stumped!")
    else:
        guess = random.choice(possible_answers)
        print(f"\nI think you're thinking of a '{guess}'!")
        speech.speak(f"I think you're thinking of a {guess}!")

        # Ask if correct
        confirm = input("Am I right? (yes/no): ").strip().lower()
        if confirm == "yes":
            print("Yay! I guessed it!")
            speech.speak("Yay! I'm correct!")
        else:
            print("Oh no, I'll do better next time!")
            speech.speak("Oh no, I'll do better next time.")