# File name:      helper_functions.py
# Author:         Dalton Cole

"""Helper file for driver
"""

from board import Board
from shape_base import Shape_base
from shape import Shape
from progressBar import ProgressBar
import sys					# Used for args and exiting
import random 				# Populate population randomly and mutate/permute
import signal				# Used to implement ctrl-c handling
import json 				# Used to read config file and write log file
import os					# Used to make directories if they don't exist
import multiprocessing		# Used to multiprocess each run
#from functools import partial	# Used for ctrl-c handling
from time import time		# Used to seed random number generator
from copy import deepcopy	# Used to make children
from math import ceil

def signal_handler(signal, frame):
	"""Used to gracefully exit when ctrl-c is pressed

	When ctrl-c is pressed, save the solution file and algorithm log file
	before exiting.

	TODO:
		* IMPLEMENT
		* Update Arguments

	Args:
		return_dict (dict {int: list of str}): Dict from each run where
			key is the run number and list of strings is the current
			eval's best fitness function
		config_dict (dict {str: value}): Dictionary of the configurations
		signal (?): Signal
		frame (?): Frame

	"""
	print('You pressed Ctrl+C!')
	"""
	print('return dict')
	print(return_dict)

	print("length: " + str(len(return_dict)))

	# Write to algorithm log file
	write_algorithm_log(config_dict['algorithm_solution_file_path'], \
		config_dict['runs'], return_dict)
	"""
	sys.exit(0)

