import tkinter
from tkinter import *
import random

#create the Tkinter GUI interface, set title and turn cursor off
root = tkinter.Tk()
root.wm_title('MineSweep 3,000')
root.configure(background='#999999', cursor="none")

#create the main game interface(where the boxes and mines are) , set its size and color and location onscreen
canvas = tkinter.Canvas(root, height=380, width=380, background='#999999')
canvas.grid(row=0, column=2, rowspan=5, columnspan = 5)
canvas.pack

#create the label with instructions, set its location onscreen
inst = tkinter.Label(root, bg = '#999999', font =('Tempus Sans ITC', 10, 'bold'),text='Click Cells to Detonate Bomb.\n Bombs may be fake or real, \n so beware...' +\
                        '\n if hit with a bomb, \n the game will terminate,\n and so will you muahaha. \n \n Fake bombs will tell you' +\
                        '\n how many bombs are touching it... \n you will have to use logic \n to figure out the rest. \n\n Good Luck!')
inst.grid(row = 3,column = 0, rowspan = 2, columnspan=2)

#set starting variables
global size 
size = 5 # how many boxes are in a row
d=380/int(size) # how big the boxes are based on how many must fit in the screen (set to fit a raspberry pi touchscreen currently)
diffm = (size*size)/4 #median difficulty, based on how many total boxes there are
diff = int(diffm) #difficulty (determined by how many of the boxes are mines)
grided = size*size #how many total boxes there are, based on how many boxes are in a row (creating a square)

#create moving variable for the slider controlling how many boxes are in a row, setting it at first as the original baseline number 
sizei = tkinter.IntVar()
sizei.set(size)

#change the original variables that deal with the amount of boxes, when given a new value for how many boxes are in a row
def newsize(new_intval):
    global size
    global d
    global diffm
    global grided
    size = sizei.get()
    grided = size*size
    d=380/int(size)
    diffm = grided/4

#set up the slider to change how many boxes are in a row
sslider = tkinter.Scale(root, from_ = 5, to=8, variable = sizei, label = 'Size', command = newsize, bg = '#999999', font=('Tempus Sans ITC',10))
sslider.grid(row = 1,column = 0)

#create moving variable for the slider controlling difficulty, setting it at first as the original baseline number 
diffi = tkinter.IntVar()
diffi.set(diff)

#change the original variable for difficulty when given a new difficulty value from slider
def newdiff(new_intval):
    global diff
    diff = (float(diffi.get())/100)*float(grided)

#set up slider that changes diffuculty (how many of the boxes are mines)
dslider = tkinter.Scale(root, from_ = 20, to=40, variable = diffi, label = 'Difficulty %', command = newdiff, bg = '#999999', font=('Tempus Sans ITC',10))
dslider.grid(row = 1,column = 1)

#when you click on a box... (this is after game play has started)
def click(event):
    global score
    #determines the box you clicked on
    if canvas.find_withtag(CURRENT):
        #if the box is a mine, clear game play screen, give final score
        if 'mine' in canvas.gettags(canvas.find_withtag(CURRENT)):
            canvas.delete(ALL)
            endseq = canvas.create_text(190, 190,fill = '#03FFC7',justify=CENTER,text='GAME OVER. \n FINAL SCORE ='+str(score), font=('Tempus Sans ITC', 15, 'bold'))  
        #if you clicked the last safe box, clear game play screen, tell player they won
        if score >= (size*size) - diff-1:
            canvas.delete(ALL)
            endseq = canvas.create_text(190,190,fill = '#03FFC7',justify=CENTER,text='Congrats. You beat the game. \n FINAL SCORE ='+str(score), font=('Tempus Sans ITC', 15, 'bold')) 
        #otherwise, increase the score, and reveal how many of the nearby boxes are a mine
        else:
            score +=1 
            distance = canvas.gettags(canvas.find_withtag(CURRENT))
            coordz = canvas.coords(canvas.find_withtag(CURRENT))
              #coordinate stuff below is all to center the text in the middle of the box
            x1 = coordz[0]
            y1 = coordz[1]
            x2 = coordz[2]
            y2 = coordz[3]
            x = (x1+x2)/2
            y = y1 + (d/2)
            canvas.itemconfig(CURRENT, fill='#FF4700')
            dis = canvas.create_text(x,y,text = distance[0], justify = RIGHT, font = ('Tempus Sans ITC',10) )   

#when a game is started... (setting up the game board)
def start():
    global score
    score = 0
    canvas.delete(ALL)
    randlist = random.sample(range(1,(size*size)+1),int(diff)) #pick which boxes will be mines
    #create all boxes, and tag them with their position (numerically)
    for colum in range(1,size+1):
        cob = colum - 1
        for cells in range(1,size+1):
            cev = cells + (6*cob)
            ceb = cells - 1
            startx = cells + (d*ceb)
            starty = colum + (d*cob)
            new_cell = canvas.create_polygon(startx, starty, startx+d,starty, startx+d, starty+d, startx, starty+d, 
                                fill = '#646464',outline = '#080808', activefill = '#ff4700', tags = (str(cev),'cells'))
            #tag boxs which are mines as mine
            if cev in randlist:
                canvas.itemconfig(new_cell, tags=('mine',str(cev),'cells'))           
    #searches all boxes or cells to see proximity to mine(s)
    
    for items in canvas.find_withtag('cells'):
        ite = str(int(items))
        itemcount = 0
        er = str(size)
        #narrows down search to only boxes that are not mines
        if 'mine' not in canvas.gettags(canvas.find_withtag(ite)):
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)-1))):
                if er in canvas.gettags(canvas.find_withtag(str(int(items)+1))):
                    itemcount = itemcount
                else:
                    itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)+1))):
                if er in canvas.gettags(canvas.find_withtag(str(int(items)-1))):
                    itemcount = itemcount
                else:
                    itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)-size))):
                itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)+size))):
                itemcount=itemcount+1
            #resets tags to only be how many mines are nearby 
            canvas.itemconfig(canvas.find_withtag(ite), tags = (str(itemcount))) 

#creates button to reset game board
reboot = tkinter.Button(root, text='Click To Start or Restart', command=start, font=('Tempus Sans ITC', 12, 'bold'), background='#a3a3a3', foreground='#4503E8')
reboot.grid(row = 0, column = 0, columnspan = 2)  

canvas.bind("<Button-1>", click)

root.mainloop()
