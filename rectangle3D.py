from OpenGL.GL import *
import math

class Rectangle3D:
    def __init__(self, x, y, z, width, height, depth, cow=False):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.cow = cow

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)
        if self.cow:
            glColor3f(0, 0, 1)
        # Front face
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x + self.width, self.y, self.z)
        glVertex3f(self.x + self.width, self.y + self.height, self.z)
        glVertex3f(self.x, self.y + self.height, self.z)

        # Back face
        glVertex3f(self.x, self.y, self.z + self.depth)
        glVertex3f(self.x + self.width, self.y, self.z + self.depth)
        glVertex3f(self.x + self.width, self.y + self.height, self.z + self.depth)
        glVertex3f(self.x, self.y + self.height, self.z + self.depth)

        # Top face
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x + self.width, self.y, self.z)
        glVertex3f(self.x + self.width, self.y, self.z + self.depth)
        glVertex3f(self.x, self.y, self.z + self.depth)

        # Bottom face
        glVertex3f(self.x, self.y + self.height, self.z)
        glVertex3f(self.x + self.width, self.y + self.height, self.z)
        glVertex3f(self.x + self.width, self.y + self.height, self.z + self.depth)
        glVertex3f(self.x, self.y + self.height, self.z + self.depth)

        # Left face
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x, self.y, self.z + self.depth)
        glVertex3f(self.x, self.y + self.height, self.z + self.depth)
        glVertex3f(self.x, self.y + self.height, self.z)

        # Right face
        glVertex3f(self.x + self.width, self.y, self.z)
        glVertex3f(self.x + self.width, self.y, self.z + self.depth)
        glVertex3f(self.x + self.width, self.y + self.height, self.z + self.depth)
        glVertex3f(self.x + self.width, self.y + self.height, self.z)

        glEnd()
        glColor3f(1, 1, 1)

    def set_color(self, r, g, b):
        glColor3f(r, g, b)

    def rotate_y(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        cos_angle = math.cos(angle_radians)
        sin_angle = math.sin(angle_radians)

        # Center of the rectangle
        center_x = self.x + self.width / 2
        center_z = self.z + self.depth / 2

        # Rotate each vertex around the Y-axis
        vertices = [
            (self.x, self.y, self.z),
            (self.x + self.width, self.y, self.z),
            (self.x + self.width, self.y + self.height, self.z),
            (self.x, self.y + self.height, self.z),

            (self.x, self.y, self.z + self.depth),
            (self.x + self.width, self.y, self.z + self.depth),
            (self.x + self.width, self.y + self.height, self.z + self.depth),
            (self.x, self.y + self.height, self.z + self.depth)
        ]

        rotated_vertices = []
        for vertex in vertices:
            x, y, z = vertex
            # Translate vertex to origin
            x -= center_x
            z -= center_z
            # Rotate around Y axis
            x_rotated = x * cos_angle - z * sin_angle
            z_rotated = x * sin_angle + z * cos_angle
            # Translate vertex back
            x_rotated += center_x
            z_rotated += center_z
            rotated_vertices.append((x_rotated, y, z_rotated))

        # Update the rectangle with rotated vertices
        self.x = rotated_vertices[0][0]
        self.y = rotated_vertices[0][1]
        self.z = rotated_vertices[0][2]
        self.width = rotated_vertices[1][0] - rotated_vertices[0][0]
        self.height = rotated_vertices[2][1] - rotated_vertices[0][1]
        self.depth = rotated_vertices[4][2] - rotated_vertices[0][2]