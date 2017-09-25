import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 5:
	print("Usage: python3 line_graph.py <file path> <number of runs> <number of evals> <instance number>")
	quit()

file_path = sys.argv[1]

number_of_runs = int(sys.argv[2])

number_of_evals = int(sys.argv[3])

instance_number = sys.argv[4]

average_list = [0] * (number_of_evals + 1)
best_list = [0] * (number_of_evals + 1)

next_is_mew = False

with open(file_path, 'r') as f:
	current_run = -1
	for line in f:
		if 'Run ' in line:
			current_run += 1
			next_is_mew = True
			continue
		if current_run < 1 or line == '\n':
			continue

		ev, ave, best = line.split()

		if next_is_mew:
			next_is_mew = False
			average_list[0] += int(ave)
			best_list[0] += int(best)
			continue

		average_list[int(ev)] += int(ave)
		best_list[int(ev)] += int(best)

for i in range(len(average_list)):
	average_list[i] /= number_of_runs
	best_list[i] /= number_of_runs

plt.plot(average_list, label="Local Average")
plt.plot(best_list, label="Local Best")
plt.xlabel('Eval')
plt.ylabel('Fitness')
plt.legend(loc='lower right')
plt.savefig('./graphs/' + instance_number)
plt.show()