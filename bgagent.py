from bgboard import BGBoard
from scoring_utilities import BGScore

class BackgammonAgent:
  def __init__(self, color):
    if(color.lower() == 'white'):
      self.__color = 0
    elif(color.lower() == 'black'):
      self.__color = 1
    self.__decisionmodel = None # this model makes decisions
    self.__evalmodel = None # this model will be fit to make better evaluations
    self.MakeDecisionModel()
    self.MakeEvalModel()
    self.__preveval = None # previous evaluation

  def MakeDecisionModel(self, model=None):
    if(model is not None):
      self.__decisionmodel = model
      return
    # make the model

  def MakeEvalModel(self, model=None):
    if(model is not None):
      self.__evalmodel = model
      return
    # make the model

  def TrainModel(self, *params):
    """ train model according to the parameters"""
    # fit the model
    pass

  def Action(self, board, dice):
    """ dice is a list of 4 values. If it's a pair, the value is repeated 4 times.
    Otherwise, the last 2 values are zero.
    white player gets positive values. Black gets negative values.
    The function returns 2 or 4 tuples of (src,dst) values."""
    pass

  

  def EvaluateBoard(self, board):
    wscore = self.get_white_score(board)
    bscore = self.get_black_score(board)

    if(self.__color == 0): # this is a white player
      return 2*wscore


  

  