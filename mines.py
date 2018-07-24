import tkinter
from tkinter import *
import random

root = tkinter.Tk()
root.wm_title('MineSweep 3,000')
root.configure(background='#999999', cursor="none")

canvas = tkinter.Canvas(root, height=380, width=380, background='#999999')
canvas.grid(row=0, column=2, rowspan=5, columnspan = 5)
canvas.pack

inst = tkinter.Label(root, bg = '#999999', font =('Tempus Sans ITC', 10, 'bold'),text='Click Cells to Detonate Bomb.\n Bombs may be fake or real, \n so beware...' +\
                        '\n if hit with a bomb, \n the game will terminate,\n and so will you muahaha. \n \n Fake bombs will tell you' +\
                        '\n how many bombs are touching it... \n you will have to use logic \n to figure out the rest. \n\n Good Luck!')
inst.grid(row = 3,column = 0, rowspan = 2, columnspan=2)
size = 5
d=380/int(size)
diffm = (size*size)/4
diff = int(diffm)
grided = size*size

sizei = tkinter.IntVar()
sizei.set(size)

def newsize(new_intval):
    global size
    global d
    global diffm
    global grided
    size = sizei.get()
    grided = size*size
    d=380/int(size)
    diffm = grided/4

sslider = tkinter.Scale(root, from_ = 5, to=8, variable = sizei, label = 'Size', command = newsize, bg = '#999999', font=('Tempus Sans ITC',10))
sslider.grid(row = 1,column = 0)

diffi = tkinter.IntVar()
diffi.set(diff)

def newdiff(new_intval):
    global diff
    diff = (float(diffi.get())/100)*float(grided)

dslider = tkinter.Scale(root, from_ = 20, to=40, variable = diffi, label = 'Difficulty %', command = newdiff, bg = '#999999', font=('Tempus Sans ITC',10))
dslider.grid(row = 1,column = 1)

def click(event):
    global score
    if canvas.find_withtag(CURRENT):
        if 'mine' in canvas.gettags(canvas.find_withtag(CURRENT)):
            canvas.delete(ALL)
            endseq = canvas.create_text(190, 190,fill = '#03FFC7',justify=CENTER,text='GAME OVER. \n FINAL SCORE ='+str(score), font=('Tempus Sans ITC', 15, 'bold'))  
        if score >= (size*size) - diff-1:
            canvas.delete(ALL)
            endseq = canvas.create_text(190,190,fill = '#03FFC7',justify=CENTER,text='Congrats. You beat the game. \n FINAL SCORE ='+str(score), font=('Tempus Sans ITC', 15, 'bold')) 
        else:
            score +=1 
            distance = canvas.gettags(canvas.find_withtag(CURRENT))
            coordz = canvas.coords(canvas.find_withtag(CURRENT))
            x1 = coordz[0]
            y1 = coordz[1]
            x2 = coordz[2]
            y2 = coordz[3]
            x = (x1+x2)/2
            y = y1 + (d/2)
            canvas.itemconfig(CURRENT, fill='#FF4700')
            dis = canvas.create_text(x,y,text = distance[0], justify = RIGHT, font = ('Tempus Sans ITC',10) )   

def start():
    global score
    score = 0
    canvas.delete(ALL)
    randlist = random.sample(range(1,(size*size)+1),int(diff))
    for colum in range(1,size+1):
        cob = colum - 1
        for cells in range(1,size+1):
            cev = cells + (6*cob)
            ceb = cells - 1
            startx = cells + (d*ceb)
            starty = colum + (d*cob)
            new_cell = canvas.create_polygon(startx, starty, startx+d,starty, startx+d, starty+d, startx, starty+d, 
                                fill = '#646464',outline = '#080808', activefill = '#ff4700', tags = (str(cev),'cells'))
            if cev in randlist:
                canvas.itemconfig(new_cell, tags=('mine',str(cev),'cells'))           
    for items in canvas.find_withtag('cells'):
        ite = str(int(items))
        itemcount = 0
        global size
        er = str(size)
        if 'mine' not in canvas.gettags(canvas.find_withtag(ite)):
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)-1))):
                if er in canvas.gettags(canvas.find_withtag(str(int(items)+1))):
                    itemcount = itemcount
                else:
                    itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)+1))):
                if er in canvas.gettags(canvas.find_withtag(str(int(items)+1))):
                    itemcount = itemcount
                else:
                    itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)-size))):
                itemcount=itemcount+1
            if 'mine' in canvas.gettags(canvas.find_withtag(str(int(items)+size))):
                itemcount=itemcount+1
            canvas.itemconfig(canvas.find_withtag(ite), tags = (str(itemcount))) 

reboot = tkinter.Button(root, text='Click To Start or Restart', command=start, font=('Tempus Sans ITC', 12, 'bold'), background='#a3a3a3', foreground='#4503E8')
reboot.grid(row = 0, column = 0, columnspan = 2)  

canvas.bind("<Button-1>", click)

root.mainloop()
