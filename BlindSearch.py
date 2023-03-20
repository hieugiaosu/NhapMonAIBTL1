from GameWorld import *
from queue import Queue

class BlindSearch:
    def __init__(self,cube,board):
        self.initialState = self.State(dict(board.map),cube.firstCube,cube.secondCube,board.buttonList)
    class State:
        def __init__(self, board,firstCube, secondCube,buttonList,prev=None):
            self.ancestor = prev
            self.board = dict(board)
            if (firstCube < secondCube):
                self.firstCube = firstCube
                self.secondCube = secondCube
            else:
                self.firstCube = secondCube
                self.secondCube = firstCube
            self.button = buttonList
            if not self.loseTest():
                self.__buttonClick()
        def __isNotSplit(self):
            if self.firstCube[0] == self.secondCube[0] and np.abs(self.firstCube[1]-self.secondCube[1])<=1:
                return True
            if self.firstCube[1] == self.secondCube[1] and np.abs(self.firstCube[0]-self.secondCube[0])<=1:
                return True
            return False
        def __buttonClick(self):
            buttonKeysList=self.button.keys()
            if self.firstCube == self.secondCube:
                if self.firstCube in buttonKeysList:
                    if self.button[self.firstCube][0]==1 or self.button[self.firstCube][0]==2:
                        for i in self.button[self.firstCube][1]:
                            if not i in self.board.keys():
                                self.board[i] =2
                            else:
                                self.board[i]+=2
                                if self.board[i]>=3:
                                    self.board[i]=0
                    elif self.button[self.firstCube][0]==3:
                        [self.firstCube, self.secondCube] = self.button[self.firstCube][1]
                        self.__buttonClick()
            else:
                if self.firstCube in buttonKeysList and self.button[self.firstCube][0]==1 and self.ancestor.firstCube != self.firstCube:
                    for i in self.button[self.firstCube][1]:
                        if not i in self.board.keys():
                            self.board[i] =2
                        else:
                            self.board[i]+=2
                            if self.board[i]>=3:
                                self.board[i]=0
                if self.secondCube in buttonKeysList and self.button[self.secondCube][0]==1 and self.ancestor.secondCube != self.secondCube:
                    for i in self.button[self.secondCube][1]:
                        if not i in self.board.keys():
                            self.board[i] =2
                        else:
                            self.board[i]+=2
                            if self.board[i]>=3:
                                self.board[i]=0

        def goalTest(self):
            if self.firstCube == self.secondCube:
                if self.firstCube in self.board.keys() and self.board[self.firstCube]==3:
                    return True
                else: return False
            else: return False
        def loseTest(self):
            if self.firstCube in self.board.keys() and self.secondCube in self.board.keys():
                if self.board[self.firstCube]!=0 and self.board[self.secondCube]!=0:
                    if self.firstCube == self.secondCube and self.board[self.firstCube]==1:
                        return True
                    return False
                else: return True
            else: return True
        def identify(self):
            keysList = []
            for i in sorted(self.board.keys()):
                if self.board[i] != 0 and self.board[i] !=3:
                    keysList.append((self.board[i],i))
            keysList = tuple(keysList)
            return tuple((self.firstCube, self.secondCube, keysList))
        def boardIdentify(self):
            keysList = []
            for i in sorted(self.board.keys()):
                if self.board[i] != 0 and self.board[i] !=3:
                    keysList.append((self.board[i],i))
            keysList = tuple(keysList)
            return keysList
        def nextState(self):
            next = []
            if self.__isNotSplit():
                if self.firstCube == self.secondCube:
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]-2,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+2,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+2),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]-2),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                elif self.firstCube[0]==self.secondCube[0]:
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-2),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]+2),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                elif self.firstCube[1]==self.secondCube[1]:
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-2,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0]+2,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = BlindSearch.State(
                        dict(self.board),
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
            else:
                state = BlindSearch.State(
                    dict(self.board),
                    (self.firstCube[0]-1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    (self.firstCube[0]+1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    (self.firstCube[0],self.firstCube[1]+1),
                    self.secondCube,
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    (self.firstCube[0],self.firstCube[1]-1),
                    self.secondCube,
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    self.firstCube,
                    (self.secondCube[0]+1,self.secondCube[1]),
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    self.firstCube,
                    (self.secondCube[0]-1,self.secondCube[1]),
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]+1),
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = BlindSearch.State(
                    dict(self.board),
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]-1),
                    self.button,
                    self
                    )
                if not state.loseTest():
                    next.append(state)
            return next
    def __BFS(self):
        visited = {}
        visited[self.initialState.identify()]=1
        stateQueue = Queue()
        stateQueue.put(self.initialState)
        ans = None
        count = 0
        while (not stateQueue.empty()) and ans == None:
            state = stateQueue.get()
            count+=1
            successors = state.nextState()
            for i in successors:
                if i.goalTest(): ans = i
                elif not i.loseTest():
                    if i.identify() not in visited.keys():
                        visited[i.identify()]=1
                        stateQueue.put(i)
        print("visited "+str(count)+" states")
        if ans == None: return [[self.initialState.firstCube,self.initialState.secondCube]]
        seriesMove = []
        while ans != None:
            seriesMove.append([ans.firstCube,ans.secondCube])
            ans = ans.ancestor   
        return seriesMove[::-1]

    def solve(self): 
        ### return a array of tupple is the position of each first and second Cube
        ### for example: [[(1,1),(1,2)],[(1,3),(1,3)]]  
        return self.__BFS()