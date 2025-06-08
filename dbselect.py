import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

from openpyxl import load_workbook
from openpyxl.comments import Comment

import os

import threading

from time import time, sleep
from datetime import datetime, timedelta

import subprocess as sp

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.source = StringVar()
        self.target = ""
        self.initFolders = IntVar()
        self.ftype = IntVar()
        self.pointer = 0
        self.identifier = StringVar()
        self.sheet = StringVar()
        self.sheet_saved = StringVar()
        self.sheetId = StringVar()
        self.sheetId_saved = StringVar()
        self.gameDesc = StringVar()
        self.allMoves = []
        self.winner = IntVar()
        self.advantage = IntVar()
        self.showFlag = IntVar()
        self.sheetsList = ['No Selection ']
        self.sheetIdsList = ['No Selection']

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="50")
        Style().configure("G.TLabel", font="Verdana 8")
        Style().configure("L.TLabel", font="Courier 40 bold", width="8")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_g = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_h = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_i = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="LOAD AND PLAY", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="This utility is for loading chess games to the database or playing the", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="games/openings loaded in the chess database.", style="S.TLabel" )

        self.load = Button(self.main_container, text="LOAD GAMES", style="B.TButton", command=self.loadGames)
        self.play = Button(self.main_container, text="PLAY GAMES", style="B.TButton", command=self.playGames)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        # Position widgets
        self.mainLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        
        self.sep_a.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.subLabelA.grid(row=2, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=3, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')

        self.sep_b.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.load.grid(row=6, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.play.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.sep_c.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.exit.grid(row=8, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')

    def loadGames(self):
        
        l = threading.Thread(None, self.loadThread, ())
        l.start()

    def loadThread(self):
        
        os.system('python dbloads.py')
        # os.system('python C:/Users/Alan/Scripts/Code/db_lister/dbloads.py')

    def playGames(self):

        o = threading.Thread(None, self.playThread, ())
        o.start()

    def playThread(self):

        os.system('python dbgames.py')
        # os.system('python C:/Users/Alan/Scripts/Code/db_lister/dbgames.py')

root = Tk()
root.title("LOAD AND PLAY")

# Set size

wh = 180
ww = 410

root.resizable(height=False, width=False)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
