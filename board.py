# File name:      board.py
# Author:         Dalton Cole

from shape import Shape
from random import shuffle 	# Shuffle list of Shapes
from random import randrange

class Board:
	"""Board with shapes optimally placed given their current order and rotation

	Fitness function used is -current_length of board.

	Attributes:
		shapes (list of Shape): All of the shapes are created (so 
			shape.original_order is maintained) and then randomly shuffled.
		max_height (int): Max height of the board (grid)
		current_length (int): The current length (max x) of the board

	"""
	max_height = 0
	def __init__(self, shape_list):
		"""Initializes a board with shapes in a random order
		Populates the shapes list with shapes taken from shape_strings_list
		and shuffles them into a random order. It then minimizes the
		amount of space the shapes take on the board.

		Args:
			shape_string_list (list of Shape): A list of all of the shapes
			max_height (int): Max height of the board
		"""
		self.shapes = []

		# Populate shapes
		for shape in shape_list:
			self.shapes.append(Shape(shape))

		# Randomize the order of the shapes and minimize the space shapes 
		# take on the board
		self.shuffle_minimize()

	def shuffle_minimize(self):
		"""Shuffles the order and orientation of the shapes, and then minimizes
		"""
		# Shuffle shape list
		shuffle(self.shapes)

		# For each shape, randomly rotate it
		for shape in self.shapes:
			shape.update_orientation(randrange(4))

		# Minimize board space
		self.minimize()

	def minimize(self, non_optimal_change=10):
		"""Compress board into smallest form given the current shapes
		The way minimize works is by finding the first place in 
		occupied_squares where the current point of the current shape
		can be placed. It then continues with the rest of the points in that
		shape until all points are placed in occupied_squares. After placement,
		the shape's offset is updated with the correct x and y values. Any 
		square that is left of the last placed shape is removed from
		ocupied_squares and all squares are shifted left such that the left
		most part of the placed shape is [0, y]. This is done to reduce the
		length of occupied_squares and speed up the 'in' operation performed.

		After this is performed, current_length is updated and the fitness
		function is evaluated.

		The fitness function is -current_length.

		Args:
			non_optimal_change (int): The % chance of not trying the first
				block that the first point could fit in. Should be between 
				0 for no chance and 100 for 100% chance 
		"""
		# Initialize x offset to 0
		x_offset = 0
		# No squares are currently occupied
		occupied_squares = []
		self.current_length = 0
		# X value of where first point of shape is placed
		first_x = -999

		### Find valid placement of shape ###
		for shape in self.shapes:
			# Get current points of the shape
			shape_coordinates = shape.get_current_coordinates()

			# See if we are in a valid state
			valid_state = False
			# x, y shape offset
			x, y = 0, 0
			# While not in valid state, look for a valid placement
			while valid_state == False:
				valid_state = True
				for point in shape_coordinates:
					# If point is already occupied or above board or if we
					# don't want to select the first possible point
					if [point[0] + x, point[1] + y] in occupied_squares or (point[1] + y) >= self.max_height \
						or (randrange(100) >= 100 - non_optimal_change and first_x != 999):
						# Increment y
						y += 1
						# If y is at max height, reset y, move right 1
						if y == self.max_height:
							y = 0
							x += 1
							x_offset += 1
						# No longer in valid state, try next offset
						valid_state = False
						first_x = -999
						break
					# Set first point's x value
					if first_x == -999:
						first_x = point[0] + x


			# Update shape's offsets
			shape.update_offset(x_offset, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.append([point[0] + x, point[1] + y])

			# Remove any occupied square left of where the last shape was placed
			occupied_squares.sort()
			while occupied_squares[0][0] < first_x: 
				occupied_squares.pop(0)
			first_x = -999

			# Shift points left by x positions
			for point in occupied_squares:
				point[0] -= x
		#####################################

		# Add remaining offset to current length
		# Find current length
		self.current_length = 0
		for shape in self.shapes:
			x_value = shape.max_x_value()
			if self.current_length < x_value:
				self.current_length = x_value

		# Fitness Function
		self.fitness = -self.current_length

	def print_info(self):
		"""Print original point with offset and active rotation of each shape
		Prints the original point (what was [0, 0] before normalizing) in
		the following format:
			(x + x_offset),(y + y_offset),(active rotation)
		This would look something like this:
			5,7,1
		If the base x and y are [2,1] and the offsets are 3 and 6 for x, y with
		a 90 degree rotation.

		NOTE:
			Should only be called when shape order no longer matters (end of 
			program). This is because the original order is brought back.
		"""
		self.shapes.sort(key=lambda shape: shape.original_order)
		for shape in self.shapes:
			shape.print_offset_orientation()

	def get_info(self):
		"""Returns original point with offset and active rotation
		Return the original point (what was [0, 0] before normalizing) in
		the following format:
			(x + x_offset),(y + y_offset),(active rotation)
		This would look something like this:
			5,7,1
		If the base x and y are [2,1] and the offsets are 3 and 6 for x, y with
		a 90 degree rotation.

		NOTE:
			Should only be called when shape order no longer matters (end of 
			program). This is because the original order is brought back.

		Returns:
			(list of str): List of strings for each shape's x,y,rotation where
				x and y are the original's point with offset
				Example: ['x,y,rotation', '1,2,0', ...]
		"""
		self.shapes.sort(key=lambda shape: shape.original_order)

		info = []
		for shape in self.shapes:
			info.append(shape.get_offset_orientation())

		return info

	def __lt__(self, other):
		"""Defines less than to be the lower fitness value
		Less than is the lower fitness value. For sorting, max fitness
		value should be considered
		Returns:
			(bool) Fitness value is less than other's
		"""
		return self.fitness < other.fitness

if __name__ == "__main__":
	points = ["R1 D1", "D1 L4 R1 U3 R3"]
	#points = ["R1", "R1 D3 U4 L2", "R1 L4", "R1 U2 R1"]

	b = Board(points, 5)

	print(b.current_length)
	b.print_info()