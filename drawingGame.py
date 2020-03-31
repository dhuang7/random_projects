import random, os


text = open("words.txt", "r")
words = list(set(text))
clear = lambda: os.system('clear')

def pick_random(words):
    return words[random.randint(0, len(words)-1)]

word = pick_random(words)
clear()

restartbool = True

while True:

    while restartbool:
        try:
            clear()
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")
            print("##########      #####      ###  ###  ###       ###   #######  ########  ########")
            print("#########   ########  ####  ###  #  ###  ########  # ######  ########  #########")
            print("##########    #####       ######  ####       ###     #####  ########  ##########")
            print("#############  ###  ###########  ####  ########  ### ####  ########  ###########")
            print("#######       ###  ###########  ####  ########  #### ###       ###       #######")
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")
            print("################################################################################")

            print("\nPress enter to start game...")
            input()
            clear()
            numplayers = int(input("Enter the number of players then press enter: "))
            restartbool = False
            i = 0
            break
        except ValueError:
            print("Please enter a valid number")

    if i == 0:
        word = pick_random(words)
        playerlst = [1]*numplayers
        playerlst[random.randint(0, numplayers-1)] = 0
        clear()
        restart = input("Press enter to start the game\n\nor\n\nType restart then hit enter to restart\n")
        if restart == "restart":
            restartbool = True
            continue
        clear()
    if playerlst[i]:
        print("player {}: ".format(str(i+1)) + word)
    else:
        print("player {}: ".format(str(i+1)) + "you don't know the word\n")
    input("press enter to clear then pass the computer to the next player")
    clear()
    input("press enter to see your word")
    clear()
    i += 1
    i %= numplayers



