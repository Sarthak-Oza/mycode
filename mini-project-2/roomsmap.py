def printMap():
    rooms_map = """

               ****         GAME MAP    ****
        +---------------------+         +---------------------+
        | Hall (Start here)   |         |    Dining Room      |
        | Exits: south, east  |    E->  | Exits: south, west  |
        | Items: key, bullets |    <-W  | Items: monster      |
        +---------------------+         +---------------------+
                N   |                           N  |
                |   S                           |  S
        +---------------------+         +---------------------+
        |       Kitchen       |         |       Garden        |
        | Exits: north        |         | Exits: north        |
        | Items: gun, potion  |         | Items: monster      |
        +---------------------+         +---------------------+
                                                    |
                                                   Exit
                                                
    """

    print(rooms_map)
