#The Game of Nim - Team 41 - L01 - T04
#Code by: Atika S., Adam B. and Andrea L.

import turtle
import random

#Global variables and constants
HORIZONTAL_GAP = 50
VERTICAL_GAP = 60
CLICK_RANGE = 10
TURTLE_SPEED = 25
BOARD_WIDTH = 500
BOARD_LENGTH = 305
TURTLE_SHAPE = "circle"
BASE_COLOR = "skyblue"
ALERT_MESSAGE_TEXT_COLOR = "red"
MIN_STONES = 1
MAX_STONES = 5
MIN_PILE = 3
MAX_PILES = 5
MESSAGE_POINT_X = -80
MESSAGE_POINT_Y = -70
MESSAGE_FONT_AND_SIZE = ('Impact',15,'normal')
previous_selected = None

# Ddisplays welcome message and instructions for the game of nim
def writeWelcomeMessage():
    welcome = turtle.Turtle()
    initial_y = 160

    welcome.penup()
    welcome.goto(-190,180)
    welcome.color("black")
    welcome.write("Game of Nim", font=('impact',55,'normal'))
    for sentence in ("  The Game of Nim is a two player game in which each player must select",
    "any combination of stones so long as they pertain to the same row, with",
    "      the objective of forcing the opponent into selecting the final stone.",
    "              If the opponent selects the final stone, you are the winner."):
        welcome.goto(-300, initial_y)
        welcome.write(sentence, font = MESSAGE_FONT_AND_SIZE)
        initial_y = initial_y - 25
    welcome.color("green")
    welcome.goto(-170,60)
    welcome.write("Press 'space' for the computer's move.",font = MESSAGE_FONT_AND_SIZE)
    welcome.goto(-260,-280)
    welcome.write("Press 's' to save your current game or 'l' to load a previous game.",font = MESSAGE_FONT_AND_SIZE)
    drawGameGrid(welcome)

#Draws board outline
def drawGameGrid(turtle):
    #Sets printing speed & width of line for turtle "nim"
    turtle.speed(TURTLE_SPEED)
    turtle.goto(-250, -250)
    turtle.down()

    #The loop creates a rectangular grid for the game
    for i in range(2):
      turtle.forward(BOARD_WIDTH)
      turtle.left(90)
      turtle.forward(BOARD_LENGTH)
      turtle.left(90)
    turtle.hideturtle()

#Creates a turtle and calls the function to draw random piles
# and stores the row coordinates in a 2D list
#Returns - 2D list of positions of stones on turtle screen
def drawStones():

    number_piles = random.randrange(MIN_PILE,MAX_PILES+1)

    stones = turtle.Turtle()
    stones.shape(TURTLE_SHAPE)
    stones.speed(TURTLE_SPEED)

    stone_x = -200
    stone_y = -220
    pile_color = 1
    coordinates = []
    #Each loop draws new pile with distinct color and stores postion of stones
    for i in range(random.randrange(MIN_PILE, MAX_PILES + 1)):
        pile = [DrawPileStorePosition(stones,stone_x, stone_y, changeColor(pile_color))]
        coordinates = coordinates + pile
        stone_y = stone_y + 60
        pile_color = pile_color + 1
    return coordinates

#Returns a new color for a new pile(row) of stones
def changeColor(new_pile):

  color = "blue"
  if new_pile == 1:
    color = "Purple"
  if new_pile == 2:
    color = "DarkBlue"
  if new_pile == 3:
    color = "ForestGreen"
  if new_pile == 4:
    color = "GoldenRod"
  if new_pile == 5:
    color = "OrangeRed"

  return color

#Stamps stones and stores the coordinates in 1D list
#Parameters - turtle, position of first stone and color of stone
# Returns - position of stones for one row
def DrawPileStorePosition(turtle, x,y,pile_color):
    coordinates = []

    for i in range(random.randrange(MIN_STONES,MAX_STONES+1)):
        turtle.color(pile_color)
        turtle.up()
        turtle.goto(x,y)
        turtle.stamp()
        coordinates = coordinates + [[x,y]]
        x = x + 100

    return coordinates

#Responds to click and keys pressed by player
def respondToUserActions(screen):

    screen.onclick(userClick, btn = 1, add = True)
    screen.onkey(compMove, 'space')
    screen.onkey(saveGame, 's')
    screen.onkey(loadGame, 'l')
    screen.listen()

