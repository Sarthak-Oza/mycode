#!/usr/bin/env python3

def main():
    woody = {
        "name": "Woody",
        "birth_year": "1995",
        "gender": "male",
        "movies": ["Toy Story", "Toy Story 2", "Toy Story 3", "Toy Story 4"],
        "favorite_food": "pizza"
    }

    print("Woody Dictionary keys:")
    for key in woody.keys():
        print(key)

    selected_key = input("Please choose one of the options from above: ")

    if selected_key in woody:
        print(f"{selected_key} is {woody.get(selected_key)}")
    else:
        print(f"{selected_key} not found in the dictionary!")

    action = input("Enter 1 to add or 2 to delete: ")

    if action == "1":
        new_key = input("Enter new key: ")
        new_value = input("Enter new value: ")
        woody.update({new_key: new_value})
        print("Updated woody -> ", woody)

    elif action == "2":
        delete_key = input("Enter key to delete: ")
        if delete_key in woody:
            del woody[delete_key]
            print(f"{delete_key} has been deleted.")
            print("Updated woody -> ", woody)
        else:
            print(f"{delete_key} not found in the dictionary!")

    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()

