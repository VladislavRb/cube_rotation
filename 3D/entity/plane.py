from entity.vector import Vector
from entity.point import Point


class Plane:
    def __init__(self, frame_origin: Point, frame_vector1: Vector, frame_vector2: Vector):
        self.frame_origin = frame_origin
        self.frame_vector1 = frame_vector1
        self.frame_vector2 = frame_vector2

        self.n = Vector(self.frame_vector1.y * self.frame_vector2.z - self.frame_vector2.y * self.frame_vector1.z,
                        self.frame_vector2.x * self.frame_vector1.z - self.frame_vector1.x * self.frame_vector2.z,
                        self.frame_vector1.x * self.frame_vector2.y - self.frame_vector1.y * self.frame_vector2.x)

        self.margin = -self.n.dot(self.frame_origin)

    def equation_value(self, point: Point):
        return self.n.dot(point) + self.margin

    def signed_dist_to(self, point: Point):
        return self.equation_value(point) / self.n.norm()
