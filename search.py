# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import sys
import util
import searchAgents
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Tiny Maze:    Path found with total cost of 10 in 0.0 seconds (Search nodes expanded: 15)
    # Medium Maze:  Path found with total cost of 130 in 0.0 seconds (Search nodes expanded: 146)
    # Big Maze:     Path found with total cost of 210 in 0.0 seconds (Search nodes expanded: 390)
   
    from util import Stack
    # python set
    closed = set() 
    # stack from util.py
    fringe = Stack()
    # start state(position, path)
    start = (problem.getStartState(),[])
    fringe.push(start)

    while True:
        # if fringe is empty then return failure
        if fringe.isEmpty(): 
            sys.exit(1)  
        # STATE[node] <- REMOVE-FRONT(fringe)
        node,actions = fringe.pop()
        # if GOAL-TEST(problem, STATE[node]) then return node
        if problem.isGoalState(node):
            return actions
        # if STATE[node] is not in closed then
        if node not in closed:
            # add STATE[node] to closed
            closed.add(node)
            # for child-node in EXPAND(STATE[node], problem) do
            children = problem.getSuccessors(node)
            # children.reverse()
            for child,action,cost in children:
                # fringe <- INSERT(child-node, fringe)
                fringe.push( (child,actions+[action]) )
                    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Medium Maze:   Path found with total cost of 68 in 0.0 seconds (Nodes expanded: 269)
    # Big Maze:      Path found with total cost of 210 in 0.0 seconds(Nodes expanded: 620)
    # TinyCorners:   Path found with total cost of 32 in 0.0 seconds (Nodes expanded: 59/252)
    # mediumCorners: Search nodes expanded: 369/1966 （2 implementations）

    from util import Queue
    # python set
    closed = set()
    # Queue from util.py
    fringe = Queue()
    # start state(position, path)
    start = (problem.getStartState(),[])
    # start position
    orinStart = start[0]
    fringe.push(start)

    while True:
        # if fringe is empty then return failure
        if fringe.isEmpty(): 
            sys.exit(1)  
        # STATE[node] <- REMOVE-FRONT(fringe)
        node,actions = fringe.pop()
        # if GOAL-TEST(problem, STATE[node]) then return node
        if problem.isGoalState(node):
            # print "actions: ",actions
            if problem.getStartState()==orinStart:
                return actions
            # This part is for implementation 1, reset data structures, start state 
            start = (problem.getStartState(),[])
            fringe = Queue()
            closed = set()
            fringe.push(start)
            node = start[0]

        # if STATE[node] is not in closed then
        if node not in closed:
            # add STATE[node] to closed
            closed.add(node)
            # for child-node in EXPAND(STATE[node], problem) do
            children = problem.getSuccessors(node)
            # children.reverse()
            for child,action,cost in children:
                # fringe <- INSERT(child-node, fringe)
                fringe.push( (child,actions+[action]) )
  

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # MediumMaze:       Path found with total cost of 68/76 in 0.0 seconds (Search nodes expanded: 269/78)
    # MediumDottedMaze: Path found with total cost of 1 in 0.0 seconds (Search nodes expanded: 186/76)
    # MediumScaryMaze:  Path found with total cost of 68719479864 in 0.0 seconds (Search nodes expanded: 98/94)
    # BigMaze:          Path found with total cost of 210 in 0.0 seconds (620 nodes)
    # TrickySearch:     Path found with total cost of 60 in 14.2 seconds. Search nodes expanded: 16688
   
    from util import PriorityQueue
    # python set
    closed = set()
    # PriorityQueue from util.py
    fringe = PriorityQueue()
    # start state(position, path, cost)
    start = (problem.getStartState(),[],0)
    fringe.push(start,0)

    while True:
        # if fringe is empty then return failure
        if fringe.isEmpty(): 
            sys.exit(1)  
        # STATE[node] <- REMOVE-FRONT(fringe)
        node,actions,nodeCost = fringe.pop()
        # if GOAL-TEST(problem, STATE[node]) then return node
        if problem.isGoalState(node):
            return actions
        # if STATE[node] is not in closed then
        if node not in closed:
            # add STATE[node] to closed
            closed.add(node)
            # for child-node in EXPAND(STATE[node], problem) do
            children = problem.getSuccessors(node)
            for child,action,cost in children:
                # fringe <- INSERT(child-node, fringe)
                fringe.push( (child,actions+[action],nodeCost+cost), nodeCost+cost )
                # fringe.update( (child,actions+[action],1), nodeCost+cost )


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # BigMaze:      Search nodes expanded: 466/481/549(manhattanHeuristic), 471(euclideanHeuristic)
    # MediumCorner: Search nodes expanded: 188/204(cornersHeuristic)
    # TrickySearch: Path found with total cost of 60 in 18.7 seconds. Search nodes expanded: 4137
    # BigSearch:    Path found with cost 323

    from util import PriorityQueue
    from searchAgents import manhattanHeuristic
    from searchAgents import cornersHeuristic
    from searchAgents import foodHeuristic

    # python set
    closed = set() 
    # PriorityQueue from util.py
    fringe = PriorityQueue()
    # start state(position, path, cost)
    start = (problem.getStartState(),[],0)
    # start position
    orinStart = start[0]
    fringe.push(start,0)

    while True:
        # if fringe is empty then return failure
        if fringe.isEmpty(): 
            sys.exit(1)  
        # STATE[node] <- REMOVE-FRONT(fringe)
        node,actions,nodeCost = fringe.pop()
        # if GOAL-TEST(problem, STATE[node]) then return node
        if problem.isGoalState(node):
            # if not (problem.getStartState()==orinStart and heuristic==cornersHeuristic):
            return actions
            
            # This part is for implementation 1, reset data structures, start state
            # start = (problem.getStartState(),[],0)
            # fringe = PriorityQueue()
            # closed = set()
            # fringe.push(start,0)
            # node = start[0]
        # if STATE[node] is not in closed then
        if node not in closed:
            # add STATE[node] to closed
            closed.add(node)
            # for child-node in EXPAND(STATE[node], problem) do
            children = problem.getSuccessors(node)
            # calculate heuristic function h(node)
            h_node = heuristic(node,problem)
            

            for child,action,cost in children:
                # calculate heuristic function h(child)
                h = heuristic(child,problem)

                # Check consistency: h(node) - h(child) <= actual cost
                if ( h_node - h > 1 ):
                    print "This ", heuristic, " is inconsistent!!!"

                # fringe <- INSERT(child-node, fringe)
                fringe.push( (child,actions+[action],nodeCost+cost), nodeCost+cost+h )
                

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch