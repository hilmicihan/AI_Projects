resultlist=[]
"""
function unify(E1, E2);
  begin
    case
      both E1 and E2 are constants or the empty list:  % base case
        if E1 = E2
          then return {}
          else return FAIL;

      E1 is a variable:
        if E1 occurs in E2
          then return FAIL;
          else return {E2/E1}

      E2 is a variable:
        if E2 occurs in E1
          then return FAIL;
          else return {E1/E2}

      otherwise:                              % both E1 and E2 are lists
        begin
          HE1 := first element of E1;
          HE2 := first element of E2;
          SUBS1 := unify(HE1, HE2);            %   recursion
          if SUBS1 = FAIL, then return FAIL;
          TE1 := apply(SUBS1, rest of E1);
          TE2 := apply(SUBS1, rest of E2);
          SUBS2 := unify(TE1, TE2);            %  recursion
          if SUBS2 = FAIL then return FAIL;
             else return composition(SUBS1, SUBS2)
        end
  end
"""
# coding=utf-8


def unify_var(var, val, subst):

    if var in subst :
        return unify(subst[var], val, subst)
    elif isinstance(val, str) and val in subst :
        return unify(var, subst[val], subst)
    #elif (var occurs anywhere in x) then return failure
    else :
        #print "%s := %s" % (var, val)
        subst[var] = val ; return subst


def unify(sym1, sym2, subst):
    #print 'unify>', sym1, sym2, subst

    if subst is False : return False
    #when both symbols match
    elif isinstance(sym1, str) and isinstance(sym2, str) and sym1 == sym2 : return subst
    #variable cases
    elif isinstance(sym1, str) and is_var(sym1) : return unify_var(sym1, sym2, subst)
    elif isinstance(sym2, str) and is_var(sym2) : return unify_var(sym2, sym1, subst)
    elif type(sym1)==type([]) and type(sym2)==type([]) : #predicate case
        if len(sym1) == 0 and len(sym2) == 0 : return subst
        #Functors of structures have to match
        if isinstance(sym1[0], str) and  isinstance(sym2[0],str) and not (is_var(sym1[0]) or is_var(sym2[0]) )and sym1[0] != sym2[0] and (sym1[0][0]!='!' or sym2[0][0]!='!' ) : return False
        if isinstance(sym1[0], str) and  isinstance(sym2[0],str) and not (is_var(sym1) or is_var(sym2)) and sym1[0] != sym2[0] and  (sym1[0][0]!='!' or sym2[0][0]!='!' ): return False
        return unify(sym1[1:],sym2[1:], unify(sym1[0], sym2[0], subst))
    elif type(sym1)==type([]) and type(sym2)==type([]) : #list-case
        if len(sym1) == 0 and len(sym2) == 0 : return subst
        return unify(sym1[1:],sym2[1:], unify(sym1[0], sym2[0], subst))

    else: return False

def is_var(x):
    if 'z'>= x[0] and 'a'<= x[0] :
        return True
    else:
        return False




x= "p(f(x),y,g(y,x))"
y="p(u,k(v),g(z,h(w)))"
result=[]
#print x.partition("(")
def convert(xs):
    stack = [[]]
    xs=changestring(xs)
    i=0
    while(i< len(xs)):
        if xs[i]== '(':
            stack[-1].append([])
            stack.append(stack[-1][-1])
            i+=1
        elif xs[i] == ')':
            stack.pop()
            i+=1
        elif xs[i]!=',':
            if xs[i]=='!':
                stack[-1].append(xs[i]+xs[i+1])
                i+=2
            else:
                stack[-1].append(xs[i])
                i+=1
        else:
            i+=1

    return (stack.pop()).pop()

def changestring(x):
    for i in range(0,len(x)-1):
        if x[i+1]=='(':
            temp = '!'+x[i]
            x=x[:i]+x[i+1]+temp+","+x[i+2:]
    return x
def checkkey(dict,key): #look for a key exist in dictionary or not
    for i in dict.keys():
        if i ==key:
            return True
    return False
def checkkey(dict,key):
    for i in dict.keys():
        if i ==key:
            return True
    return False
def applysubs(str,subs):
    for i in range(0,len(str)-1):
        if str[i].islower() and str[i+1] != '(' and checkkey(subs,str[i]):
            str.replace(str[i],subs[str[i]])
    return str

def isvariable(x):
    if x.islower() and x+1 != '(' :
        return True
    else:
        return False


"""
function PL-RESOLUTION(KB,a) returns true or false
, the query, a sentence in propositional logic
clauses =the set of clauses in the CNF representation of KB and nota
new =()
loop do
    for each pair of clauses Ci, Cj in clauses do
        resolvents =PL-RESOLVE(Ci,Cj )
        if resolvents contains the empty clause then return true
        new =new union resolvents
    if new subset clauses then return false
    clauses =clauses union new
"""
def isrelavent(clause,target): # purpose find expressipn whih are contains negate of target
    print clause.explist,  "clause.explist"
    print target.explist,  "target.explist"
    if target.explist[0][0]=='~':
        if target.explist[0][1:] in clause.explist:
            return True
    else:
        if ('~'+target.explist[0]) in clause.explist:
            return True
    return False
