import random


def game():
    print_opening_message()
    secret_word = upload_secret_word()

    correct_letters = initializes_correct_letters(secret_word)
    print(correct_letters)

    hanged = False
    right = False
    failure = 0

    while(not hanged and not right):

        guess = ask_guess()

        if(guess in secret_word):
            correct_guess_mark(guess, correct_letters, secret_word)
        else:
            failure += 1
            draw_hang(failure)

        hanged = failure == 7
        right = "_" not in correct_letters

        print(correct_letters)

    if(right):
        prints_winner_message()
    else:
        prints_loser_message(secret_word)


def draw_hang(failure):
    print("  _______     ")
    print(" |/      |    ")

    if(failure == 1):
        print (" |      (_)   ")
        print (" |            ")
        print (" |            ")
        print (" |            ")

    if(failure == 2):
        print (" |      (_)   ")
        print (" |      \     ")
        print (" |            ")
        print (" |            ")

    if(failure == 3):
        print (" |      (_)   ")
        print (" |      \|    ")
        print (" |            ")
        print (" |            ")

    if(failure == 4):
        print (" |      (_)   ")
        print (" |      \|/   ")
        print (" |            ")
        print (" |            ")

    if(failure == 5):
        print (" |      (_)   ")
        print (" |      \|/   ")
        print (" |       |    ")
        print (" |            ")

    if(failure == 6):
        print (" |      (_)   ")
        print (" |      \|/   ")
        print (" |       |    ")
        print (" |      /     ")

    if (failure == 7):
        print (" |      (_)   ")
        print (" |      \|/   ")
        print (" |       |    ")
        print (" |      / \   ")

    print(" |            ")
    print("_|___         ")
    print()



def prints_winner_message():
    print("Congratulations, you win!")
    print("       ___________       ")
    print("      '._==_==_=_.'      ")
    print("      .-\\:      /-.     ")
    print("     | (|:.     |) |     ")
    print("      '-|:.     |-'      ")
    print("        \\::.    /       ")
    print("         '::. .'         ")
    print("           ) (           ")
    print("         _.' '._         ")
    print("        '-------'        ")


def prints_loser_message(secret_word):
    print("Failed, you were hanged!")
    print("The word was {}".format(secret_word))
    print("    _______________         ")
    print("   /               \       ")
    print("  /                 \      ")
    print("//                   \/\  ")
    print("\|   XXXX     XXXX   | /   ")
    print(" |   XXXX     XXXX   |/     ")
    print(" |   XXX       XXX   |      ")
    print(" |                   |      ")
    print(" \__      XXX      __/     ")
    print("   |\     XXX     /|       ")
    print("   | |           | |        ")
    print("   | I I I I I I I |        ")
    print("   |  I I I I I I  |        ")
    print("   \_             _/       ")
    print("     \_         _/         ")
    print("       \_______/           ")

def correct_guess_mark(guess, correct_letters, secret_word):
    index = 0
    for word in secret_word:
        if (guess == word):
            correct_letters[index] = word
        index += 1

def ask_guess():
    guess = input("Which letter? ")
    guess = guess.strip().upper()
    return guess

def initializes_correct_letters(word):
    return ["_" for word in word]

def print_opening_message():
    print("*********************************")
    print("**Welcome to the Hangman game!***")
    print("*********************************")

def upload_secret_word():
    archive = open("list.txt", "r")
    word = []

    for line in archive:
        line = line.strip()
        word.append(line)

    archive.close()

    number = random.randrange(0, len(word))
    secret_word = word[number].upper()
    return secret_word


if(__name__ == "__main__"):
    game()
