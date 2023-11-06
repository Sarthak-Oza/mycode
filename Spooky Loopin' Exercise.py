#!/usr/bin/env python3

counter = 0

with open("dracula.txt","r") as file:
    file_content = file.read()
    print(file_content)

    file.seek(0)

    lines = file.readlines()
    print(lines)

    with open("vampireLines.txt","w") as vamplines:

        for line in file:
            if "vampire" in line.lower():
                print(line.strip())
                counter += 1
                vamplines.write(line)

    print(counter)