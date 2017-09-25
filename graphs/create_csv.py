import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 5:
	print("Usage: python3 line_graph.py <file path> <number of runs> <number of evals> <output file>")
	quit()

file_path = sys.argv[1]

number_of_runs = int(sys.argv[2])

number_of_evals = int(sys.argv[3])

output_file = sys.argv[4]

run_list = []

previous_line = ''
with open(file_path, 'r') as f:
	current_run = -1
	for line in f:
		if 'Run ' in line:
			current_run += 1
			continue
		if current_run < 1 :
			continue

		if line == '\n':
			print(previous_line)
		continue

		ev = int(line.split()[0])

		if ev == number_of_evals:
			run_list.append(int(line.split()[1]))
			continue

		previous_line = line

print(run_list)