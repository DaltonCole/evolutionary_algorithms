from shape import Shape

class Board:
	def __init__(self, shape_string_list, max_height):
		self.shapes = []
		self.max_height = max_height

		for i in range(len(shape_string_list)):
			self.shapes.append(Shape(shape_string_list[i], i))

		self.worst_length = 0
		for shape in self.shapes:
			self.worst_length += shape.width

		self.minimize()

	def minimize(self):
		"""Compress board into smalles form given the current shapes

		TODO: Random placement on y axis
		"""
		x_offset = 0
		occupied_squares = []
		self.current_length = 0

		for shape in self.shapes:
			shape_coordinates = shape.get_base_coordinates()
			#print(shape_coordinates)

			### Find valid placement of shape
			valid_state = False
			# x, y shape offset
			x, y = 0, 0
			while valid_state == False:
				valid_state = True
				for point in shape_coordinates:
					if [point[0] + x, point[1] + y] in occupied_squares or (point[1] + y) >= self.max_height:
						# Increment y
						y += 1
						# If y is at max height, reset y, move right 1
						if y == self.max_height:
							y = 0
							x += 1
							x_offset += 1
						# No longer in valid state, try next offset
						valid_state = False
						#print(str(point[0]+x) + " " + str(point[1]+y))
						break

			# Update shape's offsets
			shape.update_offset(x, y)

			# Add points to occupied squares
			for point in shape_coordinates:
				occupied_squares.append([point[0] + x, point[1] + y])

			# Remove any occupied square left of where the last shape was placed
			occupied_squares.sort()
			#print(occupied_squares)
			while occupied_squares[0][0] < x:
				occupied_squares.pop(0)

			# Shift points left by x positions
			for point in occupied_squares:
				point[0] -= x

			# Add x to current length
			self.current_length += x

		# Add remaining offset to current length
		self.current_length += occupied_squares[-1][0] + 1

		# Fitness Function
		self.fitness = -self.current_length

		## Testing width
		self.current_length = 0
		for shape in self.shapes:
			x_value = shape.max_x_value()
			if self.current_length < x_value:
				self.current_length = x_value
		self.fitness = -self.current_length
		print(self.current_length)

	def print_info(self):
		# Should only be called when shape order no longer matters (end of program)
		self.shapes.sort(key=lambda shape: shape.original_order)
		for shape in self.shapes:
			shape.print_offset_orientation()
			#print(shape.four_shapes[shape.active_state])

	def get_info(self):
		# Should only be called when shape order no longer matters (end of program)
		self.shapes.sort(key=lambda shape: shape.original_order)

		info = []
		for shape in self.shapes:
			info.append(shape.get_offset_orientation())

		return info

	def __lt__(self, other):
		return self.fitness < other.fitness

if __name__ == "__main__":
	points = ["R1 D1", "D1 L4 R1 U3 R3"]
	#points = ["R1", "R1 D3 U4 L2", "R1 L4", "R1 U2 R1"]

	b = Board(points, 5)

	print(b.current_length)
	b.print_info()