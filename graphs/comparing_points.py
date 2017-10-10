import json
import sys
import os

if len(sys.args) != 3:
	print("Usage: python3 comparing_points.py <input (1,2,3)> <\"Config Key\">")

directory = os.listdir('../logs/')

files = []

important_key = sys.args[2]

for d in directory:
	if sys.args[1] == '1':
		if d.startswith('1'):
			files.append(d)
	elif sys.args[1] == '2':
		if d.startswith('2'):
			files.append(d)
	elif sys.args[1] == '3':
		if d.startswith('3'):
			files.append(d)


possible_values = set()

for file_name in files:
	data = ''
	config_dict = {}

	# Find possible key values
	with open('../logs/' + str(file_name), 'r') as f:
		while True:
			temp_data = f.readline()
			if '}\n' == temp_data:
				data += temp_data
				break
			else:
				data += temp_data

		data = json.loads(data)
		config_dict = data['Config File']
		if config_dict[important_key] not in possible_values:
			possible_values.add(config_dict[important_key])


{
    "Config File": {
        "Fitness Evaluations": 10000,
        "Log File Path": null,
        "Mutation Algorithm": "Move",
        "Mutation Rate": 0.1,
        "Offspring Count": 50,
        "Parent Selection Algorithm": "k-Tournament Selection with replacement",
        "Penalty Coefficient": 1,
        "Placement Algorithm": "Random",
        "Population Size": 100,
        "Random Seed": 1001,
        "Recombination Algorithm": "Partially Mapped Crossover",
        "Runs": 30,
        "Search Algorithm": "EA",
        "Self Adaptive Mutation Rate": false,
        "Self Adaptive Offspring Count": false,
        "Self Adaptive Penalty Coefficient": false,
        "Solution File Path": null,
        "Survival Strategy": "Plus",
        "Survivor Algorithm": "Truncation",
        "Termination Convergence Criterion": 10000,
        "Tournament Size For Parent Selection": 5,
        "Tournament Size For Survival Selection": 5
    },
    "Input File": "inputs/1.txt",
    "Problem Instance Files": "./solutions/1001",
    "Random Seed": 1001,
    "Run Time": 548
}