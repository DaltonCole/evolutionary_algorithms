# File name:      board.py
# Author:         Dalton Cole

from shape import Shape
from shape_base import Shape_base
from random import shuffle 	# Shuffle list of Shapes
from random import randrange
from copy import copy

class Board:
	"""Board with shapes optimally placed given their current order and rotation

	Fitness function used is -current_length of board.

	Attributes:
		shapes (list of Shape): All of the shapes are created (so 
			shape.original_order is maintained) and then randomly shuffled.
		max_height (int): Max height of the board (grid)
		max_width (int): Max width of board (grid)
		divide_max_width (int): Used for "Random*" placement
			Randomly select x = rand(max_width // divide_max_width
			Gets updated when random fails to place fail_max number of times
		fail_max (int): Number of tries to place a shape before 
			divide_max_width decrements
		current_length (int): The current length (max x) of the board
		fitness (int): Fitness eval = -current_length
		placement_algorithm (string): Algorithm to place with
			"Minimize": Minimize by placing in most bottom left corner
			"Random": Randomly place shapes
			"Random with Repair": Randomly place shapes with repair
		penalty_value (int): What each constraint penalty costs
		penalty_weight (int): The weight to scale each penalty_value
	"""
	max_height = 0
	max_width = 0
	placement_algorithm = "Minimize"
	divide_max_width = 0
	fail_max = 20
	penalty_value = 1
	penalty_weight = 1

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

		# Minimize the space shapes take on the board
		self.minimize()

	@classmethod
	def set_placement_algorithm(self, algorithm):
		"""Set placement algorithm

		Args:
			(string): Placement algorithm
		"""
		self.placement_algorithm = algorithm

	def place_shapes(self, randomize=False):
		"""Places shapes on the grid with the specified algorithm

		Args:
			randomize (bool): Randomize placement of shapes
		"""
		if randomize == True:
			self.shuffle()

		if self.placement_algorithm == "Minimize":
			self.minimize()
		elif self.placement_algorithm == "Random":
			self.random_placement()
		elif self.placement_algorithm == "Random with Repair":
			self.random_placement_with_repair()
		elif self.placement_algorithm == "Random with Penalty":
			self.random_placement_with_penalty()
		else:
			print("ERROR IN: place_shapes! " + str(self.placement_algorithm)); quit()

	def shuffle(self):
		"""Shuffles the order and orientation of the shapes, and then minimizes
		"""
		# Shuffle shape list
		shuffle(self.shapes)

		# For each shape, randomly rotate it
		for shape in self.shapes:
			shape.update_orientation(randrange(4))

	########################## Placement Algorithms ##########################
	def minimize(self, non_optimal_change=0):
		"""Compress board into smallest form given the current shapes
		The way minimize works is by finding the first place in 
		occupied_squares where the current point of the current shape
		can be placed. It then continues with the rest of the points in that
		shape until all points are placed in occupied_squares. After placement,
		the shape's offset is updated with the correct x and y values.

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
		occupied_squares = set()
		self.current_length = 0
		# X value of where first point of shape is placed
		first_x = -999

		# x, y shape offset
		x, y = 0, 0

		### Find valid placement of shape ###
		for shape in self.shapes:
			# Get current points of the shape
			shape_coordinates = shape.get_current_coordinates()

			# See if we are in a valid state
			valid_state = False
			
			# While not in valid state, look for a valid placement
			while valid_state == False:
				valid_state = True
				for point in shape_coordinates:
					# If point is already occupied or above board or if we
					# don't want to select the first possible point
					if (point[0] + x, point[1] + y) in occupied_squares or (point[1] + y) >= self.max_height \
						or (randrange(100) >= 100 - non_optimal_change and first_x != -999):
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
			shape.update_offset(x, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.add((point[0] + x, point[1] + y))
		#####################################

		# Update fitness value
		self.update_fitness_value()

	def random_placement(self):
		"""Randomly place shapes on the board

		Randomly places shapes on the board between (0,0) and 
		(max_width, max_height).

		After this is performed, current_length is updated and the fitness
		function is evaluated.

		The fitness function is -current_length.
		"""
		# Initialize x offset to 0
		x_offset = 0
		# No squares are currently occupied
		occupied_squares = set()
		self.current_length = 0

		# x, y shape offset
		x, y = 0, 0

		### Find valid placement of shape ###
		for shape in self.shapes:
			# Get current points of the shape
			shape_coordinates = shape.get_current_coordinates()

			# See if we are in a valid state
			valid_state = False

			# Number of failed placements for shape
			fails = 0
			
			# While not in valid state, look for a valid placement
			while valid_state == False:
				valid_state = True

				if fails >= self.fail_max:
					self.divide_max_width -= 1
					fails = 0
					if self.divide_max_width == 0:
						self.divide_max_width = 1

				# Chose a random x and y within range
				x = randrange(0, self.max_width // self.divide_max_width)
				y = randrange(0, self.max_height)

				for point in shape_coordinates:
					# If point is already occupied or above board or if we
					# don't want to select the first possible point
					if (point[0] + x, point[1] + y) in occupied_squares or (point[1] + y) >= self.max_height \
						or (point[0] + x) >= self.max_width:
						# No longer in valid state, try next offset
						valid_state = False
						fails += 1
						break

			# Update shape's offsets
			shape.update_offset(x, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.add((point[0] + x, point[1] + y))
		#####################################

		# Update fitness value
		self.update_fitness_value()

	def random_placement_with_repair(self, repair_tries=2, x_move=-1, y_move=-1):
		"""Randomly place shapes on the board while using a repair function

		Randomly places shapes on the board between (0,0) and 
		(max_width, max_height). If overlap occurs, try to move shape by
		(x + x_move, y + y_move) places repair_tries times

		After this is performed, current_length is updated and the fitness
		function is evaluated.

		The fitness function is -current_length.

		Args:
			repair_tries (int): Number of times shape is moved before
				giving up
			x_move (int): X offset to move by if shape placement fails
			y_move (int): Y offset to move by if shape placement fails
		"""
		# Initialize x offset to 0
		x_offset = 0
		# No squares are currently occupied
		occupied_squares = set()
		self.current_length = 0

		# x, y shape offset
		x, y = 0, 0

		### Find valid placement of shape ###
		for shape in self.shapes:
			# Get current points of the shape
			shape_coordinates = shape.get_current_coordinates()

			# See if we are in a valid state
			valid_state = False

			# Current number of repair attempts
			repair_attempts = 0

			# Number of failed placements for shape
			fails = 0
			
			# While not in valid state, look for a valid placement
			while valid_state == False:
				valid_state = True
				
				if fails >= self.fail_max:
					self.divide_max_width -= 1
					fails = 0
					if self.divide_max_width == 0:
						self.divide_max_width = 1

				if repair_attempts == 0 or repair_attempts > repair_tries:
					# Chose a random x and y within range
					x = randrange(0, self.max_width // self.divide_max_width)
					y = randrange(0, self.max_height)
					repair_attempts = 0

				for point in shape_coordinates:
					# If point is already occupied or above board or if we
					# don't want to select the first possible point
					if (point[0] + x, point[1] + y) in occupied_squares or (point[1] + y) >= self.max_height \
						or (point[0] + x) >= self.max_width or (point[0] + x) < 0 or (point[1] + y) < 0:
						# No longer in valid state, try next offset
						repair_attempts += 1
						fails += 1
						x += x_move
						y += y_move
						valid_state = False
						break

			# Update shape's offsets
			shape.update_offset(x, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.add((point[0] + x, point[1] + y))
		#####################################

		# Update fitness value
		self.update_fitness_value()

	def random_placement_with_penalty():
		pass
	##########################################################################

	def random_replacement(self, shape_index):
		"""Randomly re-place a shape on the board

		Randomly places shapes on the board between (0,0) and 
		(max_width, max_height).
		"""
		# Initialize x offset to 0
		x_offset = 0
		# No squares are currently occupied
		occupied_squares = set()
		self.current_length = 0

		# x, y shape offset
		x, y = 0, 0

		# Populate occupied squares
		for i in range(0, len(self.shapes)):
			if i == shape_index:
				continue
			# Add points to occupied squares
			shape = self.shapes[i]
			shape_coordinates = shape.get_current_coordinates()
			x = shape.x_offset
			y = shape.y_offset
			for point in shape_coordinates:
				occupied_squares.add((point[0] + x, point[1] + y))

		# Set valid state to False
		valid_state = False

		# Set shape coordinates
		shape_coordinates = self.shapes[shape_index].get_current_coordinates()

		# Set fail count
		fails = 0

		# While not in valid state, look for a valid placement
		while valid_state == False:
			valid_state = True

			if fails >= self.fail_max:
				self.divide_max_width -= 1
				fails = 0
				if self.divide_max_width == 0:
					self.divide_max_width = 1

			# Chose a random x and y within range
			x = randrange(0, self.max_width // self.divide_max_width)
			y = randrange(0, self.max_height)

			for point in shape_coordinates:
				# If point is already occupied or above board or if we
				# don't want to select the first possible point
				if (point[0] + x, point[1] + y) in occupied_squares or (point[1] + y) >= self.max_height \
					or (point[0] + x) >= self.max_width:
					# No longer in valid state, try next offset
					valid_state = False
					fails += 1
					break

		# Update shape's offsets
		self.shapes[shape_index].update_offset(x, y)

	def update_fitness_value(self):
		"""Update fitness
		"""
		# Add remaining offset to current length
		# Find current length
		self.current_length = 0
		for shape in self.shapes:
			x_value = shape.max_x_value()
			if self.current_length < x_value:
				self.current_length = x_value

		# Fitness Function
		self.fitness = -self.current_length

	def check_for_overlap(self):
		"""Checks for shape overlap

		If shape overlap is found, randomly place second shape
		"""
		# Initialize x offset to 0
		x_offset = 0
		# No squares are currently occupied
		occupied_squares = set()
		self.current_length = 0

		# x, y shape offset
		x, y = 0, 0

		# Shapes to move
		moving_shapes = []

		### Find valid placement of shape ###
		for shape in self.shapes:
			# Get current points of the shape
			shape_coordinates = shape.get_current_coordinates()

			for point in shape_coordinates:
				if (point[0] + shape.x_offset, point[1] + shape.y_offset) not in occupied_squares:
					occupied_squares.add((point[0] + shape.x_offset, point[1] + shape.y_offset))
				else:
					# Add shape to move shape list
					print("bing\n")
					moving_shapes.append(shape)

		for shape in moving_shapes:
			# See if we are in a valid state
			valid_state = False
			
			# While not in valid state, look for a valid placement
			while valid_state == False:
				valid_state = True

				# Chose a random x and y within range
				x = randrange(0, self.max_width)
				y = randrange(0, self.max_height)

				for point in shape_coordinates:
					# If point is already occupied or above board or if we
					# don't want to select the first possible point
					if (point[0] + x, point[1] + y) in occupied_squares or (point[1] + y) >= self.max_height \
						or (point[0] + x) >= self.max_width:
						# No longer in valid state, try next offset
						valid_state = False
						break

			# Update shape's offsets
			shape.update_offset(x, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.add((point[0] + x, point[1] + y))
		#####################################

		# Update fitness value
		self.update_fitness_value()

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

	def get_area(self):
		"""Get the area of occupied points the board takes up
		This is to test for overlap. This returns the number of points
		that are covered on the board.

		Returns:
			(int): Area covered on board
		"""
		points = set()

		for shape in self.shapes:
			for point in shape.get_all_tuple_points():
				points.add(point)

		return len(points)

	def test_for_overlap(self):
		"""Test to see if there is overlap. True = overlap
		Tests to see if there is overlap. This happens by finding the total
		area the board takes up and seeing if that is equal to the number
		of points in all the shapes.

		Returns:
			(bool): True if overlap occurs, False otherwise
		"""
		total_area = self.get_area()

		num_points = 0
		for shape in self.shapes:
			num_points += shape.get_number_of_points()

		return total_area != num_points

	def find_original_order(self, original_order_to_find):
		"""Find the index of original order value in shapes list

		Returns:
			(int): Index
		"""
		for i, shape in enumerate(self.shapes):
			if shape.get_original_order() == original_order_to_find:
				return i

	def find_max_width(self):
		"""Finds the max width by summing all of shape's width
		"""
		max_width = 0
		for shape in self.shapes:
			max_width += shape.width

		return max_width

	def __lt__(self, other):
		"""Defines less than to be the lower fitness value
		Less than is the lower fitness value. For sorting, max fitness
		value should be considered
		Returns:
			(bool) Fitness value is less than other's
		"""
		return self.fitness < other.fitness

	def __len__(self):
		"""Defines len() for Board as the number of shapes

		Returns:
			(int): The number of shapes
		"""
		return len(self.shapes)

	def __getitem__(self, index):
		"""Define get [] as shape[index]

		Returns:
			(Shape): Shape at index
		"""
		return self.shapes[index]

	def __setitem__(self, index, value):
		"""Define set []

		Updates shapes[index] with value. Updates orientation
		to make sure not shallow copy.
		"""
		self.shapes[index] = copy(value)
		self.shapes[index].update_orientation(value.get_current_orientation())

	def __eq__(self, other):
		for s, t in zip(self.shapes, other.shapes):
			if s != t:
				return False
		return True

	def __hash__(self):
		s = ''
		for shape in self.shapes:
			s += str(shape.original_order)
			s += ' '
			s += str(shape.active_state)
			s += ' '
		return hash(s)


if __name__ == "__main__":
	points = ["R1 D1", "D1 L4 R1 U3 R3"]
	#points = ["R1", "R1 D3 U4 L2", "R1 L4", "R1 U2 R1"]
	shape_list = []
	for i in range(len(points)):
		shape_list.append(Shape_base(points[i], i))

	Board.max_height = 50

	b = Board(shape_list)
	c = Board(shape_list)

	print(b == c)
	b.print_info()
	print()
	c.print_info()


	"""
	print(b.current_length)
	b.print_info()
	print()

	c = Board(shape_list)
	c.print_info()
	c[0] = b[1]
	print()
	
	c[0].update_orientation(3)
	c.print_info()
	print(c[0].active_state)
	"""