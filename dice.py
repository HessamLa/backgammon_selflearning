import random
class Die:
  def __init__(self, diecount=2, doublepair=True, min=1, max=6):
    self.__diecount = diecount
    self.__doublepair = True
    self.__min = min
    self.__max = max

  def roll(self, diecount=None, doublepair=None):
    if(diecount is None):
      diecount = self.__diecount
    if(doublepair is None):
      doublepair = self.__doublepair

    v = [random.randint(self.__min, self.__max) for i in range(diecount)]
    if(doublepair is True):
      if(len(set(v)) == 1):#all is equal
        v *= 2
      else:
        v += [0]*len(v)
    return v

    
    
