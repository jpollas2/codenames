#computer needs:
#Python 2.7
#PIP installed (use https://www.youtube.com/watch?v=zPMr0lEMqpo for help)
#   (use https://pip.pypa.io/en/stable/installing/ for installation/download)
#wxPython installed (use https://wxpython.org for help and download)

#on click of board button, reduce clue number

import requests
import wx
import random
import csv
import operator
import os
from os import getcwd

#get words from internet
#use csv file of words from online
url="https://raw.githubusercontent.com/jpollas2/codenames/master/CodenameWords.csv"

#create a file where the words will go
direct=getcwd()
fname=os.path.join(direct,'codenames.csv')
#print the filename so one can delete after game if desired
print(fname)
r=requests.get(url)

#write data from online to the file
f=open(fname,'w')
f.write(r.content)
f.close()

#read csv file containing all words
with open(fname,'r') as w:
    reader=csv.reader(w)
    words=list(reader)

'''
#get words from desktop file if no internet connection and have file on
with open("/Users/jpollas2/Desktop/CodenameWords.csv",'r') as w:
    reader=csv.reader(w)
    words=list(reader)
'''

#create list of words from csv
WordList=[]
for i in words:
    word=i[0]
    word2=word.upper()
    WordList.append(word2.strip())

#create function to start the game
def startGame():
    #9 blue, 8 red, 1 assassin, and 7 civilians
    BlueFirst = ["Blue"]*9 + ["Red"]*8 + ['Black']*1 + ['Yellow']*7
    #8 blue, 9 red, 1 assassin, and 7 civilians
    RedFirst = ["Red"]*9 + ["Blue"]*8 + ["Black"] + ["Yellow"]*7

    #decide who goes first
    rValue=random.uniform(0,1)
    if rValue > 0.5:
        team= "Blue"
        NeededList=BlueFirst
    else:
        team="Red"
        NeededList=RedFirst

    #randomize the list of teams (for the gameboard)
    random.shuffle(NeededList)

    #create list of 25 words for the game
    random.shuffle(WordList)
    words=[]
    for i in range(0,25):
       words.append(WordList[i])

    #create list of tuples
    #forBoard is unshuffled and used for the gameboard
    #together is shuffled and used for the clue givers
    forBoard=zip(NeededList,words)
    together=zip(NeededList,words)
    together.sort()

    #get lists for each team and their words
    if rValue > 0.5:
        assassin=together[0]
        blue=together[1:10]
        red=together[10:18]
        civ=together[18:]
    else:
        assassin=together[0]
        blue=together[1:9]
        red=together[9:18]
        civ=together[18:]

    #return lists needed for the boards
    return [forBoard,together,red,blue,assassin,civ]
game=startGame()


#creates a button for the words
#when clicked will remove word and reveal the color of words team
class WordButton(wx.Button):
   def __init__(self,parent,label,size,color):
      super(WordButton,self).__init__(parent,-1)
      self.SetLabel(label)
      self.color=color
      self.Bind(wx.EVT_BUTTON,self.on_click) 

   def on_click(self,event):
      self.SetLabel("")
      self.SetBackgroundColour(self.color)


#creates a button for the clues
#similar to word button, but is a toggle button, so if misclicked,
#   it can be clicked again to reveal the word again
class ClueButton(wx.ToggleButton):
   def __init__(self,parent,label,size,color):
      super(ClueButton,self).__init__(parent,-1)
      self.SetLabel(label)
      self.word=label
      self.color=color
      self.Bind(wx.EVT_TOGGLEBUTTON,self.on_click) 

   def on_click(self,event):
      if self.GetValue()==False:
          self.SetLabel(self.word)
          self.SetBackgroundColour(dc)
      else:
          self.SetLabel("")
          self.SetBackgroundColour(self.color)

