from board import Board
import sys
import random
import signal	# ctrl-c handle
import json
import os
from time import time
from copy import deepcopy

def signal_handler(signal, frame):
	print('You pressed Ctrl+C!')
	#print_info()
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