#!/usr/bin/env python3

def main():

    while True:
        try:
            bottles = int(input("Enter the number of bottles (1-100): "))

            if bottles > 100:
                print("Please enter bottles value less than 100")
                continue
    
        except ValueError:
            print("Invalid Input, please try again!")
            continue


        for bottle in range(bottles, 0, -1):
            print(f"{bottle} bottles of beer on the wall!\n{bottle} bottles of beer on the wall! {bottle} bottles of beer! You take one down, pass it around!")

        break


if __name__=="__main__":
    main()