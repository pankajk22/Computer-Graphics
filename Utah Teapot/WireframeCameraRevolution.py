import math
from time import sleep
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = b'OpenGL Python Teapot'

rot_x=0
rot_y=3
rot_z=10
angle=0
def rotationy(_theta,vertices):
    print("cordinates recieved:")
    print(*vertices)
    theta=(_theta%360)*math.pi/180
    x=vertices[0]
    z=vertices[2]
    vertices[0]=round(x*math.cos(theta) + z*math.sin(theta),5)
    vertices[2]=round(z*math.cos(theta) - x*math.sin(theta),5)
        
    return vertices
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600,600)
    glutCreateWindow(name)

    glClearColor(0.,0.,0,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [-20.,2.,-2.,1.]
    lightZeroColor = [1.0,1.0,1.0,1.0] #green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glutMainLoop()
    return





# def rot():                  #rotation via rotating the model
#     global angle
#     angle=angle-1
#     glutPostRedisplay()
#     sleep(0.02)


def rot():            #rotation model via lookat vector
    global rot_x
    global rot_y
    global rot_z
    global angle
    vertices=[rot_x,rot_y,rot_z]
    vertices=rotationy(1,vertices)
    angle=(angle-1)%360
    rot_x=vertices[0]
    rot_y=vertices[1]
    rot_z=vertices[2]
    print("angle-"+str(angle)+"camera cordinates :-"+ str(vertices[0])+", "+str(vertices[1])+", "+str(vertices[2]))
    glutPostRedisplay()
    sleep(0.02)
    


def display():

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1,1.,1.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    # glRotatef(angle,0,1,0)
    # glRotatef(10,1,0,0);
    gluLookAt(rot_x,rot_y,rot_z,
              0,0,0,
              0,1,0)
    glutWireTeapot(1.5)
    glutIdleFunc(rot)
    glPopMatrix()
    glutSwapBuffers()
    
    return

if __name__ == '__main__': main()