import numpy as np


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def init_by_two_points(self, point1, point2):
        self.x = point2.x - point1.x
        self.y = point2.y - point1.y
        self.z = point2.z - point1.z

    def norm(self):
        return np.linalg.norm([self.x, self.y, self.z])

    def dot(self, other):
        return np.dot([self.x, self.y, self.z], [other.x, other.y, other.z])

    def invert(self):
        self.x *= -1
        self.y *= -1
        self.z *= -1

    def coord_list(self):
        return [self.x, self.y, self.z]
