import re, glob, pygame, sys, io, ast, hashlib, math
from scipy import special
from bitarray import bitarray

def getIndex(x, y):
    i = 0
    i += (y-1)
    i += (x-1)*20
    return i

def getData(filename, gameCount, level, found_match, counting_coords, done, pattern, tmp, bit_string):
    try:
        with open(filename, "r") as f:
            match = ""
            for line in f:
                if ":" in line:
                    index = line.strip().split(":")
                    if index[0] == "Captain's score":
                        if int(index[1]) >= level:
                            found_match = True
                            gameCount += 1
                elif "========" in line:
                    match = f.readline().strip()
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
                        found_match = False
                        counting_coords = False

                        tmp = bit_string.tobytes()

                        m = hashlib.sha256()
                        m.update(tmp)
                        key = m.hexdigest()

                        key = hex( int(key[0:(len(key))//2], 16) ^ int(key[(len(key))//2:len(key)], 16) )

                        # print("File: " + str(filename) + "\n"
                        #     + "Game: " + match + "\n"
                        #     + "Bit string: " + str(bit_string))
                        # print("File: " + str(filename) + "\n"
                        #     + "Game: " + match + "\n"
                        #     + "128-bit Hex number: " + str(key))
                        key_list.append(key)

                        tmp = ''.join('0' for i in range(0, 400))
                        bit_string = bitarray(tmp)
            tmp2 = ''.join('0' for i in range(0, 400))
            if bit_string != bitarray(tmp2):
                print("PRINTING THE LAST MATCH FROM " + str(filename))
                tmp = bit_string.tobytes()

                m = hashlib.sha256()
                m.update(tmp)
                key = m.hexdigest()

                key = hex( int(key[0:(len(key))//2], 16) ^ int(key[(len(key))//2:len(key)], 16) )
                # print("File: " + str(filename) + "\n"
                #     + "Game: " + match + "\n"
                #     + "128-bit Hex number: " + str(key))
                key_list.append(key)
    except Exception as e:
        print("Error: " + str(e))
    return gameCount

def monobitTest(key_list):
    rnd = 0
    not_rnd = 0
    key_count = 0
    count = 0
    zero_count = 0
    one_count = 0
    # If the char is 0 minus 1, else add 1
    scale = 16 ## equals to hexadecimal
    num_of_bits = 128
    for key in key_list:
        count = 0
        zero_count = 0
        one_count = 0
        bin_data = bin(int(key, scale))[2:].zfill(num_of_bits)
        for char in bin_data:
            if char == '0':
                count -= 1
                zero_count += 1
            else:
                count += 1
                one_count += 1
        # Calculate the p value
        sobs = count / math.sqrt(len(bin_data))
        p_val = special.erfc(math.fabs(sobs) / math.sqrt(2))
        print("Key has p_val: " + str(p_val) + "\nZero: " + str(zero_count) + " One: " + str(one_count) + "\n")

        if p_val >= 0.01:
            rnd += 1
        else:
            not_rnd += 1

        key_count += 1

    print("==============================================")
    print("Total keys: " + str(key_count) )
    print("Random keys: " + str(rnd) )
    print("Non-random keys " + str(not_rnd) )
    return

def main():
    global found_match
    global counting_coords
    global done
    global pattern
    global tmp
    global bit_string
    global key_list

    key_list = []

    found_match = False
    counting_coords = False
    done = False
    pattern = re.compile('(\(\d+,\d+\))')
    tmp = ''.join('0' for i in range(0, 400))
    bit_string = bitarray(tmp)

    gameCount = 0
    level = 0
    while True:
        level = input("Generate keys for games past level <int> ? ")
        try:
            level = int(level)
            break
        except:
            pass
    for filename in glob.glob('*.txt'):
        print("OPENING: " +str(filename))
        gameCount = getData(filename, gameCount, level, found_match, counting_coords, done, pattern, tmp, bit_string)
    print("Game count is: " + str(gameCount))
    print("Key count is: " + str(len(key_list)))

    monobitTest(key_list)


if __name__ == "__main__":
    main()
