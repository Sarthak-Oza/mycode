#!/usr/bin/python3

import time
import threading
import curses
import os
import random
from roomsmap import printMap
from rooms import rooms
from player import Player
from gun import Gun

# countdown when player in kicthen, to avoid locking the kitchen
countdown_completed = False

# Start the player in the Hall
currentRoom = "Hall"

# create a player
player_name = "Player"
player = Player(player_name)
gun = None

# total number of moves
moves_counter = 0


def showStatus():
    print("----------RPG Game----------")
    print("You are in the " + currentRoom)
    print("---------------------------")
    print("Commands:\ngo [direction]\nget [item]\nquit ")
    print("---------------------------")

    # getting directions player can go to
    print(
        "You can go to: "
        + " or ".join(
            [
                f"{key} ({rooms[currentRoom][key]})"
                for key in rooms[currentRoom].keys()
                if key in {"north", "south", "east", "west"}
            ]
        )
    )

    # print the current inventory
    print("Inventory: " + ", ".join(str(item) for item in player.get_inventory()))

    # print an item if there is one
    if rooms[currentRoom]["item"]:
        print("You see: " + ", ".join(rooms[currentRoom]["item"]))

    # print the player's energy
    print(f"Energy: {player.energy}")

    # get bullets in player's gun
    gun_item = next(
        (item for item in player.get_inventory() if isinstance(item, Gun)), None
    )

    if gun_item:
        bullets = gun_item.get_bullets()
        print(f"Bullets in Gun: {bullets}")

    print("---------------------------")

    # print total number of moves
    print(f"Total Moves: {moves_counter}")
    print("---------------------------")

def crushing_walls():
    global countdown_completed, moves_counter
    countdown_completed = False

    stdscr = curses.initscr()
    stdscr.nodelay(1)  # Set non-blocking mode for keyboard input
    for i in range(5, 0, -1):
        stdscr.addstr(0, 0, f"*** Kitchen walls closing, press key `e` to stop or you will be locked.***\nTime left: {i}")
        stdscr.refresh()
        # Check for keyboard input
        key = stdscr.getch()
        if key == ord('e'):
            curses.endwin()
            moves_counter += 1
            return
        time.sleep(1)

    curses.endwin()
    countdown_completed = True


# function for countdown that begins when player enters the room
def countdown():
    t = threading.Thread(target=crushing_walls)
    t.start()
    # wait for the thread to finish
    t.join()


def initialize_game():
    os.system("cls" if os.name == "nt" else "clear")
    printMap()
    print(
        """
You start the game in the Hall and can go to different rooms.
Potion will give you 20 more energy, and you can load an extra 5 bullets from the Hall.
You will need to defeat monsters and require a key to escape via the garden.
The kitchen door will be locked automatically in 5 seconds if you don't press the 'e' key.
        """
    )

initialize_game()

# --------------------------------------------------------------------  main function to play game  ------------------------------------------------------------------------
def play_game():
    global currentRoom, player_name, moves_counter, gun
    while True:
        showStatus()
        move = ""
        while move == "":
            move = input(">")

        move = move.lower().split(" ", 1)

        # go instructions handling
        if move[0] == "go":
            if move[1] in rooms[currentRoom]:
                currentRoom = rooms[currentRoom][move[1]]

                # increase moves counter
                moves_counter += 1

                # if player enter the kitchen kitechen walls will start closing
                if currentRoom == "Kitchen":
                    print(
                        f"!!!!!!!!!{currentRoom} will be locked in 5 seconds!!!!!!!!\nPress `e` to stop closing of the room door."
                    )
                    countdown()

                os.system("cls" if os.name == "nt" else "clear")    

            else:
                print("*** You can't go that way! ***\n")


        # get instructions handling
        elif move[0] == "get":
            if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]["item"]:
                # if get potion, energize player by 20
                if move[1] == "potion":
                    if player.get_energy() < 80:
                        player.energize(20)
                        print("*** Got 20 more energy! ***\n")
                    else:
                        print("*** You do not need it, you already have enough energy! ***")
                        continue

                if move[1] == "gun":
                    gun = Gun()
                    player.add_to_inventory(gun)
                    rooms[currentRoom]["item"].remove(move[1])
                    print("*** Took the gun! ***\n")
                    continue

                # finding gun from player inventory and getting bullets
                if move[1] == "bullets":
                    if any(isinstance(item, Gun) for item in player.get_inventory()):
                        gun_item = next(
                            item for item in player.get_inventory() if isinstance(item, Gun)
                        )
                        gun_item.load_gun(5)
                        rooms[currentRoom]["item"].remove(move[1])
                        print("*** Added 5 bullets to the gun! ***\n")
                        continue
                    else:
                        print("*** You need a gun to load bullets! ***\n")
                        continue

                player.inventory += [move[1]]

                print(f"*** {move[1]} added to inventory! ***\n")

                rooms[currentRoom]["item"].remove(move[1])

                # increase moves counter
                moves_counter += 1
            else:
                print(f"*** Can't get {move[1]}! ***\n")


        # quit the game
        elif move[0] == "quit":
            print("*** Exiting the game! ***\n")
            break

        else:
            print("*** Not a valid Instruction! ***\n")
            continue

        # if e not pressed while in Kitchen, player will be locked in the room and lost the game
        if countdown_completed:
            print("You have been locked in the kitchen, You Lost!!")
            break

        # Check if player has enough energy to defeat a potential monster
        if currentRoom in rooms and "monster" in rooms[currentRoom]["item"]:
            # checking and getting gun instance from player inventory
            if any(isinstance(item, Gun) for item in player.get_inventory()):
                print("Pulling Gun!")
                # bullets need to kill monster
                monster_kill_bullets = random.randint(4, 7)

                print("Fighting with the monster!")
                time.sleep(3)

                gun_item = next(
                    item for item in player.get_inventory() if isinstance(item, Gun)
                )

                if gun_item.get_bullets() > monster_kill_bullets:
                    # bullets will be used from the gun and energy will be reduced
                    gun_item.shoot(monster_kill_bullets)
                    player.deenergize(monster_kill_bullets * 10)
                    if player.get_energy() <= 0:
                        print("*** No energy left, YOU LOST! ***\n")
                        break
                    print("*** Monster Defeated! ***")
                    rooms[currentRoom]["item"].remove("monster")

                else:
                    print("*** Gun empty, no more bullets. Monster killed you!, Game Over! ***\n")
                    break

            else:
                print("*** You don't have a gun to fight with the monster\nMonster killed you, GAME OVER! ***\n")
                break

        # Check if player has the key to escape (only in the 'Garden' room)
        if currentRoom == "Garden":
            if "key" in player.inventory:
                print("You escaped the house with the key, you WON!!")
                print(f"Total Moves: {moves_counter}")
                break
            else:
                print("*** You need a key to escape! ***\n")


if __name__ == "__main__":
    play_game()