#creates the start button
#when clicked it will start a new game
class StartButton(wx.Button):
    def __init__(self,parent,label,size):
        super(StartButton,self).__init__(parent,-1)
        self.SetLabel(label)
        self.Bind(wx.EVT_BUTTON,self.on_click)
        
    def on_click(self,event):
        #run the game function
        game=startGame()
        #set a and b to be global variables
        global b
        #close the original frames
        b.board.Close()
        b.Close()

        #displays the gui's
        app=wx.App()
        #gets default color (used in the button)
        defCol=wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
        #creates and shows the game board and clue board
        #a=board(parent=None,title="Codenames",words=game[0])
        b=cluers(parent=None,r=game[2],b=game[3],c=game[5],a=game[4],board=board(parent=None,title="Codenames",words=game[0]))
        app.MainLoop()


#create a button that closes both frames when clicked
class ExitButton(wx.Button):
    def __init__(self,parent,label,size):
        super(ExitButton,self).__init__(parent,-1)
        self.SetLabel(label)
        self.Bind(wx.EVT_BUTTON,self.on_click)

    def on_click(self,event):
        b.board.Close()
        b.Close()
        

#This creates the frame for the gameboard
#It will show a 5 by 5 gird of every word as buttons
class board(wx.Frame): 
    def __init__(self, parent, title, words): 
        super(board, self).__init__(parent, title = title,size = (700,300))
        self.l=words
        self.clue=''
        self.number=''
        self.InitUI()
        self.Centre()
        self.Show()
      
   #creates the initial user interface
   #adds every word as a button from the list words
    def InitUI(self):
        p = wx.Panel(self)
        #gsmain=wx.GridSizer(1,1,0,0)
        #gsmain=wx.GridSizer(2,1,0,0)
        '''
        gsclue=wx.GridSizer(1,2,0,0)
        self.t1=wx.StaticText(p,-1, label="Clue", style = wx.ALIGN_CENTER)
        gsclue.Add(self.t1)
        p.SetSizer(gsmain)
        self.t2=wx.StaticText(p,-1,label="Number",style=wx.ALIGN_CENTER)
        gsclue.Add(self.t2)
        p.SetSizer(gsmain)
        '''
        main = wx.GridSizer(2, 1, 0, 0)
        
        #keeps track of score above the words
        scoreboard = wx.GridSizer(2, 2, 5, 5)
        
        redlab=wx.StaticText(p,-1, style = wx.ALIGN_CENTER)
        redlab.SetLabel("Red")
        redlab.SetForegroundColour("Red")

        redscore = wx.StaticText(p, -1, style = wx.ALIGN_CENTER)
        redscore.SetLabel("9")

        bluelab = wx.StaticText(p, -1, style = wx.ALIGN_CENTER)
        bluelab.SetLabel("Blue")
        bluelab.SetForegroundColour("Blue")

        bluescore = wx.StaticText(p, -1, style = wx.ALIGN_CENTER)
        bluescore.SetLabel("8")

        scoreboard.Add(redlab)
        scoreboard.Add(redscore)
        scoreboard.Add(bluelab)
        scoreboard.Add(bluescore)
        p.SetSizer(main)
        
        
        #5 by 5 grid of the words
        gs = wx.GridSizer(5, 5, 5, 5)
        for w in self.l:
            gs.Add(WordButton(p,label=w[1],size=(20,20),color=w[0]),0,wx.EXPAND)
            p.SetSizer(main)   
        p.SetSizer(main)

        #adding to main grid sizer
        main.Add(scoreboard)
        main.Add(gs)
        p.SetSizer(main)
 
