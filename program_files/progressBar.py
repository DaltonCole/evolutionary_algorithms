# File name:      progressBar.py
# Author:         Dalton Cole

from time import time
from datetime import datetime, timedelta

class ProgressBar():
	"""Creates a progress bar with percent and time remaining

	Class Attributes:
		prefix (str): What to perpend to the progress bar
		suffix (str): What to add to the end of the progress bar
		length (int): Deltas in progress bar
		decimals (int): Decimals in % complete
		fill (str): Character to fill bar with
		non_unicode_fill (str): If error with fill, use this as a back-up
			fill method
	Attributes:
		total (int): Total number of evals
		start_time (int): Time in seconds of when it was started
		percent (str): Percent complete to 1 decimal point
	"""
	prefix = 'Progress'
	suffix = 'Complete'
	length = 100
	decimals = 1
	fill = '█'
	non_unicode_fill = '#'

	def __init__(self, total):
		"""Initialize ProgressBar with total evals and starting time
		"""
		self.total = total
		self.start_time = int(time())

	def printProgressBar(self, iteration):
		"""Print the progress bar
		This function prints the progress bar with the estimated time
		remaining.

		NOTE:
			Based on: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

		Args:
			iteration (int): The current iteration. Should be less than or 
				equal to self.total
		"""
		try:
			self.percent = 100 * (iteration / float(self.total))
			filledLength = int(self.length * iteration // self.total)

			if float(self.percent) != 0.0:
				remaining_time = str(self.time_remaining())
			else:
				remaining_time = '999'

			self.percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))

			try:
				bar = self.fill * filledLength + '-' * (self.length - filledLength)
				print('\r%s |%s| %s%% %s [ %sremaining ]                         ' % (self.prefix, bar, self.percent, self.suffix, remaining_time), end = '\r')
			except:
				bar = self.non_unicode_fill * filledLength + '-' * (self.length - filledLength)
				print('\r%s |%s| %s%% %s [ %sremaining ]                         ' % (self.prefix, bar, self.percent, self.suffix, remaining_time), end = '\r')
		except:
			pass

	def time_remaining(self):
		"""Calculates the estimated time remaining in seconds
		It does this by finding the difference between the current time and the
		start time, dividing that by the percent, and multiplying that with
		the percent remaining.

		Returns:
			(str): Time remaining
		"""
		# Time taken so far
		time_diff = int(time()) - self.start_time
		# Change in time per percent
		delta = time_diff / float(self.percent)
		# Estamated time remaining = change in time so far * percent remaining
		time_remaining = int(delta * (100 - float(self.percent)))

		### Convert seconds to days, hours, minutes, seconds ###
		sec = timedelta(seconds=time_remaining)
		d = datetime(1,1,1) + sec

		time_string = ''
		if d.day - 1 == 1:
			time_string += str(d.day - 1) + ' day '
		elif d.day - 1 != 0:
			time_string += str(d.day - 1) + ' days '

		if d.hour == 1:
			time_string += str(d.hour) + ' hour '
		elif d.hour != 0:
			time_string += str(d.hour) + ' hours '

		if d.minute == 1:
			time_string += str(d.minute) + ' minute '
		elif d.minute != 0:
			time_string += str(d.minute) + ' minutes '

		if d.second == 1:
			time_string += str(d.second) + ' second '
		elif d.second != 0:
			time_string += str(d.second) + ' seconds '
		########################################################

		return time_string