from board import Board
import sys
import random
import signal	# ctrl-c handle
import json
import os
import multiprocessing
from functools import partial
from time import time
from copy import deepcopy

def signal_handler(return_dict, config_dict, signal, frame):
	print('You pressed Ctrl+C!')

	"""
	print('return dict')
	print(return_dict)

	print("length: " + str(len(return_dict)))

	# Write to algorithm log file
	write_algorithm_log(config_dict['algorithm_solution_file_path'], config_dict['runs'], return_dict)
	"""

	sys.exit(0)

def config_parser(config_file_name):
	# Initialize default inputs
	config_dict = {}
	config_dict['input_file'] = 'input.txt'
	config_dict['random_seed'] = int(time())
	config_dict['search_algorithm'] = "Random Search"
	config_dict['runs'] = 30
	config_dict['fitness_evaluations'] = 1000
	config_dict['log_file_path'] = ''
	config_dict['solution_file_path'] = ''
	config_dict['algorithm_solution_file_path'] = ''

	# Load json config file
	json_config_file = ''
	with open(config_file_name, 'r') as f:
		json_config_file = json.load(f)
	
	if json_config_file['Input File'] != "":
		config_dict['input_file'] = json_config_file['Input File']

	if json_config_file['Random Seed'] != None:
		config_dict['random_seed'] = int(json_config_file['Random Seed'])

	if json_config_file['Search Algorithm'] != ''  and json_config_file['Search Algorithm'] != None:
		config_dict['search_algorithm'] = json_config_file['Search Algorithm']
	
	if json_config_file['Runs'] != None:
		config_dict['runs'] = int(json_config_file['Runs'])

	if json_config_file['Fitness Evaluations'] != None:
		config_dict['fitness_evaluations'] = int(json_config_file['Fitness Evaluations'])

	if json_config_file['Log File Path'] != '' and json_config_file['Log File Path'] != None:
		config_dict['log_file_path'] = json_config_file['Log File Path']
	else:
		config_dict['log_file_path'] = './logs/' + str(config_dict['random_seed'])

	if json_config_file['Solution File Path'] != '' and json_config_file['Solution File Path'] != None:
		config_dict['solution_file_path'] = json_config_file['Solution File Path']
	else:
		config_dict['solution_file_path'] = './solutions/' + str(config_dict['random_seed']) + '/'

	if json_config_file['Algorithm Solution File Path'] != '' and json_config_file['Algorithm Solution File Path'] != None:
		config_dict['algorithm_solution_file_path'] = json_config_file['Algorithm Solution File Path']
	else:
		config_dict['algorithm_solution_file_path'] = './logs/algorithm_solution/' + str(config_dict['random_seed'])

	return config_dict

def open_file(file):
	if not os.path.exists(os.path.dirname(file)):
		os.makedirs(os.path.dirname(file))
	return open(file, 'w')

def write_algorithm_log(file, runs, return_dict):
	if not os.path.exists(os.path.dirname(file)):
		os.makedirs(os.path.dirname(file))

	with open(file, 'w') as f:
		for i in range(runs):
			f.write(return_dict[i])

def create_log_file(config_dict):
	log_dict = {}
	log_dict['Problem Instance Files'] = config_dict['solution_file_path']
	log_dict['Random Seed'] = config_dict['random_seed']
	log_dict['Algorithm Log File Path'] = config_dict['algorithm_solution_file_path']
	log_dict['Config File'] = config_dict

	opened_file = open_file(config_dict['log_file_path'])

	json.dump(log_dict, opened_file, indent=4)

	opened_file.close()

# {'input_file': '', 'runs': 1, 'random_seed': 1, 'search_algorithm': '', 
	#  'fitness_evaluations': 1, 'log_file_path': './', 
	#  'solution_file_path': './', 'algorithm_solution_file_path': './'}
	config_dict = config_parser(sys.argv[1])

def create_solution_file(best_board, path, run_number):
	opened_file = open_file(path + str(run_number))

	for solution in best_board.get_info():
		opened_file.write(solution + '\n')

	opened_file.close()

def run_algorithm(config_dict, max_height, shapes, population_size, run_number, return_dict):
	# Random number
	random.seed(config_dict['random_seed'] + run_number)

	return_dict[run_number] = ''
	# If random search, and "Run i" line to algo log file 
	if config_dict['search_algorithm'] == 'Random Search':
		return_dict[run_number] += ('\nRun ' + str(run_number + 1) + '\n')

	population = []

	for i in range(population_size):
		population.append(Board(shapes, max_height))

	# Sort from best fit to worst fit
	population.sort(reverse=True)

	# Apply fitness evals
	best_fitness = 0
	for current_eval in range(config_dict['fitness_evaluations']):
		print(current_eval)
		# Apply search algorithm
		if config_dict['search_algorithm'] == 'Random Search':

			# Double population
			for i in range(population_size):
				population.append(Board(shapes, max_height))

			# Sort
			population.sort(reverse=True)

			# Take best n/2 of population
			for i in range(population_size):
				population.pop(len(population) - 1)

		if population[0].fitness > best_fitness or current_eval == 0:
			best_fitness = population[0].fitness
			return_dict[run_number] += (str(current_eval + 1) + ' \t' + str(best_fitness) + '\n')

	create_solution_file(population[0], config_dict['solution_file_path'], run_number + 1)

	##### DEBUGGING #####################################
	#for shape in population[0].shapes:
	#	shape.print_all_points()

	from operator import itemgetter

	combined_points = []
	for shape in population[0].shapes:
		combined_points += shape.get_all_points()

	combined_points.sort(key=itemgetter(0,1))

	b_set = set(tuple(x) for x in combined_points)
	b = [ list(x) for x in b_set ]
	b.sort(key=itemgetter(0,1))

	print(len(b) == len(combined_points))

	print()
	print()
	print(combined_points)
	print()
	print(b)
	#####################################################

	#print(population[0].current_length)