from bgboard import BGBoard

class BGScore:
  def __init__(self):
    pass

  def white_score(self, board, denom=375):
    wchip = 1
    slots_1_24_wend = [i for i in range(1,25)] + [BGBoard.wend]
    t = [board[k]*k for k in slots_1_24_wend if board[k] >= wchip]
    return sum(t)/denom
  
  def black_score(self, board, denom=375):
    bchip = -1
    slots_1_24_bend = [i for i in range(1,25)] + [BGBoard.bend]
    t = [-board[k]*(25-k) for k in slots_1_24_bend if board[k] <= bchip]
    return sum(t)/denom

  def lone_wscore(self, board, denom=129): # score for lone chips
    wchip = 1
    slots_7_24_white = [i for i in range(7,25)]
    t = [k*2 for k in slots_7_24_white if board[k] == wchip]
    return sum(t)/denom

  def lone_bscore(self, board, denom=129):
    bchip = -1
    slots_1_18_black = [i for i in range(1,19)]
    t = [(25-k)*2 for k in slots_1_18_black if board[k] == bchip]
    return sum(t)/denom