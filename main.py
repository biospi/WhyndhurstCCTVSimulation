import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu

from camera import Camera
from ground import Ground
from plane import Plane
from rectangle3D import Rectangle3D
from scene import Scene

# Initialize Pygame and set up the window
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
display = (1600, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up the perspective and the initial view
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
# glTranslatef(0.0, -5.0, -150)  # Lowered the initial view closer to the ground

# Initialize OpenGL
glEnable(GL_DEPTH_TEST)
glEnable(GL_MULTISAMPLE)
glMatrixMode(GL_PROJECTION)
glMatrixMode(GL_MODELVIEW)

select = 0
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing


# Main loop
init()
w = 33.95
h = 55.65
ground = Ground(w, h, 1)
#plane = Plane(0, -3., 0, w, h)
scene = Scene(display, ground, Rectangle3D(-w*20 / 2, -0.501, -h*20 / 2, w*20, 1, h*20), select)
# Add multiple cameras at different positions
scene.add_camera(
    Camera(
        position=[12.5, 3.5, 24.4],
        fov_width=30.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="Hikvision",
        id=1
    )
)
scene.add_camera(
    Camera(
        position=[12.5, 3.5, 24.4 - 7.5],
        fov_width=30.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="Hikvision",
        id=2
    )
)
scene.add_camera(
    Camera(
        position=[12.5, 3.5, 24.4 - 7.5 - 5],
        fov_width=30.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="Hikvision",
        id=3
    )
)
scene.add_camera(
    Camera(
        position=[12.5, 3.5, 24.4 - 7.5 - 5 - 6.5],
        fov_width=30.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="Hikvision",
        id=4
    )
)

scene.add_camera(
    Camera(
        position=[12.5, 3.5, 24.4 - 7.5 - 5 - 6.5 -5],
        fov_width=30.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="Hikvision",
        id=5
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, 3.5, 24.4],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="New",
        id=6
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, 3.5, 24.4 -6],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="New",
        id=6
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, 3.5, 24.4 -6*2],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="New",
        id=7
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, 3.5, 24.4-6*3],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="New",
        id=8
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, 3.5, 24.4-6*4],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -3., 0, w, h),
        label="New",
        id=9
    )
)

running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        scene.select = 0
    if keys[pygame.K_2]:
        scene.select = 1
    if keys[pygame.K_3]:
        scene.select = 2
    if keys[pygame.K_4]:
        scene.select = 3
    if keys[pygame.K_5]:
        scene.select = 4
    if keys[pygame.K_6]:
        scene.select = 5
    if keys[pygame.K_7]:
        scene.select = 6
    if keys[pygame.K_8]:
        scene.select = 7
    if keys[pygame.K_9]:
        scene.select = 8

    if keys[pygame.K_0]:  # Check if key '1' is pressed
        if not pressed_last_frame:  # Check if the key was not pressed last frame
            select += 1  # Increment select
            if select >= len(scene.cameras):  # Wrap around if select exceeds the number of cameras
                select = 0
            print(select)
            scene.select = select

        pressed_last_frame = True  # Set the flag to indicate key was pressed this frame
    else:
        pressed_last_frame = False  # Reset the flag if the key is not pressed


    if keys[pygame.K_i]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, 0.1, 1)
    if keys[pygame.K_k]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, -0.1, 1)
    if keys[pygame.K_j]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, 0.1, 0)
    if keys[pygame.K_l]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, -0.1, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button pressed
                dx, dy = event.rel
                scene.cameras[scene.select].position[2] += (
                    dx * 0.05
                )  # Adjust camera position based on mouse movement
                scene.cameras[scene.select].position[0] -= dy * 0.05
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel scrolled up
                # Move camera up
                scene.cameras[scene.select].position[1] += 0.1
                scene.cameras[scene.select].plane.y -= 0.1
            elif event.button == 5:  # Mouse wheel scrolled down
                # Move camera down
                scene.cameras[scene.select].position[1] -= 0.1
                scene.cameras[scene.select].plane.y += 0.1
    scene.cameras[scene.select].plane.update()

    scene.handle_camera_movement()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    scene.draw()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
