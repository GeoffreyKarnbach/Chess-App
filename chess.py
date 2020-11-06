################# IMPORTS ###############

from tkinter import*
import pyperclip
from tkinter.messagebox import*
import socketio
import sys
import json

################## VARIABLES #############

#### UI ####
lastRect=0
lastCoords=[]
modifiable=True
imagesRefs=[]
possible=[]
possiblePositions=[]
possibleRocades=[]
imagesGUI=[]

gameInProgress = False

castlingStillPossible=[True,True]
towersMoved=[[] for loop in range(2)]
gameOver=False

currentColor = False # false == white, true == white

lastClicked=[]

board=[["*" for lopp in range(8)] for loop in range(8)]
board[0]=["r","n","b","q","k","b","n","r"]
board[1]=["p" for loop in range(8)]
board[6]=["P" for loop in range(8)]
board[7]=["R","N","B","Q","K","B","N","R"]

#### NETWORK #####

gameID=""
playerColor = ''
sio = socketio.Client()
sio.connect('http://193.80.95.47:8080/')

##### CONSTANTS #######

figures={"p":"pawn1.png","n":"knight1.png","b":"bishop1.png","r":"rooks1.png","q":"queen1.png","k":"king1.png",\
        "P":"pawn2.png","N":"knight2.png","B":"bishop2.png","R":"rooks2.png","Q":"queen2.png","K":"king2.png"}

possibleMoves={"P":[(-1,0)],\
               "p":[(1,0)],\
               "n":[(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1),],\
               "N":[(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1),],\
               "b":[(-1,-1),(+1,+1),\
                    (+1,-1),(-1,+1)],
               "B":[(-1,-1),(+1,+1),\
                    (+1,-1),(-1,+1)],\
               "r":[(1,0),(-1,0),\
                   (0,1),(0,-1)],\
               "R":[(1,0),(-1,0),\
                   (0,1),(0,-1)],\
               "k":[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)],\
               "K":[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)],\
               "q":[(-1,-1),(+1,+1),\
                    (+1,-1),(-1,+1),\
                    (1,0),(-1,0),\
                    (0,1),(0,-1)],
               "Q":[(-1,-1),(+1,+1),\
                    (+1,-1),(-1,+1),\
                    (1,0),(-1,0),\
                    (0,1),(0,-1)]}


######################## JOIN UI ######################

def cancel_game():
    sio.disconnect()
    sys.exit("No game joined but join window closed.")
    
def confirm_game_id():
    join_game(gameIdString.get())

##################### SOCKET HANDLING #############

def join_game(id):
    sio.emit('joined', {'roomId':id})

def create_game():
    sio.emit('create', {'t':'t'})

@sio.on('roomIdMsg')
def on_message(data):
    global gameID,join_game
    gameID = data
    join_game(gameID)
    print("Game ID ",gameID)

@sio.on('color')
def on_message(data):
    global playerColor
    if data['color'] != 'false':
        playerColor = data['color']

@sio.on('player')
def on_message(data):
    global gameInProgress, board,gameID
    if data['players'] >= 2:
        gameInProgress = True
        gameID=data['roomId']
        sio.emit('play', data['roomId'])

    board = parse_fen(data['board'])

@sio.on('move')
def on_message(data):
    global board
    board = parse_fen(data['board'])
    clear_images()
    update_UI(board)

def sendMove():
    global board, gameID
    sio.emit('move', {'board': parse_board(board), 'room': gameID})


##################### GAME FUNCTION ###############

def get_moves(position):

    #Returns all the existing moves from a certain possition, no matter if they are valid

    global board
    moves=[]
    if board[position[1]][position[0]] != "*":
        liste=possibleMoves[board[position[1]][position[0]]]
        for loop in liste:
            moves.append((loop[0]+position[1],loop[1]+position[0]))
    return moves

