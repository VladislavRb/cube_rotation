class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def coord_list(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)
