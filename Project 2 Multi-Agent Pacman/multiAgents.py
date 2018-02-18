# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
from game import Actions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print "successorGameState: \n",successorGameState
        newPos = successorGameState.getPacmanPosition()
        # print "newPos: \n",newPos
        newFood = successorGameState.getFood()
        # print "newFood:\n",newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        # print "newGhostStates:\n",newGhostStates
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print "newScaredTimes:\n",newScaredTimes[0]

        "*** YOUR CODE HERE ***" 
        w1,w2,w3 = 10,100,10
        f1,f2,f3,closestCap = 0,0,0,0
        x, y = newPos
        caplist, foodList = [], []
        currentFood = currentGameState.getFood()
        capsuleList = currentGameState.getCapsules()
        
        # f1: DISTANCE TO THE NEAREST FOOD
        if currentFood[x][y] == True: f1 += 10
        for food in newFood.asList():
          foodList.append(manhattanDistance(newPos, food))
        closestfood = min(foodList) if len(foodList)>0 else 1
        # The smaller the distance is, the higher f1 will be
        f1 += w1 / closestfood
        
        # f2: DISTANCE TO THE NEAREST GHOST
        if newScaredTimes[0]==0: sign = -1
        else: sign = 1
        for ghostPos in successorGameState.getGhostPositions():
          distToG = manhattanDistance(newPos, ghostPos)
          # Add a heavy penalty if pacman is one step away from the nearest ghost
          if distToG <=1: f2 += w2*sign

        # f3: DISTANCE TO THE NEAREST CAPSULE
        for cap in capsuleList:
          if newPos == cap: f1 += 10 
          caplist.append(manhattanDistance(newPos, cap))
          closestCap = min(caplist) if len(caplist)>0 else 1
        # The smaller the distance is, the higher f3 will be
        if newScaredTimes[0] > 0: f3 += w3 / (closestCap+1)

        return f1 + f2 + f3

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """ 
        "*** YOUR CODE HERE ***"
        scores = []
        # loop through all legal actions
        for action in gameState.getLegalActions(0):
          state = gameState.generateSuccessor(0, action)
          scores.append((self.value(state,0,0),action))
        # return the action with the highest score
        return max(scores, key = lambda x: x[0])[1]

    def value(self, state, agentID, depth):
        agentID += 1
        if agentID == state.getNumAgents(): 
          agentID = 0
          depth +=1
        # if the state is a terminal state: return the state utility
        if state.isWin() or state.isLose() or depth == self.depth:
          return self.evaluationFunction(state)
        # else: return maxValue(state,agentID,depth)/minValue(state,agentID,depth)
        return self.minmaxValue(state,agentID,depth)

    # combine maxValue() and minValue()
    def minmaxValue(self, state, agentID, depth):
        isPacmansTurn = 0
        # if it's pacman's turn, initialize v = -inf. Else, initialize v = inf
        if agentID == 0 or agentID == state.getNumAgents():
          isPacmansTurn = 1
          v = float('-inf')
        else: v = float('inf')

        # for each successor of state: v = max/min(v, value(successor))
        for action in state.getLegalActions(agentID):
          s = state. generateSuccessor(agentID, action)
          if isPacmansTurn: v = max(v, self.value(s,agentID,depth))
          else: v = min(v, self.value(s,agentID,depth))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        scores = []
        v, alpha, beta= float('-inf'), float('-inf'), float('inf')
        # loop through all legal actions
        for action in gameState.getLegalActions(0):
          state = gameState.generateSuccessor(0, action)
          v = max(v, self.value(state,0,0,alpha,beta))
          if v > beta: return action
          alpha = max(alpha, v)
          scores.append((v,action))
        # return the action with the highest score
        return max(scores, key = lambda x: x[0])[1]

    def value(self, state, agentID, depth, alpha, beta):
        agentID += 1
        if agentID == state.getNumAgents(): 
          agentID = 0
          depth +=1
        # if the state is a terminal state: return the state utility
        if state.isWin() or state.isLose() or depth == self.depth:
          return self.evaluationFunction(state)
        # else: return maxValue/minValue(state,agentID,depth,alpha,beta)
        return self.minmaxValue(state,agentID,depth,alpha,beta)

    # combine maxValue() and minValue()
    def minmaxValue(self, state,agentID, depth, alpha, beta):
        isPacmansTurn = 0
        # if it's pacman's turn, initialize v = -inf. Else, initialize v = inf
        if agentID == 0 or agentID == state.getNumAgents():
          isPacmansTurn = 1
          v = float('-inf')
        else: v = float('inf')

        # for each successor of state:
        for action in state.getLegalActions(agentID):
          s = state. generateSuccessor(agentID, action)

          if isPacmansTurn:
            v = max(v, self.value(s,agentID,depth,alpha,beta))
            if v > beta: return v
            alpha = max(alpha, v)
            
          else: 
            v = min(v, self.value(s,agentID,depth,alpha,beta))
            if v < alpha: return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        scores = []
        # loop through all legal actions
        for action in gameState.getLegalActions(0):
          state = gameState.generateSuccessor(0, action)
          scores.append((self.value(state,0,0),action))
        # print "At ",gameState.getPacmanPosition()," scores in expectimax: \n",scores
        # return the action with the highest score
        return max(scores, key = lambda x: x[0])[1]

    def value(self, state, agentID, depth):
        agentID += 1
        if agentID == state.getNumAgents(): 
          agentID = 0
          depth +=1
        if state.isWin() or state.isLose() or depth == self.depth:
          score = self.evaluationFunction(state)
          # print "At ",state.getPacmanPosition()," scores in value: ",score
          return score
        return self.expectimaxValue(state,agentID,depth)

    # combine maxValue() and expectValue()
    def expectimaxValue(self, state,agentID, depth):
        isPacmansTurn = 0
        # if it's pacman's turn, initialize v = -inf. Else, initialize v = 0
        if agentID == 0 or agentID == state.getNumAgents():
          isPacmansTurn = 1
          v = float('-inf')
        else: v = 0

        # for each successor of state:
        actions = state.getLegalActions(agentID)
        for action in actions:
          s = state. generateSuccessor(agentID, action)
          if isPacmansTurn: # v = max(v, value(successor))
            v = max(v, self.value(s,agentID,depth))

          else: # p = probability(successor); v += p * value(successor)
            v += (1.0/float(len(actions))) * self.value(s,agentID,depth) 
        return v

def bfsGetSuccessors(state,walls):
    "bfsGetSuccessor for bfs to get the successors of the given node, with the given walls situation"
    # The implementation is the same as PositionSearchProblem.getSuccessors() from search.py in project1
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        x, y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        if not walls[nextx][nexty]:
            nextState = (nextx, nexty)
            successors.append( ( nextState, action, 1) )
    return successors

def bfs(startPos, goalPos, walls):
    "bfs returns the step costs estimation using breadth first search for the heuristics"
    # The implementation of breadthFirstSearch is from search.py in project1
    # It returns a int representing the length of the path from start to goal
    from util import Queue
    closed, fringe, start= set(), Queue(), (startPos,[])
    fringe.push(start)
    while fringe.isEmpty() == False:  
        node,actions = fringe.pop()
        if node == goalPos: return len(actions)
        if node not in closed:
            closed.add(node)
            children = bfsGetSuccessors(node, walls)
            for child,action,cost in children:
                fringe.push( (child,actions+[action]) )

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The evaluationFunction is associated with:
      the number of food left in the state; 
      the total number of steps left to get to the terminating state(all food are eaten);
      the distance between pacman and ghost during the scared time(or non-scared time);
      the distance between pacman and the capsules
    """
    "*** YOUR CODE HERE ***"
    w1,w2,w3 = 10,100,1
    f1,f2,f3 = 0,0,0
    closestCap, numStepsLeft = 0,0.0
    caplist = []

    capsuleList = currentGameState.getCapsules()
    pacPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # f1: NUMBER OF FOOD LEFT & NUMBER OF STEPS LEFT TO EAT ALL FOOD DOTS
    for food in currentFood.asList():
      numStepsLeft += bfs(pacPos, food, currentGameState.getWalls())
    f1 += (w1 / float(numStepsLeft+1))
    f1 += (w1 / float(currentGameState.getNumFood()+1))
    
    # f2: DISTANCE TO THE GHOST DURING THE SCARED TIME OR NOT
    # During scared time, pacman can go eat the ghost like a bonus capsule
    if newScaredTimes[0]>0: 
      capsuleList = [currentGameState.getGhostPosition(1)] + capsuleList
    distToGh = manhattanDistance(pacPos, currentGameState.getGhostPosition(1))
    # f2 += distToG/100.0 
    # Add a heavy penalty to score if pacman is 1 step away from ghost
    if newScaredTimes[0]==0 and distToGh <= 1: f2 += w2*(-1)

    # f3: DISTANCE TO CAPSULES
    for cap in capsuleList: 
      caplist.append(manhattanDistance(pacPos, cap))
    #   caplist.append(bfs(pacPos, cap, currentGameState.getWalls()))
    closestCap = min(caplist) if len(caplist)>0 else 1
    if newScaredTimes[0] > 0: f3 += (w3 / (float(closestCap)+1))
  
    return f1 + f2 + f3

# Abbreviation
better = betterEvaluationFunction

