from entity.point import Point
from entity.vector import Vector
from entity.plane import Plane


class Face:
    def __init__(self, color: str, *vertices):
        self.color = color
        self.vertices = list(vertices)

        frame_origin = self.vertices[0]

        frame_vector1 = Vector()
        frame_vector1.init_by_two_points(self.vertices[1], frame_origin)

        frame_vector2 = Vector()
        frame_vector2.init_by_two_points(self.vertices[2], frame_origin)

        self.plane = Plane(frame_origin, frame_vector1, frame_vector2)

    def center(self):
        points_amount = len(self.vertices)

        face_center = Point()

        for vertex in self.vertices:
            face_center = face_center + vertex

        face_center.x /= points_amount
        face_center.y /= points_amount
        face_center.z /= points_amount

        return face_center
