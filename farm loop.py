#!/usr/bin/env python3

farms = [{"name": "NE Farm", "agriculture": ["sheep", "cows", "pigs", "chickens", "llamas", "cats"]},
         {"name": "W Farm", "agriculture": ["pigs", "chickens", "llamas"]},
         {"name": "SE Farm", "agriculture": ["chickens", "carrots", "celery"]}]

def main():

    for farm in farms:
        if farm["name"] == "NE Farm":
            for animal in farm["agriculture"]:
                print((animal))

    farm_input = input("Enter Farm: ")

if __name__=="__main__":
    main()