from entity.point import Point
from entity.face import Face
from entity.cube import Cube


face_colors = ["red", "green", "blue", "yellow", "orange", "brown"]

face1 = Face(face_colors[0], Point(50, 22, 50), Point(-50, 22, 50), Point(-50, 22, -50), Point(50, 22, -50))
face2 = Face(face_colors[1], Point(50, 122, 50), Point(-50, 122, 50), Point(-50, 122, -50), Point(50, 122, -50))
face3 = Face(face_colors[2], Point(-50, 22, -50), Point(-50, 122, -50), Point(-50, 122, 50), Point(-50, 22, 50))
face4 = Face(face_colors[3], Point(50, 22, -50), Point(50, 122, -50), Point(50, 122, 50), Point(50, 22, 50))
face5 = Face(face_colors[4], Point(50, 22, -50), Point(50, 122, -50), Point(-50, 122, -50), Point(-50, 22, -50))
face6 = Face(face_colors[5], Point(50, 22, 50), Point(50, 122, 50), Point(-50, 122, 50), Point(-50, 22, 50))

cube_sample1 = Cube(face1, face2, face3, face4, face5, face6)
