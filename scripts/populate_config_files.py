import json
import os

all_files = os.listdir('../logs/')

all_files.sort()

for file in all_files:
	config_dict = {}
	with open('../logs/' + str(file), 'r') as f:
		data = ''
		while True:
			temp_data = f.readline()
			if '}\n' == temp_data:
				data += temp_data
				break
			else:
				data += temp_data

		data = json.loads(data)
		config_dict = data['Config File']

	with open('../config_files/' + str(file), 'w') as f:
		json.dump(config_dict, f, indent=4, sort_keys=True)