#If move is invalid, shows an error on turtle screen, otherwise erases previous
#messages written on screen
def displayMessage(text):
    display = turtle.Turtle()
    display.up()

    if text:
        display.color(ALERT_MESSAGE_TEXT_COLOR)
        display.goto(MESSAGE_POINT_X,MESSAGE_POINT_Y-10)
        display.write(text, font = ('Impact',13,'normal'))
        display.hideturtle()

    else:
        eraseMessage(display)

#Erases any message conveyed to user via turtle screen
def eraseMessage(turtle):

    turtle.color(BASE_COLOR)
    turtle.shape(TURTLE_SHAPE)
    turtle.goto(MESSAGE_POINT_X,MESSAGE_POINT_Y)
    turtle.speed(TURTLE_SPEED)
    for i in range(20):
        turtle.stamp()
        turtle.forward(15)

#Removes objects from a particular row chosen by player and prevents removing
#stones from multiple rows at a time then calls the function to check if gameover
def userClick(x,y):

    global b_player_move
    global b_comp_move
    global previous_selected
    global game_state
    global pile_size

    displayMessage(None)

    if b_player_move == True:
        for i in range(len(piles_coordinates)):
            for n in range(len(piles_coordinates[i])):
                #Checks if user clicked on stone
                if isClickInRange(piles_coordinates[i][n][0],piles_coordinates[i][n][1],x,y):
                    selected_row = i
                    selected_stone = n
                    b_comp_move = True
                    #Checks if user selects stone from same row
                    if ValidRow(selected_row, previous_selected, selected_stone):
                        game_state[selected_row][selected_stone] = False
                        updateNumberStonesInPile(i)
                        previous_selected = selected_row
                        removeStone(x,y,BASE_COLOR)

    #Checks if game is over and sends which player won by changing parameters
    if game_state == game_over_state:
        b_player_move = False
        b_comp_move = True
    losingState(b_player_move, b_comp_move)

#Returns true if clicked on stone by user
def isClickInRange(stone_x,stone_y,user_x,user_y):
    result = False

    if abs(stone_x-user_x)<10 and abs(stone_y-user_y)<10:
        result = True

    return result

#Checks if stone picked is from same row as previous stone picked
#Calls the function to display error message if invalid move, else calls function
# to erase messages
# Return - True for valid click and False for invalid click
def ValidRow(selected_row, previous_selected,selected_stone):
    global game_state

    move = False
    if selected_row == previous_selected or previous_selected == None:
        if game_state[selected_row][selected_stone] == True:
            move = True
            displayMessage(None)
    else:
        displayMessage("Choose from same row")
    return move

#Function called when user presses space
# checks nimsum and makes a move accordingly
def compMove():

    global b_player_move
    global b_comp_move
    global previous_selected
    global game_state
    global pile_size

    if b_comp_move == True:
        b_player_move = False
        displayMessage(None)

        #Converts remeining stones in pile to binary representation
        row1 = changeLenOfBinary(toBinary(pile_size[0]))
        row2 = changeLenOfBinary(toBinary(pile_size[1]))
        row3 = changeLenOfBinary(toBinary(pile_size[2]))
        row4 = changeLenOfBinary(toBinary(pile_size[3]))
        row5 = changeLenOfBinary(toBinary(pile_size[4]))

        rows_list = [[row1], [row2], [row3], [row4], [row5]]
        #Calculates nim sum using binary representation of all rows
        nim_sum = NimSum(row1, row2,row3,row4,row5)

        total_stones = pile_size[0] + pile_size[1] + pile_size[2] + pile_size[3]
        + pile_size[4]

        #When computer is in losing state or if last stone is present in
        #computer's turn, then it selects a single stone
        if nim_sum == "000" or total_stones == 1:
            zeroNimSumStrategy()

        #Checks which row has odd number of stones to make nim sum zero
        else:
            binary_index = 0
            binary_found = False

            #Finds a 1 in nim sum
            while binary_found == False and binary_index <= 2:
                if nim_sum[binary_index] == "1":
                        binary_found = True
                else:
                    binary_index = binary_index + 1

            #Finds first 1 from rows and selects that row to remove stones
            row_found = False
            row = 0
            while row_found != True and row <= 4:
                if rows_list[row][0][binary_index] == "1":
                    row_found = True
                else:
                    row = row + 1
            smartAiMove(row, nim_sum)

        #Computer move ends and user can select stones
        b_player_move = True
        b_comp_move = False
        losingState(b_player_move, b_comp_move)
        previous_selected = None

