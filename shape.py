from itertools import groupby
from random import randrange

class Shape:

	def __init__(self, shape_string, original_order):
		self.original_order = original_order
		self.active_state = randrange(4)

		movements = shape_string.split()

		self.four_shapes = []
		self.original_point = []
		### 0 degree rotation ###
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(direction, amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)

		### 90 degree rotation ###
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(self._transform_direction(1, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)

		### 180 degree rotation ###
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(self._transform_direction(2, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape)

		### 270 degree rotation ###
		generated_shape = [[0, 0]]
		x = 0
		y = 0
		for movement in movements:
			direction, amount = movement[0], int(movement[1:])
			x, y = self._generate_shape(self._transform_direction(3, direction), amount, x, y, generated_shape)

		# Normalize and add to shape list
		generated_shape = self._normalize_shape(generated_shape)
		self.four_shapes.append(generated_shape) # Always normalized coordinates

		### Find width of original shape ###
		self.width = self._find_width(self.four_shapes[0])

		### Current coordinates ###
		self.current_coordinates = self.four_shapes[self.active_state]

		### Current Offsets ###
		self.x_offset = 0
		self.y_offset = 0

	def update_orientation(self, orientation):
		self.active_state = orientation

	def get_current_coordinates(self):
		return self.current_coordinates

	def get_base_coordinates(self):
		return self.four_shapes[self.active_state]

	def get_current_orientation(self):
		return self.active_state

	def get_current_offset(self):
		return [self.x_offset, self.y_offset]

	def get_original_point_of_active_shape(self):
		return self.original_point[self.active_state]

	def update_offset(self, x, y):
		self.x_offset = x
		self.y_offset = y

	def print_offset_orientation(self):
		print(str(self.x_offset + self.original_point[self.active_state][0]) + 
			"," + str(self.y_offset + self.original_point[self.active_state][1]) + 
			"," + str(self.active_state))

	def get_offset_orientation(self):
		return (str(self.x_offset + self.original_point[self.active_state][0]) + 
					"," + str(self.y_offset + self.original_point[self.active_state][1]) + 
					"," + str(self.active_state))

	def print_all_shapes(self):
		for point in self.four_shapes[self.active_state]:
			print("[" + str(self.x_offset + point[0]) + ", " + str(self.y_offset + point[1])+"]", end=", ")
		print()

	def _generate_shape(self, direction, amount, x, y, generated_shape):
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

		self.original_point.append([-min_x, -min_y])

		return generated_shape

	def _find_width(self, generated_shape):
		max_x = 0

		for point in generated_shape:
			if point[0] > max_x:
				max_x = point[0]

		return max_x

if __name__ == '__main__':
	# s = Shape("R5 L7 U2 R3 D2")
	# s = Shape("D2 L3 U2 R3")
	s = Shape("D1 L4 R1 U3 R3")
	print(s.get_current_orientation())
	print(s.get_base_coordinates())
	print(len(s.get_base_coordinates()))