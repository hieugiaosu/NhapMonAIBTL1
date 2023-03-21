from GameWorld import *
import numpy as np
import heapq as pq
class A_star:
    def __init__(self,cube,board):
        self.destination = 0
        for key, value in board.map.items():
            if value == 3:
                self.destination = key
                break
        self.initialState = self.State(dict(board.map),cube.firstCube,cube.secondCube,board.buttonList,0)
        
    def evaluateFunction(self,state):
        firstCubeDistance = np.abs(state.firstCube[0]-self.destination[0]) + np.abs(state.firstCube[1]-self.destination[1])
        secondCubeDistance = np.abs(state.secondCube[0]-self.destination[0]) + np.abs(state.secondCube[1]-self.destination[1])
        return float(np.sqrt(firstCubeDistance**2 +secondCubeDistance**2))
    class State:
        def __init__(self, board,firstCube, secondCube,buttonList,cost,prev=None):
            self.ancestor = prev
            self.board = dict(board)
            if (firstCube < secondCube):
                self.firstCube = firstCube
                self.secondCube = secondCube
            else:
                self.firstCube = secondCube
                self.secondCube = firstCube
            self.cost = cost
            self.button = buttonList
            if not self.loseTest():
                self.__buttonClick()
        def __lt__(self,other):
            return self.cost < other.cost
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
        def nextState(self):
            next = []
            if self.__isNotSplit():
                if self.firstCube == self.secondCube:
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]-2,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+2,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+2),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-2),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                elif self.firstCube[0]==self.secondCube[0]:
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-2),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+2),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                elif self.firstCube[1]==self.secondCube[1]:
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-2,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0]+2,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
                    state = A_star.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        int(self.cost+1),
                        self
                    )
                    if not state.loseTest():
                        next.append(state)
            else:
                state = A_star.State(
                    self.board,
                    (self.firstCube[0]-1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    (self.firstCube[0]+1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    (self.firstCube[0],self.firstCube[1]+1),
                    self.secondCube,
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    (self.firstCube[0],self.firstCube[1]-1),
                    self.secondCube,
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0]+1,self.secondCube[1]),
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0]-1,self.secondCube[1]),
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]+1),
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
                state = A_star.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]-1),
                    self.button,
                    int(self.cost+1),
                    self
                    )
                if not state.loseTest():
                    next.append(state)
            return next
    def solve(self): 
        ### return a array of tupple is the position of each first and second Cube
        ### for example: [[(1,1),(1,2)],[(1,3),(1,3)]]
        waitingQueue = []
        goal = None
        count = 0
        visited = {}
        pq.heappush(waitingQueue,
                    (self.initialState.cost+self.evaluateFunction(self.initialState),
                    self.initialState))
        while len(waitingQueue)!=0 and goal == None:
            state = pq.heappop(waitingQueue)[1]
            visited[state.identify()]=1
            count+=1
            for i in state.nextState():
                if i.identify() in visited.keys(): continue
                if i.goalTest(): goal=i
                else:
                    pq.heappush(
                        waitingQueue,
                        (i.cost+self.evaluateFunction(i),i)
                    )
        print("visited "+str(count)+" states")
        if goal == None: return [[self.initialState.firstCube,self.initialState.secondCube]]
        seriesMove = []
        while goal != None:
            seriesMove.append([goal.firstCube,goal.secondCube])
            goal = goal.ancestor   
        return seriesMove[::-1]