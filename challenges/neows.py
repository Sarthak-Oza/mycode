#!/usr/bin/python3
import requests
import argparse
from dotenv import load_dotenv
import os

## Define NEOW URL
NEOURL = "https://api.nasa.gov/neo/rest/v1/feed?"

def main():
    parser = argparse.ArgumentParser(description="argparser, get start/end date")

    parser.add_argument("--startdate", "-s", required=True, type=str, help="Start date")
    parser.add_argument("--enddate", "-e", type=str, help="End date")
    args = parser.parse_args()

    load_dotenv("/home/student/mycode/nasa/nasacred.env")
    nasacreds = "api_key=" + os.getenv("NASA_KEY").strip("\n")

    startdate = "start_date=" + args.startdate

    if args.enddate:
        enddate = "end_date=" + args.enddate
        URL = NEOURL + startdate + "&" + enddate +"&" + nasacreds

    else: 
        URL = NEOURL + startdate + "&" + nasacreds

    neowrequest = requests.get(URL)

    neodata = neowrequest.json()

    # print(neodata)

    max_dia = 0

    for dia in neodata.get("near_earth_objects").values():
        for d in dia:
            current_dia = d.get("estimated_diameter").get("feet").get("estimated_diameter_max")
            max_dia = current_dia if current_dia > max_dia else max_dia

    print("Biggest (Feet): ", max_dia)

if __name__ == "__main__":
    main()