def new_game():

    #Resets all the variables and the UI

    global board,lastRect,lastCoords,modifiable,imagesRefs,possible,possiblePositions,possibleRocades,imagesGUI,castlingStillPossible,towersMoved,gameOver,currentColor,lastClicked

    clear_images()
    reset_board()
    update_UI(board)
    print(board)

    lastRect=0
    lastCoords=[]
    modifiable=True
    possible=[]
    possiblePositions=[]
    possibleRocades=[]

    castlingStillPossible=[True,True]
    towersMoved=[[] for loop in range(2)]
    gameOver=False

    currentColor = False # false == white, true == white

    lastClicked=[]

def signOf(number):

    #Auxilary function to get the sign of a number

    if number > 0:
        return 1
    return -1

def rochade(color, side):

    # Executes the rochade

    global board
    if side == True:
        if color == True:
            board[0][4] = '*'
            board[0][5] = 'r'
            board[0][6] = 'k'
            board[0][7] = '*'
        else:
            board[7][4] = '*'
            board[7][5] = 'R'
            board[7][6] = 'K'
            board[7][7] = '*'
    else:
        if color == True:
            board[0][4] = '*'
            board[0][3] = 'r'
            board[0][2] = 'k'
            board[0][1] = '*'
            board[0][0] = '*'
        else:
            board[7][4] = '*'
            board[7][3] = 'R'
            board[7][2] = 'K'
            board[7][1] = '*'
            board[7][0] = '*'
    clear_images()
    update_UI(board)

def rochade_possible(colorID):

    #checks if would be possible

    global castlingStillPossible,board
    res=[]
    if colorID==0:
        if board[0][1] == "*" and board[0][2] == "*" and board[0][3] == "*" and castlingStillPossible[colorID]:
            res.append(True)
        else:
            res.append(False)
        if board[0][5] == "*" and board[0][6] == "*" and castlingStillPossible[colorID]:
            res.append(True)
        else:
            res.append(False)
    elif colorID == 1:
        if board[7][1] == "*" and board[7][2] == "*" and board[7][3] == "*" and castlingStillPossible[colorID]:
            res.append(True)
        else:
            res.append(False)
        if board[7][5] == "*" and board[7][6] == "*" and castlingStillPossible[colorID]:
            res.append(True)
        else:
            res.append(False)
    return res


