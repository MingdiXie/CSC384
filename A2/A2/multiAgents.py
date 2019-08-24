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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        #print("************")
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print("************")
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action) # this give me the whole graph in terminal
        newPos = successorGameState.getPacmanPosition() # this give me the x y axis
        newFood = successorGameState.getFood() # this give me T and F
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates() # ghost's position
        capsule = currentGameState.getCapsules()
        "*** YOUR CODE HERE ***"
        if action == "Stop":
            return float("-inf")
        sum = 0
        if newPos in oldFood.asList():
            sum += 50
        mfooddistance = min_m_distance(newPos, newFood.asList(),0)
        sum -= mfooddistance
        sfooddistance = min_m_distance(newPos, newFood.asList(),1)
        sum -= sfooddistance * 0.1

        mcapsule = min_m_distance(newPos, capsule, 0)
        if mcapsule <= 3:
            sum += (10 / (mcapsule + 1))

        # scaredtime
        switch = 0
        for ghost in newGhostStates:
            countdown = ghost.scaredTimer
            if countdown == 0:
                ghostdis = manhattanDistance(newPos, ghost.getPosition())
                if ghostdis <= 2:
                    sum -= 30 ** (3 - ghostdis)
            else:
                switch = 1
        if switch == 1:
            sum += 20
        return sum

def min_m_distance(x,nesty,num):
    a = []
    for y in nesty:
        a.append(manhattanDistance(x,y))
    if a == []:
        return 0
    if num == 1:
        a.remove(min(a))
        if a == []:
            return 0
    return min(a)

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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
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

        rs = self.maxhelper(gameState, self.depth)
        return rs[1]



    def maxhelper(self, gameState, depth):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return [self.evaluationFunction(gameState), None]
        legalAction = gameState.getLegalActions()

        a = [[float("-inf"), None]]
        for action in legalAction:
            newstate = gameState.generateSuccessor(0, action)
            temp = self.minhelper(newstate, depth, 1)
            temp[1] = action
            a.append(temp)

        curr_max = a[0]
        for numaction in a:
            if numaction[0] > curr_max[0]:
                curr_max = numaction
        return curr_max



    def minhelper(self, gameState, depth, numghost):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return [self.evaluationFunction(gameState), None]
        else:
            legalAction = gameState.getLegalActions(numghost)

            a = [[float("inf"), None]]
            for action in legalAction:
                lastGhost = gameState.getNumAgents() - 1
                if numghost != lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    temp = self.minhelper(newstate, depth, numghost + 1)
                    temp[1] = action
                    a.append(temp)
                elif numghost == lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    temp = self.maxhelper(newstate, depth - 1)
                    temp[1] = action
                    a.append(temp)

            curr_min = a[0]
            for numaction in a:
                if numaction[0] < curr_min[0]:
                    curr_min = numaction
            return curr_min



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        rs = self.maxhelper(gameState, self.depth, float("-inf"), float("inf"))
        return rs[1]

    def maxhelper(self, gameState, depth, alpha, beta):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return [self.evaluationFunction(gameState), None]
        legalAction = gameState.getLegalActions()

        a = [[float("-inf"), None]]
        maxAction = a[0]
        for action in legalAction:
            newstate = gameState.generateSuccessor(0, action)
            temp = self.minhelper(newstate, depth, 1, alpha, beta)
            temp[1] = action
            a.append(temp)
            if temp[0] > maxAction[0]:
                maxAction = temp
            if temp[0] >= beta:
                return temp
            alpha = max(alpha, temp[0])
        return maxAction


    def minhelper(self, gameState, depth, numghost, alpha, beta):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return [self.evaluationFunction(gameState), None]
        else:
            legalAction = gameState.getLegalActions(numghost)

            a = [[float("inf"), None]]
            minAction = a[0]
            for action in legalAction:
                lastGhost = gameState.getNumAgents() - 1
                if numghost != lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    temp = self.minhelper(newstate, depth, numghost + 1, alpha, beta)
                    temp[1] = action
                    a.append(temp)
                elif numghost == lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    temp = self.maxhelper(newstate, depth - 1, alpha, beta)
                    temp[1] = action
                    a.append(temp)
                if temp[0] < minAction[0]:
                    minAction = temp
                if alpha >= minAction[0]:
                    return temp
                beta = min(beta, temp[0])
            return minAction


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
        rs = self.maxhelper(gameState, self.depth)
        return rs[1]

    def maxhelper(self, gameState, depth):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return [self.evaluationFunction(gameState), None]
        legalAction = gameState.getLegalActions()

        a = [[float("-inf"), None]]
        for action in legalAction:
            newstate = gameState.generateSuccessor(0, action)
            temp = [self.avghelper(newstate, depth, 1), action]
            a.append(temp)

        curr_max = a[0]
        for numaction in a:
            if numaction[0] > curr_max[0]:
                curr_max = numaction
        return curr_max

    def avghelper(self, gameState, depth, numghost):
        if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
        else:
            legalAction = gameState.getLegalActions(numghost)

            a = []
            for action in legalAction:
                lastGhost = gameState.getNumAgents() - 1
                if numghost != lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    a.append(self.avghelper(newstate, depth, numghost + 1))
                elif numghost == lastGhost:
                    newstate = gameState.generateSuccessor(numghost, action)
                    temp = self.maxhelper(newstate, depth - 1)
                    a.append(temp[0])
            return float(float(sum(a)) / len(a))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    currPos = currentGameState.getPacmanPosition()  # this give me the x y axis
    oldFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()  # ghost's position
    capsule = currentGameState.getCapsules()
    "*** YOUR CODE HERE ***"
    sum = 0
    # food distance
    mfooddistance = min_m_distance(currPos, oldFood.asList(), 0)
    sum -= mfooddistance

    # capsule
    mcapsule = min_m_distance(currPos, capsule, 0)
    if mcapsule <= 3:
        sum += (10/(mcapsule+1))

    # scaredtime
    switch = 0
    for ghost in newGhostStates:
        countdown = ghost.scaredTimer
        if countdown == 0:
            ghostdis = manhattanDistance(currPos, ghost.getPosition())
            if ghostdis <= 2:
                sum -= 30 ** (3 - ghostdis)
            else:
                sum -= (20 - ghostdis) * 0.3
        else:
            switch = 1
    if switch == 1:
        sum += 20
    return sum + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
