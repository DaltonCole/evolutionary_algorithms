# File name:      helper_functions.py
# Author:         Dalton Cole

"""Helper file for driver
"""

from board import Board
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
			log_file_path: "./log/<random seed>"
			solution_file_path: "./solution/<random seed>"
			algorithm_solution_file_path: 
				"./log/algorithm_solution/<random seed>"

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
		if json_config_file['Population Size'] != None:
			config_dict['population_size'] = int(json_config_file['Population Size'])
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

def run_algorithm(config_dict, max_height, shapes, population_size, run_number, return_dict):
	"""TODO: DOCSTRING
	"""

	# Seed the random number generator with random_seed + run number
	# This makes each run unique
	random.seed(config_dict['random_seed'] + run_number)

	# Initialize return_dict with an empty string
	return_dict[run_number] = ''

	# If random search, add "Run i" line to algo log file 
	if config_dict['search_algorithm'] == 'Random Search':
		return_dict[run_number] += ('\nRun ' + str(run_number + 1) + '\n')

	# Start with an empty population
	population = []

	# Populate to capacity with Boards in random shape order with
	# random orientation
	for i in range(population_size):
		population.append(Board(shapes, max_height))

	# Sort from best fit to worst fit
	population.sort(reverse=True)

	# If last run, print progress bar
	print_progress_bar = False
	if run_number + 1 == config_dict['runs']:
		print_progress_bar = True

	if print_progress_bar:
		printProgressBar(0, config_dict['fitness_evaluations'], prefix = 'Progress:', suffix = 'Complete', length = 100)

	# Apply fitness evals
	best_fitness = 0
	for current_eval in range(config_dict['fitness_evaluations']):
		if print_progress_bar:
			printProgressBar(current_eval, config_dict['fitness_evaluations'], prefix = 'Progress:', suffix = 'Complete', length = 100)
		
		# Apply search algorithm
		if config_dict['search_algorithm'] == 'Random Search':

			# Add population_size members to population
			for i in range(population_size):
				population.append(Board(shapes, max_height))

			# Sort
			population.sort(reverse=True)

			# Take best 1 of population
			for i in range(len(population) - 1):
				population.pop(len(population) - 1)

		# If current best fitness is better than previous best fitness
		if population[0].fitness > best_fitness or current_eval == 0:
			# Update best_fitness
			best_fitness = population[0].fitness
			# Add new best fitness to algorithm_log
			return_dict[run_number] += (str(current_eval + 1) + ' \t' + str(best_fitness) + '\n')

	# If printing progress bar, add new line when completed and print 100% completed
	if print_progress_bar:
		printProgressBar(1, 1, prefix = 'Progress:', suffix = 'Complete', length = 100)
		print()

	# Create solution log from best Board in the population
	create_solution_file(population[0], config_dict['solution_file_path'], run_number + 1)

	##### DEBUGGING #####################################
	"""
	from operator import itemgetter

	combined_points = []
	for shape in population[0].shapes:
		combined_points += shape.get_all_points()

	combined_points.sort(key=itemgetter(0,1))

	b_set = set(tuple(x) for x in combined_points)
	b = [ list(x) for x in b_set ]
	b.sort(key=itemgetter(0,1))
	if (len(b) == len(combined_points)) == False:
		print(len(b) == len(combined_points))
	"""
	#####################################################


""" 
	NOTE: printProgressBar is BORROWED FROM: 
		https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
"""
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    try:    
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    except:
        print('\r' + str(percent) + ' ' + str(suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()
