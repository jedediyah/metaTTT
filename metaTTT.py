import Tkinter as tk
import math as math

class MetaTTT: 
    
    # Called once when first created
    def __init__(self):
        self.window_width = 800     # Window properties
        self.window_height = 800
        self.Board = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]] # 1=X, -1=O
        # For each board, 8 types of wins: 
        # 0 = no win, 1,2,3 = rows, 4,5,6 = columns, 7 = top left to bottom diagonal, 8 = other diagonal
        self.wins = [0,0,0,0,0,0,0,0,0] 
        self.turn = 1
        self.activeBoard = -1
        
    
    # Draw the scene
    def drawBoard(self):
        # Clear canvas
        self.w.delete("all")
        
        # Draw box
        self.w.create_rectangle(0,0,self.window_width,self.window_height,fill="gray20")
        for brow in range(3):
            for bcol in range(3):
                ybase = float(brow)*(self.window_width/3.0)
                yend = (float(brow)+1.0)*(self.window_width/3.0)
                xbase = float(bcol)*(self.window_height/3.0)
                xend = (float(bcol)+1)*(self.window_height/3.0)
                # Individual board background
                if 3*brow + bcol == self.activeBoard:
                    self.w.create_rectangle(xbase+3,ybase+3,xend-3,yend-3,fill="gray90")
                else:
                    self.w.create_rectangle(xbase+3,ybase+3,xend-3,yend-3,fill="gray80")
                # Draw a TTT board 
                # Horiztonal lines
                line_offset = 15
                self.w.create_line(xbase+line_offset,ybase+self.window_height/9.0,xend-line_offset,ybase+self.window_height/9.0)
                self.w.create_line(xbase+line_offset,ybase+2.0*self.window_height/9.0,xend-line_offset,ybase+2.0*self.window_height/9.0)
                # Vertical lines
                self.w.create_line(xbase+self.window_width/9.0,ybase+line_offset,xbase+self.window_height/9.0,yend-line_offset)
                self.w.create_line(xbase+2.0*self.window_width/9.0,ybase+line_offset,xbase+2.0*self.window_height/9.0,yend-line_offset)
                       
                # Draw moves
                dx = self.window_width/9.0
                dy = self.window_width/9.0
                dm = 20
                for row in range(3):
                    for col in range(3):
                        if self.Board[3*brow+bcol][3*row+col] == -1:    # Draw Os
                            self.w.create_oval(xbase+col*dx+dm, ybase+row*dy+dm, xend-(2-col)*dx-dm, yend-(2-row)*dy-dm, width=3) 
                        elif self.Board[3*brow+bcol][3*row+col] == 1:   # Draw Xs
                            self.w.create_line(xbase+col*dx+dm, ybase+row*dy+dm, xend-(2-col)*dx-dm, yend-(2-row)*dy-dm, width=3)
                            self.w.create_line(xbase+col*dx+dm, yend-(2-row)*dy-dm, xend-(2-col)*dx-dm, ybase+row*dy+dm, width=3)
                # Draw wins
                line_offset = 25
                if self.wins[3*brow+bcol] != 0:
                    win_code = math.copysign( (self.wins[3*brow+bcol]), 1 )
                    if win_code <= 3:
                        self.w.create_line(xbase+line_offset, ybase+(2*win_code-1)*self.window_height/18.0, xend-line_offset, ybase+(2*win_code-1)*self.window_height/18.0, width=3, fill="red")
                    elif win_code <= 6:
                        self.w.create_line(xbase+(2*(win_code-3)-1)*self.window_width/18.0, ybase+line_offset, xbase+(2*(win_code-3)-1)*self.window_height/18.0, yend-line_offset, width=3, fill="red")
                    elif win_code == 7: 
                        self.w.create_line(xbase+line_offset, ybase+self.window_height/18.0, xend-line_offset, ybase+5*self.window_height/18.0, width=3, fill="red")
                    elif win_code == 8:
                        self.w.create_line(xbase+line_offset, ybase+5*self.window_height/18.0, xend-line_offset, ybase+self.window_height/18.0, width=3, fill="red")
                        
                    
    # Mouse event handler
    def mousePressed(self,event):
        x = event.x
        y = event.y
        
        # Identify board clicked 
        if x < self.window_width/3.0:
            board = 0
        elif x < 2.0*self.window_width/3.0:
            board = 1
        else:
            board = 2
        if y < self.window_height/3.0: 
            pass
        elif y < 2.0*self.window_height/3.0:
            board += 3
        else:
            board += 6
            
        # Identify cell clicked
        x2 = x % (self.window_width/3.0)
        y2 = y % (self.window_height/3.0)
        if x2 < self.window_width/9.0:
            cell = 0 
        elif x2 < 2.0*self.window_width/9.0:
            cell = 1
        else:
            cell = 2
        if y2 < self.window_height/9.0:
            pass
        elif y2 < 2.0*self.window_height/9.0:
            cell += 3
        else:
            cell += 6
            
        # Check if valid move
        if self.activeBoard == board or self.activeBoard < 0:
            # Place piece
            self.Board[board][cell] = self.turn
            self.turn *= -1
            # Set next board active
            if 0 in self.Board[board]:
                self.activeBoard = cell
            else:
                self.activeBoard = -1 
            # Check for board win
            self.checkForBoardWin(board)
            # Check for overall win 
            # Redraw board
            self.drawBoard()
            
            
    # Check a single board for a win
    def checkForBoardWin(self,board_index):
        # For each board, 8 types of wins: 
        # 0 = no win, 1,2,3 = rows, 4,5,6 = columns, 7 = top left to bottom diagonal, 8 = other diagonal
        # Positive numbers represent X win, negative represent O win
        if self.wins[board_index] != 0:
            return
        board = self.Board[board_index]
        # Row wins
        for row in range(3):                                
            if board[3*row] != 0 and board[3*row] == board[3*row+1] and board[3*row+1] == board[3*row+2]:
                self.wins[board_index] = math.copysign(row+1,board[3*row])
                print self.wins
                return
        # Column wins 
        for col in range(3):                                
            if board[col] != 0 and board[col] == board[col+3] and board[col+3] == board[col+6]:
                self.wins[board_index] = math.copysign(col+4,board[col])
                return
        # Diagonal wins
        if board[0] != 0 and board[0] == board[4] and board[4] == board[8]:
            self.wins[board_index] = math.copysign(7,board[0])
            return
        if board[2] != 0 and board[2] == board[4] and board[4] == board[6]:
            self.wins[board_index] = math.copysign(8,board[2])
                
    # Check for meta win
    #def checkForMetaWin(self):
        
        
    # Run the simulation
    def run(self):
        self.master = tk.Tk()
        self.master.wm_title("Meta TTT")
        self.w = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.w.pack()
        self.w.bind("<Button-1>", self.mousePressed)
        self.w.after(0,self.drawBoard)   
        tk.mainloop()
        
game = MetaTTT()
game.run()
        


