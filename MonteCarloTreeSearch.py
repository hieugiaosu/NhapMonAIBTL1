from GameWorld import *
import numpy as np
import random as rd
class MonterCarloTreeSearch:
    def __init__(self,cube,board):
        self.initialState = self.State(dict(board.map),cube.firstCube,cube.secondCube,board.buttonList)
        self.visited = {}
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
            self.times= 0
            self.confidence = 0
            self.successor = []
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
        def nextState(self,visited=dict({})):
            next = []
            if self.__isNotSplit():
                if self.firstCube == self.secondCube:
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]-2,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+2,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+2),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-2),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                elif self.firstCube[0]==self.secondCube[0]:
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]+1,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-2),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+2),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                elif self.firstCube[1]==self.secondCube[1]:
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]-1,self.firstCube[1]),
                        (self.secondCube[0]-2,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0]+2,self.firstCube[1]),
                        (self.secondCube[0]+1,self.secondCube[1]),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]+1),
                        (self.secondCube[0],self.secondCube[1]+1),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
                    state = MonterCarloTreeSearch.State(
                        self.board,
                        (self.firstCube[0],self.firstCube[1]-1),
                        (self.secondCube[0],self.secondCube[1]-1),
                        self.button,
                        self
                    )
                    if (not state.loseTest()) and (state.identify() not in visited.keys()):
                        next.append(state)
            else:
                state = MonterCarloTreeSearch.State(
                    self.board,
                    (self.firstCube[0]-1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    (self.firstCube[0]+1,self.firstCube[1]),
                    self.secondCube,
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    (self.firstCube[0],self.firstCube[1]+1),
                    self.secondCube,
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    (self.firstCube[0],self.firstCube[1]-1),
                    self.secondCube,
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0]+1,self.secondCube[1]),
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0]-1,self.secondCube[1]),
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]+1),
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
                state = MonterCarloTreeSearch.State(
                    self.board,
                    self.firstCube,
                    (self.secondCube[0],self.secondCube[1]-1),
                    self.button,
                    self
                    )
                if (not state.loseTest()) and (state.identify() not in visited.keys()):
                    next.append(state)
            return next
    def rollOut(self,state):
        if state.goalTest(): return 1
        # visited = dict(self.visited)
        child = state.nextState(self.visited)
        curr = state
        count = 0
        while len(child)!=0 and (not state.goalTest()) and count<1000:
            count+=1
            for i in child:
                if i.goalTest(): return 1
            state = rd.choice(child)
            child = state.nextState(self.visited)
        state = curr
        return 0
    def backPropagate(self,state,confidence):
        while state != None:
            state.confidence += confidence
            state.times +=1
            state = state.ancestor          
    def UCB(self,state):
        c = np.sqrt(2)
        if state.ancestor == None:
            return 0
        if state.times == 0:
            return np.Inf
        else:
            return state.confidence/state.times + c*np.sqrt(np.log(state.ancestor.times)/state.times)
    def solve(self):
        count = 0
        goal = None
        while count<200000 and goal == None:
            count +=1
            curr = self.initialState
            while len(curr.successor)!=0:
                curr = max(curr.successor,key= self.UCB)
            curr.successor = curr.nextState(self.visited)
            if curr.goalTest(): goal = curr
            for i in curr.successor:
                self.visited[i.identify()]=i
            score = 0
            if len(curr.successor)!=0:
                score = self.rollOut(curr.successor[0])
            else:
                score = self.rollOut(curr)
            if len(curr.successor)!=0:
                self.backPropagate(curr.successor[0],score)
            else:
                self.backPropagate(curr,score)
        print(str(count)+" loop")
        highestPath = []
        curr = self.initialState
        while curr != None:
            highestPath.append([curr.firstCube,curr.secondCube])
            if len(curr.successor)!=0:
                curr = max(curr.successor,key= self.UCB)
            else:
                curr = None
        if goal == None: return highestPath
        seriesMove = []
        while goal != None:
            seriesMove.append([goal.firstCube,goal.secondCube])
            goal = goal.ancestor   
        return seriesMove[::-1]
            