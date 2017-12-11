import re, glob, pygame, sys, io, ast
from bitarray import bitarray

def getIndex(x, y):
    i = 0
    i += (y-1)
    i += (x-1)*20
    return i

def main(match):
    found_match = False
    counting_coords = False
    done = False
    pattern = re.compile('(\(\d+,\d+\))')
    tmp = ''.join('0' for i in range(0, 400))
    bit_string = bitarray(tmp)

    try:
        for filename in glob.glob('*.txt'):
            with open(filename, "r") as f:
                for line in f:
                    if done:
                        continue
                    if line.strip() == match:
                        found_match = True
                    if found_match and not counting_coords:
                        if line.strip() == "Total boats placed:":
                            counting_coords = True
                    elif found_match and counting_coords:
                        data = line.strip().split(":")
                        if pattern.match(data[0]):
                            coord = data[0].strip("()").split(",")
                            x = int(coord[0])
                            y = int(coord[1])
                            for flip in range(0, int(data[1])):
                                bit_string[getIndex(x, y)] = not bit_string[getIndex(x, y)]
                        else:
                            done = True
                            found_match = False
                            counting_coords = False
    except Exception as e:
        print("Error: " + str(e))
    print(str(bit_string))

if __name__ == "__main__":
    global match
    match = input("Enter the date - time of the match: ")
    main(match)
