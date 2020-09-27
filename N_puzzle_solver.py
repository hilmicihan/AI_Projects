import copy
opennodelist=[]#every not extendend node append this list as node
closednodelist=[]#every extended node append this list

class Node:
    def __init__(self,puzz,fvalue,gvalue,hvalue,parentnode):
        self.puzz=puzz
        self.gvalue=gvalue
        self.fvalue=fvalue
        self.hvalue=hvalue
        self.parentnode=parentnode

        """search an element position in puzzle"""

    def move(self,x1,y1,x2,y2,board):#board is a puzzle state (x1,y1) changed with (x2,y2)
        copyboard=copy.deepcopy(board)
        temp=copyboard[x1][y1]
        if x2>=0 and x2< len(board) and y2>=0 and y2<len(board):
            copyboard[x1][y1]=copyboard[x2][y2]
            copyboard[x2][y2]=temp
            return copyboard
        else:
            return -1
def search(x,board):
    for i in range(0,len(board)):
        for j in range(0,len(board[i])):
            if board[i][j]==x:
                return [i,j]
def extend(node,goal):
        x,y = search("_",node.puzz)
        trylist=[[x-1,y],[x+1,y],[x,y+1],[x,y-1]]#try possible movement with order  up down left right
        children=[]
        for i in trylist:
            resultboard=node.move(x,y,i[0],i[1],node.puzz)
            if resultboard is not -1:
                newnode=Node(resultboard,0,node.gvalue+1,0,node)
                newnode.hvalue=calculatemanhattan(newnode.puzz,goal)
                newnode.fvalue=newnode.hvalue+newnode.gvalue
                opennodelist.append(newnode)
def extend2(node,goal):
        x,y = search("_",node.puzz)
        trylist=[[x-1,y],[x+1,y],[x,y+1],[x,y-1]]
        children=[]
        for i in trylist:
            resultboard=node.move(x,y,i[0],i[1],node.puzz)
            if resultboard is not -1:
                newnode=Node(resultboard,0,node.gvalue+1,0,node)
                newnode.hvalue=calculatemanhattan(newnode.puzz,goal)
                newnode.fvalue=newnode.hvalue+newnode.gvalue
                children.append(newnode)
        return children

        #return children
def calculatemanhattan(startboard,goalboard):
    totaldistance=0
    for i in range(0,len(startboard)):
        for j in range(0,len(startboard)):
            if startboard[i][j]!="_":
                totaldistance+=abs(search(startboard[i][j],startboard)[0]-search(startboard[i][j],goalboard)[0])
                totaldistance+=abs(search(startboard[i][j],startboard)[1]-search(startboard[i][j],goalboard)[1])
    return totaldistance
def nodeinclosedlist(node):#we use this for not expend expended child again
    for i in closednodelist:
        if i==node:
            return True
    return False

def findmin(openlist,closednodelist):
    minnode=Node(openlist[0].puzz,800,0,0,None)
    for i in openlist:
        if i.fvalue<=minnode.fvalue and i.puzz not in closednodelist:
            minnode=i
    return minnode
def printlist(list1):
  print("SUCCESS")
  print("")
  for i in list1:
    for k in i:
      line=""
      for j in range(0,len(k)):
          if j==len(k)-1:
            line+=str(k[j])
          else:
            line=line+str(k[j])+" "
      print(line)
    print ""
def findnode(node,list1):
  for i in list1:
    if node.puzz==i:
      return True
  return False

def path(node):
  pathlist=[]
  pathlist.insert(0,node.puzz)
  while True:
    if node.parentnode==None or node==None:
      return pathlist
      break
    else:
      pathlist.insert(0,node.parentnode.puzz)
      node=node.parentnode
def takeinput():
  algo=raw_input()
  maxiter=raw_input()
  maxiter=int(maxiter)
  size=raw_input()
  start=[]
  goal=[]
  for i in range(0,int(size)):
    start.append(raw_input().split(" "))
  for i in range(0,int(size)):
    goal.append(raw_input().split(" "))
  lensuccess=len(start[0])
  for i in start:
    if len(i)!=lensuccess:
      print "FAILURE",
      return
  if algo=="A*":
      firstnode=Node(start,0,0,-1,None)
      extend(firstnode,goal)#first node extended and their child append opennodelist
      closednodelist.append(firstnode)
      successnode=Node(start,-1,0,0,None)
      while len(opennodelist)>0:
        newwillextendchild=findmin(opennodelist,closednodelist)
        closednodelist.append(newwillextendchild.puzz)
        opennodelist.remove(newwillextendchild)
        if newwillextendchild.fvalue>=maxiter:
          print "FAILURE",
          return
        if newwillextendchild.hvalue==0:
            successnode=newwillextendchild
            break
        else:
            extend(newwillextendchild,goal)

      solutionlist=path(newwillextendchild)
      printlist(solutionlist)
  elif algo=="IDA*":
      IDAstar(start,goal,maxiter)
#start take input
#takeinput()
def deptlimitsearch(srcnode,goaltile,fmax,minf):
  if srcnode.puzz==goaltile:
      return srcnode
  if srcnode.fvalue>fmax:
      if srcnode.fvalue < minf:
        minf=srcnode.fvalue
  children=extend2(srcnode,goaltile)
  for i in children:
    if i.hvalue==0:
      return i
    if i.fvalue>fmax:
      if i.fvalue<minf:
        minf=i.fvalue
    else:
      x=deptlimitsearch(i,goaltile,fmax,minf)
      if type(x)!= int:
        return x
      else:
          minf=x
  return minf

def IDAstar(start,goaltile,maxdept):
  firstnode=Node(start,0,0,-1,None)
  firstnode.hvalue=calculatemanhattan(start,goaltile)
  firstnode.fvalue=firstnode.hvalue
  fmax=firstnode.fvalue
  minf=99999
  while True:
    result=deptlimitsearch(firstnode,goaltile,fmax,minf)
    if type(result)!=int:
      solutionlist=path(result)
      printlist(solutionlist)
      return
    elif result >maxdept:
      break
    else:
      fmax=result

  print "FAILURE",

takeinput()

