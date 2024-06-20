import os

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
import json

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
rec_list = [Rectangle3D(-w*20 / 2, -0.501, -h*20 / 2, w*20, 1, h*20)]

cow1 = Rectangle3D(15,0,24, 1,1.8,2.5, True)
rec_list.append(cow1)

cow2 = Rectangle3D(7,0,24, 2.5,1.8,1, True)
rec_list.append(cow2)

scene = Scene(display, ground, rec_list, select)
# Add multiple cameras at different positions

m_height = 4.5

scene.add_camera(
    Camera(
        position=[12.5, m_height, 24.4],
        fov_width=26.0,
        fov_height=15.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="Hikvision",
        id=1
    )
)
scene.add_camera(
    Camera(
        position=[12.5, m_height, 24.4 - 7.5],
        fov_width=26.0,
        fov_height=15.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="Hikvision",
        id=2
    )
)
scene.add_camera(
    Camera(
        position=[12.5, m_height, 24.4 - 7.5 - 5],
        fov_width=26.0,
        fov_height=15.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="Hikvision",
        id=3
    )
)
scene.add_camera(
    Camera(
        position=[12.5, m_height, 24.4 - 7.5 - 5 - 6.5],
        fov_width=26.0,
        fov_height=15.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="Hikvision",
        id=4
    )
)

scene.add_camera(
    Camera(
        position=[12.5, m_height, 24.4 - 7.5 - 5 - 6.5 -5],
        fov_width=26.0,
        fov_height=15.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="Hikvision",
        id=5
    )
)

# Horizontal coverage at m_height : 5.509 meters
# Vertical coverage at 3.5 : 4.116 meters

# scene.add_camera(
#     Camera(
#         position=[12.5-10, 3.5, 24.4],
#         fov_width=35.0,
#         fov_height=20.0,
#         ground=ground,
#         plane=Plane(0, -m_height+0.5, 0, w, h),
#         label="QNV-C8012",
#         id=6
#     )
# )
#
# scene.add_camera(
#     Camera(
#         position=[12.5-10, 3.5, 24.4 -6],
#         fov_width=35.0,
#         fov_height=20.0,
#         ground=ground,
#         plane=Plane(0, -m_height+0.5, 0, w, h),
#         label="QNV-C8012",
#         id=6
#     )
# )
#
# scene.add_camera(
#     Camera(
#         position=[12.5-10, 3.5, 24.4 -6*2],
#         fov_width=35.0,
#         fov_height=20.0,
#         ground=ground,
#         plane=Plane(0, -m_height+0.5, 0, w, h),
#         label="QNV-C8012",
#         id=7
#     )
# )
#
# scene.add_camera(
#     Camera(
#         position=[12.5-10, 3.5, 24.4-6*3],
#         fov_width=35.0,
#         fov_height=20.0,
#         ground=ground,
#         plane=Plane(0, -m_height+0.5, 0, w, h),
#         label="QNV-C8012",
#         id=8
#     )
# )
#
# scene.add_camera(
#     Camera(
#         position=[12.5-10, 3.5, 24.4-6*4],
#         fov_width=35.0,
#         fov_height=20.0,
#         ground=ground,
#         plane=Plane(0, -m_height+0.5, 0, w, h),
#         label="QNV-C8012",
#         id=9
#     )
# )

# Horizontal coverage at 3.5 : 7.0 meters
# Vertical coverage at 3.5 : 4.592 meters

scene.add_camera(
    Camera(
        position=[12.5-10, m_height, 24.4],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="QNV-C8012",
        id=6
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, m_height, 24.4 -6],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="QNV-C8012",
        id=7
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, m_height, 24.4 -6*2],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="QNV-C8012",
        id=8
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, m_height, 24.4-6*3],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="QNV-C8012",
        id=9
    )
)

scene.add_camera(
    Camera(
        position=[12.5-10, m_height, 24.4-6*4],
        fov_width=35.0,
        fov_height=20.0,
        ground=ground,
        plane=Plane(0, -m_height+0.5, 0, w, h),
        label="QNV-C8012",
        id=10
    )
)

# Camera Model	Sensor Size	Focal Length	Height (m)	Horizontal Coverage (m)	Vertical Coverage (m)
# Hikvision DS-2CD5546G0-IZHS	1/1.8"	2.8 mm	4.5	11.709	8.748
# Hanwha Vision QNV-C8012	1/2.8"	2.4 mm	4.5	16.236	9.243


file_path = 'data.json'

# Check if the file exists
if os.path.exists(file_path):
    # Read the dictionary from the file
    with open(file_path, 'r') as f:
        try:
            DATA = json.load(f)
            print("Data loaded from the file:", DATA)
            print("load last config...")
            data_ = list(DATA.values())
            for cam, d in zip(scene.cameras, data_):
                cam.position[0] = d["x"]
                cam.position[1] = d["y"]
                cam.position[2] = d["z"]
                cam.rot = d["rotation"]
                cam.pyramid_vertices = cam.rotate_pyramid(cam.pyramid_vertices, -d["rotation"], 2)
                cam.plane.y = d["plane_y"]
        except Exception as e:
            print(e)
            os.remove(file_path)
else:
    print(f"The file {file_path} does not exist.")
    DATA = {}


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

    if keys[pygame.K_u]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, 0.5, 2)
        scene.cameras[scene.select].rot -= 0.5
    if keys[pygame.K_o]:
        scene.cameras[scene.select].pyramid_vertices = scene.cameras[scene.select].rotate_pyramid(scene.cameras[scene.select].pyramid_vertices, -0.5, 2)
        scene.cameras[scene.select].rot += 0.5

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
                #self.update()

    scene.cameras[scene.select].plane.update()
    scene.handle_camera_movement()

    pos = scene.cameras[scene.select].position
    DATA[scene.select] = {"id":scene.cameras[scene.select].id, "plane_y":scene.cameras[scene.select].plane.y, "x":pos[0], "y":pos[1], "z":pos[2], "height": pos[1], "rotation": scene.cameras[scene.select].rot}

    with open('data.json', 'w') as f:
        json.dump(DATA, f, indent=4)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    scene.draw()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
