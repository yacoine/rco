import numpy as np
import math
import matplotlib.pyplot as plt
import random
import time


class Appendage:
  

  def __init__(self,start, end, current,length,existing_holds,b_type='hand'):
    self.b_type = b_type #body type could be foot or hand 
    self.start=start#starting hold coordinates 
    self.end=end 
    self.current=current 
    self.length=length
    self.existing_holds=existing_holds

  def print_attr(self):

    #print("start:{} \nend:{} \ncurrent:{} \nexisting_holds:{}"
                #.format(self.start,self.end,self.current, self.existing_holds) )
    #print("current: {}".format(self.current))
    
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
    if len(potential_holds)==0:
        
        return -1
    else:
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

    try:
        

        rhx=list(zip(*rh))[1] #turn right hand tuple coordinates to list of only x coordinates
        lhx=list(zip(*lh))[1] # ^ same for left hand

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
        #print("validR={}".format(validR))
        #print("validL={}".format(validL))

        return validL,validR

    except IndexError:
        return -1 

    #return validL,validR

#move function that allows rh and lh to move from start to end
#issue is that the current pattern is rh and lh
#in future it would need to be random forest with ability for hands to not be sequential
def move(rh,lh):
    plot=[]
   
    hand_naming=[]    
    i=0
    while rh.current != rh.end and lh.current !=lh.end:
        i+=1 #for printing number of moves

        # checking length constraint and cross constraint
        # return of left hand (l) potential holds and right hand (r) 
        if cross_constraint(lh=lh.length_constraint(),rh= rh.length_constraint() ) ==-1:
           break
        else:
           l,r=cross_constraint(lh=lh.length_constraint(),rh= rh.length_constraint() )

        #print('lh{}'.format(i))
        hand_naming.append('left ✋{}'.format(i))
        plot.append(lh.current)
        #checking the hand to hand distance of potential holds
        #fixed versus dynamic hand, in this case LEFT hand is dynamic
        l=h2h_length_constraint(rh,lh,l)
        lh.next_move(l)
        lh.print_attr()
        
        #checking the hand to hand distance of potential holds
        #fixed versus dynamic hand, in this case RIGHT hand is dynamic
        r=h2h_length_constraint(lh,rh,r) 
        plot.append(rh.current)
        #print('rh{}'.format(i))
        hand_naming.append('right ✋{}'.format(i))
        rh.next_move(r)
        rh.print_attr()

def movex(rh,lh,lf, rf):
    
    plot=[]
   
    hand_naming=[]    
    i=0
    while rh.current != rh.end or lh.current !=lh.end:
        i+=1 #for printing number of moves

        # checking length constraint and cross constraint
        # return of left hand (l) potential holds and right hand (r)
        if cross_constraint(lh=lh.length_constraint(),rh= rh.length_constraint() ) ==-1:
           break
        else:
           l,r=cross_constraint(lh=lh.length_constraint(),rh= rh.length_constraint() )

        #print('lh{}'.format(i))
        hand_naming.append('LH{}'.format(i))
        plot.append(lh.current)
        #checking the hand to hand distance of potential holds
        #fixed versus dynamic hand, in this case LEFT hand is dynamic
        l=h2h_length_constraint(rh,lh,l)
        lh.next_move(l)
        lh.print_attr()
        
        #checking the hand to hand distance of potential holds
        #fixed versus dynamic hand, in this case RIGHT hand is dynamic
        r=h2h_length_constraint(lh,rh,r) 
        plot.append(rh.current)
        #print('rh{}'.format(i))
        hand_naming.append('RH{}'.format(i))
        rh.next_move(r)
        rh.print_attr()

        #constraints for feet, length and crossing
        l_foot,r_foot=cross_constraint(lf.length_constraint(),rf.length_constraint())
        #move left foot
        plot.append(lf.current)
        left_foot=leg_hand_constraint(lh,l_foot)
        
        #adding cross constraint to right foot and left foot
        
        lf.next_move(left_foot)
        #print('lf{}'.format(i))
        hand_naming.append('LF{}'.format(i))
        lf.print_attr()
        

        #move right foot
        plot.append(rf.current)
        right_foot=leg_hand_constraint(rh,r_foot)
        rf.next_move(right_foot)
        #print('rf{}'.format(i))
        hand_naming.append('RF{}'.format(i))
        rf.print_attr()        
        
    return plot,hand_naming

def h2h_length_constraint(fix_hand,dynamic_hand, dynamic_holds):
    
    #potential holds available to dynamic hand
    wall=dynamic_holds
    #hand to compare with
    fix=fix_hand.current

    #hand to move
    dynamic=dynamic_hand.current

    #potential holds
    potential_holds=[]

    for w in wall:
        if math.dist(fix,w)<= (fix_hand.length+dynamic_hand.length):
            #print(math.dist(hand_fix,w))
            potential_holds.append(w)

    return potential_holds

def leg_hand_constraint(hand,existing_holds):
    
    hand_current=hand.current

    potential_holds=[]
    wall=existing_holds

    for w in wall:
        if w[0] < hand_current[0]:
            potential_holds.append(wall[ wall.index(w)] )
            
    return potential_holds

#find the quickest path to the top of the wall
#right the order of hand and foot movement is:
# right hand, left hand, right foot, left foot, right foot
#and this will change to find best optimal combination
def find_min(rh,lh,rf,lf,wall,n=100):
    path_examples={}
    hand_foot_order=[]

    
    rh_start,rh_end,rh_length,rh_wall=rh.start,rh.end,rh.length,rh.existing_holds
    lh_start,lh_end,lh_length,lh_wall=lh.start,lh.end,lh.length,lh.existing_holds
    rf_start,rf_end,rf_length,rf_wall=rf.start,rf.end,rf.length,rf.existing_holds
    lf_start,lf_end,lf_length,lf_wall=lf.start,lf.end,lf.length,lf.existing_holds

    
    for x in range(n):

        r_hand=Appendage(start=rh_start,end=rh_end,current=rh_start,length=rh_length,existing_holds=wall)
        l_hand=Appendage(start=lh_start,end=lh_end,current=lh_start,length=lh_length,existing_holds=wall)
        r_foot=Appendage(start=rf_start,end=rf_end,current=rf_start,length=rf_length,existing_holds=wall)
        l_foot=Appendage(start=lf_start,end=lf_end,current=lf_start,length=lf_length,existing_holds=wall)

        
        plot,name=movex(r_hand,l_hand,l_foot,r_foot)
        hand_foot_order.append(name)
        if len(plot) in path_examples:
            path_examples[len(plot)].append(plot)
        else:
            path_examples[len(plot)]= [plot]
            #making sure that tuple is in array format

    
    min_path=min(path_examples)
        
    return min_path,path_examples[min_path],hand_foot_order
