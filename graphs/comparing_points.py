import json
import sys
import os

if len(sys.argv) != 3:
	print("Usage: python3 comparing_points.py <input (1,2,3)> <\"Config Key\">")
	quit()

directory = os.listdir('../logs/')

files = []

important_key = sys.argv[2]

for d in directory:
	if sys.argv[1] == '1':
		if d.startswith('1'):
			files.append(d)
	elif sys.argv[1] == '2':
		if d.startswith('2'):
			files.append(d)
	elif sys.argv[1] == '3':
		if d.startswith('3'):
			files.append(d)

files.sort()

# Possible values
possible_values = set()
# {(str) Possible values: (list of float) All fitness values for key}
key_dict = {}


for file_name in files:
	print(file_name)
	data = ''
	config_dict = {}

	# Find possible key values
	with open('../logs/' + str(file_name), 'r') as f:
		# Get JSON part of log file
		while True:
			temp_data = f.readline()
			if '}\n' == temp_data:
				data += temp_data
				break
			else:
				data += temp_data

		# JSON string to dict
		data = json.loads(data)
		config_dict = data['Config File']

		"""
		### TEMP ###
		if config_dict['Self Adaptive Mutation Rate'] != True:
			continue
		if config_dict['Placement Algorithm'] != "Random with Penalty":
			continue
		############
		"""

		# If key value is not in set, add it
		if config_dict[important_key] not in possible_values:
			possible_values.add(config_dict[important_key])
			# Add value to key_dict as a key
			key_dict[config_dict[important_key]] = list()

	with open('../logs/' + str(file_name), 'r') as f:
		while(True):
			if 'Result Log' not in f.readline():
				continue
			else:
				f.readline()
				break
		ave = 0
		for line in f:
			if 'Run ' in line or line == '\n':
				if line == '\n':
					key_dict[config_dict[important_key]].append(ave)

				continue
			else:
				line = line.split()
				ev, ave, best = float(line[0]), float(line[-2]), float(line[-1])
				#key_dict[config_dict[important_key]].append(ave)


for key, value in key_dict.items():
	file_to_open = './compare/average/'
	file_to_open += str(sys.argv[1]) + '_'
	file_to_open += str(important_key).replace(' ', '_')
	file_to_open += '___'
	file_to_open += str(key).replace(' ', '_')
	print(file_to_open)
	with open(file_to_open, 'w') as f:
		for v in value:
			f.write(str(v) + '\n')

"""
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
"""