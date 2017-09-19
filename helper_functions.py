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
			t_size_parent: population_size // 2
			t_size_survival: int(population_size * .9)
			mutation_rate: 10 (ie 10%)
			convergence: 25
			parent_selection_algorithm: 
				"k-Tournament Selection with replacement"

	Args:
		config_file_name (str): File name of configuration JSON file

	Returns:
		(dict {str: value}) Dict of the configuration parameters

	"""
	# Initialize default inputs
	config_dict = {}
	config_dict['input_file'] = 'input.txt'
	config_dict['random_seed'] = int(time())
	config_dict['search_algorithm'] = "Random Search"
	config_dict['runs'] = 30
	config_dict['fitness_evaluations'] = 1000
	config_dict['population_size'] = 100
	config_dict['log_file_path'] = ''
	config_dict['solution_file_path'] = ''
	config_dict['algorithm_solution_file_path'] = ''
	config_dict['offspring_count'] = 0
	config_dict['t_size_parent'] = 0
	config_dict['t_size_survival'] = int(config_dict['population_size'] * .9)
	config_dict['mutation_rate'] = 10
	config_dict['convergence'] = 25
	config_dict['parent_selection_algorithm'] = 'k-Tournament Selection with replacement'

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
	try:
		if json_config_file['Random Seed'] != None:
			config_dict['random_seed'] = int(json_config_file['Random Seed'])
	except:
		print("You need {'Random Seed': int} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['random_seed']) + " but \
			never again will I be this kind!")

	# Search Algorithm
	try:
		if json_config_file['Search Algorithm'] != ''  and json_config_file['Search Algorithm'] != None:
			config_dict['search_algorithm'] = json_config_file['Search Algorithm']
	except:
		print("You need {'Search Algorithm': ''} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['search_algorithm']) + " \
			but never again will I be this kind!")
		
	# Runs
	try:
		if json_config_file['Runs'] != None:
			config_dict['runs'] = int(json_config_file['Runs'])
	except:
		print("You need {'Runs': int} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['runs']) + " \
			but never again will I be this kind!")

	# Fitness Evaluations
	try:
		if json_config_file['Fitness Evaluations'] != None:
			config_dict['fitness_evaluations'] = int(json_config_file['Fitness Evaluations'])
	except:
		print("You need {'Fitness Evaluations': int} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['fitness_evaluations']) + " \
			but never again will I be this kind!")

	# Population Size
	try:
		if json_config_file['µ, Population Size'] != None:
			config_dict['population_size'] = int(json_config_file['µ, Population Size'])
	except:
		print("You need {'Population Size': int} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['population_size']) + " \
			but never again will I be this kind!")

	# Log File Path
	try:
		if json_config_file['Log File Path'] != '' and json_config_file['Log File Path'] != None:
			config_dict['log_file_path'] = json_config_file['Log File Path']
		else:
			config_dict['log_file_path'] = './logs/' + str(config_dict['random_seed'])
	except:
		config_dict['log_file_path'] = './logs/' + str(config_dict['random_seed'])
		print("You need {'Log File Path': ''} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['log_file_path']) + " \
			but never again will I be this kind!")

	# Solution File Path
	try:
		if json_config_file['Solution File Path'] != '' and json_config_file['Solution File Path'] != None:
			config_dict['solution_file_path'] = json_config_file['Solution File Path']
		else:
			config_dict['solution_file_path'] = './solutions/' + str(config_dict['random_seed']) + '/'
	except:
		config_dict['solution_file_path'] = './solutions/' + str(config_dict['random_seed']) + '/'
		print("You need {'Solution File Path': ''} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['solution_file_path']) + " \
			but never again will I be this kind!")

	# Algorithm Solution File Path
	try:
		if json_config_file['Algorithm Solution File Path'] != '' and json_config_file['Algorithm Solution File Path'] != None:
			config_dict['algorithm_solution_file_path'] = json_config_file['Algorithm Solution File Path']
		else:
			config_dict['algorithm_solution_file_path'] = './logs/algorithm_solution/' + str(config_dict['random_seed'])
	except:
		config_dict['algorithm_solution_file_path'] = './logs/algorithm_solution/' + str(config_dict['random_seed'])
		print("You need {'Algorithm Solution File Path': ''} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['algorithm_solution_file_path']) + " \
			but never again will I be this kind!")

	# Offspring Count
	try:
		if json_config_file['λ, Offspring Count'] != '' and json_config_file['λ, Offspring Count'] != None:
			config_dict['offspring_count'] = json_config_file['λ, Offspring Count']
		else:
			config_dict['offspring_count'] = config_dict['population_size'] // 2
	except:
		config_dict['offspring_count'] = config_dict['population_size'] // 2
		print("You need {'λ, Offspring Count': null} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['offspring_count']) + " \
			but never again will I be this kind!")

	# Tournament Size For Parent Selection
	try:
		if json_config_file['Tournament Size For Parent Selection'] != '' and json_config_file['Tournament Size For Parent Selection'] != None:
			config_dict['t_size_parent'] = json_config_file['Tournament Size For Parent Selection']
		else:
			config_dict['t_size_parent'] = config_dict['population_size'] // 2
	except:
		config_dict['t_size_parent'] = config_dict['population_size'] // 2
		print("You need {'Tournament Size For Parent Selection': null} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['t_size_parent']) + " \
			but never again will I be this kind!") 

	# Tournament Size For Survival Selection
	try:
		if json_config_file['Tournament Size For Survival Selection'] != '' and json_config_file['Tournament Size For Survival Selection'] != None:
			config_dict['t_size_survival'] = json_config_file['Tournament Size For Survival Selection']
		else:
			config_dict['t_size_survival'] = int(config_dict['population_size'] *.9)
	except:
		config_dict['t_size_survival'] = int(config_dict['population_size'] * .9)
		print("You need {'Tournament Size For Survival Selection': null} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['t_size_survival']) + " \
			but never again will I be this kind!") 

	# Mutation Rate
	try:
		if json_config_file['Mutation Rate %'] != '' and json_config_file['Mutation Rate %'] != None:
			config_dict['mutation_rate'] = json_config_file['Mutation Rate %']
		else:
			config_dict['mutation_rate'] = 10
	except:
		config_dict['mutation_rate'] = 10
		print("You need {'Mutation Rate %': null} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['mutation_rate']) + " \
			but never again will I be this kind!") 

	# Termination Convergence Criterion
	try:
		if json_config_file['Termination Convergence Criterion'] != '' and json_config_file['Termination Convergence Criterion'] != None:
			config_dict['convergence'] = json_config_file['Termination Convergence Criterion']
		else:
			config_dict['convergence'] = 25
	except:
		config_dict['convergence'] = 25
		print("You need {'Termination Convergence Criterion': null} in your JSON File! I'll let you \
			go this time by using " + str(config_dict['convergence']) + " \
			but never again will I be this kind!") 

	return config_dict

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

	with open(file, 'w') as f:
		f.write("Result Log\n")
		for i in range(runs):
			f.write(return_dict[i])

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
	log_dict['Algorithm Log File Path'] = config_dict['algorithm_solution_file_path']
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
	opened_file = open_file(path + str(run_number))

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

	# Initialize return_dict with an empty string
	return_dict[run_number] = ''

	# Add "Run i" line top of algorithm log file 
	return_dict[run_number] += ('\nRun ' + str(run_number + 1) + '\n')

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
			return_dict[run_number] += (str(current_eval + 1) + ' \t' + str(best_fitness) + '\n')

		##### DEBUG ####
		if population[0].test_for_overlap():
			print("BAD BOARD")
			quit()
		################

	# If printing progress bar, add new line when completed and print 100% completed
	if print_progress_bar:
		progress_bar.printProgressBar(config_dict['fitness_evaluations'])
		print()

	# Create solution log from best Board in the population
	create_solution_file(population[0], config_dict['solution_file_path'], run_number + 1)




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
	best_fitness = get_best_fitness_value(population):
	for board in population:
		if board.fitness == best_fitness:
			return board
	print("ERROR IN: get_best_fitness_board")

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
	if config_dict['parent_selection_algorithm'] == 'k-Tournament Selection with replacement':
		return k_tournament_selection_with_replacement(population, config_dict['t_size_parent'], config_dict['offspring_count'] * 2)


def k_tournament_selection_with_replacement(population, t_size, number_of_parents):
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

	# Initialize return_dict with an empty string
	return_dict[run_number] = ''

	# Add "Run i" line top of algorithm log file 
	return_dict[run_number] += ('\nRun ' + str(run_number + 1) + '\n')

	# Create a list of all the shapes
	shape_list = []
	for i in range(len(shape_string_list)):
		shape_list.append(Shape_base(shape_string_list[i], i))

	# Start with an empty population
	population = []

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		new_board = Board(shape_list, max_height)
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

		# Survival Selection
		select_survivors(population)

		# Find best and average fitness
		best_fitness = get_best_fitness_value(population)
		average_fitness = get_average_fitness_value(population)

		# Update stoping creteria
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

	# If printing progress bar, add new line when completed and print 100% completed
	if print_progress_bar:
		progress_bar.printProgressBar(config_dict['fitness_evaluations'])
		print()

	# Create solution log from best Board in the population
	create_solution_file(population[0], config_dict['solution_file_path'], run_number + 1)