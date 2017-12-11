import re, glob, pygame, sys, io, ast

def getData(filename, gameCount):
    pattern = re.compile('(\(\d+,\d+\))')
    searching = True
    readingCoord = False
    try:
        with open(filename, "r") as f:
            for line in f:
                if "=" in line:
                    gameCount += 1
                if searching:
                    if (line.strip() == "Total shots:") or (line.strip() == "Total boats placed:"):
                        searching = False
                        readingCoord = True
                elif readingCoord:
                    coord = line.strip().split(":")
                    if pattern.match(coord[0]):
                        coord_data[coord[0]] += int(coord[1])
                    else:
                        searching = True
                        readingCoord = False
    except Exception as e:
        print("Error: " + str(e))
    return gameCount

def genMap(secondC, secondD, thirdC, thirdD):
    pygame.display.init()
    pygame.font.init()
    myfont = pygame.font.Font("font.ttf", 15)
    GameBoard = pygame.display.set_mode((445, 570))
    GameBoard.fill((0,191,255))
    GameBoard.fill((0, 190, 190), rect=(0, 446, 445, 550))
    x = 20# spacing on x direction
    y = 20# spacing on y direction

    # for i in range(21):
    #     pygame.draw.line(GameBoard, (255,255,255),(20,y),(420,y))
    #     pygame.draw.line(GameBoard, (255,255,255),(x,20),(x,420))
    #     y += 20
    #     x += 20
    pygame.display.update()

    MOST_coord = ""
    MOST_click = 0
    Total_clicks = 0
    for coord, value in coord_data.items():
        Total_clicks += value
        if value > MOST_click:
            thirdC = secondC
            thirdD = secondD
            secondC = MOST_coord
            secondD = MOST_click
            MOST_coord = coord
            MOST_click = value
        elif value > secondD:
            thirdC = secondC
            thirdD = secondD
            secondC = coord
            secondD = value
        elif value > thirdD:
            thirdC = coord
            thirdD = value
    offset = 255//MOST_click

    red = 0
    green = 0
    blue = 0

    for key in list(coord_data.keys()):
        coord = key.strip("()").split(",")
        clicks = coord_data[key]
        blue = 255
        green = 255 - (offset*clicks)
        red = 255 - (offset*clicks)
        X = int(coord[0])*20
        Y = int(coord[1])*20
        GameBoard.fill((red,green,blue), rect=(X,Y,20,20))
        pygame.display.update()

    text = "Most clicks " + str(MOST_click) + " at " + MOST_coord
    stats = myfont.render(text, False, (0, 0, 0))
    GameBoard.blit(stats, (20,450))
    pygame.display.update()

    text = "Second most clicks " + str(secondD) + " at " + secondC
    stats = myfont.render(text, False, (0, 0, 0))
    GameBoard.blit(stats, (20,470))
    pygame.display.update()

    text = "Third most clicks " + str(thirdD) + " at " + thirdC
    stats = myfont.render(text, False, (0, 0, 0))
    GameBoard.blit(stats, (20,490))
    pygame.display.update()

    text = "Total clicks: " + str(Total_clicks)
    stats = myfont.render(text, False, (0, 0, 0))
    GameBoard.blit(stats, (20,510))
    pygame.display.update()

    choice = True
    while(choice):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    print("Quit successfully")
                    pygame.quit()
                    sys.exit(0)


def main():
    gameCount = 0
    for filename in glob.glob('*.txt'):
        gameCount = getData(filename, gameCount)
    print("Game count is: " + str(gameCount))
    genMap(secondC, secondD, thirdC, thirdD)

if __name__ == "__main__":
    global coord_data
    global offset
    global gameCount
    global secondD
    global secondC
    global thirdC
    global thirdD

    coord_data = dict()
    gameCount = 0
    secondC = "null"
    thirdC = "null"
    secondD = 0
    thirdD = 0
    for i in range(1, 21):
        for j in range(1, 21):
            coord_data["(" +str(i) + "," + str(j) + ")"] = 0
    main()
