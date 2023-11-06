#!/usr/bin/python3

import time
import threading
import msvcrt # available only on windows

# countdown when player in kicthen, to avoid locking the kitchen
countdown_completed = False

class Player:
    def __init__(self, name, initial_energy=100):
        self.name = name
        self.energy = initial_energy
        self.inventory = []

    def energize(self, energy_increase):
        self.energy += energy_increase

    def deenergize(self, energy_decrease):
        self.energy -= energy_decrease
    
    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def get_inventory(self):
       return self.inventory


# Start the player in the Hall
currentRoom = 'Hall'

# create a player
player_name = 'Player'
player = Player(player_name)

#total number of moves
moves_counter = 0

def printMap():
    rooms_map = '''
        +---------------------+         +---------------------+
        |       Hall          |         |       Dining Room   |
        | Exits: south, east  |    E->  | Exits: south, west  |
        | Items: key          |    <-W  | Items: monster      |
        +---------------------+         +---------------------+
                N   |                           N  |
                |   S                           |  S
        +---------------------+         +---------------------+
        |       Kitchen       |         |       Garden        |
        | Exits: north        |         | Exits: north        |
        | Items: knife, potion|         | Items: monster      |
        +---------------------+         +---------------------+
    '''

    print(rooms_map)

def showInstructions():
  #print a main menu and the commands
  print('''
RPG Game
========
Commands:
  go [direction]
  get [item]
  quit
''')

def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #getting directions player can go to 
  print("You can go to " + " or ".join([key for key in rooms[currentRoom].keys() if key in {"north", "south", "east", "west"}]))
  #print the current inventory
  print('Inventory : ' + str(player.inventory))
  #print an item if there is one
  if rooms[currentRoom]["item"]:
    print('You see ' + ', '.join(rooms[currentRoom]['item']))

  # Print the player's energy
  print(f'Energy: {player.energy}')
  print("---------------------------")
  #print total number of moves
  print(f"Total Moves: {moves_counter}")
  print("---------------------------")

def crushing_walls():
  global countdown_completed
  for i in range(5, 0, -1):
        print("Time left:", i, end="\r")# carriage return to overwrite the previous number with the new one
        # Check if any key pressed in console and then compare if key is "e"
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'e':
                print("Walls down stopped!!.")
                return
        time.sleep(1)
  countdown_completed = True
  return 

def countdown():
    # showStatus()
    t = threading.Thread(target=crushing_walls)
    t.start()
    # wait for the thread to finish
    t.join()

inventory = []

rooms = {
    'Hall': {
        'south': 'Kitchen',
        'east': 'Dining Room',
        'item': ['key']
    },
    'Kitchen': {
        'north': 'Hall',
        'item': ['knife', 'potion']
    },
    'Dining Room': {
        'west': 'Hall',
        'south': 'Garden',
        'item': ['monster']
    },
    'Garden': {
        'north': 'Dining Room',
        'item': ['monster']
    }
}


printMap()
showInstructions()

#loop forever
while True:

  showStatus()

  move = ''
  while move == '':
    move = input('>')

  # split allows an items to have a space on them
  # get golden key is returned ["get", "golden key"]          
  move = move.lower().split(" ", 1)

  #if they type 'go' first
  if move[0] == 'go':
    #check that they are allowed wherever they want to go
    if move[1] in rooms[currentRoom]:
      #set the current room to the new room
      currentRoom = rooms[currentRoom][move[1]]
        #there is no door (link) to the new room

        #increase moves counter
      moves_counter += 1

      if currentRoom == "Kitchen":
        print(f"!!!!!!!!!{currentRoom} will be locked in 5 seconds!!!!!!!!\nPress `e` to stop closing of the room door.")
        countdown()

    else:
        print('You can\'t go that way!')

  #if they type 'get' first
  elif move[0] == 'get' :
    #if the room contains an item, and the item is the one they want to get
    if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      #add the item to their inventory
      player.inventory += [move[1]]
      #display a helpful message
      print(move[1] + ' got!')
      #remove the item from the room
      rooms[currentRoom]['item'].remove(move[1])
    #otherwise, if the item isn't there to get

    #increase moves counter
      moves_counter += 1
    else:
      #tell them they can't get it
      print('Can\'t get ' + move[1] + '!')

  # quit the game
  elif move[0] == "quit":
     print("Exiting the game!")
     break
  
  else:
    print("Not a valid Instruction!")
    continue
  
  
  # if e not pressed while in Kitchen, player will be locked in the room and lost the game
  if countdown_completed:
     print("You have been locked in the dining room, You Lost!!")
     break
  
  # if monster in room, check if player has enough energy to defeat it
  if currentRoom in rooms and 'monster' in rooms[currentRoom]['item']:
        if player.energy >= 50:
            print('A monster is in the room, but you have enough energy to defeat it, reducing energy by 50!')
            player.deenergize(50)
            rooms[currentRoom]['item'].remove('monster')
            
        else:
            print('A monster is in the room, but you do not have enough energy to defeat it. You were killed by the monster. Game Over!')
            break

  
  # check if player has a key to escape and enough energy to defeat monster
  if currentRoom == 'Garden' and 'key' in player.inventory:
    if player.energy >= 50:
       print('You escaped the house with the ultra rare key and magic potion... YOU WIN!')
       print(f"Total Moves: {moves_counter}")
       break
    else:
       print("Monster has got you since you don not have enough enrgy to defeat it!")
       break
  
  # if player does not have a key, can not escape
  elif currentRoom == 'Garden' and 'key' not in player.inventory:
    print('You need a key to escape!!')
    print(f"Total Moves: {moves_counter}")