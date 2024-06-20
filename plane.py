from OpenGL.GL import *
import math


class Plane:
    def __init__(self, x, y, z, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.half_width = width / 2
        self.half_height = height / 2

        self.plane_vertices = [
            (x - self.half_width, y, z - self.half_height),
            (x + self.half_width, y, z - self.half_height),
            (x + self.half_width, y, z + self.half_height),
            (x - self.half_width, y, z + self.half_height),
        ]

    def update(self):
        self.plane_vertices = [
            (self.x - self.half_width, self.y, self.z - self.half_height),
            (self.x + self.half_width, self.y, self.z - self.half_height),
            (self.x + self.half_width, self.y, self.z + self.half_height),
            (self.x - self.half_width, self.y, self.z + self.half_height),
        ]

    def draw(self):
        # Draw the plane (opaque)
        # glEnable(GL_BLEND)

        glColor3f(0.0, 0.5, 1.0)
        glBegin(GL_QUADS)
        for vertex in self.plane_vertices:
            glVertex3fv(vertex)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        # glDisable(GL_BLEND)
