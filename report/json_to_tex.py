import json

with open('all_graphs.tex', 'w') as file:
	file.write('\\documentclass{standalone}\n')
	file.write('\\begin{document}\n')

	for i in range(1001, 1025):#1081):
		with open('../logs/' + str(i), 'r') as f:
			data = ''
			while True:
				temp_data= f.readline()
				if '}\n' == temp_data:
					data += temp_data
					break
				else:
					data += temp_data

			data = json.loads(data)
			config_dict = data['Config File']

			# Table
			s = "\\begin{table}[!htb]\n"
			s += "\t\\centering\n"
			s += "\t\\caption{Figure \\ref{fig:graph_" + str(i) + "} Configuration File" + "}\n"
			s += "\t\\label{tab:graph_" + str(i) + "}\n"
			s += "\t\\begin{tabular}{| c | c |}\n"
			s += "\t\t\\hline\n"

			for key, value in config_dict.items():
				s += '\t\t' + str(key) + '\t\t& ' + str(value) + '\t\t \\\\\n'
				s += '\t\t\\hline\n' 

			s += '\t\\end{tabular}\n'
			s += '\\end{table}\n'

			s += '\\begin{figure}[!htb]\n'
			s += '\t\\caption{Input 1}\n'
			s += '\t\\label{fig:graph_' + str(i) + '}\n'
			s += '\t\\includegraphics[width=\\textwidth]{../graphs/graphs/' + str(i) + '.pdf}\n'
			s += '\\end{figure}\n\n\n'

			file.write(s)

	file.write('\\end{document}\n')