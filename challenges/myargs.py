import argparse

parser = argparse.ArgumentParser(description="argparser tool")

parser.add_argument("name", type=str, help="enter your name")
parser.add_argument("--location", "-l", type=str, required=True, default="Canada", help="Your location")
parser.add_argument("--province", "-p", required=True, choices=["BC", "ON"], help="choose province")
parser.add_argument("--verbose", "-v", action="store_true", help="Use this option to enable verbose mode")

args = parser.parse_args()

print("use scriptname -h to get help on usage!")
print("My name is " + args.name)
print("I am from " + args.location)
print("I am from province " + args.province)
print(args.verbose)