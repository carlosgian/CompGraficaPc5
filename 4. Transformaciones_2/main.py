import pygame, os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Cubo import *
from LeerMalla import *
from Camara import *
from numba import jit, cuda

os.environ['SDL_VIDEO_CENTERED'] = '1'
# x= 850
# y = 200
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x, y)

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')
#cube = Cubo(GL_LINE_LOOP, position=pygame.Vector3(2, 0, 0), rotation=Rotation(0, pygame.Vector3(0, 1, 0)), scale=pygame.Vector3(0.5, 0.5, 0.5))
#cube2 = Cubo(GL_LINE_LOOP, position=pygame.Vector3(2, 0, 0), rotation=Rotation(0, pygame.Vector3(0, 1, 0)), scale=pygame.Vector3(2, 2, 2))
mesh = LeerMalla("text.obj", GL_LINE_LOOP, rotation=Rotation(0, pygame.Vector3(0, 1, 0)), scale=pygame.Vector3(0.05, 0.05, 0.05))
camera = Camara()

#@jit(target_backend='cuda') 
def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)

    #glRotatef(1,3,1,1)

    glLoadIdentity()
    gluPerspective(0, (screen_width / screen_height), 3.0, 2000.0)
    #glRotatef(0,0,0,0)
    

#@jit(target_backend='cuda') 
def camera_init():
    # modelview
    
    glMatrixMode(GL_MODELVIEW)

    #glRotatef(1,3,1,1)

    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    #glRotatef(1,3,1,1)
    camera.update(screen.get_width(), screen.get_height())

#@jit(target_backend='cuda') 
def draw_world_axes():
    glLineWidth(4)
    glBegin(GL_LINES)
    glColor(1, 0, 0)
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)
    glColor(0, 1, 0)
    glVertex3d(0, -1000, 0)
    glVertex3d(0, 1000, 0)
    glColor(0, 0, 1)
    glVertex3d(0, 0,-1000)
    glVertex3d(0, 0, 1000)
    glEnd()


    #sphere = gluNewQuadric()

    """ # x pos sphere
    glColor(1, 0, 0)
    glPushMatrix()
    glTranslated(1, 0, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    # y pos sphere
    glColor(0, 1, 0)
    glPushMatrix()
    glTranslated(0, 1, 0)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix()

    # z pos sphere
    glColor(0, 0, 1)
    glPushMatrix()
    glTranslated(0, 0, 1)
    gluSphere(sphere, 0.05, 10, 10)
    glPopMatrix() """

    glLineWidth(1)
    glColor(1, 1, 1)

#@jit(target_backend='cuda') 
def display():
    #glRotatef(1,3,1,1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #camera_init()
    #draw_world_axes()
    mesh.draw()

    # cube.draw()


done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

#rotation_angle = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            if event.key == K_SPACE:
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
    #glRotatef(1,3,1,1)

    #rotation_angle += 30
    glRotatef(10,0,1,0)
    display()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()