from entity.point import Point
from entity.plane import Plane
from entity.vector import Vector
from entity.project_plane import ProjectPlane
from entity.face import Face

import numpy as np


class Cube:
    def __init__(self, *faces):
        self.faces = list(faces)
        self.faces_amount = 6

        side_vector = Vector()
        side_vector.init_by_two_points(self.faces[0].vertices[0], self.faces[0].vertices[1])

        self.side = side_vector.norm()
        self.r = self.side / np.sqrt(2)

        self.cube_center = Point()

        face_centers = [face.center() for face in self.faces]

        for face_center in face_centers:
            self.cube_center = self.cube_center + face_center

        self.cube_center.x /= self.faces_amount
        self.cube_center.y /= self.faces_amount
        self.cube_center.z /= self.faces_amount

        self.cam_far = self.cube_center.y - self.r

        for i in range(self.faces_amount):
            if self.faces[i].plane.signed_dist_to(self.cube_center) > 0:
                self.faces[i].plane.n.invert()

        projection_plane_origin = Point(0, self.cam_far, 0)

        self.projection_plane = ProjectPlane(
            Plane(projection_plane_origin, Vector(1, 0, 0), Vector(0, 0, 1)), projection_plane_origin)

        if self.projection_plane.plane.signed_dist_to(self.cube_center) < 0:
            self.projection_plane.plane.n.invert()

        self.project_on(self.projection_plane)

    def rotation_matrix(self, angle: float, rotation_direction: str):
        d = np.linalg.norm(self.cube_center.coord_list())
        angle *= 1 if rotation_direction == "left" or rotation_direction == "down" else -1

        if rotation_direction == "left" or rotation_direction == "right":
            return [[np.cos(angle), -np.sin(angle), 0, d * np.sin(angle)],
                    [np.sin(angle), np.cos(angle), 0, d - d * np.cos(angle)],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]

        return [[1, 0, 0, 0],
                [0, np.cos(angle), -np.sin(angle), d - d * np.cos(angle)],
                [0, np.sin(angle), np.cos(angle), -d * np.sin(angle)],
                [0, 0, 0, 1]]

    def scaling_matrix(self, delta: float, scale_direction: str):
        return [[1, 0, 0, 0],
                [0, 1, 0, delta * (1 if scale_direction == "forward" else -1)],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

    def rotate(self, angle: float, rotation_direction: str):
        rot_matrix = np.array(self.rotation_matrix(angle, rotation_direction))

        for face_index in range(self.faces_amount):
            face_color = self.faces[face_index].color
            face_vertices = self.faces[face_index].vertices

            for i in range(len(face_vertices)):
                face_vertex = face_vertices[i]

                face_vertex_coords = np.array([*face_vertex.coord_list(), 1])

                new_face_vertex_coords = rot_matrix @ face_vertex_coords
                new_face_vertex = Point(new_face_vertex_coords[0], new_face_vertex_coords[1], new_face_vertex_coords[2])

                face_vertices[i] = new_face_vertex

            new_face = Face(face_color, *face_vertices)

            if new_face.plane.signed_dist_to(self.cube_center) > 0:
                new_face.plane.n.invert()

            self.faces[face_index] = new_face

    def scale(self, delta: float, scale_direction: str):
        sc_matrix = np.array(self.scaling_matrix(delta, scale_direction))
        self.cube_center.y += delta * (1 if scale_direction == "forward" else -1)

        for face_index in range(self.faces_amount):
            face_color = self.faces[face_index].color
            face_vertices = self.faces[face_index].vertices

            for i in range(len(face_vertices)):
                face_vertex = face_vertices[i]

                face_vertex_coords = np.array([*face_vertex.coord_list(), 1])

                new_face_vertex_coords = sc_matrix @ face_vertex_coords
                new_face_vertex = Point(new_face_vertex_coords[0], new_face_vertex_coords[1], new_face_vertex_coords[2])

                face_vertices[i] = new_face_vertex

            new_face = Face(face_color, *face_vertices)

            if new_face.plane.signed_dist_to(self.cube_center) > 0:
                new_face.plane.n.invert()

            self.faces[face_index] = new_face

        self.cam_far += delta * (1 if scale_direction == "forward" else -1)

        projection_plane_origin = Point(0, self.cam_far, 0)

        self.projection_plane = ProjectPlane(
            Plane(projection_plane_origin, Vector(1, 0, 0), Vector(0, 0, 1)), projection_plane_origin)

        if self.projection_plane.plane.signed_dist_to(self.cube_center) < 0:
            self.projection_plane.plane.n.invert()

    def project_on(self, projection_plane: ProjectPlane):
        for face in self.faces:
            if projection_plane.plane.n.dot(face.plane.n) < 0:
                projection_plane.project_face(face)

    def __str__(self):
        cube_str = ""

        for face in self.faces:
            for vertex in face.vertices:
                cube_str += str(vertex.coord_list()) + " → "

            cube_str += "\n"

        return cube_str
