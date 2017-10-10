import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 5:
	print("Usage: python3 line_graph.py <file path> <number of runs> <number of evals> <graph number>")
	quit()

# File Path
file_path = sys.argv[1]

# Number of runs
number_of_runs = int(sys.argv[2])

# Number of evaluations
number_of_evals = int(sys.argv[3])

# Graph number
instance_number = sys.argv[4]

# List of the number of evals for average and best
eval_list = [0] * (number_of_evals + 1)
average_list = [0] * (number_of_evals + 1)
best_list = [0] * (number_of_evals + 1)


with open(file_path, 'r') as f:
	while(True):
		if 'Result Log' not in f.readline():
			continue
		else:
			f.readline()
			break

	counter = 0
	for line in f:
		if 'Run ' in line or line == '\n':
			counter = 0
			continue
		else:
			line = line.split()
			ev, ave, best = float(line[0]), float(line[-2]), float(line[-1])

			eval_list[counter] += ev
			average_list[counter] += ave
			best_list[counter] += best
			counter += 1

while(eval_list[-1] == 0):
	eval_list.pop(-1)
	average_list.pop(-1)
	best_list.pop(-1)

for i in range(len(eval_list)):
	eval_list[i] /= number_of_runs
	average_list[i] /= number_of_runs
	best_list[i] /= number_of_runs



#print(eval_list)
#print(average_list)
#print(best_list)

plt.plot(eval_list, average_list, label="Local Average")
plt.plot(eval_list, best_list, label="Local Best")
plt.xlabel('Eval')
plt.ylabel('Fitness')
#plt.yticks(np.arange(min(average_list + best_list), max(average_list + best_list)+1, 1.0))
plt.legend(loc='lower right')
plt.savefig('../graphs/graphs/' + str(instance_number) + '.pdf')
#plt.show()

with open('../graphs/points/' + str(instance_number), 'w') as f:
	for i in average_list:
		f.write(str(i))
		f.write('\n')