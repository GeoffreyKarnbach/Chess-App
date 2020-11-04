from tkinter import*
import pyperclip

lastRect=0
lastCoords=[]
modifiable=True
imagesRefs=[]
possible=[]
possiblePositions=[]
imagesGUI=[]

lastClicked=[]

board=[["*" for lopp in range(8)] for loop in range(8)]
board[0]=["r","n","b","q","k","b","n","r"]
board[1]=["p" for loop in range(8)]
board[6]=["P" for loop in range(8)]
board[7]=["R","N","B","Q","K","B","N","R"]


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

def get_moves(position):
    global board
    moves=[]
    if board[position[1]][position[0]] != "*":
        liste=possibleMoves[board[position[1]][position[0]]]
        for loop in liste:
            moves.append((loop[0]+position[1],loop[1]+position[0]))
    return moves

def signOf(number):
    if number > 0:
        return 1
    return -1

#SHOWING POSSIBLE MOVES WITH GREEN SQUARES
def show_moves(moves):
    global possible,lastCoords,possiblePositions,board
    coords=((lastCoords[1]-2)//100,(lastCoords[0]-2)//100)
    currentCharacter=board[(lastCoords[1]-2)//100][(lastCoords[0]-2)//100]
    possiblePositions=[]
    if currentCharacter != "b" and currentCharacter != "B" and currentCharacter != "r" and currentCharacter != "R" and currentCharacter != "q" and currentCharacter != "Q":
        for loop in moves:
            try:
                #KNIGHT
                if (currentCharacter=="n" and board[loop[0]][loop[1]]=="*") or (currentCharacter=="N" and board[loop[0]][loop[1]]=="*"):
                    possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                    possiblePositions.append(loop)

                #KING
                elif currentCharacter=='k' or currentCharacter=='k':
                    for i in range(3):
                        for j in range(3):
                            if board[loop[0]][loop[1]] == '*':
                                possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                                possiblePositions.append(loop)

                #PAWN
                elif currentCharacter=='p' or currentCharacter=='P':
                    if (coords[0] == 1 and currentCharacter=='p'):
                        if board[loop[0]][loop[1]] == '*' and board[loop[0]+1][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0]+1)*100+98,outline="green",width=4))
                            possiblePositions.extend([loop, (loop[0]+1, loop[1])])
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)
                    elif (coords[0] == 6 and currentCharacter=='P'):
                        if board[loop[0]][loop[1]] == '*' and board[loop[0]-1][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0]-1)*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.extend([loop, (loop[0]-1, loop[1])])
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)
                    else:
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))      
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
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass
                
        elif currentCharacter=='B':
            for bmove in possibleMoves['B']:
                print(bmove)
                r = 1
                try:
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass
        #ROOK
        elif currentCharacter=="r":
            for bmove in possibleMoves['r']:
                r = 1
                try:
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass

        elif currentCharacter=="R":
            for bmove in possibleMoves['R']:
                r = 1
                try:
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass

        #QUEEN
        elif currentCharacter=="q":
            for bmove in possibleMoves['q']:
                r = 1
                try:
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass

        elif currentCharacter=="Q":
            for bmove in possibleMoves['Q']:
                r = 1
                try:
                    while r < 8 and board[r*bmove[0]+coords[0]][r*bmove[1]+coords[1]] == '*':
                        possible.append(can.create_rectangle((r*bmove[1]+coords[1])*100+2,(r*bmove[0]+coords[0])*100+2, (r*bmove[1]+coords[1])*100+98,(r*bmove[0]+coords[0])*100+98,outline="green",width=4))
                        possiblePositions.append((r*bmove[0]+coords[0],r*bmove[1]+coords[1]))
                        r+=1
                except:
                    pass
                    
                


def confirm_case(event):
    global lastCoords,modifiable,possible
    if lastCoords!=[]:
        if modifiable:
            modifiable=False
            show_moves(get_moves(((lastCoords[0]-2)//100,(lastCoords[1]-2)//100)))
        else:
            modifiable=True
            for loop in possible:
                can.delete(loop)
    else:
        print("Select a case before confirming")

#Converts FEN string to array usable to draw board in tkinter | TODO: add who is playing at the end
def parse_fen(fenString):
    lines = fenString.split(' ')[0].split('/')
    for i in range(len(lines)):
        lines[i] = list(lines[i])
        for j in range(len(lines[i])):
            if lines[i][j].isdigit() == True:
                for k in range(int(lines[i][j])-1):
                    lines[i].insert(j+1, '*')
                lines[i][j] = '*'
    return lines
#Converts array to FEN string to send to server | TODO: add who is playing at the end
def parse_board(board):
    fen = ''
    for i in range(8):
        star = 0
        for j in range(8):
            if board[i][j] == '*':
                star+=1
            elif star == 0:
                fen+=board[i][j]
            if star != 0:
                if board[i][j] != '*' or j == 7:
                    fen+=str(star)
                    star = 0
        if i != 7:
            fen+='/'
    return fen

def click(event):
    global lastRect,lastCoords,modifiable,possiblePositions,lastClicked
    if modifiable:
        if [(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98] == lastCoords:
            lastClicked=(event.x//100,event.y//100)
            can.delete(lastRect)
            lastCoords=[]
        else:
            can.delete(lastRect)
            lastRect=can.create_rectangle((event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98,outline="red",width=4)
            lastCoords=[(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98]
    else:
        print(event.x//100,event.y//100,possiblePositions)
        if (event.y//100,event.x//100) in possiblePositions:
            print("Valid move",lastClicked)
        else:
            print("Non valid move")



def update_UI(board):
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
    colors=["#f2d08a","white"]
    offset,current=0,0
    for loop in range(8):
        offset=(offset+1)%2
        current=offset
        for lopp in range(8):
            can.create_rectangle(lopp*100,loop*100,lopp*100+100,loop*100+100,fill=colors[current])
            current=(current+1)%2

def clear_images():
    global imagesGUI
    for loop in imagesGUI:
        can.delete(loop)
    imagesGUI=[]

def import_board():
    global board
    new_board=pyperclip.paste()
    print(new_board)
    board=eval(new_board)
    clear_images()
    update_UI(board)

def reset_board():
    global board
    board=[["*" for lopp in range(8)] for loop in range(8)]
    board[0]=["r","n","b","q","k","b","n","r"]
    board[1]=["p" for loop in range(8)]
    board[6]=["P" for loop in range(8)]
    board[7]=["R","N","B","Q","K","B","N","R"]
    clear_images()
    update_UI(board)


window=Tk()
window.title("Chess")
window.geometry("850x900")
window.config(bg="grey")

can=Canvas(window,width=797,height=797,bg="grey")
can.grid(column=0,row=0,padx=25,pady=25,columnspan=2)

draw_board()
update_UI(board)

Button(window,text="Import board",command = import_board).grid(column=0,row=1,padx=10,pady=10)
Button(window,text="Reset board",command = reset_board).grid(column=1,row=1,padx=10,pady=10)

can.bind("<Button-1>",click)
window.bind("<Return>", confirm_case)
window.mainloop()
