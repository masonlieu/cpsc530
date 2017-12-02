# Edited by Mason Lieu Date: 11/20/17
# Original code: https://github.com/nati-natnael/Battleship Date: 11/20/17
#************************************************************************************************
#================================================================================================
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Class for Vessle Production ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#================================================================================================
class Vessel(object):

    def ship(self, size, mainShipList):

        import random
        import pygame
        import sys
        overLap = True # Over lap boolean

        while(overLap):

            #List(Tuple) for holding coordinate spaces
            myTuple = (20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400)

            RandomX = 0
            RandomY = 0
            receiving_boat = True
            try:
                while(receiving_boat):
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONUP:
                            X, Y = pygame.mouse.get_pos()
                            if (X>= 20) and (X<= 420) and (Y>= 20) and (Y<= 420):
                                RandomX = myTuple[(X-20)//20]
                                RandomY = myTuple[(Y-20)//20]
                                receiving_boat = False
                        if event.type==pygame.KEYUP:
                            if event.key==pygame.K_q:
                                quitGame(1)
            except:
                print("Error placing boats")
                quitGame(1)


            # RandomX = myTuple[int(random.uniform(0, 19))]# Random number for x coordinate
            # RandomY = myTuple[int(random.uniform(0, 19))]# Random number for y coordinate

            shipList = []# Holds current Vessle list


            z = 0
            a = 0


            while(z < size):
                if((RandomX + 20*size) <= 420):
                    shipList.extend([(RandomX+a, RandomY)])

                elif((RandomX + 20*size) > 420):
                    shipList.extend([(RandomX-a, RandomY)])

                a += 20
                z += 1
#===================================================================
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#======================= Check for overlaps ========================
            for i in range(0, len(shipList)):
                for j in range(0, len(mainShipList)):
                    if(shipList[i] == mainShipList[j]):
                        overLap = True
                        break
                    else:
                        overLap = False
                if(overLap):
                    break
        return shipList
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#============================= // ==================================
#*******************************************************************
#*******************************************************************
#===================================================================
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#======================= Game Grid =================================
def debug(s):
    if DEBUG == True:
        print("DEBUG: " + s)
    return

def quitGame(flag):
    import pygame
    import sys
    import datetime
    try:
        with open("game_data.txt", "a") as f:
            f.write("====================================\n")
            now = datetime.datetime.now()
            f.write(now.strftime("%Y-%m-%d %H:%M") + "\n")

            f.write("Captain\'s score: " + str(captain_score) + "\n")
            f.write("Captain - matches won: " + str(cmatches) + "\n")
            if MULTI:
                f.write("Pirate\'s score: " + str(pirate_score) + "\n")
                f.write("Pirate - matches won: " + str(pmatches) + "\n")
                f.write("Total shots:" + "\n")
                for x in range(20, 420, 20):
                    for y in range(20, 420, 20):
                        count = Total_Shots.count((x,y))
                        if count != 0:
                            f.write("(" + str(x//20) + "," + str(y//20) + "): " + str(count) + "\n")
            if SINGLE:
                f.write("AI\'s score: " + str(pirate_score) + "\n")
                f.write("AI - matches won: " + str(pmatches) + "\n")
                f.write("Total shots by AI:" + "\n")
                for x in range(20, 420, 20):
                    for y in range(20, 420, 20):
                        count = Total_Shots.count((x,y))
                        if count != 0:
                            f.write("(" + str(x//20) + "," + str(y//20) + "): " + str(count) + "\n")

            f.write("Total boats placed:" + "\n")

            for x in range(20, 420, 20):
                for y in range(20, 420, 20):
                    count = Total_Ships.count((x,y))
                    if count != 0:
                        f.write("(" + str(x//20) + "," + str(y//20) + "): " + str(count) + "\n")
            print("Game data saved.")
    except:
        print("Your game data could not be saved.")
    pygame.quit()
    sys.exit(0)



def main():
    import pygame
    import random
    import time
    import sys
    import io
    import ast

    global DEBUG, captain_score, pirate_score, Total_Ships, Total_Shots, pmatches, cmatches, SINGLE
    global MULTI
    DEBUG = False
    SINGLE = False
    MULTI = False


    if len(sys.argv) == 2:
        if str(sys.argv[1]) == "debug":
            DEBUG = True


    boatNum = 1
    captain_score = 0
    captain_hscore = 0
    pirate_score = 0
    pirate_hscore = 100
    Total_Shots = []
    Total_Ships = []
    pmatches = []
    cmatches = []


    try:
        with open("game_data.txt", "r") as f:
            debug("Reading high score")
            for line in f:
                data = line.split(":")
                debug(str(data[0]))
                if data[0] == "AI - matches won":
                    debug("Checking AI score")
                    score = ast.literal_eval(data[1].strip())
                    if len(score) > 0:
                        if pirate_hscore > score[0]:
                            pirate_hscore = score[0]
                        if captain_hscore < (score[0]-1):
                            captain_hscore = score[0]-1
    except:
        pass

    pygame.display.init()
    pygame.font.init()
    myfont = pygame.font.Font("font.ttf", 15)
    myfontsmall = pygame.font.Font("font.ttf", 14)
    GameBoard = pygame.display.set_mode((445, 570))
    GameBoard.fill((0,191,255))
    GameBoard.fill((0, 190, 190), rect=(0, 446, 445, 550))

    start = myfont.render('Welcome to Battleboat!', False, (0, 0, 0))
    playerNum = myfont.render('Enter \'1\' for single player or \'2\' for multiplayer', False, (0, 0, 0))
    GameBoard.blit(start, (20,450))
    GameBoard.blit(playerNum, (20,470))
    pygame.display.update()

    choice = True
    while(choice):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    debug("Single set")
                    SINGLE = True
                    choice = False
                elif event.key == pygame.K_2:
                    debug("Multi set")
                    MULTI = True
                    choice = False


    for h in range(1, 101): #
        pygame.display.init()
        pygame.font.init()
        myfont = pygame.font.Font("font.ttf", 15)
        myfontsmall = pygame.font.Font("font.ttf", 14)
        GameBoard = pygame.display.set_mode((445, 570))
        GameBoard.fill((0,191,255))
        GameBoard.fill((0, 190, 190), rect=(0, 446, 445, 550))

        x = 20# spacing on x direction
        y = 20# spacing on y direction

        for i in range(21):
            pygame.draw.line(GameBoard, (255,255,255),(20,y),(420,y))
            pygame.draw.line(GameBoard, (255,255,255),(x,20),(x,420))
            y += 20
            x += 20

        #===================================================================
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        #============================ Ship placement ==========================
        mainShipList = [(0,0)]

        Vessels = Vessel() # Calling class Vessle

        if len(pmatches) >0:
            if pirate_hscore > pmatches[0]:
                pirate_hscore = pmatches[0]

            if captain_hscore < pmatches[0]-1:
                captain_hscore = pmatches[0]-1

        boatsRemaining = boatNum
        placed = 0
        if SINGLE:
            welcome = myfont.render('Game ' + str(h) +'. My listening sockets are closed.', False, (0, 0, 0))
        if MULTI:
            welcome = myfont.render('Game ' + str(h) +'. Let the pirate look away.', False, (0, 0, 0))
        boatPlacer = myfont.render('Captain please place ' + str(boatsRemaining) + ' boats!', False, (0, 0, 0))
        score1 = myfontsmall.render('Captain\'s score: ' + str(captain_score), False, (0, 0, 0))
        score2 = myfontsmall.render('Pirate\'s score: ' + str(pirate_score), False, (0, 0, 0))
        quit = myfontsmall.render('Press \'q\' to quit.', False, (0, 0, 0))
        hscore1 = myfontsmall.render('Captain\'s longest win: ' + str(captain_hscore), False, (0, 0, 0))
        hscore2 = myfontsmall.render('Pirate\'s quickest win: ' + str(pirate_hscore), False, (0, 0, 0))
        GameBoard.blit(hscore1, (230,510))
        GameBoard.blit(hscore2, (230,530))
        GameBoard.blit(welcome, (20,450))
        GameBoard.blit(boatPlacer, (20,470))
        GameBoard.blit(score1, (20,510))
        GameBoard.blit(score2, (20,530))
        GameBoard.blit(quit, (230,550))

        pygame.display.update()

        while (placed < boatsRemaining):
            PTship = Vessels.ship(1, mainShipList)
            for i in range(0, len(PTship)):
                X = PTship[i][0]
                Y = PTship[i][1]
                GameBoard.fill((0,0,255), rect=(X,Y,20,20))
            mainShipList.extend(PTship)
            pygame.display.update()
            boatsRemaining -= 1
            text = 'Captain please place ' + str(boatsRemaining) + ' boats!'
            GameBoard.fill((0,190,190), pygame.Rect((20, 470), myfont.size(text)))
            boatPlacer = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(boatPlacer, (20,470))
            pygame.display.update()

        del mainShipList[0]
        #===================================================================
        pygame.display.update()
        #===================================================================

        GameBoard.fill((0,191,255), rect=(0, 0, 425, 449))

        x = 20# spacing on x direction
        y = 20# spacing on y direction

        for i in range(21):
            pygame.draw.line(GameBoard, (255,255,255),(20,y),(420,y))
            pygame.draw.line(GameBoard, (255,255,255),(x,20),(x,420))
            y += 20
            x += 20

        GameBoard.fill((0,190,190), rect=(0, 446, 444, 480))
        if SINGLE:
            text = "I am thinking of where to fire."
            attack = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(attack, (20,450))
            pygame.display.update()
            time.sleep(0.3)
            text = "I am thinking of where to fire.."
            attack = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(attack, (20,450))
            pygame.display.update()
            time.sleep(0.3)
            text = "I am thinking of where to fire..."
            attack = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(attack, (20,450))
            pygame.display.update()
            time.sleep(0.3)
            GameBoard.fill((0,190,190), rect=(0, 446, 444, 480))
            text = "FIRE!"
            attack = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(attack, (20,450))
            pygame.display.update()
            time.sleep(0.7)
        if MULTI:
            text = "Pirate, try and sink one boat!"
            attack = myfont.render(text, False, (0, 0, 0))
            GameBoard.blit(attack, (20,450))
            quit = myfontsmall.render('Press \'q\' to quit.', False, (0, 0, 0))
            score1 = myfontsmall.render('Captain\'s score: ' + str(captain_score), False, (0, 0, 0))
            score2 = myfontsmall.render('Pirate\'s score: ' + str(pirate_score), False, (0, 0, 0))
            GameBoard.blit(score1, (20,510))
            GameBoard.blit(score2, (20,530))
            GameBoard.blit(quit, (230,550))
            pygame.display.update()

        Scount = 0 # count for checking if all the vessels be hit or not
        shotCount = 0 # Total random shots needed to take down the fleet
        miss = 0
        attempt = 1

        # check for the random shot not to be shot at that place again
        CurrentShot_L = []

        # To not to shoot the vessel already been taken/contains all successful shots
        Total_S_List = []

        Tuple = (20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400)

        #=======================================================================================

        while(Scount <= 0) and (miss < attempt) :
            if SINGLE:
                boat_pr=[]
                for x in range(20, 420, 20):
                    for y in range(20, 420, 20):
                        count = Total_Ships.count((x,y))
                        while (count >0):
                            boat_pr.append([x, y])
                            count -= 1
                        if len(Total_Ships) <5:
                            debug("TOTAL SHIPS LT 5")
                            rnd = int(random.uniform(0, 20))
                            if rnd == 1:
                                boat_pr.append([x, y])

                choice = boat_pr[int(random.uniform(0, len(boat_pr)))]
                X = choice[0]
                Y = choice[1]

            if MULTI:
                receiving_shot = True
                while(receiving_shot):
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONUP:
                            X, Y = pygame.mouse.get_pos()
                            if (X>= 20) and (X<= 420) and (Y>= 20) and (Y<= 420):
                                X = Tuple[(X-20)//20]
                                Y = Tuple[(Y-20)//20]
                                receiving_shot = False
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_q:
                                quitGame(1)

            RandomShot = [] # Contains random x and random y co-ordinates as a tuple
            RandomShot.extend([(X, Y)])
            Total_Shots.extend([(X, Y)])
            shotCount += 1
            if(RandomShot in Total_S_List):
                break
            elif(not(RandomShot in Total_S_List)):
            #===================================================================================
                if(RandomShot[0] in mainShipList) and (not(RandomShot[0] in Total_S_List)):
                    GameBoard.fill((255,0,0), rect=(X,Y,20,20))
                    Total_S_List.extend([(X, Y)])
                    pygame.display.update()
                    Scount += 1

                    text = "The pirate won!"
                    pirate_score += 1
                    pmatches.append(h)
                    GameBoard.fill((0,190,190), rect=(20, 446, 444, 480))
                    attack = myfont.render(text, False, (0, 0, 0))
                    GameBoard.blit(attack, (20,450))
                    pygame.display.update()
                    for boat in mainShipList:
                        if (boat[0],boat[1]) != (X, Y):
                            GameBoard.fill((0,0,255), rect=(boat[0],boat[1],20,20))
                    pygame.display.update()
                    time.sleep(2)
                    quitGame(1)
            #================================================================================================

                elif(not(RandomShot[0] in mainShipList)) and (not(RandomShot[0] in Total_S_List)):
                       debug("INSIDE LOSE")
                       Total_S_List.extend([(X, Y)])
                       X = RandomShot[0][0]
                       Y = RandomShot[0][1]
                       GameBoard.fill((0,0,0), rect=(X,Y,20,20))
                       pygame.display.update()
                       miss +=1
                       if miss >=attempt:
                           text = "The captain won!"
                           captain_score += 1
                           cmatches.append(h)
                           GameBoard.fill((0,190,190), rect=(20, 446, 444, 480))
                           attack = myfont.render(text, False, (0, 0, 0))
                           GameBoard.blit(attack, (20,450))
                           pygame.display.update()

                if (miss >= attempt) or (Scount>0):
                    for boat in mainShipList:
                        if (boat[0],boat[1]) != (X, Y):
                            GameBoard.fill((0,0,255), rect=(boat[0],boat[1],20,20))



        time.sleep(0.004)

        debug("=================== Running total stats for this session ===================")

        # GameBoard.fill((0,190,190), rect=(20, 446, 444, 480))
        text = "Press any key to play again or \'q\' to quit"
        endtext = myfont.render(text, False, (0, 0, 0))
        GameBoard.blit(endtext, (20,480))
        pygame.display.update()

        endScreen = True
        while(endScreen):
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        quitGame(1)
                    else:
                        endScreen = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    endScreen = False

        for x in range(20, 420, 20):
            for y in range(20, 420, 20):
                count = Total_Shots.count((x,y))
                if count != 0:
                    debug("Total shots on " + str(x) + "," + str(y) + " is " + str(count))

        for x in range(20, 420, 20):
            for y in range(20, 420, 20):
                count = Total_Ships.count((x,y))
                if count != 0:
                    debug("Total ships placed on " + str(x) + "," + str(y) + " is " + str(count))

        boatNum += 1
        Total_Ships.extend(mainShipList)
    #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    #======================================== THE END ======================================================
while True:
    main()
