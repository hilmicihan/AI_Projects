import copy
import sys
import random
def takeinput():
   with open(sys.argv[1], 'r') as fp:
    line1 = fp.readline() #firts line show which algorithms work
    theta=0 #termination condition factor
    discountfactor=0
    obsset=[]
    pitfalset=[]

    if line1=='V\n':
        line2=fp.readline()
        theta=float(line2.replace("\n",""))
        discountfactor=float(fp.readline().replace("\n",""))
        line = fp.readline().replace("\n", "")
        delim = line.find(" ")
        dimx = int(line[0:delim])
        dimy = int(line[delim:])
        numobstacles=int(fp.readline().replace("\n",""))
        for i in range(0,numobstacles):
            line = fp.readline().replace("\n","")
            delim = line.find(" ")
            x = int(line[0:delim])
            y = int(line[delim:])
            obsset.append((x,y))
        numpitfall = int(fp.readline().replace("\n", ""))
        for i in range(0, numpitfall):
            line = fp.readline().replace("\n","")
            delim=line.find(" ")
            x = int(line[0:delim])
            y = int(line[delim:])
            pitfalset.append((x, y))
        line = fp.readline().replace("\n", "")
        delim = line.find(" ")
        x = int(line[0:delim])
        y = int(line[delim:])
        goalset=(x,y)
        line = fp.readline().replace("\n", "")
        line=line.split(" ")
        r_d,r_o,r_p,r_g=float(line[0]), float(line[1]),float(line[2]),float(line[3])# rewards of regular step , hitting an obstacle/wall ,getting damaged by pitfall , reaching the goal respectively
        mdp=Node(obsset,pitfalset,goalset, r_d,r_o,r_p,r_g,theta,discountfactor,dimx,dimy,"V")
        U= valueiter(mdp, theta, discountfactor)
        way=findtheway(mdp,U)
        out = findoutput(way, mdp)  # printing output
        with open(sys.argv[2], 'w') as outF:
            for i in range(1, mdp.dimx + 1):
                for j in range(1, mdp.dimy + 1):
                    if (i, j) in out and out[i, j] != None:
                        text = str(i) + " " + str(j) + " " + str(out[(i, j)]) + "\n"
                        outF.write(text)
                    else:
                        text = str(i) + " " + str(j) + " " + "0" + "\n"
                        outF.write(text)
        outF.close()
    elif line1=='Q\n':
        line2 = fp.readline()
        numberofepisode = int(line2.replace("\n", ""))
        line2 = fp.readline()
        learningrate = float(line2.replace("\n", "")) #learning rate 0.1
        line2 = fp.readline()
        discountfactor = float(line2.replace("\n", ""))  # discountfactor 0.9
        line2 = fp.readline()
        egreedyparam = float(line2.replace("\n", ""))  #parameter for e greedy approach
        line = fp.readline().replace("\n", "")
        delim = line.find(" ")
        dimx = int(line[0:delim])
        dimy = int(line[delim:])
        numobstacles = int(fp.readline().replace("\n", ""))
        obsset= []
        for i in range(0,numobstacles):
            line = fp.readline().replace("\n","")
            delim = line.find(" ")
            x = int(line[0:delim])
            y = int(line[delim:])
            obsset.append((x,y))
            pitfalset=[]
        numpitfall = int(fp.readline().replace("\n", ""))
        for i in range(0, numpitfall):
            line = fp.readline().replace("\n", "")
            delim = line.find(" ")
            x = int(line[0:delim])
            y = int(line[delim:])
            pitfalset.append((x, y))
        line = fp.readline().replace("\n", "")
        delim = line.find(" ")
        x = int(line[0:delim])
        y = int(line[delim:])
        goalset = (x, y)
        line = fp.readline().replace("\n", "")
        line = line.split(" ")
        r_d, r_o, r_p, r_g = float(line[0]), float(line[1]), float(line[2]), float(line[3])  # rewards
        mdp = Node(obsset, pitfalset, goalset, r_d, r_o, r_p, r_g, theta, discountfactor, dimx, dimy,"Q",learningrate,egreedyparam)
        #print random.uniform(0, 1)
        #print mdp.ramdomstates
        #print mdp.reward((2,6))
        U =  Qlearning(mdp,numberofepisode)
        way = findtheway2(mdp, U)
        initial = (1, 1)
        out= findoutput(way, mdp)  # printing output
        with open(sys.argv[2], 'w') as outF:
            for i in range(1, mdp.dimx + 1):
                for j in range(1, mdp.dimy + 1):
                    if (i,j) in out and out[i,j]!=None:
                        text=str(i) +" "+str(j)+" " +str(out[(i,j)])+"\n"
                        outF.write(text)
                    else:
                        text = str(i) + " " + str(j) + " " + "0"+"\n"
                        outF.write(text)
            outF.close()
def findoutput(way,mdp):
    policy=dict()
    for initial in mdp.validstates:
        newstate=way[initial]
        dir=direction(initial,newstate)
        new=[initial,dir]
        policy[new[0]]=new[1]
    return policy

