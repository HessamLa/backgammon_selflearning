class BGBoard:
  maxposition = 27
  minposition = 0
  wchip =  1 # white chips are positive values
  bchip = -1 # black chips are negative values
  wjail = 0
  bjail = 25
  wend = 26
  bend = 27
  wstart_quarter = [i for i in range( 1, 7)] # 1- 6
  bstart_quarter = [i for i in range(19,25)] #19-24
  # white bear off quarter is 19-24 and 26
  wend_quarter = bstart_quarter+[wend]
  # black bear off quarter is 6-1 and 27
  bend_quarter = wstart_quarter+[bend]

  errormessage = {
    0:"no error",
    1:"wrong move or nothing to move",
    2:"there is still a chip in the jail",
    3:"The move cannot be backwards (must be increasing for white)",
    4:"from jail you can only move to the starting quarter",
    5:"if moving to the end slot, all other chips must be in this quarter",
    6:"the destination is blocked"
  }

  def __init__(self):
    self.__board = [0]*28
    self.__config = {1:2, 6:-5, 8:-3, 12:5, 13:-5, 17:3, 19:5, 24:-2}
    self.resetboard()
    
  @property
  def board(self):
    return self.__board
  
  def resetboard(self, config=None):
    print("Reset board")
    if(config is None):
      config = self.__config
    elif(type(config) is not dict):
      print("config must be a dict. Like the following")
      print(self.__config)
      return

    for k in config.keys():
      self.__board [k] = config[k]
  def verifyconfig(self, config):
    if(max(config.keys()) > BGBoard.maxposition or min(config.keys()) < BGBoard.minposition):
      return False
    if(sum (config.values()) != 0):
      return False
    a = [i for i in config.values() if i > 0]
    if(sum(a) != 15):
      return False
    return True
  def makemove(self, color, src, dst):
    """move a chip from src to dst. color=0 for white and color=1 for black.
    befor calling this, verify the move"""
    bchip = BGBoard.bchip
    wchip = BGBoard.wchip
    if (color == 0): # white move
      if(self.__board[dst] == bchip): # move the black chip to jail
        self.__board[dst] = 0
        self.__board[BGBoard.bjail] += bchip
      self.__board[src] -= wchip      # remove the white chip from source
      self.__board[dst] += wchip      # place the white chip to destination
    elif (color == 1): #black move
      # do the black move
      if(self.__board[dst] == wchip): # move the white chip to jail
        self.__board[dst] = 0
        self.board[BGBoard.wjail] += wchip
      self.__board[src] -= bchip      # remove the black chip from source
      self.__board[dst] += bchip      # place the black chip in destination
    else:
      print(color, "is not accepted. color must be 0(white) or 1(black)")    

  def verifymove_white(self, src, dst):
    """verify a white move (positive)"""
    wend = BGBoard.wend# use shorter names
    wj = BGBoard.wjail
    weq = BGBoard.wend_quarter
    bchip = BGBoard.bchip
    wchip = BGBoard.wchip
    moveflag = 0
    if(self.__board[src]<=0): # wrong move or nothing to move
      moveflag = 1
    elif(self.__board[wj]>0 and wj != src): #there is still something in the jail
      moveflag = 2
    elif(src>=dst): # The move cannot be backwards (must be increasing for white)
      moveflag = 3
    elif(src == wj and dst not in BGBoard.wstart_quarter): #from jail you can only move to the starting quarter
      moveflag = 4
    elif(dst == wend): # if breaing off, all chips must be in last quarter
      t = {k:self.__board[k] for k in weq}
      if(sum(t.values())!= 15):
        moveflag = 5
    elif(self.__board[dst] < bchip): # the destination is blocked
      moveflag = 6
    return moveflag

  def verifymove_black(self, src, dst):
    """verify a black move (negative)"""
    bend = BGBoard.bend# use shorter names
    bj = BGBoard.bjail
    beq = BGBoard.bend_quarter
    bchip = BGBoard.bchip
    wchip = BGBoard.wchip
    moveflag = 0
    
    if(self.__board[src]>=0): # wrong move or nothing to move
      moveflag = 1
    elif(self.__board[bj]<0 and bj != src): #there is still something in the jail
      moveflag = 2
    elif(src<=dst): # The move cannot be backwards (must be decreasing for black)
      moveflag = 3
    elif(src == bj and dst not in BGBoard.bstart_quarter): #from jail you can only move to the starting quarter
      moveflag = 4
    elif(dst==bend): # if breaing off, all chips must be in last quarter
      t = {k:self.__board[k] for k in beq}
      if(sum(t.values())!= 15):
        moveflag = 5
    elif(self.__board[dst]>wchip): # the destination is blocked
      moveflag = 6
    return moveflag

  def runmoves(self, moves, show=True):
    bwname =["white", "black"]
    verifymove = [self.verifymove_white, self.verifymove_black]
    for color, src, dst in moves:
      r = verifymove[color](src, dst)
      print(bwname[color], f"{src:2d} -> {dst:2d}", BGBoard.errormessage[r])
      if(r == 0):
        self.makemove(color, src, dst)
        if(show==True):
          self.showboard()

  def assessmoves(self, moves):
    """move is a list of tuples (color, source, destination).
    """
    result=[]
    for (color, src, dst) in moves:
      if(color == 0):
        r = self.verifymove_white(src, dst)
        result.append( ("white", src, dst, BGBoard.errormessage[r]))
      elif(color == 1):
        r = self.verifymove_black(src, dst)
        result.append( ("black", src, dst, BGBoard.errormessage[r]))
      else:
        result.append( (color, src, dst, "unknown color turn"))
    return 
    
  def verifymoves(self, moves):
    """returns true if all moves are legit"""
    for (color, src, dst) in moves:
      if(color == 0):
        if (self.verifymove_white(src, dst) != 0):
          return False
      elif(color == 1):
        if (self.verifymove_black(src, dst) != 0):
          return False
    return True

  def showboard(self):
    from scoring_utilities import BGScore
    # show the upper slot numbers
    s = ""
    for i in range(1,7):
      s = f"{i:2d} "+s
    s = " | "+s
    for i in range(7,13):
      s = f"{i:2d} "+s
    s = " "+s
    print(s)
    
    horiz = "+"+"---"*6+"-+"+"---"*6+"-+"
    print(horiz)
    print("|", end="")#v line
    
    for i in range(12,6, -1):
      if (self.__board[i] == 0):
        print(f" . ",end="")
      else:
        print(f"{self.__board[i]:2d} ",end="")
    print(" | ",end="")
    for i in range(6,0,-1):
      if (self.__board[i] == 0):
        print(f" . ",end="")
      else:
        print(f"{self.__board[i]:2d} ",end="")
    print("|")

    midhor = "|"+"   "*6+" |"+"   "*6+" |"
    print(midhor, end="")
    print(f" White lone: {BGScore.lone_wscore(None, self.board):.2f}")
    print("|"+"   "*6+f"{self.__board[BGBoard.wjail]:2d}"+"   "*6+" |", end="")
    print(f" White score: {BGScore.white_score(None, self.board):.2f}")
    print("|"+"   "*6+f"{self.__board[BGBoard.bjail]:2d}"+"   "*6+" |", end="")
    print(f" Black score: {BGScore.black_score(None, self.board):.2f}")
    print(midhor, end="")
    print(f" Black lone: {BGScore.lone_bscore(None, self.board):.2f}")
    
    print("|", end="")#v line
    for i in range(13,19):
      if (self.__board[i] == 0):
        print(f" . ",end="")
      else:
        print(f"{self.__board[i]:2d} ",end="")
    print(" | ",end="")
    for i in range(19,25):
      if (self.__board[i] == 0):
        print(f" . ",end="")
      else:
        print(f"{self.__board[i]:2d} ",end="")
    
    print("|")
    print(horiz)
    # show the lower slot numbers
    s = " "
    for i in range(13,19):
      s += f"{i:2d} "
    s += " | "
    for i in range(19,25):
      s += f"{i:2d} "
    print(s)