#Function that is called when the desired nim sum is "000"
def zeroNimSumStrategy():

    global game_state

    row = False
    row_index = 0

    #Loops through the game state until it finds a 'True' value, indicating
    # the presence of a stone, and then removing it
    while row != True:
        if True in game_state[row_index]:
            stone_index = game_state[row_index].index(True)
            x = piles_coordinates[row_index][stone_index][0]
            y = piles_coordinates[row_index][stone_index][1]
            removeStone(x, y, BASE_COLOR)
            game_state[row_index][stone_index] = False
            updateNumberStonesInPile(row_index)
            row = True
        else:
            row_index = row_index + 1

#Removes stones until nim sum is zero from selected row
def smartAiMove(selected_row, nim_sum):

    global game_state
    global pile_size
    global piles_coordinates

    move = False
    stone = 0
    pile_size_clone = pile_size[:]

    #Checks is stones after smart ai move will put computer in losing position
    # according to misere game of nim rules
    # If computer will lose after move then it changes its strategy
    if isSuggestedMoveWrong(selected_row, nim_sum, stone, pile_size_clone):
        misereNimStrategy(selected_row, pile_size_clone)

    #Follows normal game of nim strategy i.e. remove stones from a row to make
    # nim sum zero by end of move
    else:
        while nim_sum != "000":

            if game_state[selected_row][stone]== True:
                x = piles_coordinates[selected_row][stone][0]
                y = piles_coordinates[selected_row][stone][1]
                removeStone(x,y,BASE_COLOR)
                game_state[selected_row][stone] = False
                updateNumberStonesInPile(selected_row)
                row1 = changeLenOfBinary(toBinary(pile_size[0]))
                row2 = changeLenOfBinary(toBinary(pile_size[1]))
                row3 = changeLenOfBinary(toBinary(pile_size[2]))
                row4 = changeLenOfBinary(toBinary(pile_size[3]))
                row5 = changeLenOfBinary(toBinary(pile_size[4]))
                stone = stone + 1
                nim_sum = NimSum(row1, row2,row3,row4,row5)

            else:
                stone = stone + 1

#Checks if computer will be losing after future move
def isSuggestedMoveWrong(selected_row, future_nim_sum, stone, pile_copy):

    global game_state

    result = False

    while future_nim_sum != "000":

        if game_state[selected_row][stone]== True:
            pile_copy[selected_row] = pile_copy[selected_row] - 1
            row1 = changeLenOfBinary(toBinary(pile_copy[0]))
            row2 = changeLenOfBinary(toBinary(pile_copy[1]))
            row3 = changeLenOfBinary(toBinary(pile_copy[2]))
            row4 = changeLenOfBinary(toBinary(pile_copy[3]))
            row5 = changeLenOfBinary(toBinary(pile_copy[4]))

            if isSpecialCase(pile_copy):
                result = True
            stone = stone + 1
            future_nim_sum = NimSum(row1, row2,row3,row4,row5)

        else:
            stone = stone + 1

    return result

#If stones in all piles are less than 2, then computer changes strategy to win
# by following misere strategy
def isSpecialCase(pile_copy):

    result = []
    #Adds true if pile size is less than 2
    for index in range(len(pile_copy)):
        if pile_copy[index] < 2:
            result.append(True)

    if result == [True, True, True, True, True]:
        return True

#Different strategy for winning
def misereNimStrategy(selected_row, pile_copy):

    global game_state
    global b_player_move
    global b_comp_move

    #If future move would have left 1 stone then it changes move to take all
    # stones
    if pile_copy[selected_row] == 1:

        for state_index in range(len(game_state[selected_row])):
            if game_state[selected_row][state_index] == True:
                x = piles_coordinates[selected_row][state_index][0]
                y = piles_coordinates[selected_row][state_index][1]
                removeStone(x,y,BASE_COLOR)
                game_state[selected_row][state_index] = False
                updateNumberStonesInPile(selected_row)

    #If future move would have left 0 stone then it changes move to leave 1
    # stone
    elif pile_copy[selected_row] == 0:
        for index in range(len(game_state[selected_row])-1):
            if game_state[selected_row][index] == True:
                x = piles_coordinates[selected_row][index][0]
                y = piles_coordinates[selected_row][index][1]
                removeStone(x,y,BASE_COLOR)
                game_state[selected_row][index] = False
                updateNumberStonesInPile(selected_row)

    b_player_move = True
    b_comp_move = False
    losingState(b_player_move, b_comp_move)
    previous_selected = None

