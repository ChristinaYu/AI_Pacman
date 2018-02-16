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
        # distance to food
        x, y = newPos
        caplist = []
        foodList = []
        ghostList = []
        w1,w2,w3 = 10,100,10
        f1,f2,f3,closestCap = 0,0,0,0
        currentFood = currentGameState.getFood()
        capsuleList = currentGameState.getCapsules()
        
        # f1: dist to food
        if currentFood[x][y] == True: f1 += 10
        for food in newFood.asList():
          foodList.append(manhattanDistance(newPos, food))
        closestfood = min(foodList) if len(foodList)>0 else 1
        f1 += float(w1 / closestfood)
        
        # f2: distance to ghost
        if int(newScaredTimes[0])==0: sign = -1
        else: sign = 1
        for ghostPos in successorGameState.getGhostPositions():
          distToG = manhattanDistance(newPos, ghostPos)
          ghostList.append(distToG)
          if distToG <=1: 
            f2 += 100*sign
        f2 += w2/(min(ghostList)+1)
        # print "f2: ",f2

        # f3: dist to cap
        for cap in capsuleList:
          if (x,y) == cap: f1 += 10 
          caplist.append(manhattanDistance(newPos, cap))
          closestCap = min(caplist) if len(caplist)>0 else 1
        if not newScaredTimes[0] == 0:
          f3 += w3 / (closestCap+1)

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
        for action in gameState.getLegalActions(0):
          state = gameState.generateSuccessor(0, action)
          scores.append((self.value(state,0,0),action))
        return max(scores, key = lambda x: x[0])[1]

    def value(self, state, agentID, depth):
        agentID += 1
        if agentID == state.getNumAgents(): 
          agentID = 0
          depth +=1
        if state.isWin() or state.isLose() or depth == self.depth:
          return self.evaluationFunction(state)
        return self.minmaxValue(state,agentID,depth)

    # combine maxValue() and minValue()
    def minmaxValue(self, state,agentID, depth):
        if agentID == 0 or agentID == state.getNumAgents():
          v = float('-inf')
        else: v = float('inf')

        for action in state.getLegalActions(agentID):
          s = state. generateSuccessor(agentID, action)
          if agentID == 0 or agentID == state.getNumAgents():
            v = max(v, self.value(s,agentID,depth))
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
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

