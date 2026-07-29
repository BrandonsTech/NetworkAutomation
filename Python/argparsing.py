import argparse
import math

parser = argparse.ArgumentParser() #Defines a parser instance. We can add arguments to this parser
#parser.add_argument('moregreeting', help= "This is a greeting message!")
parser.add_argument("-v", "--verbose", help="This is a verbose message")
parser.add_argument("-n", "--numbers", type = float, nargs=2, help="The numbers to be added")
parser.add_argument("--debug", action='store_true', help="Enables Debug Mode") #BOOLEAN OPERATION
parser.add_argument("-i", action="append", nargs="+") #Create lists with multiple entries or multiple lists with multipls "-i"
args = parser.parse_args()
print(args) #This is the dictionary
#print(args.greeting) #Print Dictionary Key
print(args.i)

if args.numbers is not None:
    print(args.numbers[0] + args.numbers[1])

if args.debug:
    print(math.pi * math.pi)