# EC Assignment 1a

## General Info

* Name: Dalton Cole
* Email: drcgy5@mst.edu
* Assignment: COMP SCI 5401 FS2017 Assignment 1a

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

The configuation file used to feed into the program. The default format is the following:
```
{
	"Random Seed": 1,
	"Search Algorithm": "Random Search",
	"Runs": 30,
	"Fitness Evaluations": 1000,
	"Population Size": 1,
	"Log File Path": "./logs/1",
	"Solution File Path": "./solution/1/",
	"Algorithm Solution File Path": "./logs/algorithm_solution/"
}
```

If any of the above are null, then default values are used. The default "Random Seed" is time. Log and solution files generated have the same name as "Random Seed".

### logs/

The default file path for log files.

### solutions/<random seed>/

The default file path for solution files.

### logs/algorithm_solution/

The default file path for algorithm solution files.

### graphs/

Directory where graph.py script and *.png files reside.

### inputs/

Directory with default inputs.