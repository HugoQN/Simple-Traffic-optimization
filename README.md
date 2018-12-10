# Simple-Traffic-optimization
Simple Traffic optimization

game.py: This is the most basic components of a traffic maps, which contains:\\

	 1. Class[Info]: This class is a matrix with a specific width and height, and each entry will be label as FIELD,  INTERSECTION, CROSSROAD,  ROAD. If each of these entry are continuous, the continuous entry will be set to the same number.
	
	2. Class[Intersection] and Class[Crossroad]: Both of these classes will group up each block of intersection/crossroad into the same instance, with the same assigning number and multiple Inroad/Outroad.

	3. Class[Road]: This class also assign each road segments with a distinct number, and it also saves a variable containing the direction of each road index. 


layout.py : This file contains the Class[Layout], which takes a text file as input and construct a map with road, intersection and  crossroad combined together. Features including:

	1. From input text, find the same block of Road/Intersection/Crossroad recursively and label them with distinct integers.

	2. For each Intersection/Crossroad block, we check if there is a specific road connecting it. If there exists such road, we check the direction and update if the road starts at this Intersection/Crossroad or ends at this Intersection/Crossroad.

car.py: This file contains the Class[Carmap], which is used to combine the layout with car and traffic light.
	
	1. function [getDirection]: Using bread-first-search to reach the destination in shortest distance, and back track to the start, which will return a tuple (total distance, list of ($Road_i$, length to walk in $Road_i$)) in order of the path.

	2. Some other helpful function that used to do the moving and traficlight-checking. These functions will be further used when we are doing simulation later.

simulation.py : This file is used to similuate the whole process of all cars moving from their start point to the end point. Given a car map with roads and lights information, we calculate the result as a tupe (total time, average time), which is what we want to optimize.

	1. class[Car]: This [Car] is different from the [Car] in "car.py." The class[Car] has a move function that it can change its states repeatly, where we can treat it as a "moving car."

	2. function[run]: By moving car recursively and change the clock repeatly, we will return the tuple result as desired.

ga.py : The main class[Gene] is used to construct or initial the gene by the car map representing one specific generation. For instance, given a car map with N traficlights, we will have a gene string of length 2*N.

	1. Each Intersection corresponds to a list of traffic light dictionary (InRoad: trafict light duration). We can use InRoad to fetch Intersection and fetch trafficLight infomation of that road.
	
	To modify class[Gene], such as doing crossover, evolution and muation, we introduce class[GeneEvolve]. This class take two Gene and a mutateRate (default = 0.2). This generates a new Gene by randomly select each traffic light's duration and mutate each duration according to a given mutateRate.

generation.py : This generation class[Generation] takes parameters as (mapLayout, carmap, cars, geneNumber, roundNumber). 	
	
	1. The class[Generation] run a simulation, and update its gene in each round, and out up the result.

	2. To optimize our solution: When we finish each round, we will first sort all our gene in this round, and take the first half of them(the part that performs better), and do the evolvement.
