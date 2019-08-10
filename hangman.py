import requests
import json
from random import randrange
import os

# request a 151 pokemon long list
request = requests.get("https://pokeapi.co/api/v2/pokemon?limit=151")
parsed = json.loads(request.text)["results"]

print(" ")
print("WELCOME TO POKEMON HANGMAN!")
print("Discover the hidden pokemon name")
print(" ")

# define os for clear console function
def cls():
    os.system("cls" if os.name == "nt" else "clear")

# the game
while True:

    # choose a level to play
    while True:

        level = raw_input("Choose a difficulty level from 1 to 5: ")

        if level == "1":
            top_strikes = 10
            # clear the screen
            cls()
            break
        elif level == "2":
            top_strikes = 9
            # clear the screen
            cls()
            break
        elif level == "3":
            top_strikes = 8
            # clear the screen
            cls()
            break
        elif level == "4":
            top_strikes = 7
            # clear the screen
            cls()
            break
        elif level == "5":
            top_strikes = 6
            # clear the screen
            cls()
            break
        else:
            print("Enter a number from 1 to 5")

    # get random pokemon
    pokemon_index = randrange(151)
    counter = 0
    for pokemon_item in parsed:
        counter = counter + 1
        if pokemon_index == counter:
            # establish a string to be displayed at the end of the game with the hidden result
            pokemon_result = pokemon_item["name"]
            # establish a string to be substituted with "0" each time a letter is correctly guessed
            pokemon = pokemon_item["name"]
            # get selected pokemon type
            pokemon_result_data = requests.get("https://pokeapi.co/api/v2/pokemon/%s" % pokemon_result)
            parsed_pokemon_result_data = json.loads(pokemon_result_data.text)["types"][0]["type"]["name"]

    # set an list for pokemon letters to be stored
    letters_list = []

    # set a string for pokemon letters to be stored
    letters_string = ""

    # loop through previously entered pokemon to fill in the list with as many underscores as letters
    for x in range(len(pokemon)):
        letters_list.append("_")

    # make a string out of the list to print on the screen
    letters_string = " ".join(letters_list)

    # print on the screen
    print(letters_string)

    # set number of strikes
    strikes = 0

    # set list for letters guessed
    guesses = []

    while strikes < top_strikes:

        # function to display messages in each guess
        def status_print(strikes, top_strikes, guesses, letters_string, message):
            print('Last shot: %s' % message)
            print("Strikes: %s/%s" % (strikes, top_strikes))
            print("Letters already tried: %s" % guesses)
            print(letters_string.upper())

            if strikes == top_strikes - 1:
                print(" ")
                print("WATCH OUT!")
                print("You have only one strike left!")
                print("Hint: It's a %s type pokemon!" % parsed_pokemon_result_data)

            print(" ")

        # input, try to guess a letter from pokemon
        while True:

            shot = raw_input("Try guessing a letter: ")

            # do not allow more than one characters
            if len(shot) == 1:

                break

            print(" ")
            print("Please enter only one string character")
            print(" ")

        # get the index inside the string where the ocurrence took place
        index = pokemon.find(shot)

        # in case is correct
        if index != -1:

            # loop same letter until index = pokemon.find(shot) is no longer != -1
            while True:

                if index != -1:

                    # add correct chosen letter to list
                    letters_list.insert(index, shot)
                    # remove underscore from correct chosen letter index from list
                    letters_list.pop(index + 1)

                    pokemon = pokemon.replace(shot, "0", 1)

                    # find a new ocurrence of shot3 in pokemon string
                    index = pokemon.find(shot)

                    # convert resulted list into a string to be printed
                    letters_string = " ".join(letters_list)

                else:

                    # add new shot to guesses list
                    guesses.append(shot)

                    # clear the screen
                    cls()

                    # print all inputs and guesses
                    status_print(
                        strikes, top_strikes, guesses, letters_string, "Correct!"
                    )
                    break

            # is every character in pokemon string = 0? then display success message
            string_len_checker = int(len(pokemon))
            if pokemon == string_len_checker * "0":
                print("Congratulations, you won!")
                break

        # in case is not correct
        elif index == -1:

            # add one strike
            strikes = strikes + 1

            # add to log of letters guessed
            guesses.append(shot)

            # clear the screen
            cls()

            # print all inputs and guesses
            status_print(strikes, top_strikes, guesses, letters_string, "Missed!")

            if strikes == top_strikes:
                print("The pokemon was: %s" % pokemon_result.upper())
                print("Game over")
                print(" ")

    # ask if want to quit playing
    quit_playing = raw_input("Enter any key to continue, 'q' to quit: ")

    # clear the screen
    cls()

    if quit_playing == "q":
        break

