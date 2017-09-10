from helper_functions import *

def config_parser_test():
	config_dict = config_parser('./test/config_test.json')
	for key, value in config_dict.items():
		print(key, end=': ')
		print(value)




if __name__ == '__main__':
	config_parser_test()