def printMap():
    rooms_map = '''

               ****         GAME MAP    ****
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