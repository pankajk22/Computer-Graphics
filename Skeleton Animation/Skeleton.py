import math
from os import X_OK
from pickle import NONE
from time import sleep
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import numpy as np

name = b'Skeleton Animation'

x = 0
BoneInfo = {}
r = 1
g = 0
b = 0
relative_angle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class Bone:
    def __init__(self, rootcordinates, length, rotation, parent, name):
        self.rotation = rotation
        self.rootcordinates = rootcordinates
        self.length = length
        self.parent = parent
        self.name = name
        self.draw()
        self.addinfo()

    def addinfo(self):
        global BoneInfo
        bone = {}
        bone['Bone_Name'] = self.name
        bone['Rotation'] = self.rotation
        bone['Starting_point'] = self.rootcordinates
        bone['End_point'] = self.getEndPoint()
        bone['Length'] = self.length
        BoneInfo[self.name] = bone

    def getEndPoint(self):
        if self.parent == None:
            theta = (self.getRotation() % 360)*math.pi/180
            return (
                round(self.rootcordinates[0]+self.length*math.cos(theta), 4),
                round(self.rootcordinates[1]+self.length*math.sin(theta), 4),
                0
            )
        else:
            startPoint = self.parent.getEndPoint()
            theta = (self.getRotation() % 360)*math.pi/180
            return (
                round(startPoint[0]+self.length*math.cos(theta), 4),
                round(startPoint[1]+self.length*math.sin(theta), 4),
                0
            )

    def getRotation(self):
        if self.parent == None:
            return self.rotation
        else:
            return self.parent.getRotation()+self.rotation

    def draw(self):

        if len(self.rootcordinates) > 0:
            # self.rootcordinates=self.getEndPoint()
            #print("Inside draw function")
            center_x = self.rootcordinates[0]
            center_y = self.rootcordinates[1]
            center_z = self.rootcordinates[2]
            #print("Starting Point:(")
            # print(*self.rootcordinates)
            # print(")")
            glTranslatef(center_x, center_y, center_z)
            glRotatef(-90, 1, 0, 0)

            glRotate(self.getRotation()-90, 0, -1, 0)
            # print(str(self.getRotation()))
            glutSolidCone(0.3, self.length, 35, 34)
            glRotate(-self.getRotation()+90, 0, -1, 0)

            glRotatef(90, 1, 0, 0)
            glTranslatef(-1*center_x, -1*center_y, -1*center_z)
            # #print("Starting point: ("+str(center_x)+","+str(center_y)+","+str(center_z)+")")
            endpoint = self.getEndPoint()
            #print("End point: ("+str(endpoint[0])+","+str(endpoint[1])+","+str(endpoint[2])+")")

        else:
            self.rootcordinates = self.parent.getEndPoint()
            center_x = self.rootcordinates[0]
            center_y = self.rootcordinates[1]
            center_z = self.rootcordinates[2]

            # print(*self.rootcordinates)

            glTranslatef(center_x, center_y, center_z)
            glRotatef(-90, 1, 0, 0)

            glRotate(self.getRotation()-90, 0, -1, 0)
            # print(str(self.getRotation()))
            glutSolidCone(0.3, self.length, 35, 34)
            glRotate(-self.getRotation()+90, 0, -1, 0)

            glRotatef(90, 1, 0, 0)
            glTranslatef(-1*center_x, -1*center_y, -1*center_z)
            # #print("Starting point: ("+str(center_x)+","+str(center_y)+","+str(center_z)+")")
            endpoint = self.getEndPoint()
            #print("End point: ("+str(endpoint[0])+","+str(endpoint[1])+","+str(endpoint[2])+")")

        point1 = Sphere(self.getEndPoint())
        point1.draw()


class Sphere():
    def __init__(self, center, radius=0.2):
        self.center = center
        self.radius = radius

    def draw(self):
        ##print("draw sphere")
        # print(str(round(self.center[0],2))+","+str(round(self.center[1],2)))
        glTranslatef(round(self.center[0], 2), round(self.center[1], 2), 0)
        glutSolidSphere(self.radius, 32, 32)
        glTranslatef(-1*round(self.center[0],
                              2), -1*round(self.center[1], 2), 0)


rot_x = 0
rot_y = 3
rot_z = 10
angle = 0


