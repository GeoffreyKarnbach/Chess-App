from tkinter import*

lastRect=0
lastCoords=[]
modifiable=True
imagesRefs=[]
possible=[]

board=[["*" for lopp in range(8)] for loop in range(8)]
board[0]=["r","n","b","q","k","b","n","r"]
board[1]=["p" for loop in range(8)]
board[6]=["P" for loop in range(8)]
board[7]=["R","N","B","Q","K","B","N","R"]

figures={"p":"pawn1.png","n":"knight1.png","b":"bishop1.png","r":"rooks1.png","q":"queen1.png","k":"king1.png",\
        "P":"pawn2.png","N":"knight2.png","B":"bishop2.png","R":"rooks2.png","Q":"queen2.png","K":"king2.png"}

possibleMoves={"P":[(-1,0),(-2,0)],\
               "p":[(1,0),(2,0)],\
               "n":[(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1),],\
               "N":[(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1),],\
               "b":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8)],
               "B":[(-8,-8),(-7,-7),(-6,-6),(-5,-5),(-4,-4),(-3,-3),(-2,-2),(-1,-1),(+1,+1),(+2,+2),(+3,+3),(+4,+4),(+5,+5),(+6,+6),(+7,+7),(+8,+8),\
                    (+8,-8),(+7,-7),(+6,-6),(+5,-5),(+4,-4),(+3,-3),(+2,-2),(+1,-1),(-1,+1),(-2,+2),(-3,+3),(-4,+4),(-5,+5),(-6,+6),(-7,+7),(-8,+8)]}

def get_moves(position):
    global board
    moves=[]
    if board[position[1]][position[0]] != "*":
        liste=possibleMoves[board[position[1]][position[0]]]
        for loop in liste:
            moves.append((loop[0]+position[1],loop[1]+position[0]))
    return moves

def show_moves(moves):
    global possible
    for loop in moves:
        possible.append(can.create_rectangle((loop[1])*100+2,(loop[0])*100+2,(loop[1])*100+98,(loop[0])*100+98,outline="green",width=4))
        print(loop)

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
    global lastRect,lastCoords,modifiable
    if modifiable:
        if [(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98] == lastCoords:
            can.delete(lastRect)
            lastCoords=[]
        else:
            can.delete(lastRect)
            lastRect=can.create_rectangle((event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98,outline="red",width=4)
            lastCoords=[(event.x//100)*100+2,(event.y//100)*100+2,(event.x//100)*100+98,(event.y//100)*100+98]


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