#creates frame for the clue givers
#will show which words belong to which team as buttons
#also contains the new game button and exit game button
class cluers(wx.Frame):
    def __init__(self,parent,r,b,a,c,board):
        super(cluers,self).__init__(parent,size=(600,400))
        self.board=board
        self.r=r
        self.a=a
        self.b=b
        self.c=c
        self.InitUI()
        self.Centre()
        self.Show()

    #creates initial user interface
    #adds every word as a button from each list
    def InitUI(self):
        p=wx.Panel(self)
        #creates a grid of 1 row and 5 columns
        gsmain=wx.GridSizer(1,5,5,5)

        #for the red team words
        #creates 10 rows and 1 column
        gsr=wx.GridSizer(10,1,5,5)
        #adds label to top signifying red team
        redlab=wx.StaticText(p,-1, style = wx.ALIGN_CENTER)
        redlab.SetLabel("Red")
        redlab.SetForegroundColour("Red")
        gsr.Add(redlab)
        #adds the words that belong to red team as buttons
        for w in self.r:
           gsr.Add(ClueButton(p,label=w[1],size=(20,20),color=w[0]),0,wx.EXPAND)
           p.SetSizer(gsmain)

        #for the blue team words
        #creates 10 rows and 1 column
        gsb=wx.GridSizer(10,1,5,5)
        #adds label to top signifying blue team
        bluelab=wx.StaticText(p,-1, style = wx.ALIGN_CENTER)
        bluelab.SetLabel("Blue")
        bluelab.SetForegroundColour("Blue")
        gsb.Add(bluelab)
        #adds words that belong to blue team as buttons
        for w in self.b:
           gsb.Add(ClueButton(p,label=w[1],size=(20,20),color=w[0]),0,wx.EXPAND)
           p.SetSizer(gsmain)

        #creates 2 rows and 1 column
        gsa=wx.GridSizer(2,1,5,5)
        #adds label to top signifying the assassin
        alab=wx.StaticText(p,-1, style = wx.ALIGN_CENTER)
        alab.SetLabel("Assassin")
        gsa.Add(alab)
        #adds the assassin as a button
        gsa.Add(ClueButton(p,label=self.a[1],size=(20,20),color=self.a[0]),0,wx.EXPAND)
        p.SetSizer(gsmain)

        #creates 8 rows and 1 column
        gsc=wx.GridSizer(8,1,5,5)
        #adds label to top signifying the civilians
        clab=wx.StaticText(p,-1, style = wx.ALIGN_CENTER)
        clab.SetLabel("Civilians")
        clab.SetForegroundColour("Brown")
        gsc.Add(clab)
        #adds words that belong to the civilians as buttons
        for w in self.c:
           gsc.Add(ClueButton(p,label=w[1],size=(20,20),color=w[0]),0,wx.EXPAND)
           p.SetSizer(gsmain)
        
        #adds a start button to the clue givers board
        gss=wx.GridSizer(4,1,5,5)
        nada=wx.StaticText(p,-1)
        nada.SetLabel("")
        gss.Add(nada)
        gss.Add(StartButton(p,label="New Game",size=(20,20)),0,wx.EXPAND)
        p.SetSizer(gsmain)
        gss.Add(ExitButton(p,label="Exit Game",size=(20,20)),0,wx.EXPAND)
        p.SetSizer(gsmain)
        GCB=wx.Button(p,label="Give Clue",size=(20,20))
        GCB.Bind(wx.EVT_BUTTON,self.giveClue)
        gss.Add(GCB,0,wx.EXPAND)
        p.SetSizer(gsmain)
        
        #adds the 5 previous panels to the original panel made so it shows
        #  on the gameboard
        gsmain.Add(gsr)
        gsmain.Add(gsb)
        gsmain.Add(gsa)
        gsmain.Add(gsc)
        gsmain.Add(gss)
        p.SetSizer(gsmain)

    def giveClue(self,event):
        cl=wx.TextEntryDialog(parent=self,message="What's your clue?",defaultValue='')
        cl.ShowModal()
        num=wx.TextEntryDialog(parent=self,message="How many words?",defaultValue='')
        num.ShowModal()
        result=cl.GetValue()
        result2=num.GetValue()
        cl.Destroy()
        num.Destroy()
        self.board.t1.SetLabel(result)
        self.board.t2.SetLabel(result2)        
        
        

#displays the gui's
app=wx.App()
#gets default color (used in the button)
dc=(236,236,236,255)
#creates and shows the game board and clue board
#a=board(parent=None,title="Codenames",words=game[0])
b=cluers(parent=None,r=game[2],b=game[3],c=game[5],a=game[4],board=board(parent=None,title="Codenames",words=game[0]))
app.MainLoop()