def rotationy(_theta, vertices):
    #print("cordinates recieved:")
    # print(*vertices)
    theta = (_theta % 360)*math.pi/180
    x = vertices[0]
    z = vertices[2]
    vertices[0] = round(x*math.cos(theta) + z*math.sin(theta), 5)
    vertices[2] = round(z*math.cos(theta) - x*math.sin(theta), 5)

    return vertices


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(300, 400)
    glutCreateWindow(name)

    glClearColor(0., 0., 1., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [-20., 2., -2., 1.]
    lightZeroColor = [1.8, 1.0, 0.8, 1.0]  # green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(create)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40., 1., 1., 40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 20,
              0, 0, 0,
              0, 1, 0)
    glPushMatrix()
    glutMainLoop()
    return


angledata = []


def getangles():
    global BoneInfo
    global angledata
    row = []
    row.append(BoneInfo['rootbone']['Rotation'])
    row.append(BoneInfo['waistbone']['Rotation'])
    row.append(BoneInfo['chestbone']['Rotation'])
    row.append(BoneInfo['neckbone']['Rotation'])
    row.append(BoneInfo['rightforearmbone']['Rotation'])
    row.append(BoneInfo['leftforearmbone']['Rotation'])
    row.append(BoneInfo['rightfemur']['Rotation'])
    row.append(BoneInfo['leftfemur']['Rotation'])
    row.append(BoneInfo['rightarm']['Rotation'])
    row.append(BoneInfo['leftarm']['Rotation'])
    row.append(BoneInfo['rightleg']['Rotation'])
    row.append(BoneInfo['leftleg']['Rotation'])
    angledata.append(row)
    print(*row)


# def rot():                  #rotation via rotating the model
#     global angle
#     angle=angle-1
#     glutPostRedisplay()
#     sleep(0.02)


# def rot():            #rotation model via lookat vector
#     global rot_x
#     global rot_y
#     global rot_z
#     global angle
#     vertices=[rot_x,rot_y,rot_z]
#     vertices=rotationy(1,vertices)
#     angle=(angle-1)%360
#     rot_x=vertices[0]
#     rot_y=vertices[1]
#     rot_z=vertices[2]
#     #print("angle-"+str(angle)+"camera cordinates :-"+ str(vertices[0])+", "+str(vertices[1])+", "+str(vertices[2]))
#     glutPostRedisplay()
#     sleep(0.02)


animdata = []
# animdata_raw=[]


