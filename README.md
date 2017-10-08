# EC Assignment 1b

## General Info

* Name: Dalton Cole
* Email: drcgy5@mst.edu
* Assignment: COMP SCI 5401 FS2017 Assignment 1b

## Description

For this assignment, the task is to implement the Cutting Stock Problem by implementing a random search evolutionary algorithm. This is done by randomly creating a new "board" state with the "shapes" by placing shapes in random orientation in a random order.

In detail, this is done by creating a list of boards that represents the population. For each evaluation step, the populations doubles and is sorted by highest fitness to lowest. Fitness value is calculated as -(length of board used). The top n of the population is selected to go onto the next eval, where n the the size of the original population. This process continues until the number of evals specified in the config.json file is reached.

The above process is done for each run. Currently runs are done in parallel. 

## How to run
```
./run.sh <config.json> <problem file>
```

## File Descriptions

### shape.py

Creates each individual shape

### board.py

A collection of shapes that have been placed on a grid.

The way placement works is by finding the first place in  occupied_squares where the current point of the current shape can be placed. It then continues with the rest of the points in that shape until all points are placed in occupied_squares. After placement, the shape's offset is updated with the correct x and y values. Any square that is left of the last placed shape is removed from ocupied_squares and all squares are shifted left such that the left most part of the placed shape is [0, y]. This is done to reduce the length of occupied_squares and speed up the 'in' operation performed.

### helper_functions.py

A collection of functions that help the driver

### driver.py

The face of the program

### config.json

The configuation file used to feed into the program. There are the following options (**bold** represents default):
* Random Seed:
	* Any Int
	* **Time in seconds since epoch**
* Search Algorithm:
	* **"Random Search"**
	* "EA"
* Runs
	* Any Int
	* **30**
* Fitness Evaulations
	* Any Int
	* **1000**
* Population Size
	* Any Int
	* **100**
* Log File Path
	* File path from running directory or absolute
	* **/log/(random seed)**
* Solution File Path
	* File path from running directory or absolute
	* **/solution/(random seed)**
* Offspring Count
	* Any Int
	* **µ // 2**
* Tournament Size For Parent Selection
	* Any Int < population
	* **2**
* Tournament Size For Survival Selection
	* Any Int < population
	* **2**
* Mutation Rate
	* Float between (0,1)
	* **0.1**
* Termination Convergence Criterion:
	* Any Int < Fitness Evaulations
	* **100**
* Parent Selection Algorithm
	* **k-Tournament Selection with replacement**
	* Fitness Proportional Selection
* Recombination Algorithm
	* **Partially Mapped Crossover**
	* Order Crossover
* Mutation Algorithm
	* Flip
		* Rotate shape
	* Switch
		* Swap placement of two shapes (Only useful if using Placement Algorithm "Minimize")
	* **Both** flip and switch
	* Shuffle
	  * Shuffles the shapes in-between two points of size (Mutation Rate * # of Shapes)
	  * Only useful if using Placement Algorithm "Minimize"
	* Move
		* Randomly re-places a shape
		* Note useful with Placement Algorithm "Minimize"

* Survivor Algorithm
	* **Truncation**
	* k-Tournament Selection without replacement
* Placement Algorithm
	* **Minimize**
	* Random
		* This randomly places shapes on the board. Must be selected if using repair function.
	* Random with Repair
		* Randomly place shapes. Uses a repair function if a shape is invalidly placed instead of randomly choosing a new point right away. 
		* Repair works by trying to place the shape (x + x_move, y + y_move) moves over. It attempts this n times.
			* Internal Defaults:
				* n = 2
				* x_move = -1
				* y_move = -1
* Survivor Strategy
	* **Plus**
		* Combines parent and child generations before survival selection
	* Comma 
		* Survivor selection is only done on the children
		* Note: "Offspring Count" should be larger than "Population Size"


If any of the above are null, then default values are used. The default "Random Seed" is time. Log and solution files generated have the same name as "Random Seed".

### logs/

The default file path for log files.

### solutions/\<random seed\>/

The default file path for solution files.

### logs/algorithm_solution/

The default file path for algorithm solution files.

### graphs/

Directory where graph.py script and \*.png files reside.

### inputs/

Directory with default inputs.

### EC Assignment 1a.pdf

File containing the three graphs in pdf format.