import numpy as np
from tkinter import Tk, Canvas, Label, N

from entity.cube import Cube


class Draw:
    def __init__(self, cube: Cube, window_width: float, window_height: float):
        self.window_width = window_width
        self.window_height = window_height

        self.window = Tk()
        self.window.geometry(str(self.window_width) + "x" + str(self.window_height))

        self.canvas = Canvas(self.window, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.cube = cube

        self.cf_limit = self.cube.side * np.sqrt(2) / self.window_height
        self.scaling_border = 1
        self.default_scale_step = (self.scaling_border - self.cf_limit) / 2

        self.rotation_angle = np.pi / 16
        self.delta = self.default_scale_step

        # for cube text info
        self.total_horizontal_rotation_angle = 0
        self.total_vertical_rotation_angle = 0

        self.draw_initial_cube_state()

        self.window.bind("<Up>", lambda event: self.update_image("up"))
        self.window.bind("<Down>", lambda event: self.update_image("down"))
        self.window.bind("<Left>", lambda event: self.update_image("left"))
        self.window.bind("<Right>", lambda event: self.update_image("right"))
        self.window.bind("<Key-w>", lambda event: self.update_image("forward"))
        self.window.bind("<Key-s>", lambda event: self.update_image("backward"))

        self.window.mainloop()

    def draw_initial_cube_state(self):
        self.cube.project_on(self.cube.projection_plane)
        self.draw_cube()

    def info_label_text(self):
        info_label_str = "Press arrow keys to rotate, W/S - to move forward/backward\n\n"

        cube_center_coordinates = np.around(self.cube.cube_center.coord_list(), 2)
        info_label_str += "cube center: x = " + str(cube_center_coordinates[0])\
            + ", y = " + str(cube_center_coordinates[1])\
            + ", z = " + str(cube_center_coordinates[2]) + "\n"

        info_label_str += "total horizontal rotation angle = " + str(self.total_horizontal_rotation_angle) + "\n"
        info_label_str += "total vertical rotation angle = " + str(self.total_vertical_rotation_angle)

        return info_label_str

    def scaled_image(self):
        return self.cube.projection_plane.projected_faces / self.cube.cam_far

    def rotate_and_update_cube(self, rotation_direction: str):
        self.cube.rotate(self.rotation_angle, rotation_direction)

        self.cube.projection_plane.projected_faces = []
        self.cube.projection_plane.projected_face_colors = []

        self.cube.project_on(self.cube.projection_plane)

    def scale_and_update_cube(self, scale_direction: str):
        self.cube.scale(self.delta, scale_direction)

        self.cube.projection_plane.projected_faces = []
        self.cube.projection_plane.projected_face_colors = []

        self.cube.project_on(self.cube.projection_plane)

    def draw_cube(self):
        shapes_coordinates = self.scaled_image()

        for i in range(len(shapes_coordinates)):
            shape_coordinates = shapes_coordinates[i]

            raveled_shape_coordinates = list(np.ravel(shape_coordinates))
            canvas_poly_coordinates = [raveled_shape_coordinates[ind] +
                                       (self.window_height / 2 if ind % 2 else self.window_width / 2)
                                       for ind in range(len(raveled_shape_coordinates))]

            self.canvas.create_polygon(
                *canvas_poly_coordinates, outline="black", fill=self.cube.projection_plane.projected_face_colors[i])

        info_label = Label(self.canvas, width=400, height=100, anchor="ne", font="Arial 11", text=self.info_label_text())
        self.canvas.create_window(self.window_width / 2, 0, width=400, height=100, anchor=N, window=info_label)

    def update_image(self, instruction: str):
        if instruction == "up" or instruction == "down" or instruction == "left" or instruction == "right":
            rotation_angle_in_degrees = self.rotation_angle * 180 / np.pi

            if instruction == "up" or instruction == "down":
                if instruction == "up":
                    self.total_vertical_rotation_angle += rotation_angle_in_degrees
                else:
                    self.total_vertical_rotation_angle -= rotation_angle_in_degrees

                if self.total_vertical_rotation_angle < 0 or self.total_vertical_rotation_angle >= 360:
                    self.total_vertical_rotation_angle %= 360
            else:
                if instruction == "right":
                    self.total_horizontal_rotation_angle += rotation_angle_in_degrees
                else:
                    self.total_horizontal_rotation_angle -= rotation_angle_in_degrees

                if self.total_horizontal_rotation_angle < 0 or self.total_horizontal_rotation_angle >= 360:
                    self.total_horizontal_rotation_angle %= 360

            self.rotate_and_update_cube(instruction)
        else:
            if self.cube.cam_far <= self.scaling_border:
                if instruction == "backward":
                    self.delta = (self.cube.cam_far - self.cf_limit) / 2
                else:
                    self.delta = self.cube.cam_far - self.cf_limit
            else:
                self.delta = self.default_scale_step

            self.scale_and_update_cube(instruction)

        self.canvas.delete("all")
        self.draw_cube()
