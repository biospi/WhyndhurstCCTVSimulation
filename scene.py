import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# from ground import Ground
# from main import Rectangle3D


class Scene:
    def __init__(self, display, ground, rectangle, select):
        self.display = display
        self.ground = ground
        self.rectangle = rectangle
        self.cameras = []
        self.camera_angle = 90
        self.camera_height = 0
        self.camera_x = -20
        self.camera_speed = 0.1
        self.zoom_speed = 30
        self.select = select
        # self.font = pygame.font.SysFont('Arial', 24)
        # Load the font
        self.font = pygame.font.SysFont("Arial", 34)

    def add_camera(self, camera):
        self.cameras.append(camera)

    def handle_camera_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.camera_height -= 0.1
        if keys[pygame.K_DOWN]:
            self.camera_height += 0.1
        if keys[pygame.K_LEFT]:
            self.camera_angle += 1
        if keys[pygame.K_RIGHT]:
            self.camera_angle -= 1
        if keys[pygame.K_w]:
            self.zoom_speed += 0.1
        if keys[pygame.K_s]:
            self.zoom_speed -= 0.1
        if keys[pygame.K_d]:
            self.camera_x -= 0.1
        if keys[pygame.K_a]:
            self.camera_x += 0.1

        # Apply transformations
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 500.0)
        glTranslatef(0.0, -10, -60)  # Lowered the initial view closer to the ground
        glTranslatef(self.camera_x, self.camera_height, self.zoom_speed)
        glRotatef(self.camera_angle, 0, 1, 0)

    def render_text(self, text, i):
        # Render text to a surface
        back_color = (0, 0, 0)
        if self.select == i:
            back_color = (255, 0, 0)
        text_surface = self.font.render(text, True, (255, 255, 255), back_color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        # Create a texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            text_data,
        )
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id, width, height

    def draw_text(self, texture_id, width, height, x, y, z):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glPushMatrix()
        glTranslatef(x, y + 1, z)

        # Billboard the text
        modelview = glGetFloatv(GL_MODELVIEW_MATRIX)
        billboard_matrix = np.identity(4, dtype=np.float32)
        billboard_matrix[:3, :3] = modelview[
            :3, :3
        ].T  # Transpose the rotation part of the modelview matrix
        glMultMatrixf(billboard_matrix)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(-width / 200.0, -height / 200.0, 0)
        glTexCoord2f(1, 0)
        glVertex3f(width / 200.0, -height / 200.0, 0)
        glTexCoord2f(1, 1)
        glVertex3f(width / 200.0, height / 200.0, 0)
        glTexCoord2f(0, 1)
        glVertex3f(-width / 200.0, height / 200.0, 0)
        glEnd()
        glPopMatrix()

        glDisable(GL_TEXTURE_2D)

    def draw(self):
        self.ground.draw()
        for r in self.rectangle:
            r.draw()
        # glDisable(GL_DEPTH_TEST)
        for i, camera in enumerate(self.cameras):
            if i == self.select:
                camera.draw_highlight()
            else:
                camera.draw()
            camera_position = camera.get_position()
            texture_id, width, height = self.render_text(f"{camera_position[1]:0.2f}|{camera.label}|{camera.id}", i)
            self.draw_text(
                texture_id,
                width,
                height,
                camera_position[0],
                camera_position[1] + 1,
                camera_position[2],
            )
            #camera.draw_intersection()
        # glEnable(GL_DEPTH_TEST)
        # self.draw_text('0', 0, 0, 5.0)