def pl_resolution(clauselist,relativelist):
    resolvents=[]
    new=set()
    while True:# loop do
        #for each pair of clauses Ci, Cj in clauses do
        #resolvents =PL - RESOLVE(Ci, Cj)
        len1=len(clauselist)
        len2=len(relativelist)
        for i in range(len1):
                for j in range(len2):
                    resolvents=pl_resolve(clauselist[i],relativelist[j]) #Return all clauses that can be obtained by resolving clauses ci and target
                    if "empty" in resolvents: #if resolvents contains the empty clause then return true
                        return True
                    new=new.union(set(resolvents)) #new = new union resolvents
        if new.issubset(set(relativelist)): # if new subset clauses then return false
            return False
        for i in new:  # clauses = clauses union new it is a little tricky part because set dont contains dublicates we have to eliminate them
            if i not in relativelist:
                relativelist.append(i)
def substitute(cl,subs): #substitute the substitution subst into the expression str.
    list=[]
    if len(cl.explist)==0:
        return []
    for str in cl.explist:
        for i in range(0, len(str) - 1):
            if str[i].islower() and str[i + 1] != '(' and checkkey(subs, str[i]):
                str=str.replace(str[i], subs[str[i]])
        list.append(str)
    return list

def pl_resolve(cl1,cl2):#Return all clauses that can be obtained by resolving clauses ci and cj.
    resolvents=[]
    subs = {}
    for di in cl1.explist:
        for dj in cl2.explist:
            if (di[0] !='~' and dj[0]=='~') or (di[0] =='~' and dj[0]!='~'):
                copydi=di[:]
                copydj=dj[:]
                if copydi[0]=='~':
                    copydi=copydi[1:]
                elif copydj[0] =='~':
                    copydj=copydj[1:]
                copydi=convert(copydi)
                copydj=convert(copydj)
                subs=unify(copydi, copydj, subs)
            if subs:
                global resultlist

                str1=resultstr(cl2.explist)
                str2=resultstr(cl1.explist)

                cl1.explist.remove(di)
                cl2.explist.remove(dj)
                new1=[]
                new1=substitute(cl1,subs)
                cl1.explist=new1
                new2=[]
                new2=substitute(cl2,subs)
                cl2.explist=new2
                #print  "new",new

                if cl1.explist == [] and cl2.explist == []:
                    c = "empty"
                elif cl1.explist == []:
                    c = cl2
                elif cl2.explist == []:
                    c = cl1
                else:
                    c = cl1.concat(cl2)
                if c != "empty":
                    str3=resultstr(c.explist)
                    resultlist.append(str1+"$"+str2+"$"+str3)
                else:
                    str3="empty"
                    resultlist.append(str1 + "$" + str2 + "$" + str3)

                resolvents.append(c)
    return resolvents
def resultstr(list): # return string represantation of list
    str=""
    for i in list:
        str+=i
        str+="+"
    return str[:-1]
def makekb(str):
    list=[]
    if "+" in str:
        list=str.split("+")
        return [list]
    list.append(str)
    return list
class Node:
    def __init__(self,negation,explist):
        if not isinstance(explist,list):
            self.explist=[explist]
            if explist[0]=='~':
                self.negation=True
            else:
                self.negation = False
        else:
           self.explist=explist
           self.negation=False


    def __repr__(self):
        str=""
        for i in self.explist:
            str+=i
        return str
    def concat(self,c2):
        newexplist = list(set(self.explist + c2.explist))
        return Node(0,newexplist)



"""    def __init__(self, op, negation, args):
        self.op = op                        # Predicate Symbol
        self.args = map(expr, args)  # ['x', 'A', Expr('f',0,['y'])]
        self.negation = negation            # 1 or 0
    def negate(self):
        if self.negation == 1:
            return Expr(self.op,0,self.args)
        else:
            return Expr(self.op,1,self.args)
    def __repr__(self):
        flag = 0
        st = self.op+"("
        for arg in self.args:
            if flag==1:
                st = st + "," + str(arg)
            else:
                st = st + str(arg)
            flag = 1
        st = st + ")"
        if(self.negation == 1):
            st = "~" + st
        return st"""
def theorem_prover(x,y):
    global resultlist
    resultlist = []
    kb = []
    kb2=[]
    relativelist = []
    clauselist = []
    for i in x:
        kb = kb + makekb(i)
    for i in kb:
        clauselist.append(Node(0, i))
    for i in y:
        kb2 = kb2 + makekb(i)
    for i in kb2:
        relativelist.append(Node(0, i))
    result = pl_resolution(clauselist, relativelist)
    if result:
        return ("yes", resultlist)
    else:
        return ("no", [])
