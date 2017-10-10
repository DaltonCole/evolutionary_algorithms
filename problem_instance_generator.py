import json
import subprocess

random_seed = 3000
search_algorithms = ['EA']
runs = [30]
fitness_evaulations = [10000]
population_size = [10]
offspring_count = [5]
tournament_parent = [2]
tournament_survival = [2]
mutation_rate = [0.1]
termination_convergence = [10000] 
parent_selection_algorithm = ['k-Tournament Selection with replacement']#, 'Fitness Proportional Selection']#, 'Uniform Random']
recombination_algorithm = ['Partially Mapped Crossover', 'Order Crossover']
mutation_algorithm = ['Flip', 'Move']
survivor_algorithm = ['Truncation']#, 'k-Tournament Selection without replacement', 'Fitness Proportional Selection']
placement_algorithm = ['Random', 'Random with Repair', 'Random with Penalty']
survival_strategy = ['Plus']
self_adaptive_mutation_rate = [False, True]
self_adaptive_penalty_coefficient = [False, True]
self_adaptive_offspring_count = [False, True]
penalty_coefficient = [1]


config_dict = {}

config_dict["Log File Path"] = None
config_dict["Solution File Path"] = None
config_dict["Random Seed"] = random_seed 

import os
directory = set(os.listdir("./logs/"))

for a in search_algorithms:
	config_dict["Search Algorithm"] = a
	for b in runs:
		config_dict["Runs"] = b
		for c in fitness_evaulations:
			config_dict["Fitness Evaluations"] = c
			for d in population_size:
				config_dict["Population Size"] = d
				for e in offspring_count:
					config_dict["Offspring Count"] = e
					for f in tournament_parent:
						config_dict["Tournament Size For Parent Selection"] = f
						for g in tournament_survival:
							config_dict["Tournament Size For Survival Selection"] = g
							for z in mutation_rate:
								config_dict['Mutation Rate'] = z
								for y in termination_convergence:
									config_dict["Termination Convergence Criterion"] = y
									for x in parent_selection_algorithm:
										config_dict["Parent Selection Algorithm"] = x
										for w in placement_algorithm:
											config_dict["Placement Algorithm"] = w
											for v in recombination_algorithm:
												config_dict["Recombination Algorithm"] = v
												for n in penalty_coefficient:
													config_dict["Penalty Coefficient"] = n
													for i in survivor_algorithm:
														config_dict["Survivor Algorithm"] = i
														for j in survival_strategy:
															config_dict["Survival Strategy"] = j
															for k in self_adaptive_mutation_rate:
																config_dict["Self Adaptive Mutation Rate"] = k
																for l in self_adaptive_penalty_coefficient:
																	config_dict["Self Adaptive Penalty Coefficient"] = l
																	for m in self_adaptive_offspring_count:
																		config_dict["Self Adaptive Offspring Count"] = m
																		for h in mutation_algorithm:
																			config_dict["Mutation Algorithm"] = h

																			if config_dict['Self Adaptive Penalty Coefficient'] == True and config_dict['Placement Algorithm'] != 'Random with Penalty':
																				continue

																			config_dict["Random Seed"] += 1 

																			if str(config_dict['Random Seed']) not in directory:
																				with open('temp_config.json', 'w') as f:
																					json.dump(config_dict, f)
																				command = './run.sh temp_config.json inputs/3.txt'
																				process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
																				process.wait()
																			#print(process.returncode)
																			print(config_dict["Random Seed"])
"""	
config_dict["Mutation Rate"] = 
config_dict["Termination Convergence Criterion"] =  
 = 
"""


#config_dict["Random Seed"] = random_seed 