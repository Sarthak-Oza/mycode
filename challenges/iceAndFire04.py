#!/usr/bin/python3
"""Alta3 Research - Exploring OpenAPIs with requests"""
# documentation for this API is at
# https://anapioficeandfire.com/Documentation

import requests
import pprint

AOIF_CHAR = "https://www.anapioficeandfire.com/api/characters/"

def main():
        ## Ask user for input
        got_charToLookup = input("Pick a number between 1 and 1000 to return info on a GoT character! " )

        ## Send HTTPS GET to the API of ICE and Fire character resource
        gotresp = requests.get(AOIF_CHAR + got_charToLookup)

        ## Decode the response
        got_dj = gotresp.json()
        # pprint.pprint(got_dj)

        # print("Books: \n" + "\n".join(got_dj["books"]))

        print("Books: \n" + "\n".join([requests.get(url).json()["name"] for url in got_dj["books"]]))
        
        if got_dj["allegiances"]:
                print("allegiances: " + "\n".join(got_dj["allegiances"]))
        else: 
                print("No allegiances found!")

        if got_dj["name"]:
                print("name: " + got_dj["name"])
        else:   
                print("No name found, displaying aliases!")
                print("aliases: " + "\n".join(got_dj["aliases"]))

if __name__ == "__main__":
        main()

