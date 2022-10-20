import numpy as np
import math
import matplotlib.pyplot as plt

class Appendage:

  def __init__(self,start, end, current,length,existing_holds,b_type='hand'):
    self.b_type = b_type #body type could be foot or hand 
    self.start=start#starting hold coordinates 
    self.end=end 
    self.current=current 
    self.length=length
    self.existing_holds=existing_holds

  #Returns potential holds based on its length
  def length_constraint(self):

    start=self.current
    end=self.end
    wall=self.existing_holds
    length=self.length

    potential_holds=[]

    for w in wall:
        if  w > start and math.dist(start,w)<=length:
            #print(w,'POTENTIAL HOLD'.format(w))
            potential_holds.append(w)
            #{action}
            #time.sleep(0.5) 
        elif math.dist(start,w)>length and w==wall[-1] :
            break
        else:
            wall.pop(0) #remove previous hold from potential holds
        

    self.existing_holds=wall #make sure that the object has the latest wall coordinates available

    return wall+potential_holds

  def cross_constraint(rh,lh):
    pass



start=(199.48, 358.29) #change to current hold and pop previous node
end=(303.71, 502.35)
wall = [(6.6, 414.4), (86.84, 364.68), (199.48, 358.29), (262.61, 519.3), (303.71, 502.35), (305.0, 301.83), (370.83, 424.47), (438.82, 326.27), (485.72, 500.79), (615.33, 449.24), (645.94, 465.55), (646.93, 525.24), (675.85, 452.34), (796.38, 224.31), (815.16, 455.12), (902.74, 453.68), (962.45, 274.77), (1006.76, 274.98), (1059.12, 562.71), (1143.13, 419.56), (1177.59, 657.45), (1236.67, 196.72), (1274.25, 736.07), (1330.17, 190.39)]


rh=Appendage(start=start,end=end,current=start,length=250,existing_holds=wall)
lh=Appendage(start=start,end=end,current=start,length=250,existing_holds=wall)

rh.length_constraint()

print(rh.existing_holds)


