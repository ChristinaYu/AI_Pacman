************************************************************
Project 1:	Search in Pacman README File
Date:		02/04/2018 
Author:		Christina Xuan Yu
************************************************************

DFS, BFD, UCS, A star, corner problem, corner heuristics, food heuristics, suboptimal problem

Question 1:

	python pacman.py -l tinyMaze -p SearchAgent
		Path found with total cost of 10 in 0.0 seconds
		Search nodes expanded: 15

	python pacman.py -l mediumMaze -p SearchAgent
		Path found with total cost of 130 in 0.0 seconds
		Search nodes expanded: 146

	python pacman.py -l bigMaze -z .5 -p SearchAgent
		Path found with total cost of 210 in 0.0 seconds
		Search nodes expanded: 390

Question 2:

	python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
		Path found with total cost of 68 in 0.0 seconds
		Search nodes expanded: 269

	python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
		Path found with total cost of 210 in 0.0 seconds
		Search nodes expanded: 620

Question 3:

	python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
		Path found with total cost of 68 in 0.0 seconds
		Search nodes expanded: 269

	python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
		Path found with total cost of 1 in 0.0 seconds
		Search nodes expanded: 186

	python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
		Path found with total cost of 68719479864 in 0.0 seconds
		Search nodes expanded: 98

Question 4:

	python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
		Path found with total cost of 210 in 0.0 seconds
		Search nodes expanded: 549

Question 5:

	python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
		Path found with total cost of 32 in 0.0 seconds
		Search nodes expanded: 59

	python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
		Path found with total cost of 106 in 0.0 seconds
		Search nodes expanded: 369

Question 6:

	python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
		Path found with total cost of 106 in 4.7 seconds
		Search nodes expanded: 204

Question 7:

	python pacman.py -l trickySearch -p AStarFoodSearchAgent
		Path found with total cost of 60 in 20.1 seconds
		Search nodes expanded: 4137

Question 8:

	python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 
		Path found with cost 323


