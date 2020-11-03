from tkinter import*

lastRect=0
lastCoords=[]
modifiable=True
imagesRefs=[]
possible=[]
possiblePositions=[]

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
               "b":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8)],
               "B":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8)],\
               "r":[(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),(-8,0),\
                   (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),(0,-8)],\
               "R":[(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),(-8,0),\
                   (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),(0,-8)],\
               "k":[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)],\
               "K":[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)],\
               "q":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8),\
                    (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),(-8,0),\
                    (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),(0,-8)],
               "Q":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8),\
                    (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),(-8,0),\
                    (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7),(0,-8)]}

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

def show_moves(moves):
    global possible,lastCoords,possiblePositions,board
    coords=((lastCoords[1]-2)//100,(lastCoords[0]-2)//100)
    currentCharacter=board[(lastCoords[1]-2)//100][(lastCoords[0]-2)//100]
    possiblePositions=[]
    for loop in moves:
        try:
            if (currentCharacter=="n" and board[loop[0]][loop[1]]=="*") or (currentCharacter=="N" and board[loop[0]][loop[1]]=="*"):
                possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                possiblePositions.append(loop)

            elif currentCharacter=="r" or currentCharacter=="R":
                x,y=loop[0]-coords[0],loop[1]-coords[1]
                if x!=0:
                    movePossible=True
                    for lopp in range(1,abs(x)+1):
                        if board[coords[0]+(lopp*signOf(x))][loop[1]] != "*":
                            movePossible=False
                    if movePossible:
                        possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                        possiblePositions.append(loop)
                elif y!=0:
                    movePossible=True
                    for lopp in range(1,abs(y)+1):
                        if board[loop[0]][coords[1]+(lopp*signOf(y))] != "*":
                            movePossible=False
                    if movePossible:
                        possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                        possiblePositions.append(loop)

            elif currentCharacter=='k' or currentCharacter=='k':
                for i in range(3):
                    for j in range(3):
                        if board[loop[0]][loop[1]] == '*':
                            possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2, (loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
                            possiblePositions.append(loop)

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

#Converts FEN string to array usable to draw board in tkinter
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
#Converts array to FEN string to send to server
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
    global lastRect,lastCoords,modifiable,possiblePositions
    if modifiable:
        if [(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98] == lastCoords:
            can.delete(lastRect)
            lastCoords=[]
        else:
            can.delete(lastRect)
            lastRect=can.create_rectangle((event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98,outline="red",width=4)
            lastCoords=[(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98]
    else:
        print(event.x//100,event.y//100,possiblePositions)
        if (event.y//100,event.x//100) in possiblePositions:
            print("Valid move")
        else:
            print("Non valid move")



def update_UI(board):
    global imagesRefs
    for loop in range(8):
        for lopp in range(8):
            try:
                fileName="Images/"+figures[board[loop][lopp]]
                imagesRefs.append(PhotoImage(file=fileName))
                can.create_image(lopp*100+20,loop*100+20,image=imagesRefs[-1],anchor=NW)
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

window=Tk()
window.title("Chess")
window.geometry("850x850")
window.config(bg="grey")

can=Canvas(window,width=797,height=797,bg="grey")
can.grid(column=0,row=0,padx=25,pady=25)

draw_board()
update_UI(board)

can.bind("<Button-1>",click)
window.bind("<Return>", confirm_case)
window.mainloop()