#SHOWING POSSIBLE MOVES WITH GREEN SQUARES
def show_moves(moves):
    global possible,lastCoords,possiblePositions,board,currentColor,castlingStillPossible,possibleRocades
    coords=((lastCoords[1]-2)//100,(lastCoords[0]-2)//100)
    currentCharacter=board[(lastCoords[1]-2)//100][(lastCoords[0]-2)//100]
    possiblePositions=[]
    if currentCharacter != "b" and currentCharacter != "B" and currentCharacter != "r" and currentCharacter != "R" and currentCharacter != "q" and currentCharacter != "Q":
        for loop in moves:
            try:
                #KNIGHT
                if (currentCharacter=="n" and (board[loop[0]][loop[1]]=="*" or currentColor==board[loop[0]][loop[1]].isupper())) or (currentCharacter=="N" and (board[loop[0]][loop[1]]=="*" or currentColor==board[loop[0]][loop[1]].isupper())):
                    possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                    possiblePositions.append(loop)

                #KING
                elif currentCharacter=='k' or currentCharacter=='K':
                    if board[loop[0]][loop[1]] == '*' or currentColor==board[loop[0]][loop[1]].isupper():
                        possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                        possiblePositions.append(loop)

                    if currentCharacter=='k':

                        result=rochade_possible(0)
                        if result[0]:
                            possible.append(can.create_rectangle(0*100+2,0*100+2, 0*100+98,0*100+98,outline="cyan",width=4))
                            possibleRocades.append((0,0))
                        if result[1]:
                            possible.append(can.create_rectangle(7*100+2,0*100+2, 7*100+98,0*100+98,outline="cyan",width=4))
                            possibleRocades.append((0,7))
                        
                    elif currentCharacter=='K':
                                                
                        result=rochade_possible(1)
                        if result[0]:
                            possible.append(can.create_rectangle(0*100+2,7*100+2, 0*100+98,7*100+98,outline="cyan",width=4))
                            possibleRocades.append((7,0))
                        if result[1]:
                            possible.append(can.create_rectangle(7*100+2,7*100+2, 7*100+98,7*100+98,outline="cyan",width=4))
                            possibleRocades.append((7,7))

                #PAWN
                elif currentCharacter=='p' or currentCharacter=='P':
                    if (coords[0] == 1 and currentCharacter=='p'):
                        if board[loop[0]][loop[1]] == '*' and board[loop[0]+1][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0]+1)*100+98,outline="green",width=4))
                            possiblePositions.extend([loop, (loop[0]+1, loop[1])])
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)
                        if board[loop[0]][loop[1]-1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]-1)*100+2,(loop[0])*100+2, (loop[1]-1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]-1)) 
                        if board[loop[0]][loop[1]+1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]+1)*100+2,(loop[0])*100+2, (loop[1]+1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]+1)) 

                    elif (coords[0] == 6 and currentCharacter=='P'):
                        if board[loop[0]][loop[1]] == '*' and board[loop[0]-1][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0]-1)*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.extend([loop, (loop[0]-1, loop[1])])
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)
                        if board[loop[0]][loop[1]-1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]-1)*100+2,(loop[0])*100+2, (loop[1]-1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]-1)) 
                        if board[loop[0]][loop[1]+1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]+1)*100+2,(loop[0])*100+2, (loop[1]+1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]+1)) 

                    else:
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)   
                        if board[loop[0]][loop[1]-1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]-1)*100+2,(loop[0])*100+2, (loop[1]-1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]-1)) 
                        if board[loop[0]][loop[1]+1] != "*" and (currentColor == board[loop[0]][loop[1]-1].isupper() or not currentColor == board[loop[0]][loop[1]-1].islower()):
                            possible.append(can.create_rectangle((loop[1]+1)*100+2,(loop[0])*100+2, (loop[1]+1)*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append((loop[0],loop[1]+1)) 

                else:
                    pass
            except:
                pass
    else:
        #BISHOP
        if currentCharacter=='b':
            for bmove in possibleMoves['b']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1

                        if not stillPossible:
                            break
                        
                except: 
                    pass
                    
        elif currentCharacter=='B':
            for bmove in possibleMoves['B']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                        
                        if not stillPossible:
                            break
                        
                except: 
                    pass
        #ROOK
        if currentCharacter=='r':
            for bmove in possibleMoves['R']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                        
                        if not stillPossible:
                            break
                except: 
                    pass
                    
        elif currentCharacter=='R':
            for bmove in possibleMoves['R']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                        
                        if not stillPossible:
                            break
                except: 
                    pass

        #QUEEN
        if currentCharacter=='q':
            for bmove in possibleMoves['q']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                        
                        if not stillPossible:
                            break
                except: 
                    pass
                    
        elif currentCharacter=='Q':
            for bmove in possibleMoves['Q']:
                r = 1
                try:
                    stillPossible=True
                    while r < 8 and (board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*' or currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper()) and (r*bmove[0]+coords[0])>-1 and (r*bmove[0]+coords[0])<8 and (r*bmove[1]+coords[1]) > -1 and (r*bmove[1]+coords[1]) <8:
                        if currentColor==board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]].isupper() and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] != '*' and stillPossible:
                            stillPossible=False

                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                        
                        if not stillPossible:
                            break
                except: 
                    pass
                    
                