def hello(array):
    global relative_angle
    animdata_raw = array
    global animdata
    animdata.clear()
    # animdata_raw=[[90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
    #         [90, 0, 0, -14, -136, 134, -123, 135, -29, 31, -39, 7],
    #         [90, 0, 0, -12, -124, 140, -113, 135, -29, 31, -25, 7],
    #         [90, 0, 0, -14, -134, 148, -127, 155, -27, 31, -25, -41],
    #         [90, 0, 0, -14, -150, 156, -127, 165, -11, 1,-23, -35,],
    #         [90, 0, 0, -14, -162, 170, -161, 177, -11, 1, -11, -13],
    #         [90, 0, 0, -14, -192, 192, -199, 203, -11, 3, -5, -21],
    #         [90, 0, 0, -14, -204, 208, -199, 221, 17, -21, -1, -39],
    #         [90, 0, 0, -14, -204, 214, -181, 215, 17, -21, -17, -35],
    #         [90, 0, 0, -14, -170, 172, -171, 203, -11, -21, -25, -11],
    #         [90, 0, 0, -14, -148, 158, -149, 181, -1, -5, -25, -11,],
    #         [90, 0, 0, -14, -148, 158, -139, 163, -15, -9, -43, 1]]

    # animdata_raw=[
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15],
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, -155, -15, 15],
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15]
    #             ]

    # animdata_raw=[
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -3, 3, -15, 15],
    #                 [90, 0, 0, 0, -90, 90, -135, 135, -3, 3, -15, 15],
    #                 [90, 0, 0, 0, -76, 88, -135, 135, -25, 3, -15, 15],
    #                 [90, 0, 0, 0, -82, 82, -135, 135, -17, 13, -15, 15],
    #                 [90, 0, 0, 0, -90, 76, -135, 135, 1, 35, -15, 15],
    #                [ 90, 0, 0, 0, -74, 90, -135, 135, -45, 3, -13, 15],

    # ]

    # animdata_raw=[
    #                 [90, 0, 0, 0, -180, 184, -167, 181, -15, 15, -11, -5],
    #                [ 90, 0, 0, 0, -160, 158, -153, 165, 9, 21, -23, -17],
    #                 [90, 0, 0, 0, -180, 184, -167, 181, -15, 15, -11, -5],
    #                 [90, 0, 0, 0, -158, 150, -195, 205, 9, 21, -23, -17],
    #                 [90, 0, 0, 0, -180, 184, -167, 181, -15, 15, -11, -5]
    # ]
    # animdata_raw=[
    #                 [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
    #                 [90, -4, -10, -56, -122, 154, -175, 171, 133, 15, -15, -1],
    #                 [90, -6, -10, -56, -122, 154, -179, 207, 133, 15, 1, -23],
    #                 [90, -6, -10, -56, -122, 154, -147, 181, 131, 15, -29, 1]
    # ]

    for i in range(len(animdata_raw)-1):
        frame1 = animdata_raw[i]
        frame2 = animdata_raw[i+1]
        for subframe in range(1, 21):
            frame = [0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for j in range(len(animdata_raw[i])):

                frame[j] = round(frame1[j]+round(subframe/21, 5)
                                 * (frame2[j]-frame1[j]), 5)
                # frame[j]=round(frame[j]-animdata_raw[0][j],5)

            animdata.append(frame)

    # print(*animdata)
    # print(str(len(animdata)))


tx = 0
ty = 0
tz = 0
index = 0
repeat = 0
dec_factor = 0


def animation():
    global dec_factor
    global relative_angle
    global animdata
    global tx
    global index
    global repeat

    if(tx < -11):
        tx = 11
    elif(tx > 11):
        tx = -11
    else:
        tx = tx+dec_factor

    # print(tx)
    relative_angle = animdata[index]
    # index=(index+1)%len(animdata)
    if(index < len(animdata)-1):
        index = index+1
    else:
        # print("yes")
        index = repeat

    # print(index)

    # print(*relative_angle)
    glutPostRedisplay()
    sleep(0.05)


def createbonestructure():
    # global relative_angle
    # rootbone=Bone((0+tx,-2+ty,0+tz),0,90+relative_angle[0],None,"rootbone")
    # waistbone=Bone((),2,0+relative_angle[1],rootbone,"waistbone")
    # chestbone=Bone((),4,0+relative_angle[2],waistbone,"chestbone")
    # neckbone=Bone((),2,0+relative_angle[3],chestbone,"neckbone")
    # rightforearmbone=Bone((),3,-120+relative_angle[4],chestbone,"rightforearmbone")
    # leftforearmbone=Bone((),3,120+relative_angle[5],chestbone,"leftforearmbone")
    # rightfemur=Bone((),2.5,-135+relative_angle[6],rootbone,"rightfemur")
    # leftfemur=Bone((),2.5,135+relative_angle[7],rootbone,"leftfemur")
    # rightarm=Bone((),2.,-15+relative_angle[8],rightforearmbone,"rightarm")
    # leftarm=Bone((),2.,15+relative_angle[9],leftforearmbone,"leftarm")
    # rightleg=Bone((),2.5,-15+relative_angle[10],rightfemur,"rightleg")
    # leftleg=Bone((),2.5,15+relative_angle[11],leftfemur,"leftleg")

    rootbone = Bone((0+tx, -2+ty, 0+tz), 0,
                    relative_angle[0], None, "rootbone")
    waistbone = Bone((), 2, relative_angle[1], rootbone, "waistbone")
    chestbone = Bone((), 4, relative_angle[2], waistbone, "chestbone")
    neckbone = Bone((), 2, relative_angle[3], chestbone, "neckbone")
    rightforearmbone = Bone(
        (), 3, relative_angle[4], chestbone, "rightforearmbone")
    leftforearmbone = Bone(
        (), 3, relative_angle[5], chestbone, "leftforearmbone")
    rightfemur = Bone((), 2.5, relative_angle[6], rootbone, "rightfemur")
    leftfemur = Bone((), 2.5, relative_angle[7], rootbone, "leftfemur")
    rightarm = Bone((), 2., relative_angle[8], rightforearmbone, "rightarm")
    leftarm = Bone((), 2., relative_angle[9], leftforearmbone, "leftarm")
    rightleg = Bone((), 2.5, relative_angle[10], rightfemur, "rightleg")
    leftleg = Bone((), 2.5, relative_angle[11], leftfemur, "leftleg")
    # leftleg.rotate(relative_angle)


bonenumber = 12


def keyboard(key, x, y):
    global tx
    global dec_factor
    global repeat
    global animdata_raw
    global index
    if(key == b'w'):
        print("Simple-walk selected")
        matrix = [
            [90, -2, 0, -22, -176, 178, -183, 189, 17, -9, -7, -7],
            [90, -2, 0, -22, -160, 158, -183, 207, -5, 17, -27, -23],
            [90, -2, 0, -22, -186, 180, -163, 187, -5, 17, -27, -23],
            [90, -2, 0, -22, -200, 202, -143, 179, -5, 17, -41, -37],
            [90, -2, 0, -22, -176, 178, -183, 189, 17, -9, -7, -7]
        ]
        dec_factor = 0.08
        repeat = 0
        index = 0
        hello(matrix)

    elif(key == b'm'):
        print("Moon-walk selected")
        matrix = [
            [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
            [90, -4, -10, -56, -122, 154, -175, 171, 133, 15, -15, -1],
            [90, -6, -10, -56, -122, 154, -179, 207, 133, 15, 1, -23],
            [90, -6, -10, -56, -122, 154, -147, 181, 131, 15, -29, 1]
        ]

        dec_factor = -0.1
        index = 0
        repeat = 40
        hello(matrix)
    elif(key == b'h'):
        print("Moving Hi selected")
        # matrix=[
        #             [90, 2, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
        #             [90, -46, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
        #             [90, -92, 2, -24, -82, 268, -191, 149, -15, 15, -15, 15],
        #             [90, -92, 2, -24, -82, 268, -191, 149, 69, 87, -15, 15],
        #             [90, -92, 2, -24, -82, 268, -191, 149, 69, 87, -79, -61],
        #             [90, -96, 12, -8, -82, 268, -191, 149, 69, 87, -79, -61],

        #         ]
        matrix = [
            [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
            [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15],
            [90, 0, 0, 0, -120, 120, -135, 135, -15, -155, -15, 15],
            [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15]
        ]
        dec_factor = 0.05
        repeat = 20
        index = 0
        # tx=-2.5
        hello(matrix)

    else:
        print("Wrong key pressed")


# def keyboard(key,x,y):
#     global angledata
#     # print(key)
#     global bonenumber
#     if(key==b'q'):
#         bonenumber=0
#     elif(key==b'a'):
#         bonenumber=1
#     elif(key==b'z'):
#         bonenumber=2
#     elif(key==b'w'):
#         bonenumber=3
#     elif(key==b's'):
#         bonenumber=4
#     elif(key==b'x'):
#         bonenumber=5
#     elif(key==b'e'):
#         bonenumber=6
#     elif(key==b'd'):
#         bonenumber=7
#     elif(key==b'c'):
#         bonenumber=8
#     elif(key==b'r'):
#         bonenumber=9
#     elif(key==b'f'):
#         bonenumber=10
#     elif(key==b'v'):
#         bonenumber=11
#     elif(key==b'\r'):
#         getangles()
#     elif(key==b'\x13'):
#         np.savetxt("angledata.csv",
#            angledata,
#            delimiter =", ",
#            fmt ='% s')
#     else:
#         print("different key pressed")
def spkeyboard(key, x, y):
    # print(key)
    global bonenumber
    if(key == 100):
        relative_angle[bonenumber] = relative_angle[bonenumber]+2
    if(key == 102):
        relative_angle[bonenumber] = relative_angle[bonenumber]-2


def create():
    global x
    global dec_factor
    global repeat
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [r, g, b, 1.]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

    # b1=Bone((0,-1,0),2,90,None)
    # b2=Bone((),4,120,b1)
    glTranslatef(x, 0, 0)

    createbonestructure()

    glutKeyboardFunc(keyboard)
    glutSpecialFunc(spkeyboard)
    glutIdleFunc(animation)
    glPopMatrix()
    glutSwapBuffers()

    return


if __name__ == '__main__':

    matrix = [
        [90, 0, 0, 0, -120, 120, -135, 135, -15, 15, -15, 15],
        [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15],
        [90, 0, 0, 0, -120, 120, -135, 135, -15, -155, -15, 15],
        [90, 0, 0, 0, -120, 120, -135, 135, -15, -79, -15, 15]
    ]

    dec_factor = 0
    repeat = 20
    index = 0
    hello(matrix)
    print("Welcome to skeleton animation!!")
    print("Press w for simple walking")
    print("Press m for moon-walk")
    print("Press h for Moving Hi-Animation")
    print("Default: Static Hi")

    main()