#Calculates nim sum using binary representation of each row
def NimSum(row1, row2, row3, row4, row5):
    column1 = int(row1[0])+ int(row2[0]) + int(row3[0]) + int(row4[0]) + int(row5[0])
    column2 = int(row1[1]) + int(row2[1]) + int(row3[1]) + int(row4[1]) + int(row5[1])
    column3 = int(row1[2]) + int(row2[2]) + int(row3[2]) + int(row4[2]) + int(row5[2])
    column_list = [column1, column2, column3]

    #Adds zero if even number and one if number is odd
    value = ""
    for column in column_list:
        if column % 2 == 0 or column == 0:
            value = value + "0"
        else:
            value = value + "1"

    return value

#Function that is called to convert the given parameter(integer) to its equivalent
#binary number using recursion
def toBinary(x):

    convertString = "01"
    if x < 2:
        return convertString[x]
    else:
        return toBinary(x//2) + convertString[x%2]

def changeLenOfBinary(row):
    for i in range(3):
        if len(row) < 3:
            row = "0" + row
    return row

#Changes number of stones in rows left in 1D list after user or comp's move
def updateNumberStonesInPile(row):
    global pile_size

    pile_size[row] = pile_size[row] - 1
    return updateNumberStonesInPile

#When move is valid, the object is removed by the function
def removeStone(x,y,color):
    remove_stones = turtle.Turtle()
    remove_stones.shape(TURTLE_SHAPE)
    remove_stones.color(color)
    remove_stones.shapesize(2)
    remove_stones.up()
    remove_stones.goto(x,y)
    remove_stones.stamp()

#Calculates number of stones in each row and stores in 1D list
#Return - 1D list with number of stones in each row
def calcPileSize(pile = None, game_state = None):

    row1 = len(pile[0])
    row2 = len(pile[1])
    row3 = len(pile[2])
    if len(pile) >= 4:
        row4 = len(pile[3])
    else:
        row4 = 0
    if len(pile) == 5:
        row5 = len(pile[4])
    else:
        row5 = 0
    piles_list = [row1, row2, row3, row4, row5]

    #Load game uses game state to calculate game over state
    # Adds false for every stone to develop game over state
    if game_state:
        piles_list = []
        for row_index in range(len(game_state)):
            row = 0
            for stone_index in range(len(game_state[row_index])):
                if game_state[row_index][stone_index] == True:
                    row = row + 1
            piles_list.append(row)

    return piles_list

#Checks game state to determine if game is over and displays which player won
def losingState(player, ai):
    global game_state
    global wn
    global game_over_state

    if player == True:
        message = "You won!"
    elif player == False:
        message = "You lost!"

    if game_state == game_over_state:
        gameover = turtle.Turtle()
        gameover.up()
        gameover.color("blue")
        gameover.setpos(-170,-150)
        gameover.speed(TURTLE_SPEED)
        gameover.write("Game Over"+"\n"+ "  " +message,font=('impact', 50,'normal'))
        gameover.hideturtle()
        wn.onscreenclick(None)
        wn.exitonclick()
        game_continue = False

    else:
        game_continue = True

    return game_continue

#Develops initial gamestate depending upon number of piles and stones
#Return - a 2D list of initial gamestate
def calcGamestate(piles):
    gamestate = []
    for row in piles:
        gamestate = gamestate + [[True]*row]
    return gamestate

#Develops the gameover state depending on initial number of piles & stones
def calcLosingState(piles_list, game_state = None):
    game_over_state = []
    for row in piles_list:
        game_over_state = game_over_state + [[False]*row]

    if game_state:
        row_list = []
        for row_index in range(len(game_state)):
            sub_list = []
            for stone_index in range(len(game_state[row_index])):
                sub_list.append(False)
            row_list.append(sub_list)
        game_over_state = row_list

    return game_over_state

#Takes the current game state and stamps stones on screen wherever stone in
#  game state list is True
def gamestateToGraphics():
    global game_state

    clearBoard()
    logicToVisual = turtle.Turtle()
    logicToVisual.shape(TURTLE_SHAPE)
    pile = 1
    #Checks which stones are present in previous game and draws new gameboard
    for row_index in range(len(game_state)):
        for stone_index in range(len(game_state[row_index])):
            #Stamps where stone was present in saved game
            logicToVisual.color(changeColor(pile))
            if game_state[row_index][stone_index] == True:
                x = piles_coordinates[row_index][stone_index][0]
                y = piles_coordinates[row_index][stone_index][1]
                logicToVisual.up()
                logicToVisual.goto(x,y)
                logicToVisual.stamp()

        pile = pile + 1

#Clears game board to load new game
def clearBoard():

    #Removes previous stones to clear board
    clearStones = turtle.Turtle()
    clearStones.color(BASE_COLOR)
    clearStones.shape("square")
    clearStones.speed(TURTLE_SPEED)
    clearStones.shapesize(14)
    clearStones.goto(-100,-100)
    clearStones.stamp()
    clearStones.forward(200)

#loads a previously saved game when user presses 'l', by updating the game state
#and redrawing the stones
def loadGame():
    global game_state
    global piles_coordinates
    global b_comp_move
    global b_player_move
    global previous_selected
    global pile_size
    global game_over_state

    try:
    #Creates an empty list to add boolean values for gamestate of loaded game
        game_state = []
        piles_coordinates = []
        pile_size = []

        configure_coordinates = False
        configure_player = False
        configure_gamestate = False

        file = open('savedgame.txt', "r")

        #Iterates via each line and converts strings to boolean value
        for aline in file:
           state = []
           coordinates = []
           sub_coordinates = []
           sub_items = 0

           values = aline.split()
           # Loops through each item in a line, and configures the game based on
           #  the corrosponding information
           for column in values:
               # The following lines of code configure the game state, the
               #coordinates, and identify whose move it is
               if column == "True" or column == "False":
                   configure_gamestate = True
                   state = state + [column == 'True']

               elif column == "Computer_Move":
                   configure_coordinates = False
                   b_comp_move = True
                   b_player_move = False

               elif column == "Player_Move":
                   configure_coordinates = False
                   configure_player = True
                   b_player_move = True

               elif configure_player:
                   if column == 'None': previous_selected = None
                   else: previous_selected = int(column)
                   configure_player = False

               else:
                   configure_gamestate = False
                   configure_coordinates = True
                   sub_coordinates = sub_coordinates + [int(column)]
                   sub_items = sub_items + 1

                   if sub_items == 2:
                        coordinates = coordinates + [sub_coordinates]
                        sub_items = 0
                        sub_coordinates = []

           #stores the accumulators above as sublists
           if configure_gamestate:
                game_state = game_state + [state]
           if configure_coordinates:
               piles_coordinates = piles_coordinates + [coordinates]
        #adds empty sub-lists to the gamestate based on the number of rows un-accounted for
        if len(game_state) < 5:
           for i in range (5 - len(game_state)):
                game_state = game_state + [[]]

        #Calls functions to redraw the stones on the gameboard and store positions
        gamestateToGraphics()
        pile_size = calcPileSize(piles_coordinates, game_state)
        game_over_state = calcLosingState(pile_size, game_state)
        displayMessage("It is currently your turn")

    except IOError:
        print("Error: can't find file or read data")
        displayMessage(None)
        displayMessage("Error: can't find file or read data")

#Saves the current game state in a text file when the user presses 's'
def saveGame():

    global game_state
    global piles_coordinates

    try:
        file = open("savedgame.txt", "w")
        #Iteration goes through the 2d game state list and creates & stores boolean
        # values for each stone in which each row is a new line
        for row in game_state:
            for item in row:
                file.write(str(item) + " ")
            file.write("\n")

        #Stores the coordinates of stones that are present when user presses 's'
        for row in piles_coordinates:
            for stone in row:
                for coor in stone:
                    file.write(str(coor) + " ")
            file.write("\n")

        #Adds which player move will be next in text file
        if b_comp_move and not b_player_move:
            file.write("Computer_Move")
        if b_player_move:
            file.write("Player_Move" + " " + str(previous_selected))
        displayMessage(None)
        displayMessage('You have now saved your game.')
        wn.exitonclick()

    except IOError:
        print("Error: can't save current game")
        displayMessage(None)
        displayMessage("Error: can't save current game")

#Randomly determines whether the user or the computer gets to make the first move
def firstMove():
    global b_player_move
    global b_comp_move

    rand_num = random.randrange(2)

    #Player will be user if number is 0
    if rand_num == 0:
        displayMessage("You get to go first")
        b_player_move = True
        b_comp_move = False

    #Player will be computer if number is 1
    else:
        displayMessage("The computer went first")
        b_comp_move = True
        compMove()

#Initializes the game and draws stones on screen
def drawBoardStorePositions():
    writeWelcomeMessage()
    stones_position = drawStones()
    return stones_position

wn = turtle.Screen()
wn.bgcolor(BASE_COLOR)
piles_coordinates = drawBoardStorePositions()
pile_size = calcPileSize(piles_coordinates)
game_state = calcGamestate(pile_size)
b_player_move = None
b_comp_move = None
game_over_state = calcLosingState(pile_size)
respondToUserActions(wn)
firstMove()
x = input("")
