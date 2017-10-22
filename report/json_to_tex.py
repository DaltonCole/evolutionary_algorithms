import json
import os

all_files = os.listdir('../logs/')

all_files.sort()

with open('all_graphs.tex', 'w') as file:
	file.write('\\documentclass{standalone}\n')
	file.write('\\begin{document}\n')

	for i in all_files:#1081):
		i = int(i)
		with open('../logs/' + str(i), 'r') as f:
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
			s += '\t\\caption{Input ' + str(i)[0] + '}\n'
			s += '\t\\label{fig:graph_' + str(i) + '}\n'
			s += '\t\\includegraphics[width=\\textwidth]{../graphs/graphs/' + str(i) + '.pdf}\n'
			s += '\\end{figure}\n\n\n'

			s += '\\begin{figure}[!htb]\n'
			s += "\t\\caption{Figure \\ref{fig:graph_" + str(i) + "} Representation" + "}\n"
			s += '\t\\label{fig:picture_' + str(i) + '}\n'
			s += '\t\\includegraphics[width=\\textwidth]{../graphs/picture/' + str(i) + '.pdf}\n'
			s += '\\end{figure}\n\n\n'

			file.write(s)

			if i % 10 == 0:
				file.write('\\clearpage\n')

	file.write('\\end{document}\n')