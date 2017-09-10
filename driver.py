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

	random.seed(config_dict['random_seed'])

	# Create log file
	create_log_file(config_dict)
	# Initalize algorithm log file
	algorithm_log = open_file(config_dict['algorithm_solution_file_path'])
	algorithm_log.write("Result Log\n\n")

	### Constants ###
	population_size = 100
	#################

	max_height = 0
	shapes = []
	with open(config_dict['input_file'], 'r') as f:
		max_height, _ = f.readline().split()
		max_height = int(max_height)
		for line in f:
			shapes.append(line)

	
	# Start run
	for run in range(config_dict['runs']):
		# If random search, and "Run i" line to algo log file 
		if config_dict['search_algorithm'] == 'Random Search':
			algorithm_log.write('\nRun ' + str(run + 1) + '\n')

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
				algorithm_log.write(str(current_eval + 1) + ' \t' + str(best_fitness) + '\n')

		create_solution_file(population[0], config_dict['solution_file_path'], run + 1)

	algorithm_log.close()


if __name__ == '__main__':
	main()