def config_parser(config_file_name):
	"""Take in config parameters from file and store in dictionary
	This function uses the supplied file name, reads it in, and populates
	a dictionary with it. If a value does not exist in the json file,
	then default values are used.

	Note:
		The defaults are:
			input_file: "input.txt"
			random_seed: int(time())
			search_algorithm: "Random Search"
			runs: 30
			fitness_evaluations: 1000
			population_size: 100
			log_file_path: "./log/<random seed>"
			solution_file_path: "./solution/<random seed>"
			algorithm_solution_file_path: 
				"./log/algorithm_solution/<random seed>"
			offspring_count: population_size // 2
			t_size_parent: 2
			t_size_survival: 2
			mutation_rate: 0.1 (ie 10%)
			convergence: 25
			parent_selection_algorithm: 
				"k-Tournament Selection with replacement"
			recombination_algorithm:
				"Partially Mapped Crossover"
			mutation_algorithm:
				"Both" This means both "Flip" and "Switch"
			survivor_algorithm: "Truncation"
			placement_algorithm: "Minimize"
			survival_strategy: "Plus"

	Args:
		config_file_name (str): File name of configuration JSON file

	Returns:
		(dict {str: value}) Dict of the configuration parameters

	"""
	# Initialize default inputs
	config_dict = {}
	config_dict['input_file'] = 'input.txt'

	# Load JSON config file
	json_config_file = ''
	try:
		with open(str(config_file_name), 'r') as f:
			json_config_file = json.load(f)
	except:
		print("Failed to load file: " + str(config_file_name))
		quit()
	
	# Input File
	try:
		if json_config_file['Input File'] != "":
			config_dict['input_file'] = json_config_file['Input File']
	except:
		pass

	# Random Seed
	config_parser_helper(config_dict, 'random_seed', 'Random Seed', json_config_file, int(time()))

	# Search Algorithm
	config_parser_helper(config_dict, 'search_algorithm', 'Search Algorithm', json_config_file, "Random Search")
		
	# Runs
	config_parser_helper(config_dict, 'runs', 'Runs', json_config_file, 30)

	# Fitness Evaluations
	config_parser_helper(config_dict, 'fitness_evaluations', 'Fitness Evaluations', json_config_file, 1000)

	# Population Size
	config_parser_helper(config_dict, 'population_size', 'Population Size', json_config_file, 100)

	# Log File Path
	config_parser_helper(config_dict, 'log_file_path', 'Log File Path', json_config_file, './logs/' + str(config_dict['random_seed']))

	# Solution File Path
	config_parser_helper(config_dict, 'solution_file_path', 'Solution File Path', json_config_file, './solutions/' + str(config_dict['random_seed']))

	# Offspring Count
	config_parser_helper(config_dict, 'offspring_count', 'Offspring Count', json_config_file, int(config_dict['population_size'] // 2))

	# Tournament Size For Parent Selection
	config_parser_helper(config_dict, 't_size_parent', 'Tournament Size For Parent Selection', json_config_file, 2)

	# Tournament Size For Survival Selection
	config_parser_helper(config_dict, 't_size_survival', 'Tournament Size For Survival Selection', json_config_file, 2) 

	# Mutation Rate
	config_parser_helper(config_dict, 'mutation_rate', 'Mutation Rate', json_config_file, .1)

	# Termination Convergence Criterion
	config_parser_helper(config_dict, 'convergence', 'Termination Convergence Criterion', json_config_file, 25)

	# Parent Selection Algorithm
	config_parser_helper(config_dict, 'parent_selection_algorithm', 'Parent Selection Algorithm', json_config_file, 'k-Tournament Selection with replacement')

	# Recombination Algorithm
	config_parser_helper(config_dict, 'recombination_algorithm', 'Recombination Algorithm', json_config_file, 'Partially Mapped Crossover')

	# Mutation Algorithm
	config_parser_helper(config_dict, 'mutation_algorithm', 'Mutation Algorithm', json_config_file, 'Both')

	# Survivor Algorithm
	config_parser_helper(config_dict, 'survivor_algorithm', 'Survivor Algorithm', json_config_file, 'Truncation')

	# Placement Algorithm
	config_parser_helper(config_dict, 'placement_algorithm', 'Placement Algorithm', json_config_file, 'Minimize')

	# Survival Strategy
	config_parser_helper(config_dict, 'survival_strategy', 'Survival Strategy', json_config_file, 'Plus')

	return config_dict

def config_parser_helper(config_dict, key_string, json_string, json_config_file, default_value):
	"""Helps config_parser by adding an element into config_dict

	Args:
		config_dict (dict {str: val}): Dictionary of configuration values
		key_string (str): String of key value in dictionary
		json_string (str): JSON term corresponding to the key_string
		json_config_file (dict {str: val}): JSON dictionary
		default_value (any): Value for config_dict[key_string] if null in
			json_config_file[json_string]

	Returns:
		Nothing. Modifies config_dict by adding key:value 
	"""
	try:
		if json_config_file[json_string] != '' and json_config_file[json_string] != None:
			config_dict[key_string] = json_config_file[json_string]
		else:
			config_dict[key_string] = default_value
	except:
		config_dict[key_string] = default_value
		print("You need {'", end='')
		print(json_string, end='')
		print("': null} in your JSON File! I'll let  you go this", end='')
		print(" time by using ", end='')
		print(config_dict[key_string], end='')
		print(", but never again will I be this kind!")

def open_file(file):
	"""Open a file and create sub-directories as needed

	Returns:
		(_io.TextIOWrapper) Open file handle
	"""
	# If path to file does not exist, make it
	if not os.path.exists(os.path.dirname(file)):
		os.makedirs(os.path.dirname(file))
	# Return opened file
	return open(file, 'w')

def write_algorithm_log(file, runs, return_dict):
	"""Write evals to algorithm log file, creating sub-directory if needed
	Writes algorithm log's \nin the following format:
		<run number><tab><fitness function value>
	These lines are only written if the fitness function value improves
	
	Args:
		file (str): File to open, including directories
		runs (int): The number of runs completed
		returning_dict (dict {int: str}): Dict to write file to
	"""
	if not os.path.exists(os.path.dirname(file)):
		os.makedirs(os.path.dirname(file))

	with open(file, 'a') as f:
		f.write("\n\nResult Log\n")
		for i in range(runs):
			f.write(return_dict[i][0])
		# Add extra new line for parsing means
		f.write('\n')

def create_log_file(config_dict):
	"""Create log file
	Create a log file in the config_dict['log_file_path'] file.

	The log file has the following format:
		{
			"Problem Instance Files": "../solution/1234567890.txt",
			"Random Seed": "1234567890",
			"Config File": {
				"Random Seed": 1234567890,
				"Search Algorithm": "Random Search",
				"Runs": 20,
				"Fitness Evaluations": 20,
				"Log File Path": "./logs/1234567890.log",
				"Solution File Path": "./solution/1234567890.txt"
			}
			"Algorithm Log File Path:": "../algorithm_log/1234567890.txt"
		}

	"""
	log_dict = {}
	log_dict['Problem Instance Files'] = config_dict['solution_file_path']
	log_dict['Random Seed'] = config_dict['random_seed']
	log_dict['Config File'] = config_dict
	log_dict['Run Time'] = config_dict['run_time']
	log_dict['Input File'] = config_dict['input_file']

	config_dict.pop('input_file', None)
	config_dict.pop('run_time', None)

	# Open file, create directories if needed
	opened_file = open_file(config_dict['log_file_path'])
	# Dump JSON to file in alphabetical order with pretty formatting
	json.dump(log_dict, opened_file, indent=4, sort_keys=True)
	# Close opened file
	opened_file.close()

def create_solution_file(best_board, path, run_number):
	"""Create solution file using the best board from the run

	Use the best board from a run to create a solution file. The solution file
	is formated in the following form:
		x,y,rotation
	One line is printed for each shape in the same order as they were
	originally given.

	Args:
		best_board (Board): Best board from a run
		path (str): Solution file path
		run_number (int): The run number, used to name the file

	"""
	# Open file, create directories if needed
	opened_file = open_file(path)

	# Write x,y,rotation for each shape
	for solution in best_board.get_info():
		opened_file.write(solution + '\n')

	# Close file
	opened_file.close()

def random_search(config_dict, max_height, shape_string_list, population_size, run_number, return_dict):
	"""Does a random search over the search space to find solutions
	This function does a random search over the search space to find a 
	solution. This is done by first, creating a list of all the shapes. This
	is used to populate each Board with random shapes in a random orientation.
	Population_size Boards are originally created. During each evaluation,
	population_size Boards are created and all but 1 are destroyed. When
	the number of evaluations are reached the best result is logged in the
	return_dict.

	Args:
		config_dict (dict: {str: val}): A dictionary of configuration values
		max_height (int): The max height of the board
		shape_string_list (list of str): A list of shapes in string format
		population_size (int): The population size
		run_number (int): This run's number
		return_dict (dict: {int: val}): A dictionary used to store the needed
			solution to be returned to the main process
	"""

	# Seed the random number generator with random_seed + run number
	# This makes each run unique
	random.seed(config_dict['random_seed'] + run_number)

	# Initialize algorithm log string
	return_string = ''

	# Add "Run i" line top of algorithm log file 
	return_string += ('\nRun ' + str(run_number + 1) + '\n')

	# Create a list of all the shapes
	shape_list = []
	for i in range(len(shape_string_list)):
		shape_list.append(Shape_base(shape_string_list[i], i))

	# Start with an empty population
	population = []

	# Set Board's max height
	Board.max_height = max_height
	# Set placement algorithm
	Board.set_placement_algorithm(config_dict['placement_algorithm'])

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		new_board = Board(shape_list)

		# If first board, set max width of board
		if(i == 0):
			Board.max_width = new_board.find_max_width()
			Board.divide_max_width = Board.max_width // 2

		new_board.place_shapes(randomize=True)
		population.append(new_board)

	# Sort from best fit to worst fit
	population.sort(reverse=True)

	# If last run, print progress bar
	print_progress_bar = False
	if run_number + 1 == config_dict['runs']:
		print_progress_bar = True

	progress_bar = 0
	if print_progress_bar:
		progress_bar = ProgressBar(config_dict['fitness_evaluations'])
		progress_bar.printProgressBar(0)

	# Apply fitness evals
	best_fitness = 0
	for current_eval in range(config_dict['fitness_evaluations']):
		if print_progress_bar:
			progress_bar.printProgressBar(current_eval)

		### Apply search algorithm ###
		# Add population_size members to population
		for i in range(population_size):
			new_board = Board(shape_list)
			new_board.place_shapes(randomize=True)
			population.append(new_board)

		# Sort
		population.sort(reverse=True)

		# Take best 1 of population
		for i in range(len(population) - 1):
			population.pop(len(population) - 1)
		##############################

		# If current best fitness is better than previous best fitness
		if population[0].fitness > best_fitness or current_eval == 0:
			# Update best_fitness
			best_fitness = population[0].fitness
			# Add new best fitness to algorithm_log
			return_string += (str(current_eval + 1) + ' \t' + str(best_fitness) + '\n')

		##### DEBUG ####
		"""
		if population[0].test_for_overlap():
			print("BAD BOARD")
			quit()
		"""
		################

	# If printing progress bar, add new line when completed and print 100% completed
	if print_progress_bar:
		progress_bar.printProgressBar(config_dict['fitness_evaluations'])
		print()

	# Add to return dict a tuple of (algorithm log string, best Board)
	return_dict[run_number] = (return_string, population[0])


def get_best_fitness_value(population):
	"""Find the best fitness value out of all the boards in the population

	Args:
		population (list of Board): The current population

	Returns:
		(int): The best fitness eval
	"""
	best_fitness = population[0].fitness
	for board in population:
		if best_fitness < board.fitness:
			best_fitness = board.fitness
	return best_fitness

def get_best_fitness_board(population):
	"""Find the board with the best fitness value

	Args:
		population (list of Board): The population to chose from

	Returns:
		(Board): The board with the best fitness value
	"""
	best_fitness = get_best_fitness_value(population)
	for board in population:
		if board.fitness == best_fitness:
			return board
	print("ERROR IN: get_best_fitness_board")

def get_best_fitness_board_index(population):
	"""Find the best board in the population and return the index of that board
	
	Args:
		population (list of Board): The population to chose from

	Returns:
		(int): The index of the board with the best fitness value
	"""
	best_fitness = get_best_fitness_value(population)
	for i, board in list(enumerate(population)):
		if board.fitness == best_fitness:
			return i
	print("ERROR IN: get_best_fitness_board_index")

def get_average_fitness_value(population):
	"""Find the average fitness value of all the boards in the population

	Args:
		population (list of Board): The current population

	Returns:
		(int): The average fitness value, rounded down
	"""
	average_fitness = 0
	for board in population:
		average_fitness += board.fitness

	return average_fitness // len(population)

############################# Parents #########################################
def find_parents(population, config_dict):
	"""Finds the parents to reproduce using an algorithm specified in configs

	Args:
		population (list of Board): The current population
		config_dict (dict {str: val}): Contains the algorithm to use in
			config_dict['parent_selection_algorithm']

	Returns:
		(list of Board): The parents
	"""
	# Call k tournament function if specified
	if config_dict['parent_selection_algorithm'] == 'k-Tournament Selection with replacement':
		# Use t_size_parent as the k, 2 * offspring for number of parents
		return k_tournament_selection_with_replacement(population, config_dict['t_size_parent'], config_dict['offspring_count'])
	elif config_dict['parent_selection_algorithm'] == 'Fitness Proportional Selection':
		return fitness_proportional_selection(population, config_dict['offspring_count'])
	elif config_dict['parent_selection_algorithm'] == 'Uniform Random':
		return uniform_random_parent_selection(population, config_dict['offspring_count'])

	print("ERROR IN: find_parents"); quit()


def k_tournament_selection_with_replacement(population, t_size, number_of_parents):
	"""Create a population using k-tournament with replacement

	Args:
		population (list of Board): A population of Boards
		t_size (int): The size of each tournament
		number_of_parents (int): The size of the returned population
			Should be less than the size of the population

	Returns:
		(list of Board): A new population of size number_of_parents 
			that was selected using k-tournament with replacement
	"""
	parents = []
	# If tournament size is greater than population size, use population size
	if t_size > len(population):
		t_size = len(population)

	# While we need more parents, add parents
	while len(parents) < number_of_parents:
		# Randomly chose t_size boards from the population
		# Append best board to parents list
		parents.append(get_best_fitness_board(random.sample(population, t_size)))

	return parents

def k_tournament_selection_without_replacement(population, t_size, return_population_size):
	"""Create a population using k-tournament without replacement

	Args:
		population (list of Board): A population of Boards
		t_size (int): The size of each tournament
		return_population_size (int): The size of the returned population
			Should be less than the size of the population

	Returns:
		(list of Board): A new population of size return_population_size 
			that was selected using k-tournament without replacement
	"""
	# New population list
	new_population = []
	# Create a set of indexes form 0 to len(pop)
	# This is so we don't have to remote elements from the population for speed
	index_set = {x for x in range(len(population))}

	# While we need more elements in the new population
	while len(new_population) < return_population_size:
		#person = get_best_fitness_board(random.sample(population, t_size))
		#new_population.append(person)
		sample_list = []
		# Get t_size number of elements from index_set, or as many
		# as possible if there are not t_size elements left
		try:
			sample_list = random.sample(index_set, t_size)
		except:
			sample_list = random.sample(index_set, len(index_set) - 1)

		# Create small population
		population_list = [population[x] for x in sample_list]

		# Find the index of the best fitness value
		best_fitness_index = get_best_fitness_board_index(population_list)

		# Add element to new population
		new_population.append(population[best_fitness_index])

		# Remove element from original population's index_set
		index_set.remove(sample_list[best_fitness_index])

	return new_population

def fitness_proportional_selection(population, offspring_count):
	"""Create a population using fitness proportional selection

	Args:
		population (list of Board): A population of Boards
		offspring_count (int): The size of the returned population

	Returns:
		(list of Board): A new population of size return_population_size 
			that was selected using fitness proportional selection
	"""
	# Create an empty chosen parents list
	chosen_parents = []

	# While more parents are needed
	while len(chosen_parents) < offspring_count:
		# Initialize total fitness
		total_fitness = 0
		# Find total fitness
		for board in population:
			# Board fitness is negative, so negate it
			total_fitness -= board.fitness

		# Randomly chose a value
		chosen_fitness = random.randrange(0, total_fitness)

		# Find chosen value in possible parents
		tracked_fitness = 0
		for board in population:
			tracked_fitness -= board.fitness
			# If chosen value is found, add it to chosen parents, and
			# remove it from possible parents 
			if chosen_fitness <= tracked_fitness:
				chosen_parents.append(board)
				break

	return chosen_parents
	"""
	# If population is smaller than needed parents, raise error
	if len(population) < offspring_count:
		print("ERROR in: fitness_proportional_selection")

	# Create a copy list of the population
	possible_parents = list(population)
	# Create an empty chosen parents list
	chosen_parents = []

	# While more parents are needed
	while len(chosen_parents) < offspring_count:
		# Initialize total fitness
		total_fitness = 0
		# Find total fitness
		for board in possible_parents:
			# Board fitness is negative, so negate it
			total_fitness -= board.fitness

		# Randomly chose a value
		chosen_fitness = random.randrange(0, total_fitness)

		# Find chosen value in possible parents
		tracked_fitness = 0
		for board in possible_parents:
			tracked_fitness -= board.fitness
			# If chosen value is found, add it to chosen parents, and
			# remove it from possible parents 
			if chosen_fitness <= tracked_fitness:
				chosen_parents.append(board)
				possible_parents.remove(board)
				break

	return chosen_parents
	"""

def uniform_random_parent_selection(population, offspring_count):
	"""Create a population randomly

	Args:
		population (list of Board): A population of Boards
		offspring_count (int): The size of the returned population

	Returns:
		(list of Board): A new population of size return_population_size 
			that was selected randomly
	"""
	# Create an empty chosen parents list
	chosen_parents = []

	# While more parents are needed
	while len(chosen_parents) < offspring_count:
		# Randomly select a parent
		chosen_parents.append(random.choice(population))

	return chosen_parents

############################# Children ########################################
def make_children(parents, config_dict):
	"""Makes the number of children specified in the config_dict
	This is done using the algorithm specified in config_dict.

	Args:
		parents (list of Board): The population to make children from
		config_dict (dict {str: val}): Configuration parameters
			'offspring_count' will be used as the number of children
			'recombination_algorithm' will be the algorithm used

	Returns:
		(list of Board): The created children
	"""
	# Initialize children list
	children_list = []

	# If using PMX
	if config_dict['recombination_algorithm'] == 'Partially Mapped Crossover':
		# For each pair of parents
		for i in range(0, len(parents), 2):
			# Make a baby! :D
			children_list.append(partially_mapped_crossover(parents[i], parents[i + 1], config_dict))
			children_list.append(partially_mapped_crossover(parents[i + 1], parents[i], config_dict))

	elif config_dict['recombination_algorithm'] == 'Order Crossover':
		# For each pair of parents
		for i in range(0, len(parents), 2):
			# Make a baby! :D
			children_list.append(order_crossover(parents[i], parents[i + 1], config_dict))
			children_list.append(order_crossover(parents[i + 1], parents[i], config_dict))

	"""
	# If any shapes overlap with another shape, randomly place second overlapping shape
	if config_dict['placement_algorithm'] != 'Minimize':
		for board in children_list:
			board.check_for_overlap()
	"""

	return children_list
	"""
	elif config_dict['recombination_algorithm'] == 'Cycle Crossover':
		# For each pair of parents
		for i in range(0, len(parents), 2):
			# Make a baby! :D
			children_list.append(cycle_crossover(parents[i], parents[i + 1], config_dict))
			children_list.append(cycle_crossover(parents[i + 1], parents[i], config_dict))

		return children_list
	"""

def partially_mapped_crossover(parent1, parent2, config_dict):
	"""Partially mapped crossover algorithm to make children
	Apply PMX by using two randomly chosen crossover points

	If there are only 3 or fewer shapes on the board, return parent1

	Args:
		parent1 (Board): Parent 1
		parent2 (Board): Parent 2

	Returns:
		(Board): Child
	"""
	if len(parent1) <= 3:
		return parent1

	point1 = random.randrange(1, len(parent1) - 3)
	point2 = random.randrange(point1 + 1, len(parent1))

	child = Board(config_dict['shape_list'])
	included_set = set()

	for i in range(point1, point2):
		child[i] = parent1[i]
		included_set.add(child[i].get_original_order())

	for i in range(point1, point2):
		if parent2[i].get_original_order() not in included_set:
			other_spot = parent2.find_original_order(parent1[i].get_original_order())
			child[other_spot] = parent2[i]
			included_set.add(parent2[i].get_original_order())

	for i in range(len(parent1)):
		if parent2[i] not in included_set:
			child[i] = parent2[i]
			included_set.add(parent2[i].get_original_order())

	if len(included_set) != len(parent1):
		print("ERROR IN: partially_mapped_crossover")

	return child

def order_crossover(parent1, parent2, config_dict):
	"""Ordered crossover algorithm to make children
	Apply Ordered Crossover by using two randomly 
	chosen crossover points.

	If there are only 3 or fewer shapes on the board, return parent1

	Args:
		parent1 (Board): Parent 1
		parent2 (Board): Parent 2

	Returns:
		(Board): Child
	"""
	if len(parent1) <= 3:
		print("ERROR IN: order_crossover")
		return parent1

	# Randomly pick two points
	point1 = random.randrange(1, len(parent1) - 3)
	point2 = random.randrange(point1 + 1, len(parent1) - 1)

	# Initialize child
	child = Board(config_dict['shape_list'])
	# Initialize included set
	included_set = set()

	# Copy shapes in between points 1 and 2 from parent 1
	for i in range(point1, point2):
		child[i] = parent1[i]
		included_set.add(child[i].get_original_order())

	# Where to start copying from in parent 2
	current_child_index = point2
	current_parent2_index = point2

	# While there are more shapes to add
	while len(included_set) < len(parent1):
		# If shape not already in child
		if parent2[current_parent2_index].get_original_order() not in included_set:
			# Add shape to child at given index
			child[current_child_index] = parent2[current_parent2_index]
			# Add it to included set
			included_set.add(child[current_child_index].get_original_order())
			# Increment counters
			current_child_index = (current_child_index + 1) % len(parent2)
			current_parent2_index = (current_parent2_index + 1) % len(parent2)
		else:
			# Increment parent 2 index
			current_parent2_index = (current_parent2_index + 1) % len(parent2)

	if len(included_set) != len(parent1):
		print("ERROR IN: partially_mapped_crossover")

	return child

"""
def cycle_crossover(parent1, parent2, config_dict):
	###Ordered crossover algorithm to make children
	Apply Ordered Crossover by using two randomly 
	chosen crossover points.

	If there are only 3 or fewer shapes on the board, return parent1

	Args:
		parent1 (Board): Parent 1
		parent2 (Board): Parent 2

	Returns:
		(Board): Child
	###
	if len(parent1) <= 3:
		print("ERROR IN: order_crossover")
		return parent1

	included_set = set()
	current_index = 0
	current_cycle = 1

	relative_parent = None
	other_parent = None

	while len(included_set) < len(parent1):
		# If current parent's value is in child, continue
		if current_cycle % 2 == 1:
			if parent1[current_index].get_original_order() in included_set:
				current_index += 1
				continue
			relative_parent = parent1
			other_parent = parent2
		else:
			if parent2[current_index].get_original_order() in included_set:
				current_index += 1
				continue
			relative_parent = parent2
			other_parent = parent1
		# Find cycle
		parents_index = set()
		parents_index.add(current_index)
		current_parent_index = current_index
		set_size = len(parents_index)
		while True:
			current_parent_index = find_order_index(other_parent, )
"""

def find_order_index(population, order_number):
	"""Find index of order_number in population
	Args:
		parents (list of Board): The population to look through
		order_number (int): The shape number to look for

	Returns:
		(int): The requested index
	"""
	for i in range(len(population)):
		if population[i].get_original_order() == order_number:
			return i

	print("ERROR IN: find_order_index")
	return

############################# Mutation ########################################
def mutate_population(population, config_dict):
	"""Mutates the population with the given algorithm and rate in config_dict
	Mutates the population variable given the values in config_dict

	Args:
		parents (list of Board): The population to mutate
		config_dict (dict {str: val}): Configuration parameters
			'mutation_rate' Rate of mutation between [0,1]
			'mutation_algorithm' will be the algorithm used

	Returns:
		Nothing, alters population
	"""
	if config_dict['mutation_algorithm'] == 'Flip':
		mutate_flip(population, config_dict)
	elif config_dict['mutation_algorithm'] == 'Switch':
		mutate_switch(population, config_dict)
	elif config_dict['mutation_algorithm'] == 'Both':
		mutate_flip(population, config_dict)
		mutate_switch(population, config_dict)
	elif config_dict['mutation_algorithm'] == 'Shuffle':
		mutate_shuffle(population, config_dict)
	elif config_dict['mutation_algorithm'] == 'Move':
		mutate_move(population, config_dict)

	# If employing minimize strategy, minimize board
	if config_dict['placement_algorithm'] == 'Minimize':
		for board in population:
			board.place_shapes()

	return

def mutate_flip(population, config_dict):
	"""Flips each shape of each board with the probability given in config_dict

	Args:
		population (list of Board): Population to mutate
		config_dict (dict {str: val}): Configuration parameters
			'mutation_rate' is the rate of mutation

	Returns:
		Nothing, alters the population
	"""
	for board in population:
		for shape in board.shapes:
			if random.uniform(0, 1) < config_dict['mutation_rate']:
				shape.update_orientation(random.randrange(4))

def mutate_switch(population, config_dict):
	"""Flips two shapes given a probability of flipping for each shape in pop
	For each shape in each board in pop, there is a 
	config_dict['mutation_rate'] chance of switching that shape and another
	shape

	Args:
		population (list of Board): Population to mutate
		config_dict (dict {str: val}): Configuration parameters
			'mutation_rate' is the rate of mutation

	Returns:
		Nothing, alters the population
	"""
	num_shapes_in_board = len(population[0])
	for board in population:
		for i in range(num_shapes_in_board):
			if random.uniform(0, 1) < config_dict['mutation_rate']:
				switch_with = random.randrange(0, num_shapes_in_board)
				board[i], board[switch_with] = board[switch_with], board[i]

def mutate_shuffle(population, config_dict):
	"""Shuffles shapes between two random points

	The two points are chosen by random, and the size in-between those two
	points is mutation_rate * number of shapes

	Args:
		population (list of Board): Population to mutate
		config_dict (dict {str: val}): Configuration parameters
			'mutation_rate' is the rate of mutation

	Returns:
		Nothing, alters the population
	"""
	point = random.randrange(0, len(population))

	pop_length = len(population[0])
	upper_bound = int(ceil(pop_length * config_dict['mutation_rate']))

	for board in population:
		point = random.randrange(0, pop_length - upper_bound)
		shuffled = board[point:point+upper_bound]
		random.shuffle(shuffled)

		shuffled_index = 0
		for i in range(point, point + upper_bound):
			#print(str(i) + '\t' + str(shuffled_index))
			board[i] = shuffled[shuffled_index]
			shuffled_index += 1

def mutate_move(population, config_dict):
	"""Randomly re-places shapes

	Re-place a shape. Each shape has a 'mutation_rate' chance of being
	re-placed.

	Args:
		population (list of Board): Population to mutate
		config_dict (dict {str: val}): Configuration parameters
			'mutation_rate' is the rate of mutation

	Returns:
		Nothing, alters the population
	"""
	num_shapes_in_board = len(population[0])
	for board in population:
		for i in range(num_shapes_in_board):
			if random.uniform(0,1) < config_dict['mutation_rate']:
				board.random_replacement(i)
		board.update_fitness_value()



###########################Survivor Selection #################################
def select_survivors(population, config_dict):
	"""Select survivors form the population according to config_dict parameters

	Args:
		population (list of Board): Population to kill! I mean, reduce
		config_dict (dict {str: val}): Configuration parameters
			'population_size': End population size
			't_size_survival': Tournament size
			'survivor_algorithm': Algorithm to use

	Returns:
		Nothing, alters population
	"""
	if config_dict['survivor_algorithm'] == 'Truncation':
		survivor_selection_truncation(population, config_dict)
	elif config_dict['survivor_algorithm'] == 'k-Tournament Selection without replacement':
		new_pop = survivor_selection_k_tournament_without_replacement(population, config_dict)
		del population[:]
		for board in new_pop:
			population.append(board)
	elif config_dict['survivor_algorithm'] == 'Uniform Random':
		survivor_selection_uniform_random(population, config_dict)
	elif config_dict['survivor_algorithm'] == 'Fitness Proportional Selection':
		new_pop = fitness_proportional_selection(population, config_dict['population_size'])
		del population[:]
		for board in new_pop:
			population.append(board)

def survivor_selection_truncation(population, config_dict):
	"""Select the best n survivors from the population

	Args:
		population (list of Board): Population to kill! I mean, reduce
		config_dict (dict {str: val}): Configuration parameters
			'population_size': End population size

	Returns:
		Nothing, alters population
	"""
	# Sort elements from best to worst
	population.sort(reverse=True)

	# While there are too many people, I mean boards, kill the worst ones
	while len(population) > config_dict['population_size']:
		# Remove from back
		del population[-1]

def survivor_selection_k_tournament_without_replacement(population, config_dict):
	"""Select the best n survivors from by population by conducting a tournament

	Args:
		population (list of Board): Population to kill
		config_dict (dict {str: val}): Configuration parameters
			'population_size': End population size
			't_size_survival': Size of the tournament

	Returns:
		(list of Board): The new population
	"""
	new_pop = k_tournament_selection_without_replacement(population, \
		config_dict['t_size_survival'], config_dict['population_size'])
	return new_pop


def survivor_selection_uniform_random(population, config_dict):
	"""Select random survivors

	Args:
		population (list of Board): Population to kill
		config_dict (dict {str: val}): Configuration parameters
			'population_size': End population size

	Returns:
		Nothing, alters the population
	"""
	# Shuffle population
	random.shuffle(population)

	# While there are too many boards
	while len(population) > config_dict['population_size']:
		# remove last board
		del population[-1]

################################### EA ########################################
def ea_search(config_dict, max_height, shape_string_list, population_size, run_number, return_dict):
	"""Perform EA search

	Args:
		config_dict (dict: {str: val}): A dictionary of configuration values
		max_height (int): The max height of the board
		shape_string_list (list of str): A list of shapes in string format
		population_size (int): The population size
		run_number (int): This run's number
		return_dict (dict: {int: val}): A dictionary used to store the needed
			solution to be returned to the main process
	"""

	# Seed the random number generator with random_seed + run number
	# This makes each run unique
	random.seed(config_dict['random_seed'] + run_number)

	# Initialize algorithm log
	algorithm_log_string = ''

	# Add "Run i" line top of algorithm log file 
	algorithm_log_string += ('\nRun ' + str(run_number + 1) + '\n')

	# Create a list of all the shapes and add to config_dict
	shape_list = []
	for i in range(len(shape_string_list)):
		shape_list.append(Shape_base(shape_string_list[i], i))
	config_dict['shape_list'] = shape_list

	# Start with an empty population
	population = []

	# Set Board's max height
	Board.max_height = max_height
	# Set Placement Algorithm
	Board.set_placement_algorithm(config_dict['placement_algorithm'])

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		new_board = Board(shape_list)

		# If first board, set max width of board
		if(i == 0):
			Board.max_width = new_board.find_max_width()
			Board.divide_max_width = Board.max_width // 2

		new_board.place_shapes(randomize=True)
		population.append(new_board)

	# If last run, print progress bar
	print_progress_bar = False
	if run_number + 1 == config_dict['runs']:
		print_progress_bar = True

	# Initialize progress_bar if last run
	progress_bar = 0
	if print_progress_bar:
		progress_bar = ProgressBar(config_dict['fitness_evaluations'])
		progress_bar.printProgressBar(0)

	### Set Stoping Creteria ###
	# Set Current evaluation number to population size
	current_eval = population_size
	# Current fitness
	best_fitness = 0
	average_fitness = 0
	# Times with same fitness
	same_fitness = 0
	same_average_fitness = 0
	# Previous fitness
	previous_fitness = get_best_fitness_value(population)
	previous_average_fitness = get_average_fitness_value(population)

	# Row 0 of algorithm log 
	algorithm_log_string += str(len(population)) + '\t' + 	str(previous_average_fitness) + '\t' + str(previous_fitness) + '\n'

	# While not at stoping creteria, continue
	while current_eval < config_dict['fitness_evaluations'] and same_fitness < config_dict['convergence'] and same_average_fitness < config_dict['convergence']:
		# Increment evaulation count by children count
		current_eval += config_dict['offspring_count']

		# Print progress bar if last run
		if print_progress_bar:
			progress_bar.printProgressBar(current_eval)

		# Find the parents
		parents = find_parents(population, config_dict)

		# Make children
		children = make_children(parents, config_dict)

		# Mutate children
		mutate_population(children, config_dict)

		# Set population
		if config_dict['survival_strategy'] == "Plus":
			# Add children
			population += children
		elif config_dict['survival_strategy'] == 'Comma':
			# Make population only children
			population = children

		# Survival Selection
		select_survivors(population, config_dict)

		### If not population size, make random new ###
		population = list(set(population))
		while len(population) != population_size:
			temp = Board(shape_list)
			temp.place_shapes(randomize=True)
			population.append(temp)
		###############################################
		
		# Find best and average fitness
		best_fitness = get_best_fitness_value(population)
		average_fitness = get_average_fitness_value(population)

		# Update stopping criteria
		if best_fitness == previous_fitness:
			same_fitness += config_dict['offspring_count']
		else:
			previous_fitness = best_fitness
			same_fitness = 0

		if average_fitness == previous_average_fitness:
			same_average_fitness += config_dict['offspring_count']
		else:
			previous_average_fitness = average_fitness
			same_average_fitness = 0

		### Algorithm Log ###
		algorithm_log_string += str(current_eval) + '\t' + 	str(average_fitness) + '\t' + str(best_fitness) + '\n'	
		#####################

	# If printing progress bar, add new line when completed and print 100% completed
	if print_progress_bar:
		progress_bar.printProgressBar(config_dict['fitness_evaluations'])
		print()

	population.sort(reverse=True)
	# Put (algorithm log, best board) in return dictionary
	return_dict[run_number] = (algorithm_log_string, population[0])


	"""
	##### DEBUG ####
	if population[0].test_for_overlap():
		print("BAD BOARD")
		quit()
	################
	print(current_eval)
	print(same_fitness)
	print(population[0].fitness)

	population.sort(reverse=True)
	test = ''
	for i in population[0].get_info():
		test += (i + '\n')

	with open('test2', 'w') as f:
		f.write(test)
	"""