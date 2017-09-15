
from shape_base import Shape_base
from random import randrange

# current_coordinates
# x_offset
# y_offset
# active_state

class Shape(Shape_base):
	def __init__(self, base_shape):
		### Stuff too shallow copy ###
		self.original_order = base_shape.original_order
		self.four_shapes = base_shape.four_shapes
		self.original_point = base_shape.original_point
		self.width = base_shape.width
		##############################

		self.x_offset = 0
		self.y_offset = 0
		self.active_state = randrange(4)
		self.current_coordinates = self.four_shapes[self.active_state]