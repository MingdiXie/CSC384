# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import *  # for search engines
from lunarlockout import LunarLockoutState, Direction, \
  lockout_goal_state  # for LunarLockout specific classes and problems


# LunarLockout HEURISTICS
def heur_trivial(state):
  '''trivial admissible LunarLockout heuristic'''
  '''INPUT: a LunarLockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  total = 0
  center = state.width // 2
  for i in state.xanadus:
    total += ((i[0] - center) ** 2 + (i[1] - center) ** 2) ** (1 / 2)
  return total


def heur_manhattan_distance(state):
  # OPTIONAL
  '''Manhattan distance LunarLockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
  # Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
  total = 0
  center = state.width // 2
  for i in state.xanadus:
    for j in i:
      total += abs(j - center)
  return total


def heur_L_distance(state):
  # IMPLEMENT
  '''L distance LunarLockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
  # Your function should return a sum of the L distances between each xanadu and the escape hatch.
  total = 0
  center = state.width // 2
  for i in state.xanadus:
    if i[0] == center or i[1] == center:
      total += 1
    else:
      total += 2
  return total


def heur_alternate(state):
  # IMPLEMENT
  '''a better lunar lockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Your function should return a numeric value for the estimate of the distance to the goal.

  # First we calculate the L distance for all the rover, if they are on the same row or colomn with the escape hatch
  # it will take at least one move, if not it will take at least two move. Then we check through all the robot whether i
  # it block the escape hatch or there is no robot adjacent to it, we will need to add cost, since we need to shift it
  # Afterwards, we check if there is any rover is at the outer layer that become a dead state, then we will add infinite
  # cost to it, meanwhile we will check if there is any rover or robot at the same row or colomn with the rover, if
  # there is no such block, then we will need at least one move to make it to the block spot.
  total = 0
  center = state.width // 2
  xlist = []
  ylist = []
  # calculate the L distance
  for i in state.xanadus:
    if i[0] == center or i[1] == center:
      total += 1
    else:
      total += 2
    xlist.append(i[0])
    ylist.append(i[1])
  # check if the robot block the escape hatch or if it is at the adjacent spot
  extra = 2
  for j in state.robots:
    if j[0] == center and j[1] == center:
      total += 2
    xlist.append(j[0])
    ylist.append(j[1])
    if j in [(center+1,center),(center,center+1),(center-1,center),(center, center-1)]:
       extra = 0
  total += extra

  k = 0
  # check dead state and add more to L distance
  while k < len(state.xanadus):
    x = xlist.pop(0)
    y = ylist.pop(0)
    xmax = max(xlist)
    xmin = min(xlist)
    ymax = max(ylist)
    ymin = min(ylist)
    if (x < xmin and y < ymin) or (x < xmin and y > ymax) or (x > xmax and y < ymin) or (x > xmax and y > ymax):
      total = float("inf")
    if x not in xlist and y not in ylist:
      total += 1
    k += 1
    xlist.append(x)
    ylist.append(y)
  return total


def fval_function(sN, weight):
  # IMPLEMENT
  """
  Provide a custom formula for f-value computation for Anytime Weighted A star.
  Returns the fval of the state contained in the sNode.

  @param sNode sN: A search node (containing a LunarLockoutState)
  @param float weight: Weight given by Anytime Weighted A star
  @rtype: float
  """

  # Many searches will explore nodes (or states) that are ordered by their f-value.
  # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
  # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
  # The function must return a numeric f-value.
  # The value will determine your state's position on the Frontier list during a 'custom' search.
  # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
  return sN.gval + (weight * sN.hval)


def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound=2):
  # IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  se = SearchEngine('custom', 'full')
  wrapper_function = (lambda sN: fval_function(sN, weight))
  se.init_search(initial_state, lockout_goal_state, heur_fn, wrapper_function)
  starttime = os.times()[0]
  final = se.search(timebound)

  if final:
    time_remain = timebound - (os.times()[0] - starttime)
    while time_remain > 0:
      weight = 0.75 * weight
      wrapper_function = (lambda sN: fval_function(sN, weight))
      se.init_search(initial_state, lockout_goal_state, heur_fn, wrapper_function)
      initialtime = os.times()[0]
      new_final = se.search(time_remain)
      if new_final:
        final = new_final
      time_remain = time_remain - (os.times()[0] - initialtime)
  return final


def anytime_gbfs(initial_state, heur_fn, timebound = 2):
#OPTIONAL
  '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
  '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
  '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  return 0

PROBLEMS = (
  #5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2),(0,4),(2,0),(4,0)),((4, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 3),)),
  #7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6,3), (5,4)), ((6, 2),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2,6)), ((4, 6),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2,6), (4,6)), ((2, 0),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0 ,2), (2 ,3), (4, 4), (2, 5)), ((2, 4),(3, 1),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0 ,2), (1 ,2), (6, 4), (2, 5)), ((2, 0),(3, 0),(4, 0))),
  )

if __name__ == "__main__":

  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(len(PROBLEMS)): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    print("*******RUNNING A STAR*******") 
    se = SearchEngine('astar', 'full')
    se.init_search(s0, lockout_goal_state, heur_alternate)
    final = se.search(timebound) 

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime Weighted A-star")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    weight = 4
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime GBFS")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    final = anytime_gbfs(s0, heur_alternate, timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************")   



  

