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
	config_parser_helper(config_dict, 'population_size', 'µ, Population Size', json_config_file, 100)

	# Log File Path
	config_parser_helper(config_dict, 'log_file_path', 'Log File Path', json_config_file, './logs/' + str(config_dict['random_seed']))

	# Solution File Path
	config_parser_helper(config_dict, 'solution_file_path', 'Solution File Path', json_config_file, './solutions/' + str(config_dict['random_seed']))

	# Offspring Count
	config_parser_helper(config_dict, 'offspring_count', 'λ, Offspring Count', json_config_file, int(config_dict['population_size'] // 2))

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

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		new_board = Board(shape_list)
		new_board.shuffle_minimize()
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
			new_board.shuffle_minimize()
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

		return children_list

	print('ERROR IN: make_children'); quit()

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

"""
def order_crossover(parent1, parent2, config_dict):

	if len(parent1) <= 3:
		return parent1

	point1 = random.randrange(1, len(parent1) - 3)
	point2 = random.randrange(point1 + 1, len(parent1))

	child = Board(config_dict['shape_list'])
	included_set = set()

	for i in range(point1, point2):
		child[i] = parent1[i]
		included_set.add(child[i].get_original_order())

	for i in range(len(parent1)):
		##########################

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
"""



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
	if config_dict['survivor_algorithm'] == 'k-Tournament Selection without replacement':
		new_pop = survivor_selection_k_tournament_without_replacement(population, config_dict)
		del population[:]
		for person in new_pop:
			population.append(person)


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


def ea_search(config_dict, max_height, shape_string_list, population_size, run_number, return_dict):
	"""

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

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		new_board = Board(shape_list)
		new_board.shuffle_minimize()
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
	# Current evaluation number
	current_eval = 0
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
		# Increment evaulation count
		current_eval += 1

		# Print progress bar if last run
		if print_progress_bar:
			progress_bar.printProgressBar(current_eval)

		# Find the parents
		parents = find_parents(population, config_dict)

		# Make and add children
		population += make_children(parents, config_dict)

		# Mutate
		mutate_population(population, config_dict)

		# Minimize Boards
		for board in population:
			board.minimize()

		# Survival Selection
		select_survivors(population, config_dict)

		# Find best and average fitness
		best_fitness = get_best_fitness_value(population)
		average_fitness = get_average_fitness_value(population)

		# Update stopping criteria
		if best_fitness == previous_fitness:
			same_fitness += 1
		else:
			previous_fitness = best_fitness
			same_fitness = 0

		if average_fitness == previous_average_fitness:
			same_average_fitness += 1
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