def confirm_case(event):

    #Locks the selected case by pressing the enter key, used to trigger the green possible cases

    global lastCoords,modifiable,possible,currentColor
    if lastCoords!=[]:
        if currentColor != board[(lastCoords[1]-2)//100][(lastCoords[0]-2)//100].isupper() and board[(lastCoords[1]-2)//100][(lastCoords[0]-2)//100] != "*":
            if modifiable:
                modifiable=False
                show_moves(get_moves(((lastCoords[0]-2)//100,(lastCoords[1]-2)//100)))
            else:
                modifiable=True
                for loop in possible:
                    can.delete(loop)

def check_current_color(piece):

    # Returns the color of a certain piece, depending on if it is upper or lower (FEN NOTATION)

    global currentColor
    if currentColor == True and piece.isupper() != True:
        return True
    elif currentColor == False and piece.isupper() == True:
        return True
    else:
        return False


def parse_fen(fenString): # CASTLING
    global currentColor
    #Converts FEN string to array usable to draw board in tkinter
    splitString = fenString.split(' ')
    lines = splitString[0].split('/')

    if splitString[1] == 'w':
        currentColor = False
    else:
        currentColor = True

    board=[[] for loop in range(8)]

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j].isdigit() == True:
                for k in range(int(lines[i][j])):
                    board[i].append('*')
            else:
                board[i].append(lines[i][j])

    return board

def parse_board(board): # CASTLING

    #Converts array to FEN string to send to server

    fen = ''
    for i in range(8):
        star = 0
        for j in range(8):
            if board[i][j] == '*':
                star+=1

            if star == 0 and board[i][j] != '*':
                fen+=board[i][j]

            if star != 0 and board[i][j] != '*':
                fen+=str(star)
                fen+=board[i][j]
                star = 0
        if star != 0:
            fen+=str(star)
        if i != 7:
            fen+='/'

    if currentColor == True:
        print(fen)
        return fen + ' b'
    else:
        print(fen)
        return fen + ' w'

def click(event):

    #Function managing a click on the chessboard, no matter if it was a click to select a case or a click to confirm a move

    global lastRect,lastCoords,modifiable,possiblePositions,lastClicked,currentColor,castlingStillPossible,towersMoved,possibleRocades,gameOver
    if gameOver:
        return

    if modifiable:
        if [(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98] == lastCoords:
            lastClicked=[]
            can.delete(lastRect)
            lastCoords=[]
        else:
            lastClicked=[event.y//100,event.x//100]
            can.delete(lastRect)
            lastRect=can.create_rectangle((event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98,outline="red",width=4)
            lastCoords=[(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98]
    else:
        if (event.y//100,event.x//100) in possiblePositions and check_current_color(board[lastClicked[0]][lastClicked[1]]) == True:

            if board[lastClicked[0]][lastClicked[1]] == "k":
                castlingStillPossible[0]=False

            elif board[lastClicked[0]][lastClicked[1]] == "r" and lastClicked==[0,0] or lastClicked==[0,7]:
                towersMoved[0].append(lastClicked)
                if len(towersMoved[0])==2:
                    castlingStillPossible[0]=False
                
            elif board[lastClicked[0]][lastClicked[1]] == "K":
                castlingStillPossible[1]=False
            
            elif board[lastClicked[0]][lastClicked[1]] == "R" and lastClicked==[7,0] or lastClicked==[7,7]:
                towersMoved[1].append(lastClicked)
                if len(towersMoved[1])==2:
                    castlingStillPossible[1]=False
                
            board[event.y//100][event.x//100]=board[lastClicked[0]][lastClicked[1]]

            if board[lastClicked[0]][lastClicked[1]] == "p" and event.y//100==7:
                board[event.y//100][event.x//100]="q"
            elif board[lastClicked[0]][lastClicked[1]] == "P" and event.y//100==0:
                board[event.y//100][event.x//100]="Q"


            board[lastClicked[0]][lastClicked[1]]="*"
            lastClicked=[]
            can.delete(lastRect)
            for loop in possible:
                can.delete(loop)
            lastCoords=[]
            modifiable=True
            possibleRocades=[]
            clear_images()
            update_UI(board)
            currentColor = not currentColor
            if currentColor:
                currentPlayer.config(text="Current turn: Black")
            else:
                currentPlayer.config(text="Current turn: White")
            sendMove()
        if (event.y//100,event.x//100) in possibleRocades and check_current_color(board[lastClicked[0]][lastClicked[1]]) == True:
            if board[event.y//100][event.x//100].isupper():
                if event.x//100 == 7:
                    rochade(False,True)
                else:
                    rochade(False,False)
            else:
                if event.x//100 == 7:
                    rochade(True,True)
                else:
                    rochade(True,False)
            lastClicked=[]
            can.delete(lastRect)
            for loop in possible:
                can.delete(loop)
            lastCoords=[]
            modifiable=True
            possibleRocades=[]
            currentColor = not currentColor
            if currentColor:
                currentPlayer.config(text="Current turn: Black")
            else:
                currentPlayer.config(text="Current turn: White")
            sendMove()

    alive=False
    for loop in board:
        if "k" in loop:
            alive=True

    if not alive:
        gameOver=True
        showinfo("White won.")

    alive=False
    for loop in board:
        if "K" in loop:
            alive=True
            
    if not alive:
        gameOver=True
        showinfo("Black won.")



def update_UI(board):

    #Updates the entire images on the board depending of the array, board

    global imagesRefs,imagesGUI

    for loop in range(8):
        for lopp in range(8):
            try:
                fileName="Images/"+figures[board[loop][lopp]]
                imagesRefs.append(PhotoImage(file=fileName))
                imagesGUI.append(can.create_image(lopp*100+20,loop*100+20,image=imagesRefs[-1],anchor=NW))
                
            except:
                pass

def draw_board():

    # Draws the basic board (white and black cases)

    colors=["#f2d08a","white"]
    offset,current=0,0
    for loop in range(8):
        offset=(offset+1)%2
        current=offset
        for lopp in range(8):
            can.create_rectangle(lopp*100,loop*100,lopp*100+100,loop*100+100,fill=colors[current])
            current=(current+1)%2

def clear_images():

    #Removes all the current pieces on the board

    global imagesGUI
    for loop in imagesGUI:
        can.delete(loop)
    imagesGUI=[]

def import_board():

    #After pressing on a button on the program map-generator.py, possibility to easily import a new board

    global board,currentColor
    new_board=pyperclip.paste()
    board=eval(new_board)
    clear_images()
    update_UI(board)
    currentColor = False

def import_fen(fenString):
    global board
    board=parse_fen(fenString)
    clear_images()
    update_UI(board)

def send_fen():
    global board
    newFen=parse_board(board)
    print(newFen)

def reset_board():

    # Resets the entire board

    global board,currentColor
    board=[["*" for lopp in range(8)] for loop in range(8)]
    board[0]=["r","n","b","q","k","b","n","r"]
    board[1]=["p" for loop in range(8)]
    board[6]=["P" for loop in range(8)]
    board[7]=["R","N","B","Q","K","B","N","R"]
    clear_images()
    update_UI(board)
    currentColor = False

############## JOIN UI ##############

window2=Tk()
window2.title("Server connection")

Label(window2,text="Game ID: ").grid(column=0,row=0,padx=10,pady=10)
gameIdString=StringVar()
Entry(window2,textvariable=gameIdString,width=30).grid(column=1,row=0,padx=10,pady=10)
Button(window2,text="Connect to this game ID",width=35,command=confirm_game_id).grid(column=0,row=1,columnspan=2,padx=10,pady=10)
Button(window2,text="Create new game",width=35,command=create_game).grid(column=0,row=2,columnspan=2,padx=10,pady=10)

window2.mainloop()

########### CANCEL MAIN GAME ############

if gameID == "":
    cancel_game()

########### MAIN UI PART ##############

window=Tk()
window.title("Chess")
window.geometry("850x900")
window.config(bg="grey")

can=Canvas(window,width=797,height=797,bg="grey")
can.grid(column=0,row=0,padx=25,pady=25,columnspan=3)

draw_board()
update_UI(board)

currentPlayer=Label(window,text="Current turn: White")
currentPlayer.grid(column=1,row=1,padx=10,pady=10)


can.bind("<Button-1>",click)
window.bind("<Return>", confirm_case)

################## EXECTUTING THE GAME WINDOW ###############

window.mainloop()

sio.disconnect()