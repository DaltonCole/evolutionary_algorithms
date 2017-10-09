# File name:      driver.py
# Author:         Dalton Cole

from helper_functions import *

def main():
	# If we do not recieve 3 arguments, exit
	if len(sys.argv) != 3:
		print('Usage: python3 driver.py <config file> <problem>')
		quit()

	# Start timer
	start_time = int(time())

	"""Dictionary from the config file in the following format:
		{'input_file': '', 'runs': 1, 'random_seed': 1, 'search_algorithm': '', 
	  	 'fitness_evaluations': 1, 'log_file_path': './', 
	  	 'solution_file_path': './', 'algorithm_solution_file_path': './'}
	"""
	config_dict = config_parser(sys.argv[1])

	# Set problem file
	config_dict['input_file'] = sys.argv[2]

	### Constants ###
	population_size = config_dict['population_size']
	#################

	# Multiprocess
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	jobs = []

	# ctrl-c handler
	signal.signal(signal.SIGINT, signal_handler)
	# signal.signal(signal.SIGINT, partial(signal_handler, return_dict, config_dict)) # With partial

	# Get max_height and list of shape strings from input file
	max_height = 0
	shapes = []
	with open(config_dict['input_file'], 'r') as f:
		max_height, _ = f.readline().split()
		max_height = int(max_height)
		for line in f:
			shapes.append(line)

	
	# Start each run as different processes. 
	# Last run should display the progress bar.
	for run in range(config_dict['runs']):
		if config_dict['search_algorithm'] == 'Random Search':
			p = multiprocessing.Process(target=random_search, args=( \
				config_dict, max_height, shapes, population_size, run, \
				return_dict))
		elif config_dict['search_algorithm'] == 'EA':
			p = multiprocessing.Process(target=ea_search, args=( \
				config_dict, max_height, shapes, population_size, run, \
				return_dict))
		jobs.append(p)
		p.start()

	# Wait for jobs to finish
	for proc in jobs:
		proc.join()

	# Add total run time to log file
	config_dict['run_time'] = int(time()) - start_time

	# Create log file
	create_log_file(config_dict)

	# Write to algorithm log file
	write_algorithm_log(config_dict['log_file_path'], config_dict['runs'], return_dict, config_dict)

	# Find best solution
	best_solution = return_dict[0][1]
	best_index = 0
	for i in range(config_dict['runs']):
		if return_dict[i][1] > best_solution:
			best_solution = return_dict[i][1]
			best_index = i

	# Write to solution file best solution
	create_solution_file(return_dict[best_index][1], config_dict['solution_file_path'], best_index + 1)


if __name__ == '__main__':
	main()

