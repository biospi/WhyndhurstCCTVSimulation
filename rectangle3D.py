from OpenGL.GL import *


class Rectangle3D:
    def __init__(self, x, y, z, width, height, depth):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)
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
