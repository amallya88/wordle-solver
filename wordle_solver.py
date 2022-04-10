import random
import re

def get_user_guess(wrd_list: list) -> 'str':
    while True:
        user_guess = input("Enter the guess or !list to see word list or !q to quit: \n").lower()
        if user_guess == "!list":
            list_viewer(wrd_list)
        if len(user_guess) != 5:
            print(user_guess + " is not a five letter word")
            continue
        if not user_guess.isalpha():
            print(user_guess + " not a word")
            continue
        if user_guess not in wrd_list:
            print(user_guess + " seems to be an invalid word")
            while True:
                decision = input("Are you sure this is a valid word? (y/n): ")
                if decision == "y" or decision == "n":
                    break
            if decision == "n":
                continue
        return user_guess


def get_game_response() -> 'str':
    p = "[^\/+#]"  # match any characters that are not /, +, or #
    while True:
        guess_match_rtg = input("Enter / for mismatch, + for full-match, and # for \n"
                               "letters in wrong position: \n")
        if len(guess_match_rtg) != 5:
            print("Too many characters")
            continue
        if re.search(p, guess_match_rtg):
            print("Invalid characters entered. Only enter /, + or #")
            continue
        return guess_match_rtg


def get_filtered_wl(user_guess: str, guess_match_rtg: str, wrd_list: list) -> 'list':
    f1 = wrd_list
    f2 = []
    char_pos = 0
    exact_pattrn = "." * 5
    for c, r in zip(user_guess, guess_match_rtg):
        char_pos = char_pos + 1
        if r == "/":
            f2 = [w for w in f1 if c not in w]  # words without non-matching character
        elif r == "#":
            f2 = [w for w in f1 if c in w]  # words with character that is in wrong position
        elif r == "+":  # exact match position of char
            exact_pattrn = exact_pattrn[:char_pos - 1] + c + exact_pattrn[char_pos:]
            f2 = [w for w in f1 if re.search(exact_pattrn, w)]
        f1 = f2.copy()
    return f2


def list_viewer(wrd_list: list):
    user_in = ""
    while user_in != '!q':
        user_in = input("Enter a pattern to see a list of possible words,\n"
                        "!rand to get a random suggestion or !q to quit: ")
        if user_in == "!q":
            break
        elif user_in == "!rand":
            print(get_random_word(wrd_list))
            continue
        user_in = "^" + user_in  # add start of line anchor
        if len(user_in) > 5:
            print("Invalid pattern")
            continue
        disp_list = [w for w in wrd_list if re.search(user_in, w)]
        print("There are {} words matching the pattern".format(len(disp_list)))
        for i in range(0, len(disp_list), 8):
            l = disp_list[i:i+8]
            print(l)



def get_random_word(lst):
    w = random.randint(0, len(lst))
    return lst[w]


if __name__ == "__main__":

    five_letter_words = []
    active_list = []
    user_guess = ""

    with open('five_letter_words.txt', 'r', encoding="utf-8") as f:
        five_letter_words = [w.strip('\n') for w in f.readlines()]

    active_list = five_letter_words.copy()
    print("There are {} possible five letter words".format(len(active_list)))

    for _ in range(6):
        user_guess = get_user_guess(active_list)
        if user_guess == "!q":
            print("It was a pleasure!~")
            break
        guess_match_rtg = get_game_response()
        active_list = get_filtered_wl(user_guess, guess_match_rtg, active_list)
        print("There are {} five letter words remaining".format(len(active_list)))
        print("Entering word list browser...")
        list_viewer(active_list)
