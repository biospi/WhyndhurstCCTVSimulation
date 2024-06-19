import pygame
from OpenGL.GL import *


# Load the ground texture
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture

class Ground:
    def __init__(self, width, length, thickness):
        self.width = width
        self.texture = load_texture('ground_texture.png')
        self.length = length
        half_width = width / 2
        half_length = length / 2
        half_thickness = thickness / 2
        self.y_position = half_thickness  # Y-coordinate of the ground
        self.vertices = [
            (-half_width, -half_thickness, -half_length),
            (half_width, -half_thickness, -half_length),
            (half_width, half_thickness, -half_length),
            (-half_width, half_thickness, -half_length),
            (-half_width, -half_thickness, half_length),
            (half_width, -half_thickness, half_length),
            (half_width, half_thickness, half_length),
            (-half_width, half_thickness, half_length)
        ]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
            (0, 4), (1, 5), (2, 6), (3, 7)  # Vertical edges
        ]

        # Define texture coordinates for the top surface
        self.tex_coords_top = [
            (0, 1),  # Top-left corner of the texture
            (1, 1),  # Top-right corner of the texture
            (1, 0),  # Bottom-right corner of the texture
            (0, 0)   # Bottom-left corner of the texture
        ]

    def draw(self):
        # glColor3f(0.5, 0.5, 0.5)  # Gray color
        # glPushMatrix()
        # self._draw_object(self.vertices, self.edges)
        # glPopMatrix()

        glPushMatrix()
        self._draw_object(self.vertices, self.edges)
        glPopMatrix()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPushMatrix()
        glBegin(GL_QUADS)
        top_face_vertices = [self.vertices[3], self.vertices[2], self.vertices[6], self.vertices[7]]
        for i, vertex in enumerate(top_face_vertices):  # Consider only the vertices of the top face
            glTexCoord2fv(self.tex_coords_top[i])  # Use texture coordinates for the top face
            glVertex3fv(vertex)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)


    @staticmethod
    def _draw_object(vertices, edges):
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