if __name__ == "__main__":
    bg = BGBoard()
    bg.showboard()
    
    wturn = 0
    bturn = 1
    wjail = BGBoard.wjail
    bjail = BGBoard.bjail
    wend = BGBoard.wend
    bend = BGBoard.bend

    bwname =["white", "black"]

#  12 11 10  9  8  7  |  6  5  4  3  2  1
# +-------------------+-------------------+
# | 5  .  .  . -3  .  | -5  .  .  .  .  2 |
# |                   |                   |
# |                   0                   |
# |                   0                   |
# |                   |                   |
# |-5  .  .  .  3  .  |  5  .  .  .  . -2 |
# +-------------------+-------------------+
#  13 14 15 16 17 18  | 19 20 21 22 23 24
    moves = [(bturn, 6,5), (bturn, 7,5)]
    bg.runmoves(moves)
    bg.runmoves([(wturn, 1,4),(wturn, 1,5)])
    bg.runmoves([(bturn, bjail,24),(bturn, 6,5),(bturn, 6,4),(bturn, 24,22)])
    bg.runmoves([(wturn, wjail,4),(wturn, 4,5)])
    bg.runmoves([(wturn, 5,6),(wturn, 1,5)])
    bg.runmoves([(bturn, 24,23)])
    bg.runmoves([(wturn, wjail,5), (wturn, 5,7)])
    
    # for turn, src, dst in moves:
    #   r = bwverify[turn](src, dst)
    #   print(bwname[turn], f"{src:2d} -> {dst:2d}", BGBoard.errormessage[r])
    #   if(r == 0):
    #     bg.makemove(turn, src, dst)
    #     bg.showboard()
    
    # moves = [(wturn, 6,5), (wturn, 7,5)]
    # for turn, src, dst in moves:
    #   r = bwverify[turn](src, dst)
    #   print(bwname[turn], f"{src:2d} -> {dst:2d}", BGBoard.errormessage[r])
    #   if(r == 0):
    #     bg.makemove(turn, src, dst)
    #     bg.showboard()
    
    # moves = [(wturn, 6,5), (wturn, 7,5)]
    # for turn, src, dst in moves:
    #   r = bwverify[turn](src, dst)
    #   print(bwname[turn], f"{src:2d} -> {dst:2d}", BGBoard.errormessage[r])
    #   if(r == 0):
    #     bg.makemove(turn, src, dst)
    #     bg.showboard()
    
    # moves = [(24,23), (6,7)]
    # bg.makemove(moves)
    # bg.showboard()
    
    # moves = [(1,3), (19,23), (19,20)]
    # bg.makemove(moves)
    # bg.showboard()

    # moves = [(3,5), (24,23)]
    # bg.makemove(moves)
    # print(24, bg.board[24])
    # print(23, bg.board[23])
    # bg.showboard()