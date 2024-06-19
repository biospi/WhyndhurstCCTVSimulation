import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Plane vertices (in XY plane)
plane_vertices = [
    (-1, 0.2, -1),
    (1, 0.2, -1),
    (1, 0.2, 1),
    (-1, 0.2, 1)
]

# Pyramid vertices
pyramid_vertices = [
    (0, 2, 0),      # top vertex
    (0.5, -1, 0.5),  # front-right
    (-0.5, -1, 0.5), # front-left
    (-0.5, -1, -0.5),# back-left
    (0.5, -1, -0.5)  # back-right
]

# Pyramid faces
pyramid_faces = [
    (0, 1, 2),
    (0, 2, 3),
    (0, 3, 4),
    (0, 4, 1),
    (1, 2, 3, 4)
]


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

    glTranslatef(0.0, 0.0, -5)

    rotate_x, rotate_y, rotate_z = 0, 0, 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rotate_y = -1
                elif event.key == pygame.K_RIGHT:
                    rotate_y = 1
                elif event.key == pygame.K_UP:
                    rotate_x = -1
                elif event.key == pygame.K_DOWN:
                    rotate_x = 1
                elif event.key == pygame.K_q:
                    rotate_z = -1
                elif event.key == pygame.K_e:
                    rotate_z = 1
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    rotate_y = 0
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    rotate_x = 0
                elif event.key in (pygame.K_q, pygame.K_e):
                    rotate_z = 0

        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        glRotatef(rotate_z, 0, 0, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw the plane (opaque)
        glColor3f(0.0, 0.5, 1.0)
        glBegin(GL_QUADS)
        for vertex in plane_vertices:
            glVertex3fv(vertex)
        glEnd()

        # Draw the pyramid (transparent)
        glColor4f(0.0, 1.0, 0.0, 0.5)  # Green color with 50% opacity
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_TRIANGLES)
        for face in pyramid_faces[:-1]:  # Draw the triangular faces
            for vertex in face:
                glVertex3fv(pyramid_vertices[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for vertex in pyramid_faces[-1]:  # Draw the base face
            glVertex3fv(pyramid_vertices[vertex])
        glEnd()

        glDisable(GL_BLEND)

        glDisable(GL_DEPTH_TEST)
        # Draw the slicing section
        glColor3f(1.0, 0.0, 0.0)  # Red color for the intersection section
        glBegin(GL_LINES)
        for face in pyramid_faces:
            for i in range(len(face)):
                v1 = pyramid_vertices[face[i]]
                v2 = pyramid_vertices[face[(i + 1) % len(face)]]
                if v1[1] > plane_vertices[0][1] and v2[1] < plane_vertices[0][1] or v1[1] < plane_vertices[0][1] and v2[1] > plane_vertices[0][1]:
                    # Interpolate to find the intersection point
                    t = (plane_vertices[0][1] - v1[1]) / (v2[1] - v1[1])
                    intersection_point = (
                        v1[0] + t * (v2[0] - v1[0]),
                        plane_vertices[0][1],
                        v1[2] + t * (v2[2] - v1[2])
                    )
                    glVertex3fv(intersection_point)
        glEnd()
        glEnable(GL_DEPTH_TEST)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
