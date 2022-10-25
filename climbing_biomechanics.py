import numpy as np
import math
import matplotlib.pyplot as plt
import random

class Appendage:

  

  def __init__(self,start, end, current,length,existing_holds,b_type='hand'):
    self.b_type = b_type #body type could be foot or hand 
    self.start=start#starting hold coordinates 
    self.end=end 
    self.current=current 
    self.length=length
    self.existing_holds=existing_holds

  def print_attr(self):

    print("start:{} \nend:{} \ncurrent:{} \nexisting_holds:{}"
                .format(self.start,self.end,self.current, self.existing_holds) )

    return 0
            

  #Returns potential holds based on its length
  def length_constraint(self):

    start=self.current
    end=self.end
    wall=self.existing_holds
    length=self.length


    potential_holds=[]
# issue in if else statement
    for w in wall:

        if  w > start and math.dist(start,w)<=length:  
            
            potential_holds.append(w)

        elif math.dist(start,w)>length and w==wall[-1]:
            break
 

    self.existing_holds=wall #make sure that the object has the latest wall coordinates available

    return potential_holds

  def next_move(self, potential_holds):

    ###!!!###
    # ADD LENGTH_CONSTRAINT() 
        #select random hold from potential holds
    current_hold=random.sample(potential_holds,1)  
            #update current hold of appendage to newly select hold

    self.current=current_hold[0]

            #remove current hold from existing holds
    #self.existing_holds.remove(current_hold[0])
            #turn start hold as current hold
    
    self.start=self.current

    return 0

#supporting def to compare two tuples, false if not equal, true means one value min is equal
def comp_tuple(tuple1,tuple2):
    for a in tuple1:
        for b in tuple2:
            if a==b:
                return True
    return False       

def cross_constraint(lh,rh):

    rhx=list(zip(*rh))[0] #turn right hand tuple coordinates to list of only x coordinates
    lhx=list(zip(*lh))[0] # ^ same for left hand

    #if there are common values check no cross constaint,
    #if no values are the same then no need to check constraint 

    if comp_tuple(lh,rh):  

        validL=[]

        #min(rhx) 
        for i in lhx:
            if i <= min(rhx):
                validL.append(lh[ lhx.index(i)] )
          #Find the index of the array and append the tuple based on the index

        #print(validL)

        validR=[]

    
        for j in rhx:
            if j >= min(rhx):
                validR.append(rh[ rhx.index(j)] )
    else:
        validL=lh
        validR=rh

    return validL,validR


def move(rh,lh):    
    i=0
    while rh.current != rh.end and lh.current !=lh.end:
        i+=1
        print(rh.existing_holds)
        print('right hand length')
        print(rh.length_constraint())
        l,r=cross_constraint(lh=lh.length_constraint(),rh= rh.length_constraint() )

        print('lh{}'.format(i))
        lh.next_move(l)
        lh.print_attr()


        print('rh{}'.format(i))
        rh.next_move(r)
        rh.print_attr()
        
    return 0



 