class Node:
    def __init__(self,obsset,pitfallset,goalset, r_d,r_o,r_p,r_g,theta,discountfactor,dimx,dimy,type,learningrate=0,egreedyparam=0):
        self.type=type
        self.learningrate=learningrate
        self.egreedyparam=egreedyparam
        self.obsset=obsset
        self.pitfallset=pitfallset
        self.goalset=goalset
        self.r_d=r_d #regular step reward
        self.r_o=r_o #obstacle or wall reward
        self.r_p=r_p    #getting damaged by pitfal reward
        self.r_g=r_g    #reaching goal reward
        self.theta=theta
        self.discountfactor=discountfactor
        self.dimx=dimx
        self.dimy=dimy
        self.grid = self.makegrid(dimx, dimy)
        self.validstates=self.makevalidstates()

        self.randomstates=self.makerandomstate()
        self.allstates=self.makeallstates()
    def makevalidstates(self): #obsset are not reachable so we cannot go there they are not valid so allstates-obssets
        list = []
        for i in range(1, self.dimx + 1):
            for j in range(1, self.dimy + 1):
                if (i,j) not in (self.obsset):
                    list.append((i, j))
        return list
    def makeallstates(self):
        list = []
        for i in range(1, self.dimx + 1):
            for j in range(1, self.dimy + 1):
                    list.append((i, j))
        return list
    def makerandomstate(self):
        list = []
        for i in range(1, self.dimx + 1):
            for j in range(1, self.dimy + 1):
                if (i, j) not in (self.obsset) and (i,j) != self.goalset and (i,j) not in self.pitfallset:
                    list.append((i, j))
        return list

    def actionlist(self,state): # return every valid actions
        if state == self.goalset: #or state in  self.pitfallset:
            return [(-1,-1)]
        else:
            return self.actions(state)
        

    def printvalidstates(self):
        for i in self.validstates:
            print i
    def makegrid(self,dimx,dimy): #its compose grid according to reverse order
        list=[]
        for i in range(1,dimy+1):
            list1=[]
            for j in range(1,dimx+1):
                list1.append((j,i))
            list.insert(0,list1)
        return list
    def reward(self,state):


        if state in self.pitfallset:
                    return self.r_p
        elif state in self.obsset or not state in self.validstates:
                    return self.r_o
        elif state == self.goalset:
                    return self.r_g
        else:#otherwise it is a regular step return regular reward
                    return self.r_d
    def printgrid(self):
        for i in self.grid:
            print i
    def isactionpossible(self,state):
        if (state[0] in range(1,self.dimx+1) and state[1]in range(1,self.dimy+1))==False:
            return False
        if state in self.obsset:
            return False
        return True
    #def go_up(self,state):
    def actions(self,state):
        up=(state[0],state[1]+1)
        down = (state[0], state[1] - 1)
        right=(state[0]+1, state[1])
        left = (state[0] -1, state[1])
        list=[]
        if up in self.validstates:
            list.append(up)
        if down in self.validstates:
            list.append(down)
        if right in self.validstates:
            list.append(right)
        if left in self.validstates:
            list.append(left)
        return list

def valueiter(mdp,theta,discountfactor):
    Uprime={s:0 for s in mdp.validstates} # U <-Uprime;
    Uprime[mdp.goalset]=mdp.reward(mdp.goalset)
    Uprime[(-1,-1)]=0 # i use this to differentiate goal and pitfalll
    for i in mdp.pitfallset:
        Uprime[i]=mdp.reward(i)
    #print "uprime",Uprime
    while True:
        U=Uprime.copy() # # U <- Uprime;
        delta= 0 #  delta<-0
        for state in mdp.validstates:
            list=[]
            for x in mdp.actionlist(state):
                    list.append(x)
            Uprime[state]=mdp.reward(state)+discountfactor*max([U[a] for a in list])
            #if state==(5,5):
                # print Uprime[state]
            # if abs(Uprime(s) - U(s)) > delta then delta = abs(Uprime(s) - U(s)) we have to implement this
            if abs(Uprime[state]- U[state]):
                delta=Uprime[state]-U[state]
        #until delta  < terminationcondition_factor *(1 - discountfactor)/discountfactor
        if delta < mdp.theta*(1-discountfactor)/discountfactor:
            return U
def add(x,y):
    return (x[0]+y[0],x[1]+y[1])
