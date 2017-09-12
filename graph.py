import numpy as np
from numpy import ma
import matplotlib.pyplot as plt

# First instance, run 8
x1 = [1,2,33,185,542,1000]
y1 = [-19,-18,-17,-16,-15,-15]

plt.step(x1, y1, label="First Instance, Run 8")

plt.legend(loc='lower right')
plt.xlim(0, 1000)

plt.savefig('./graphs/instance1')
plt.show()

# Second instace, run 1
x1 = [1,8,14,29,67,1000]
y1 = [-49,-47,-46,-45,-42,-42]

plt.step(x1, y1, label="Second Instance, Run 1")

plt.legend(loc='lower right')
plt.xlim(0, 1000)

plt.savefig('./graphs/instance2')
plt.show()

# Third instance, run 23
x1 = [1,2,13,21,52,88,177,429,1000]
y1 = [-137,-127,-124,-121,-120,-116,-115,-109,-109]

plt.step(x1, y1, label="Third Instance, Run 23")

plt.legend(loc='lower right')
plt.xlim(0, 1000)

plt.savefig('./graphs/instance3')
plt.show()

print("Files saved to ./graphs*")