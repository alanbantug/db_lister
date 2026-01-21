import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

import os

from time import time, sleep
from datetime import date, datetime, timedelta

import subprocess as sp

import dbaccess as db

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.pointer = 0
        self.tag = StringVar()
        self.tagSelect = StringVar()
        self.player = StringVar()
        self.description = StringVar()
        self.opening = StringVar()
        self.variation = StringVar()
        self.selNotable = IntVar()
        self.selTactical = IntVar()
        self.selPlayed = IntVar()
        self.allMoves = []
        self.allComments = {}
        self.winner = IntVar()
        self.advantage = IntVar()
        self.whiteWin = IntVar()
        self.blackWin = IntVar()
        self.drawGame = IntVar()
        self.gameTactical = IntVar()
        self.gameNotable = IntVar()
        self.tagList = []
        self.varCount = StringVar()
        self.limitList = ['= 0', '= 0', '= 1', '>= 1', '=2', '>= 2']

        self.resToCount = StringVar()
        self.countList = ['0', '0', '1', '2', '3', '4']

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="25")
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
        self.mainLabel = Label(self.main_container, text="GAME MOVES", style="M.TLabel" )

        self.tagOpt = LabelFrame(self.main_container, text=' TAG ', style="O.TLabelframe")
        self.tagPattern = Entry(self.tagOpt, textvariable=self.tag, width="18")
        self.openingOpt = LabelFrame(self.main_container, text=' OPENING ', style="O.TLabelframe")
        self.openingName = Entry(self.openingOpt, textvariable=self.opening, width="50")
        self.playerOpt = LabelFrame(self.main_container, text=' PLAYER ', style="O.TLabelframe")
        self.playerName = Entry(self.playerOpt, textvariable=self.player, width="18")
        self.variationOpt = LabelFrame(self.main_container, text=' VARIATION ', style="O.TLabelframe")
        self.variationText = Entry(self.variationOpt, textvariable=self.variation, width="50")
        self.results = LabelFrame(self.main_container, text=' RESULTS ', style="O.TLabelframe")
        self.optNotbl = Checkbutton(self.main_container, text=" Notable ", style="B.TCheckbutton", variable=self.selNotable)
        self.optTactl = Checkbutton(self.main_container, text=" Tactical ", style="B.TCheckbutton", variable=self.selTactical)
        self.optPlay = Checkbutton(self.main_container, text=" Played ", style="B.TCheckbutton", variable=self.selPlayed)
        self.playCount = OptionMenu(self.main_container, self.varCount, *self.limitList)
        self.playCount.config(width=5)

        self.white = Checkbutton(self.results, text=" White ", style="B.TCheckbutton", variable=self.whiteWin)
        self.black = Checkbutton(self.results, text=" Black ", style="B.TCheckbutton", variable=self.blackWin)
        self.draw = Checkbutton(self.results, text=" Draw ", style="B.TCheckbutton", variable=self.drawGame)

        self.fetch = Button(self.main_container, text="GET GAMES", style="B.TButton", width=32, command=self.buildGameList)
        self.reset = Button(self.main_container, text="RESET OPTIONS", style="B.TButton", width=32, command=self.resetProcess)
        
        self.gameOptions = LabelFrame(self.main_container, text=' SELECT GAMES ', style="O.TLabelframe")
        self.gameList = Listbox(self.gameOptions, selectmode='single', width=60, height=5)
        self.gscroller = Scrollbar(self.gameOptions, orient=VERTICAL, command=self.gameList.yview)
        self.gameList.config(font=("Courier New", 8), yscrollcommand=self.gscroller.set)

        self.start = Button(self.main_container, text="PLAY", style="B.TButton", command=self.startGame)
        self.export = Button(self.main_container, text="EXPORT", style="B.TButton", command=self.exportGames)
        self.resetCount = Button(self.main_container, text="RESET GAME COUNT", style="B.TButton", command=self.displayResetPanel)
        
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=self.exitApp)

        # Position widgets
        self.mainLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        
        self.sep_a.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.tagPattern.grid(row=0, column=0, padx=10, pady=(5,10), sticky='NSEW')
        self.tagOpt.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.openingName.grid(row=0, column=0, padx=10, pady=(5,10), sticky='NSEW')
        self.openingOpt.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')
        self.playerName.grid(row=0, column=0, padx=10, pady=(5,10), sticky='NSEW')
        self.playerOpt.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.variationText.grid(row=0, column=0, padx=10, pady=(5,10), sticky='NSEW')
        self.variationOpt.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.optNotbl.grid(row=4, column=0, padx=10, pady=2, sticky='NSW')
        self.optTactl.grid(row=5, column=0, padx=10, pady=2, sticky='NSW')
        self.optPlay.grid(row=6, column=0, padx=10, pady=2, sticky='NSW')
        self.playCount.grid(row=6, column=0, padx=(80,5), pady=2, sticky='NSW')
        self.white.grid(row=0, column=0, padx=10, pady=12, sticky='NSW')
        self.black.grid(row=0, column=0, padx=(120,10), pady=12, sticky='NSW')
        self.draw.grid(row=0, column=0, padx=(240,10), pady=12, sticky='NSW')
        self.results.grid(row=4, rowspan=3, column=1, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.sep_b.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        
        self.fetch.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.reset.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.sep_c.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
                
        self.gameList.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='W')
        self.gscroller.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky='W')
        self.gameOptions.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.start.grid(row=11, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        self.export.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.resetCount.grid(row=12, column=2, columnspan=2, padx=5, pady=5, sticky='NSEW')
        
        self.sep_e.grid(row=13, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        
        self.exit.grid(row=14, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.dataconn = db.databaseConn()
        self.processControl(1)

    def buildGameList(self):

        self.gameList.delete(0, END)
        
        if self.check_options() == 0:
            game_count = self.getGameCount()[0][0]

            res = messagebox.askquestion(title="Game count", message=f"You will extract {game_count} games. Do you want to continue?")
            if res == 'no':
                return

        select_sql = "select tag, opening, white, black, result from game_details "

        # where_count = 0

        # if self.tag.get():
        #     add_text = self.tag.get()
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, f"tag like '{add_text}%'")
        #         where_count += 1

        # if self.opening.get():
        #     add_text = self.opening.get()
        #     add_text = add_text.replace("'", "''")
        #     add_opening = f"opening like '%{add_text}%'" 
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, add_opening)
        #     else:
        #         select_sql = self.add_where(1, select_sql, add_opening)

        #     where_count += 1

        # if self.player.get():
        #     add_text = self.player.get().capitalize()
        #     if add_text.isalnum():
        #         pass 
        #     else:
        #         messagebox.showerror("Error in string","Search string contains special characters. Please remove.")
        #         return
            
        #     add_player = f"(white like '%{add_text}%' or black like '%{add_text}%')"
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, add_player)
        #     else:
        #         select_sql = self.add_where(1, select_sql, add_player)

        #     where_count += 1

        # if self.drawGame.get() or self.whiteWin.get() or self.blackWin.get():
        #     res_count = 0
        #     if self.whiteWin.get():
        #         if res_count == 0:
        #             res_text = "(result = 1"    
        #         else:
        #             res_text += " or result = 1 "
        #         res_count += 1

        #     if self.blackWin.get():
        #         if res_count == 0:
        #             res_text = "(result = 2"    
        #         else:
        #             res_text += " or result = 2 "
        #         res_count += 1

        #     if self.drawGame.get():
        #         if res_count == 0:
        #             res_text = "(result = 0"
        #         else:
        #             res_text += " or result = 0"
        #         res_count += 1

        #     res_text += ")"

        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, res_text)
        #     else:
        #         select_sql = self.add_where(1, select_sql, res_text)
        #     where_count += 1

        # if self.selNotable.get():
        #     nota_text = 'notable = TRUE'
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, nota_text)
        #     else:
        #         select_sql = self.add_where(1, select_sql, nota_text)
        #     where_count += 1

        # if self.selTactical.get():
        #     tact_text = 'tactical = TRUE'
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, tact_text)
        #     else:
        #         select_sql = self.add_where(1, select_sql, tact_text)
        #     where_count += 1

        # if self.selPlayed.get():

        #     qual_count = self.varCount.get()
        #     tact_text = f'plays {qual_count} '
        #     if where_count == 0:
        #         select_sql = self.add_where(0, select_sql, tact_text)
        #     else:
        #         select_sql = self.add_where(1, select_sql, tact_text)
        #     where_count += 1

        where_statement = self.buildSelectStatement()
        select_sql += where_statement
        select_sql += " order by tag"

        all_data = self.dataconn.execute_select(select_sql)

        if len(all_data) == 0:
            messagebox.showerror("No games found","No games found with the selection entered")
            return

        self.tagList = []
        for dat in all_data:
            
            t, o, w, b, r = dat
            
            self.tagList.append(t)

            g = t.strip() + '(' + self.checkAdvantage(r) + ')' + ' - ' + o.strip() + ' - ' + w.strip() + ' - ' + b.strip()  

            self.gameList.insert(END, g)

        msg = f"There are {len(all_data)} games selected"

        messagebox.showinfo("Games selected", msg)

    def check_options(self):

        option_count = 0
         
        if self.tag.get() != "":
            option_count += 1

        if self.player.get() != "":
            option_count += 1

        if self.opening.get() != "":
            option_count += 1

        if self.variation.get() != "":
            option_count += 1

        if self.selNotable.get():
            option_count += 1

        if self.selTactical.get():
            option_count += 1

        if self.selPlayed.get():
            option_count += 1

        if self.whiteWin.get():
            option_count += 1

        if self.blackWin.get():
            option_count += 1

        if self.drawGame.get():
            option_count += 1

        return option_count

    def buildSelectStatement(self):

        where_statement = ''
        where_count = 0

        if self.tag.get():
            add_text = self.tag.get()
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, f"tag like '{add_text}%'")
                where_count += 1

        if self.opening.get():
            add_text = self.opening.get().capitalize()
            add_text = add_text.replace("'", "''")
            add_opening = f"opening like '%{add_text}%'" 
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, add_opening)
            else:
                where_statement = self.add_where(1, where_statement, add_opening)

            where_count += 1

        if self.player.get():
            add_text = self.player.get().capitalize()
            if add_text.isalnum():
                pass 
            else:
                messagebox.showerror("Error in string","Search string contains special characters. Please remove.")
                return
            
            add_player = f"(white like '%{add_text}%' or black like '%{add_text}%')"
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, add_player)
            else:
                where_statement = self.add_where(1, where_statement, add_player)

            where_count += 1

        if self.drawGame.get() or self.whiteWin.get() or self.blackWin.get():
            res_count = 0
            if self.whiteWin.get():
                if res_count == 0:
                    res_text = "(result = 1"    
                else:
                    res_text += " or result = 1 "
                res_count += 1

            if self.blackWin.get():
                if res_count == 0:
                    res_text = "(result = 2"    
                else:
                    res_text += " or result = 2 "
                res_count += 1

            if self.drawGame.get():
                if res_count == 0:
                    res_text = "(result = 0"
                else:
                    res_text += " or result = 0"
                res_count += 1

            res_text += ")"

            if where_count == 0:
                where_statement = self.add_where(0, where_statement, res_text)
            else:
                where_statement = self.add_where(1, where_statement, res_text)
            where_count += 1

        if self.selNotable.get():
            nota_text = 'notable = TRUE'
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, nota_text)
            else:
                where_statement = self.add_where(1, where_statement, nota_text)
            where_count += 1

        if self.selTactical.get():
            tact_text = 'tactical = TRUE'
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, tact_text)
            else:
                where_statement = self.add_where(1, where_statement, tact_text)
            where_count += 1

        if self.selPlayed.get():

            qual_count = self.varCount.get()
            tact_text = f'plays {qual_count} '
            if where_count == 0:
                where_statement = self.add_where(0, where_statement, tact_text)
            else:
                where_statement = self.add_where(1, where_statement, tact_text)
            where_count += 1

        return where_statement

    def getGameCount(self):
        
        select_sql = "select count(*) from game_details "
        
        return self.dataconn.execute_select(select_sql)

    def add_where(self,mode, sel_sql, add_text):

        if mode == 0:
            sel_sql += "where " + add_text
        else:
            sel_sql += " and " + add_text

        return sel_sql
    
    def checkAdvantage(self, res):

        if res == 0:
            self.advantage.set(0)
            return 'D'
        elif res == 1:
            self.advantage.set(1)
            return 'W'
        else:
            self.advantage.set(0)
            return 'B'
        
    def resetProcess(self):
        ''' reset labels, lists and flags
        '''
        
        res = messagebox.askquestion(title="Reset process?", message="Do you want to reset selections?")

        if res == 'no':
            return

        os.chdir(self.origin)

        self.gameNotable.set(0)
        self.gameTactical.set(0)
        self.whiteWin.set(0)
        self.blackWin.set(0)
        self.drawGame.set(0)

        self.tag.set("")
        self.opening.set("")
        self.player.set("")

        self.gameList.delete(0, END)

        self.processControl(1)

    def exportGames(self):
        
        if self.check_options() == 0:
            game_count = self.getGameCount()[0][0]

            res = messagebox.askquestion(title="Game count", message=f"You will extract {game_count} games. Do you want to continue?")
            if res == 'no':
                return

        select_sql = "select * from game_details "

        where_statement = self.buildSelectStatement()

        select_sql += where_statement 
        select_sql += " order by tag"

        all_data = self.dataconn.execute_select(select_sql)

        data_count = len(all_data)
        if data_count == 0:
            messagebox.showerror("No games found","No games found with the selection entered")
            return

        res = messagebox.askquestion("Reset played count", f"{data_count} rows will be exported. Continue?")

        if res == 'no':
            return

        outfile = 'game_details_' + datetime.now().strftime("%Y-%m-%d") + '.csv'

        f = open(outfile, 'w')

        for d in all_data:

            tag, ope, var, whi, bla, res, com, tac, pla, nta, lpd = d 
            
            if var == None:
                var = ''
            if com == None:
                com = ''
            if tac == True:
                tac = 't'
            else:
                tac = ''
            if nta == True:
                nta = 't'
            else:
                nta = ''

            if lpd == None:
                lpd = ''
            else:
                lpd = lpd.strftime("%Y-%m-%d")
                
            res = str(res)
            pla = str(pla)
            
            line_list = [tag, ope, var, whi, bla, res, com, tac, pla, nta, lpd]
            line = ','.join(line_list)

            f.write(line)
            f.write('\n')

        f.close()
        messagebox.showinfo("Export complete.","Selected games exported successfully")

    def startGame(self):

        if self.gameList.curselection():
            pass
        else: 
            messagebox.showerror("No game selected", "Please select game to play.")
            return 
        
        self.tagSelect.set(self.tagList[self.gameList.curselection()[0]])

        select_sql = f"select white_moves, black_moves from game_moves where tag = '{self.tagSelect.get()}' "

        moves = self.dataconn.execute_select(select_sql)

        self.displayPlayPanel()
        
        self.progress_bar.start()
        
        self.loadGameMoves(moves)
        self.postFirstMove()
        self.processControl(0)

    def displayResetPanel(self):

        self.resetPanel = Toplevel(self.main_container)
        self.resetPanel.title('Reset Counts')

        self.res_a = Separator(self.resetPanel, orient=HORIZONTAL)
        self.res_b = Separator(self.resetPanel, orient=HORIZONTAL)
        self.res_c = Separator(self.resetPanel, orient=HORIZONTAL)

        self.resetMainA = Label(self.resetPanel, text="RESET GAME PLAY COUNT ", style="M.TLabel" )
        self.resetMainB = Label(self.resetPanel, text="Reset game play count of selected games ", style="S.TLabel" )
        self.resetMainC = Label(self.resetPanel, text="to value selected below", style="S.TLabel" )

        self.reset = Button(self.resetPanel, text="RESET", style="B.TButton", command=self.resetGameCount)
        self.exitReset = Button(self.resetPanel, text="EXIT", style="B.TButton", command=self.resetPanel.destroy)

        self.resetLabel = Label(self.resetPanel, text="RESET VALUE : ", style="S.TLabel" )
        self.resetTo = OptionMenu(self.resetPanel, self.resToCount, *self.countList)
        self.resetTo.config(width=5)

        self.resetMainA.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")
        self.resetMainB.grid(row=1, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.resetMainC.grid(row=2, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")

        self.res_a.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.resetLabel.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.resetTo.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="NSEW")

        self.res_b.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.reset.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.exitReset.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky="NSEW")

        ph = 180
        pw = 370

        self.resetPanel.maxsize(pw, ph)
        self.resetPanel.minsize(pw, ph)

        ws = self.resetPanel.winfo_screenwidth()
        hs = self.resetPanel.winfo_screenheight()

        x = (ws/2) - (pw/2) 
        y = (hs/2) - (ph/2)

        self.resetPanel.geometry('%dx%d+%d+%d' % (pw, ph, x, y))

        self.processControl(1)

    def resetGameCount(self):

        ''' This function will check the number of games to reset before updating
            counts
        ''' 

        if self.check_options() == 0:
            messagebox.askquestion(parent=self.resetPanel, title="No options", message=f"No options entered and selected. Set options before resetting.")
            return

        select_sql = "select tag, opening, white, black, result from game_details "

        # where_statement = ''
        # where_count = 0

        # if self.tag.get():
        #     add_text = self.tag.get()
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, f"tag like '{add_text}%'")
        #         where_count += 1

        # if self.opening.get():
        #     add_text = self.opening.get().capitalize()
        #     add_text = add_text.replace("'", "''")
        #     add_opening = f"opening like '%{add_text}%'" 
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, add_opening)
        #     else:
        #         where_statement = self.add_where(1, where_statement, add_opening)

        #     where_count += 1

        # if self.player.get():
        #     add_text = self.player.get().capitalize()
        #     if add_text.isalnum():
        #         pass 
        #     else:
        #         messagebox.showerror("Error in string","Search string contains special characters. Please remove.")
        #         return
            
        #     add_player = f"(white like '%{add_text}%' or black like '%{add_text}%')"
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, add_player)
        #     else:
        #         where_statement = self.add_where(1, where_statement, add_player)

        #     where_count += 1

        # if self.drawGame.get() or self.whiteWin.get() or self.blackWin.get():
        #     res_count = 0
        #     if self.whiteWin.get():
        #         if res_count == 0:
        #             res_text = "(result = 1"    
        #         else:
        #             res_text += " or result = 1 "
        #         res_count += 1

        #     if self.blackWin.get():
        #         if res_count == 0:
        #             res_text = "(result = 2"    
        #         else:
        #             res_text += " or result = 2 "
        #         res_count += 1

        #     if self.drawGame.get():
        #         if res_count == 0:
        #             res_text = "(result = 0"
        #         else:
        #             res_text += " or result = 0"
        #         res_count += 1

        #     res_text += ")"

        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, res_text)
        #     else:
        #         where_statement = self.add_where(1, where_statement, res_text)
        #     where_count += 1

        # if self.selNotable.get():
        #     nota_text = 'notable = TRUE'
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, nota_text)
        #     else:
        #         where_statement = self.add_where(1, where_statement, nota_text)
        #     where_count += 1

        # if self.selTactical.get():
        #     tact_text = 'tactical = TRUE'
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, tact_text)
        #     else:
        #         where_statement = self.add_where(1, where_statement, tact_text)
        #     where_count += 1

        # if self.selPlayed.get():

        #     qual_count = self.varCount.get()
        #     tact_text = f'plays {qual_count} '
        #     if where_count == 0:
        #         where_statement = self.add_where(0, where_statement, tact_text)
        #     else:
        #         where_statement = self.add_where(1, where_statement, tact_text)
        #     where_count += 1

        where_statement = self.buildSelectStatement()
        select_sql += where_statement

        all_data = self.dataconn.execute_select(select_sql)

        row_count = len(all_data)
        if row_count == 0:
            messagebox.showerror(parent=self.resetPanel, title="No games found",message="No games found with the selection entered")
            return

        res = messagebox.askquestion(parent=self.resetPanel, title="Reset played count", message=f"{row_count} rows will be updated. Continue?")

        if res == 'no':
            return

        count = self.resToCount.get()
        update_sql = f"update game_details set plays = {count} "
        update_sql += where_statement

        if self.dataconn.execute_update(update_sql):
            messagebox.showinfo("Update complete.","Updated plays successfully")
        else:
            messagebox.showerror("Update error.","Error updating plays")
    
    def displayPlayPanel(self):

        Style().configure("PS.TLabel", font="Verdana 8", height="50" )
        self.playMoves = Toplevel(self.main_container)
        self.playMoves.title(self.tagSelect.get())

        self.pop_a = Separator(self.playMoves, orient=HORIZONTAL)
        self.pop_b = Separator(self.playMoves, orient=HORIZONTAL)
        self.pop_c = Separator(self.playMoves, orient=HORIZONTAL)
        self.pop_d = Separator(self.playMoves, orient=HORIZONTAL)
        self.pop_e = Separator(self.playMoves, orient=HORIZONTAL)

        self.playPlayers = Label(self.playMoves, text=" ", style="S.TLabel" )
        self.playOpening = Label(self.playMoves, text=" ", style="S.TLabel" )
        self.playVariation = Label(self.playMoves, text=" ", style="S.TLabel" )

        self.whiteFrame = LabelFrame(self.playMoves, text=' WHITE ', style="O.TLabelframe")
        self.whiteMove = Label(self.whiteFrame, text=" ", style="L.TLabel" )
        self.blackFrame = LabelFrame(self.playMoves, text=' BLACK ', style="O.TLabelframe")
        self.blackMove = Label(self.blackFrame, text=" ", style="L.TLabel" )
        
        self.next = Button(self.playMoves, text="NEXT", style="B.TButton", command=self.getNextMove)
        self.prev = Button(self.playMoves, text="PREV", style="B.TButton", command=self.getPrevMove)
        self.info = Button(self.playMoves, text="GAME MOVES AND INFO", style="B.TButton", command=self.displayAllMoves)
        self.restart = Button(self.playMoves, text="RESTART", style="B.TButton", command=self.restartMoves)

        self.progress_bar = Progressbar(self.playMoves, orient="horizontal", mode="indeterminate", maximum=50)

        self.playOpening.configure(font=("Courier New", 10))
        self.playPlayers.configure(font=("Courier New", 10))
        self.playVariation.configure(font=("Courier New", 10))

        self.close = Button(self.playMoves, text="CLOSE", style="B.TButton", command=self.hidePlay)

        self.playPlayers.grid(row=1, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.playOpening.grid(row=2, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.playVariation.grid(row=3, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        
        self.pop_a.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")        

        self.whiteMove.grid(row=0, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.whiteFrame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.blackMove.grid(row=0, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.blackFrame.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky="NSEW")

        self.pop_b.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")        

        self.prev.grid(row=8, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.next.grid(row=8, column=2, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.restart.grid(row=9, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.info.grid(row=9, column=2, columnspan=2, padx=5, pady=0, sticky='NSEW')

        self.pop_c.grid(row=10, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.close.grid(row=11, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.pop_d.grid(row=12, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")
        
        self.progress_bar.grid(row=13, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        
        t = self.tagSelect.get()

        select_sql = f"select opening, variation, white, black from game_details where tag = '{t}'"
        
        dat = self.dataconn.execute_select(select_sql)

        o, v, w, b = dat[0]

        self.playPlayers["text"] = w.strip() + " vs. " + b.strip()
        self.playOpening["text"] = o.strip()
        if v:
            self.playVariation["text"] = v.strip()

        ph = 320
        pw = 580

        self.playMoves.maxsize(pw, ph)
        self.playMoves.minsize(pw, ph)

        ws = self.playMoves.winfo_screenwidth()
        hs = self.playMoves.winfo_screenheight()

        x = (ws/2) - (pw/2) - 200
        y = (hs/2) - (ph/2)

        self.playMoves.geometry('%dx%d+%d+%d' % (pw, ph, x, y))

    def loadGameMoves(self, moves):

        white_moves = moves[0][0]
        black_moves = moves[0][1]

        self.allMoves = []
        count = 0

        while True:

            try:
                if white_moves[count]:
                    self.allMoves.append(white_moves[count].strip())

                if black_moves[count]:
                    self.allMoves.append(black_moves[count].strip())

                count += 1
            except:
                break         

        self.pointer = 0

    def postFirstMove(self):

        move = self.allMoves[self.pointer]
        self.whiteMove["text"] = move
        self.blackMove["text"] = ""

    def getNextMove(self):

        if self.pointer + 1 == len(self.allMoves):
            messagebox.showinfo(parent=self.playMoves, title="Last moves", message="Last moves already displayed.")
            return

        self.pointer += 1

        move = self.allMoves[self.pointer]

        if self.pointer % 2 == 1:
            self.blackMove["text"] = move
        else:
            self.whiteMove["text"] = move
            self.blackMove["text"] = ""

        if self.pointer + 1 == len(self.allMoves):
            self.getAndUpdatePlays()

    def getPrevMove(self):

        if self.pointer == 0:
            messagebox.showinfo(parent=self.playMoves, title="First moves", message="First moves already displayed.")
            return

        self.pointer -= 1

        move = self.allMoves[self.pointer]

        if self.pointer % 2 == 1:
            self.blackMove["text"] = move 

            white = self.allMoves[self.pointer - 1]
            self.whiteMove["text"] = white
        else:
            self.whiteMove["text"] = move
            self.blackMove["text"] = ""

    def displayAllMoves(self):

        Style().configure("PS.TLabel", font="Verdana 8", height="50" )
        self.popMoves = Toplevel(self.main_container)
        self.popMoves.title(self.tagSelect.get())

        self.pop_a = Separator(self.popMoves, orient=HORIZONTAL)
        self.pop_b = Separator(self.popMoves, orient=HORIZONTAL)
        self.pop_c = Separator(self.popMoves, orient=HORIZONTAL)
        self.pop_d = Separator(self.popMoves, orient=HORIZONTAL)
        self.pop_e = Separator(self.popMoves, orient=HORIZONTAL)

        self.descFrame = LabelFrame(self.popMoves, text=' DESCRIPTION ', style="O.TLabelframe")
        self.popDescription = Text(self.descFrame, width="41", height="5" )
        self.popTactical = Checkbutton(self.descFrame, text=" Tactical", style="B.TCheckbutton", variable=self.gameTactical)
        self.popNotable = Checkbutton(self.descFrame, text=" Notable", style="B.TCheckbutton", variable=self.gameNotable)

        self.upddesc = Button(self.popMoves, text="UPDATE", style="B.TButton", command=self.updateDescription)

        self.moveListFrame = LabelFrame(self.popMoves, text=' MOVES LIST ', style="O.TLabelframe")
        self.moveList = Listbox(self.moveListFrame, width=38, height=8)
        self.scroller = Scrollbar(self.moveListFrame, orient=VERTICAL, command=self.moveList.yview)
        self.moveList.config(font=("Courier New", 10), yscrollcommand=self.scroller.set)
        
        self.closeMoves = Button(self.popMoves, text="CLOSE", style="B.TButton", command=self.hideMoves)

        self.popDescription.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")
        self.popTactical.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
        self.popNotable.grid(row=1, column=2, columnspan=2, padx=5, pady=5,sticky="NSEW")

        self.descFrame.grid(row=1, column=0, columnspan=4, padx=5, pady=1, sticky="NSEW")
        self.upddesc.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.pop_a.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")        

        self.moveList.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        self.scroller.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.moveListFrame.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.pop_c.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.closeMoves.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

        self.loadMoveList()

        desc = self.getDescription()
        self.popDescription.insert(INSERT, desc)

        self.gameTactical.set(0)
        if self.getTactical():
            self.gameTactical.set(1)

        self.gameNotable.set(0)
        if self.getNotable():
            self.gameNotable.set(1)
        
        ph = 420
        pw = 360

        self.popMoves.maxsize(pw, ph)
        self.popMoves.minsize(pw, ph)

        ws = self.popMoves.winfo_screenwidth()
        hs = self.popMoves.winfo_screenheight()

        x = (ws/2) - (pw/2) + 300
        y = (hs/2) - (ph/2)

        self.popMoves.geometry('%dx%d+%d+%d' % (pw, ph, x, y))

        self.info["state"] = DISABLED
        self.close["state"] = DISABLED

    def loadMoveList(self):

        self.moveList.delete(0, END)
        count = 1
        idx = 0

        while True:
            
            try:
                w = self.allMoves[idx]

                idx += 1

            except:
                break 

            try:
                b = self.allMoves[idx]

                idx += 1

                self.moveList.insert(END, '{:2d}'.format(count) + '. ' + w.ljust(6) + '  -  ' + b)

                count += 1

            except:
                
                self.moveList.insert(END, '{:2d}'.format(count) + '. ' + w)
                break 

    def getTactical(self):

        select_sql = f"select tactical from game_details where tag = '{self.tagSelect.get()}'"

        desc = self.dataconn.execute_select(select_sql)[0]
     
        if desc[0]:
            return True
        else:
            return False

    def getNotable(self):

        select_sql = f"select notable from game_details where tag = '{self.tagSelect.get()}'"

        desc = self.dataconn.execute_select(select_sql)[0]
     
        if desc[0]:
            return True
        else:
            return False

    def getDescription(self):

        select_sql = f"select comments from game_details where tag = '{self.tagSelect.get()}'"

        desc = self.dataconn.execute_select(select_sql)[0]
     
        if desc[0]:
            return desc[0].strip()
        else:
            return ''
    
    def updateDescription(self):

        comment = self.popDescription.get(1.0, END).strip()
        comment = comment.replace(',', '')

        update_sql = f"update game_details set comments = '{comment}'"

        if self.gameTactical.get():
            update_sql = update_sql + f", tactical = TRUE "
        else:
            update_sql = update_sql + f", tactical = FALSE "

        if self.gameNotable.get():
            update_sql = update_sql + f", notable = TRUE "
        else:
            update_sql = update_sql + f", notable = FALSE "

        update_sql = update_sql + f" where tag = '{self.tagSelect.get()}'"

        if self.dataconn.execute_update(update_sql):
            messagebox.showinfo(parent=self.popMoves, title="Update complete.",message="Updated comment successfully")
        else:
            messagebox.showerror(parent=self.popMoves,title="Update error.",message="Error updating description")

    def getAndUpdatePlays(self):

        curr_date = date.today()

        get_sql = f"select plays, last_play_date from game_details where tag = '{self.tagSelect.get()}'"

        plays = self.dataconn.execute_select(get_sql)[0][0]
        last_play = self.dataconn.execute_select(get_sql)[0][1]

        if last_play != curr_date:

            plays += 1

            update_sql = f"update game_details set plays = {plays}, last_play_date = '{curr_date}' where tag = '{self.tagSelect.get()}'"

            if self.dataconn.execute_update(update_sql):
                pass
            else:
                messagebox.showerror(parent=self.playMoves,title="Update error.",message="Error updating plays count")

    def hidePlay(self):

        self.progress_bar.stop()
        self.processControl(1)
        self.playMoves.destroy()

    def hideMoves(self):

        self.info["state"] = NORMAL
        self.close["state"] = NORMAL
        self.popMoves.destroy()

    def restartMoves(self):

        res = messagebox.askquestion(parent=self.playMoves, title="Restart moves?", message="Do you want to restart game/opening?")

        if res == 'no':
            return

        self.pointer = 0
        self.postFirstMove()

    def processControl(self, mode):
        ''' enable/disable buttons as needed
        '''

        if mode:
            
            self.fetch["state"] = NORMAL
            self.reset["state"] = NORMAL
            self.start["state"] = NORMAL
            self.exit["state"] = NORMAL

        else:

            self.fetch["state"] = DISABLED
            self.reset["state"] = DISABLED
            self.start["state"] = DISABLED
            self.exit["state"] = DISABLED

    def exitApp(self):

        root.destroy()

root = Tk()
root.title("GAMES MOVES")

# Set size

wh = 540
ww = 490

root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
