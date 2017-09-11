""" Config file:
Random Seed: 1234567890
Search Algorithm: Random Search
Runs: 20
Fitness Evaluations: 20
Log File Path: ./logs/1234567890.log
Solution File Path: ./solution/1234567890.txt
"""

""" Log file:
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
"""

""" Algoirthm log:
Result Log

Run 1
1	1
2	10
14	11
15	12
48	14

Run 2
1	2
10	3
100	5

"""

from helper_functions import *

def main():
	if len(sys.argv) != 2:
		print('Usage: python3 driver.py <config file>')
		quit()

	# {'input_file': '', 'runs': 1, 'random_seed': 1, 'search_algorithm': '', 
	#  'fitness_evaluations': 1, 'log_file_path': './', 
	#  'solution_file_path': './', 'algorithm_solution_file_path': './'}
	config_dict = config_parser(sys.argv[1])

	#random.seed(config_dict['random_seed'])

	# Create log file
	create_log_file(config_dict)

	### Constants ###
	population_size = 10
	#################

	# Multiprocess
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	jobs = []

	# ctrl-c handler
	signal.signal(signal.SIGINT, partial(signal_handler, return_dict, config_dict))

	max_height = 0
	shapes = []
	with open(config_dict['input_file'], 'r') as f:
		max_height, _ = f.readline().split()
		max_height = int(max_height)
		for line in f:
			shapes.append(line)

	
	# Start run
	for run in range(config_dict['runs']):
		p = multiprocessing.Process(target=run_algorithm, args=(config_dict, max_height, shapes, population_size, run, return_dict))
		jobs.append(p)
		p.start()

	for proc in jobs:
		proc.join()

	# Write to algorithm log file
	write_algorithm_log(config_dict['algorithm_solution_file_path'], config_dict['runs'], return_dict)


if __name__ == '__main__':
	main()