def Qlearning(mdp,numberofepisode):
    north = (0, 1)
    south = (0, -1)
    west = (-1, 0)
    east = (1, 0)
    actionlist=[north,west,south,east]
    Uprime = {s: 0 for s in mdp.validstates}  # U <-Uprime; it holds state max values
    #Uprime[mdp.goalset] = mdp.reward(mdp.goalset)
    Uprime[(-1, -1)] = 0  # i use this to differentiate goal and pitfalll
    for i in mdp.pitfallset:
        Uprime[i] = mdp.reward(i)

    Q={(s,a):0 for s in mdp.allstates for a in actionlist}
    for i in range(0,numberofepisode):
        reached=False
        validrandomstates = mdp.randomstates
        state = random.choice(validrandomstates)
        while not reached:
            epsilon=random.uniform(0, 1)
            if epsilon<= mdp.egreedyparam: # it is random selection
                randomaction=random.choice(actionlist)
                newstate=add(state,randomaction)
                rewardstate=newstate=add(state,randomaction)
                if newstate not in mdp.validstates:
                    newstate=state
                Q[state,randomaction]=(1-mdp.learningrate)*Q[state,randomaction]+mdp.learningrate*(mdp.reward(rewardstate)+mdp.discountfactor*Uprime[newstate])
                if state not in mdp.pitfallset:
                    if Uprime[state]< Q[state,randomaction]:
                        Uprime[state]=Q[state,randomaction]
                state=newstate
                if newstate==mdp.goalset:
                    reached=True
                    break
            elif epsilon>mdp.egreedyparam:
                for a in actionlist:
                    newstate = add(state, a)
                    if newstate not in mdp.validstates:
                        newstate = state
                    rewardstate= add(state, a)
                    Q[state, a] = (1 - mdp.learningrate) * Q[state, a] + mdp.learningrate * (mdp.reward(rewardstate) + mdp.discountfactor * Uprime[newstate])
                maxvalue=Q[state,actionlist[0]]
                maxaction=actionlist[0]
                for a in actionlist:
                    if Q[state,a]>maxvalue:
                        maxvalue=Q[state,a]
                        maxaction=a
                if Uprime[state]<maxvalue and state not in mdp.pitfallset:
                    Uprime[state]=maxvalue
                newstate=add(state,maxaction)
                if newstate not in mdp.validstates:
                    newstate = state
                if newstate==mdp.goalset:
                    reached=True
                    break
                state=newstate


    #print Q
    Uprime[mdp.goalset]=mdp.r_g
    return Uprime


    """
    Uprime = {s: 0 for s in mdp.validstates}  # U <-Uprime;
    Uprime[mdp.goalset] = mdp.reward(mdp.goalset)
    Uprime[(-1, -1)] = 0  # i use this to differentiate goal and pitfalll
    validrandomstates=mdp.randomstates
    for i in mdp.pitfallset:
        Uprime[i] = mdp.reward(i)
    # print "uprime",Uprime
    for i in range(0,numberofepisode):
        U = Uprime.copy()
        reachedgoal = False
        state = random.choice(validrandomstates)
        state=(2,4)
        while not reachedgoal:
            list=[]
            for x in mdp.actionlist(state):
                list.append(x)
            maxvalue=-999
            for a in list:
                if Uprime[a]>maxvalue:
                    maxstate=a
                    maxvalue=Uprime[a]
            Uprime[state] =(1-mdp.learningrate)*Uprime[state]+mdp.learningrate*(mdp.reward((state[0],state[1]+1))+mdp.discountfactor*(Uprime[maxstate]))
            state=maxstate
            if maxstate==mdp.goalset:
                reachedgoal=True
    return U
    """






def trystate(mdp,theta,discountfactor,state):
    Uprime = {s: 0 for s in mdp.validstates}  # U <-Uprime;
    Uprime[mdp.goalset] = mdp.reward(mdp.goalset)
    Uprime[(-1, -1)] = 0  # i use this to differentiate goal and pitfalll

    for i in mdp.pitfallset:
        Uprime[i] = mdp.reward(i)
    U=Uprime.copy()
    list=[]

    for x in mdp.actionlist(state):
        list.append(x)
    Uprime[state] = mdp.reward(state) + discountfactor * max([U[a] for a in list])
    return Uprime[state]

def findtheway(mdp,U): # it calculates which states we go for every states
    way={}
    for s in mdp.validstates:
        list = []
        for x in mdp.actionlist(s):
            list.append(x)
        maxvalue=-9999
        for a in list:
            if U[a]>=maxvalue and a!=(-1,-1):
                maxvalue=U[a]
                maxstate=a

        way[s]=maxstate

    return way
def findtheway2(mdp,U): # it calculates which states we go for every states
    way={}
    for s in mdp.validstates:
        list = []
        for x in mdp.actionlist(s):
            list.append(x)
        maxvalue=-9999
        for a in list:
            if U[a]>=maxvalue and a!=(-1,-1):
                maxvalue=U[a]
                maxstate=a

        way[s]=maxstate

    return way
def direction(s,news):
    x1=s[0]
    x2=news[0]
    y1=s[1]
    y2=news[1]
    if x1==x2 and y2==y1+1:
        return 0#go north case
    elif x1==x2 and y2==y1-1:
        return 2#go south case
    elif y1==y2 and x2==x1+1:
        return 1  # go east case
    elif y1==y2 and x2==x1-1:
        return 3  # go west caseg



takeinput()


