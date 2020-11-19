from entity.point import Point
from entity.vector import Vector
from entity.plane import Plane
from entity.face import Face


class ProjectPlane:
    def __init__(self, three_dimensional_plane: Plane, three_dimensional_origin: Point):
        self.projected_faces = []
        self.projected_face_colors = []

        self.origin = three_dimensional_origin
        self.plane = three_dimensional_plane

    def vector_coordinates_on_plane(self, vector: Vector):
        basis_vector_non_zero_coordinates = []
        corresponding_vector_coordinates = []

        if self.plane.frame_vector1.x or self.plane.frame_vector2.x:
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector1.x)
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector2.x)

            corresponding_vector_coordinates.append(vector.x)

        if self.plane.frame_vector1.y or self.plane.frame_vector2.y:
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector1.y)
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector2.y)

            corresponding_vector_coordinates.append(vector.y)

        if not len(basis_vector_non_zero_coordinates) == 4:
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector1.z)
            basis_vector_non_zero_coordinates.append(self.plane.frame_vector2.z)

            corresponding_vector_coordinates.append(vector.z)

        [x1, x2, y1, y2] = basis_vector_non_zero_coordinates
        [v1, v2] = corresponding_vector_coordinates

        alpha = (v2 * y1 - v1 * y2) / (x2 * y1 - x1 * y2)
        beta = (v1 * x2 - v2 * x1) / (y1 * x2 - y2 * x1)

        return [alpha, beta]

    def point_projection(self, point: Point):
        point_projection_line_parameter = -self.plane.equation_value(point) / self.plane.n.norm() ** 2
        point_projection = Point(self.plane.n.x * point_projection_line_parameter + point.x,
                                 self.plane.n.y * point_projection_line_parameter + point.y,
                                 self.plane.n.z * point_projection_line_parameter + point.z)

        point_projection_radius_vector = Vector()
        point_projection_radius_vector.init_by_two_points(point_projection, self.origin)

        return self.vector_coordinates_on_plane(point_projection_radius_vector)

    def project_face(self, face: Face):
        face_projection = list(map(lambda vertex: self.point_projection(vertex), face.vertices))

        self.projected_faces.append(face_projection)
        self.projected_face_colors.append(face.color)
