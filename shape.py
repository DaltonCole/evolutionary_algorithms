# File name:      shape.py
# Author:         Dalton Cole

from shape_base import Shape_base
from random import randrange

class Shape(Shape_base):
	"""Used as an interface to Shape_base
	This class is used to implement Shape_base without requiring the
	expensive calculations from it each time a new board is created.
	Instead, the Shape_bases can be initialized and passed into this class.
	This class then overrides the relevant member variables.

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
	def __init__(self, base_shape):
		### Stuff to shallow copy ###
		self.original_order = base_shape.original_order
		self.four_shapes = base_shape.four_shapes
		self.original_point = base_shape.original_point
		self.width = base_shape.width
		#############################

		### Variables that require a new version ###
		self.x_offset = 0
		self.y_offset = 0
		self.active_state = randrange(4)
		self.current_coordinates = self.four_shapes[self.active_state]
		############################################