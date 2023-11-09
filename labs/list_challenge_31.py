#!/usr/bin/env python3
import random

def main():
    wordbank= ["indentation", "spaces"]

    tlgstudents= ['Albert', 'Anthony', 'Brenden', 'Craig', 'Deja', 'Elihu', 'Eric', 'Giovanni', 'James', 'Joshua', 'Maria', 'Mohamed', 'PJ', 'Philip', 'Sagan', 'Suchit', 'Meka', 'Trey', 'Winton', 'Xiuxiang', 'Yaping']

    wordbank.append(4)

    class_size = len(tlgstudents)

    num = int(input(f"Enter a number between 1 and {class_size}: "))

    student_name = tlgstudents[num-1]

    print(f"{student_name} always uses {wordbank[-1]} {wordbank[-2]} to indent")

    print("------ Randomly picked student-------")

    random_student = tlgstudents[random.randint(0, len(tlgstudents)-1)]

    print(f"{random_student} always uses {wordbank[-1]} {wordbank[-2]} to indent")

if __name__ == "__main__":
    main()
