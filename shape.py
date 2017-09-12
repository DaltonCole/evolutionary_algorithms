# File name:      shape.py
# Author:         Dalton Cole

from itertools import groupby 	# Used to make a list of unique lists
from random import randrange 	# Used to set a random orientation

"""
TODO: Make 1 = 90 degrees and 3 = 270 degrees within the class, not just
		mapped to the correct version
	This can be done by switching the order they are added to the four_shape
	(maybe)

	Store the highest x value of each shape for each orientation
	max_x_value would then become self.highest_x[self.active_state] + x_offset
"""

class Shape:
	"""Shape which is defined as a set of points that can be rotated

	Attributes:
		original_order (int): This is the Nth shape to be made for a board
			Used for sorting into the original order
		active_state (int): The current active rotation
			(0 = 0 degrees, 1 = 90, 2 = 180, 3 = 270)
		four_shapes (list of list of points): Every rotation. four_shapes 
			indexed with active_state returns that rotation. Point is in [x, y]
			format.Shapes are normalized such that no shape has negative 
			points, and there are only unique points in each shape.
		original_point (list of points): The starting point of each shape
			This would correspond to [0,0] before normalizing.
		width (int): Width of non rotated shape
		current_coordinates (list of list of int): Points for shape given
			the current orientation
		x_offset (int): Difference between where all of the points are
			on the board and the base shape for the x direction
		y_offset (int): Difference between where all of the points are
			on the board and the base shape for the y direction
	"""

	def __init__(self, shape_string, original_order):
		"""Initializes a shape and every possible rotation

		Sets the original order parameter. Randomly choses a rotation. 
		Populates four_shapes with every possible rotation and normalizes
		it such that no point is negative and there are no repeat points.
		Finds the current width of the base shape. Makes a list of the
		original points of the shape (four points for 4 possible rotations).
		Defines the current_coordinates of the current orientation.
		Also initializes the x and y offset to 0

		Args:
			shape_string (str): A string of the shape in a specified format
				example: "R4 U2 D7 L8 U4"
			original_order (int): This is the Nth shape to be made for a board

		"""
		##### Initialize variables #####
		# Order in which shape was created in
		self.original_order = original_order
		# Randomize the current rotation
		self.active_state = randrange(4)

		# Split movement string into each action
		movements = shape_string.split()

		# Declare shapes and the starting points of each rotation
		self.four_shapes = []
		self.original_point = []
		################################

		##### 0 degree rotation #####
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			# Separate direction and amount
			direction, amount = movement[0], int(movement[1:])
			# Add (amount) points in given direction. Update x, y of the last
			# placed point
			x, y = self._generate_shape(direction, amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)
		#############################

		##### 90 degree rotation #####
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			# Transform direction for corresponding rotation
			x, y = self._generate_shape(self._transform_direction(1, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)
		#############################

		##### 180 degree rotation #####
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(self._transform_direction(2, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)
		#############################

		##### 270 degree rotation #####
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(self._transform_direction(3, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)
		#############################

		### Find width of original shape ###
		self.width = self._find_width(self.four_shapes[0])

		### Current coordinates ###
		self.current_coordinates = self.four_shapes[self.active_state]

		### Current Offsets ###
		self.x_offset = 0
		self.y_offset = 0

	def update_orientation(self, orientation):
		"""Update current orientation to a new rotation

		Updates self.active_state to new orientation.
		Sets self.current_coordinates to new active coordinates 

		Args:
			orientation (int): Orientation to change to.
				0 = 0 degree orientation
				1 = 90 degree orientation, clockwise
				2 = 180 degree orientation, clockwise
				3 = 270 degree orientation, clockwise
		"""
		self.active_state = orientation
		self.current_coordinates = self.four_shapes[self.active_state]

	def get_current_coordinates(self):
		"""Returns a list of the current points
		Returns:
			(list of list of ints) List of the current points
				Example: [[0, 0], [1, 0], [0, 1]]
		"""
		return self.current_coordinates

	def get_current_orientation(self):
		"""Returns the current orientation
		Returns:
			(int) Current orientation
				0 = 0 degree orientation
				1 = 90 degree orientation, clockwise
				2 = 180 degree orientation, clockwise
				3 = 270 degree orientation, clockwise
		"""
		return self.active_state

	def get_current_offset(self):
		"""Returns the current offset in [x, y] format
		Returns:
			(list of ints): Current offset of [x, y]
		"""
		return [self.x_offset, self.y_offset]

	def get_original_point_of_active_shape(self):
		"""Return the original point for the active state
		Returns:
			(list of ints): Original point of active state
				This would be [0, 0] for each rotation before it was normalized
		"""
		return self.original_point[self.active_state]

	def update_offset(self, x, y):
		"""Update offsets with the given value
		x_offset and y_offset will be updated with x and y, respectively

		Args:
			x (int): New x offset
			y (int): New y offset
		"""
		self.x_offset = x
		self.y_offset = y

	def print_offset_orientation(self):
		"""Print original point with offset and active rotation
		Prints the original point (what was [0, 0] before normalizing) in
		the following format:
			(x + x_offset),(y + y_offset),(active rotation)
		This would look something like this:
			5,7,1
		If the base x and y are [2,1] and the offsets are 3 and 6 for x, y with
		a 90 degree rotation.
		"""
		print(str(self.x_offset + self.original_point[self.active_state][0]) + 
			"," + str(self.y_offset + self.original_point[self.active_state][1]) + 
			"," + str(self.active_state))

	def get_offset_orientation(self):
		"""Returns original point with offset and active rotation
		Return the original point (what was [0, 0] before normalizing) in
		the following format:
			(x + x_offset),(y + y_offset),(active rotation)
		This would look something like this:
			5,7,1
		If the base x and y are [2,1] and the offsets are 3 and 6 for x, y with
		a 90 degree rotation.

		NOTE:
			Due to errors in the class, internally a 1 = 270 degrees and 3 = 90
			degree rotations.

		Returns:
			(str): current point, orientation
		"""
		state = self.active_state
		if state == 1:
			state = 3
		elif state == 3:
			state = 1

		return (str(self.x_offset + self.original_point[self.active_state][0]) + 
					"," + str(self.y_offset + self.original_point[self.active_state][1]) + 
					"," + str(state))

	def print_all_points(self):
		"""Print all points with offsets
		Print all of the points with offsets in the following format:
			[1, 2], [2, 3], [4, 5], ...
		"""
		for point in self.four_shapes[self.active_state]:
			print("[" + str(self.x_offset + point[0]) + ", " + str(self.y_offset + point[1])+"]", end=", ")
		print()

	def get_all_points(self):
		"""Get a list of all points with offsets applied
		Returns:
			(list of list of int) A list of all the current points with
				the current offsets
		"""
		all_points = []
		for point in self.four_shapes[self.active_state]:
			all_points.append([self.x_offset + point[0], self.y_offset + point[1]])
		return all_points

	def _generate_shape(self, direction, amount, x, y, generated_shape):
		"""Append point to the generated shape and return x, y value of point

		Args:
			direction (string): Direction to move in.
				One of: 'R', 'L', 'U', 'D'
			amount (int): How much to move by
			x (int): X coordinate of previous shape
			y (int): Y coordinate of previous shape
			generated_shape (list of list of int): List of points for shape.
				Is updated with generated point based on direction and amount

		Returns:
			x, y: The updated x, y values of the last placed point
		"""
		if direction == 'R':
			for i in range(amount):
				x += 1
				generated_shape.append([x, y])
		if direction == 'L':
			for i in range(amount):
				x -= 1
				generated_shape.append([x, y])
		if direction == 'U':
			for i in range(amount):
				y += 1
				generated_shape.append([x, y])
		if direction == 'D':
			for i in range(amount):
				y -= 1
				generated_shape.append([x, y])

		return x, y

	def _transform_direction(self, orientation, direction):
		"""Return direction with the applied flip
		Args:
			orientation (int): The orientation to calculate the flip for
				0 = 0 degree orientation
				1 = 90 degree orientation, clockwise
				2 = 180 degree orientation, clockwise
				3 = 270 degree orientation, clockwise
			direction (str): The direction to go in
				One of 'U', 'R', 'D', 'L'

		Returns:
			(str) Direction with the needed flip
		"""
		if orientation == 0:
			return direction
		# 90 degree rotation
		elif orientation == 1:
			if direction == 'U':
				return 'L'
			elif direction == 'L':
				return 'D'
			elif direction == 'D':
				return 'R'
			elif direction == 'R':
				return 'U'
		# 180 degree rotation
		elif orientation == 2:
			if direction == 'U':
				return 'D'
			elif direction == 'L':
				return 'R'
			elif direction == 'D':
				return 'U'
			elif direction == 'R':
				return 'L'
		# 270 degree rotation
		elif orientation == 3:
			if direction == 'U':
				return 'R'
			elif direction == 'L':
				return 'U'
			elif direction == 'D':
				return 'L'
			elif direction == 'R':
				return 'D'

	def _normalize_shape(self, generated_shape):
		"""Normalize shape so no points are negative and only unique points
		Sorts the generated shape by x value and removes duplicate points.
		Adds an x and y values to the points so all points are positive.

		NOTE:
			This function needs to be called in the same order as shapes
			are added to four_shapes. This is so original_point corresponds
			to the four rotations

		Args:
			generated_shape (list of list of int): A list of points

		Returns:
			generated_shape (list of list of int): A list of points
				with the properties of all unique points and no negative
				points. Returning this is necessary because removing points
				creates a new list with a different reference.
		"""
		# Only unique points
		generated_shape.sort()
		generated_shape = list(i for i,_ in groupby(generated_shape))

		# Normalize, so only positive points
		min_x = 0
		min_y = 0
		for point in generated_shape:
			if point[0] < min_x:
				min_x = point[0]
			if point[1] < min_y:
				min_y = point[1]

		if min_x < 0 or min_y < 0:
			for point in generated_shape:
				point[0] -= min_x
				point[1] -= min_y

		# Add point to original point list
		# Note: Needs to be added in same order as four_shapes
		self.original_point.append([-min_x, -min_y])

		return generated_shape

	def _find_width(self, generated_shape):
		"""Find the width of the shape
		Used to find the highest x value of any point in the shape
		Returns:
			(int) Highest x value of base shape
		"""
		max_x = 0

		for point in generated_shape:
			if point[0] > max_x:
				max_x = point[0]

		return max_x

	def max_x_value(self):
		"""Find the max x value of the shape
		Returns:
			(int) The highest x value
		"""
		max_x = 0

		for point in self.four_shapes[self.active_state]:
			if max_x < point[0] + self.x_offset:
				max_x = point[0] + self.x_offset

		return max_x

if __name__ == '__main__':
	# s = Shape("R5 L7 U2 R3 D2")
	# s = Shape("D2 L3 U2 R3")
	s = Shape("D1 L4 R1 U3 R3")
	print(s.get_current_orientation())
	print(s.get_base_coordinates())
	print(len(s.get_base_coordinates()))