from tkinter import*
import pyperclip

lastRect=0
lastCoords=[]
modifiable=True
imagesRefs=[]
imagesGUI=[]
possible=[]
possiblePositions=[]

board=[["*" for lopp in range(8)] for loop in range(8)]
indexes=[[0 for lopp in range(8)] for loop in range(8)]

characters=["*","p","P","n","N","b","B","r","R","q","Q","k","K"]

figures={"p":"pawn1.png","n":"knight1.png","b":"bishop1.png","r":"rooks1.png","q":"queen1.png","k":"king1.png",\
        "P":"pawn2.png","N":"knight2.png","B":"bishop2.png","R":"rooks2.png","Q":"queen2.png","K":"king2.png"}



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

def copy_to_clipboard():
    pyperclip.copy("board="+str(board))

def click(event):
    global indexes,characters,board
    try:
        indexes[event.y//100][event.x//100]=(indexes[event.y//100][event.x//100]+1)%13
        board[event.y//100][event.x//100]=characters[indexes[event.y//100][event.x//100]]
        clear_images()
        update_UI(board)
    except:
        pass


def clear_images():
    global imagesGUI
    for loop in imagesGUI:
        can.delete(loop)

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

window=Tk()
window.title("Chess")
window.geometry("850x900")
window.config(bg="grey")

can=Canvas(window,width=797,height=797,bg="grey")
can.grid(column=0,row=0,padx=25,pady=25)

Button(window,text="Copy current board to clipboard",command=copy_to_clipboard).grid(column=0,row=1,padx=10,pady=10)

draw_board()
update_UI(board)

can.bind("<Button-1>",click)
window.mainloop()
