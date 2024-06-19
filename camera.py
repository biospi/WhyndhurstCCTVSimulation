import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Camera:
    def __init__(self, position, fov_width, fov_height, ground, plane, label, id):
        self.position = position
        self.fov_width = fov_width
        self.ground = ground
        self.plane = plane
        self.label = label
        self.id = id
        # self.rectangle = Rectangle3D(0,0,0,1,1, 1)
        self.fov_height = fov_height
        self.ground_distance = position[1]
        self.direction = np.array([0.0, 0.0, -1.0])  # Initial direction of the camera
        self.cube_vertices = [
            (-0.05, -0.05, -0.05),
            (0.05, -0.05, -0.05),
            (0.05, 0.05, -0.05),
            (-0.05, 0.05, -0.05),
            (-0.05, -0.05, 0.05),
            (0.05, -0.05, 0.05),
            (0.05, 0.05, 0.05),
            (-0.05, 0.05, 0.05)
        ]
        self.cube_edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),  # Bottom face
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),  # Top face
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),  # Vertical edges
        ]
        self.pyramid_vertices = self._get_pyramid_vertices()
        self.pyramid_faces = self._get_pyramid_faces()

    def _get_pyramid_vertices(self):
        half_width = self.fov_width / 2
        half_height = self.fov_height / 2
        vertices = [
            (0, 0.5, 0),  # top vertex
            (half_width, -10, half_height),  # front-right
            (-half_width, -10, half_height),  # front-left
            (-half_width, -10, -half_height),  # back-left
            (half_width, -10, -half_height)  # back-right
        ]
        return vertices

    def rotate_pyramid(self, vertices, angle_degrees, direction):
        # Convert angle from degrees to radians
        angle_radians = np.radians(angle_degrees)

        if direction == 0: #"left/right"
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle_radians), -np.sin(angle_radians)],
                [0, np.sin(angle_radians), np.cos(angle_radians)]
            ])
        if direction == 1:#front/back
            rotation_matrix = np.array([
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1]
            ])

        # The top vertex (assuming the first vertex in the list) remains fixed
        top_vertex = vertices[0]

        # Rotate all other vertices
        rotated_vertices = [top_vertex]  # Start with the top vertex unchanged
        for vertex in vertices[1:]:
            # Translate vertex to origin (relative to top_vertex)
            relative_vertex = np.array(vertex) - np.array(top_vertex)
            # Apply the rotation
            rotated_vertex = np.dot(rotation_matrix, relative_vertex)
            # Translate back
            rotated_vertex = rotated_vertex + np.array(top_vertex)
            rotated_vertices.append(tuple(rotated_vertex))

        return rotated_vertices

    def _get_pyramid_faces(self):
        faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 2, 3, 4)]
        return faces

    def draw_intersection(self):
        glDisable(GL_DEPTH_TEST)
        # Draw the slicing section
        glColor3f(1.0, 0.0, 0.0)  # Red color for the intersection section
        glBegin(GL_LINES)
        y_plane = self.plane.plane_vertices[0][1]
        for face in self._get_pyramid_faces():
            for i in range(len(face)):
                v1 = self._get_pyramid_vertices()[face[i]]
                v2 = self._get_pyramid_vertices()[face[(i + 1) % len(face)]]
                if ((y_plane < v1[1] and y_plane > v2[1]) or (v1[1] < y_plane and v2[1] > y_plane)):
                    # Interpolate to find the intersection point
                    t = (y_plane - v1[1]) / (v2[1] - v1[1])
                    intersection_point = (
                        v1[0] + t * (v2[0] - v1[0]),
                        y_plane,
                        v1[2] + t * (v2[2] - v1[2]),
                    )
                    glVertex3fv(intersection_point)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def draw_highlight(self):
        # Draw the camera cube
        glColor3f(1, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(*self.position)
        glTranslatef(0, 0.5, 0)
        self.ground._draw_object(self.cube_vertices, self.cube_edges)
        glPopMatrix()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Draw the FOV pyramid
        glPushMatrix()
        glTranslatef(*self.position)
        self.draw_intersection()

        glColor4f(0.0, 1.0, 0.0, 0.2)
        if "XNV" in self.label:
            glColor4f(39/255, 168/255, 247/255, 0.2)
        self._draw_pyramid()

        glColor4f(1.0, 0.0, 0.0, 0.2)

        # glEnable(GL_DEPTH_TEST)
        glColor4f(0.5, 0.5, 0.5, 1)
        self.ground._draw_object(
            self.pyramid_vertices,
            [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)],
        )
        glPopMatrix()
        glDisable(GL_BLEND)
        glColor3f(1.0, 1.0, 1.0)  # Reset color to white

    def draw(self):
        # Draw the camera cube
        glPushMatrix()
        glTranslatef(*self.position)
        glTranslatef(0, 0.5, 0)
        self.ground._draw_object(self.cube_vertices, self.cube_edges)
        glPopMatrix()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Draw the FOV pyramid
        glPushMatrix()
        glTranslatef(*self.position)
        self.draw_intersection()

        glColor4f(0.0, 1.0, 0.0, 0.2)
        if "XNV" in self.label:
            glColor4f(39/255, 168/255, 247/255, 0.2)
        # glDisable(GL_DEPTH_TEST)  # Enable depth testing
        self._draw_pyramid()

        glColor4f(1.0, 0.0, 0.0, 0.2)

        # glEnable(GL_DEPTH_TEST)
        glColor4f(0.5, 0.5, 0.5, 1)
        self.ground._draw_object(
            self.pyramid_vertices,
            [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)],
        )
        glPopMatrix()
        glDisable(GL_BLEND)
        glColor3f(1.0, 1.0, 1.0)  # Reset color to white

    def _draw_pyramid(self):
        glBegin(GL_TRIANGLES)
        for face in self.pyramid_faces:
            for vertex in face:
                glVertex3fv(self.pyramid_vertices[vertex])
        glEnd()

    @staticmethod
    def _draw_object(vertices, edges):
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertex)
        glEnd()

    def get_position(self):
        return self.position
