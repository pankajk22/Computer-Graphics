import contextlib, ctypes, logging, sys
from OpenGL import GL as gl
import glfw
import math 
import threading
import numpy as np
import time 
log = logging.getLogger(__name__)
class pyopenGL:
    def __init__(self,BGColor):
        self.bgcolor=BGColor
        self.vertex_data=[]
        self.color=[]
        self.linewidth=0.5

    def drawline(self,vertexdata,colordata):
        # print("adding point to buffer")
        
        self.vertex_data.append(vertexdata[0])
        self.vertex_data.append(vertexdata[1])
        self.vertex_data.append(vertexdata[2])
        self.vertex_data.append(vertexdata[3])
        self.vertex_data.append(vertexdata[4])
        self.vertex_data.append(vertexdata[5])
        # print("adding color to buffer")
        
        self.color.append(colordata[0])
        self.color.append(colordata[1])
        self.color.append(colordata[2])
        self.color.append(colordata[3])
        self.color.append(colordata[4])
        self.color.append(colordata[5])

    def LineWidth(self,width):
        self.linewidth=width
        # print("New Line width :- "+str(self.lineWidth))
    
    def LineColor(self,r,g,b):
        self.color=[r,g,b,
                    r,g,b]
        
        # print("New Line Color :-" +str(r)+str(g)+str(b))

    def BGColor(self,r,g,b):
        self.bgcolor=[r,g,b]
        # gl.glClearColor(r,g,b,0)
        # print("New BG Color :- "+str(r)+str(g)+str(b))

    def ClearScreen(self):
        self.vertex_data=[]
        self.color=[]
    
    @contextlib.contextmanager
    def create_main_window(self):
        if not glfw.init():
            sys.exit(1)
        try:
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            title = "Turtle Graphics"
            window = glfw.create_window(500, 500, title, None, None)
            if not window:
                sys.exit(2)
            glfw.make_context_current(window)

            glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
            # gl.glClearColor(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], 0)

            yield window

        finally:
            glfw.terminate()

    @contextlib.contextmanager
    def create_vertex_array_object(self):
        vertex_array_id = gl.glGenVertexArrays(1)
        try:
            gl.glBindVertexArray(vertex_array_id)
            yield
        finally:
            gl.glDeleteVertexArrays(1, [vertex_array_id])

    @contextlib.contextmanager
    def create_vertex_buffer(self):
        with self.create_vertex_array_object():
            log.debug('creating and binding the vertex buffer (VBO)')
            # self.vertex_data = np.array(self.vertex_data, dtype=np.float32)
            # print(*self.vertex_data,sep=" , ")
            # print(*self.color,sep=" , ")
            print("Total Vertices:"+str(len(self.vertex_data)))
            print("Total Colors for Vertices :"+str(len(self.color)))
            vertex_buffer = gl.glGenBuffers(1)
            try:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
                
                array_type = (gl.GLfloat * len(self.vertex_data))
                gl.glBufferData(gl.GL_ARRAY_BUFFER,
                                len(self.vertex_data) * ctypes.sizeof(ctypes.c_float),
                                array_type(*self.vertex_data),
                                gl.GL_STATIC_DRAW)

                log.debug('setting the vertex attributes')
                gl.glVertexAttribPointer(
                0,            # attribute 0.
                3,                  # components per vertex attribute
                gl.GL_FLOAT,        # type
                False,              # to be normalized?
                0,                  # stride
                None                # array buffer offset
                )
                # print("Linewidth")
                # print(str(self.linewidth))

                gl.glLineWidth((self.linewidth))
                gl.glEnableVertexAttribArray(0)  # use currently bound VAO
            
                color_buffer=gl.glGenBuffers(1)
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER,color_buffer)
                gl.glBufferData(gl.GL_ARRAY_BUFFER,len(self.color)*ctypes.sizeof(ctypes.c_float),array_type(*self.color),gl.GL_STATIC_DRAW)
                gl.glVertexAttribPointer(
                1,            # attribute 0.
                3,                  # components per vertex attribute
                gl.GL_FLOAT,        # type
                False,              # to be normalized?
                0,                  # stride
                None                # array buffer offset
                )
                gl.glEnableVertexAttribArray(1)  # use currently bound VAO
                
                yield
            finally:
                log.debug('cleaning up buffer')
                gl.glDisableVertexAttribArray(0)
                gl.glDeleteBuffers(1, [vertex_buffer])
                gl.glDisableVertexAttribArray(1)
                gl.glDeleteBuffers(1, [color_buffer])
    @contextlib.contextmanager
    def load_shaders(self):
        shaders = {
            gl.GL_VERTEX_SHADER: '''\
                #version 330 core
                layout(location = 0) in vec3 vertexPosition_modelspace;
                layout(location = 1) in vec3 color_modelspace;
                out vec3 v_color;
                void main(){
                gl_Position.xyz = vertexPosition_modelspace;
                gl_Position.w = 1.0;
                v_color = color_modelspace;
                }
                ''',
            gl.GL_FRAGMENT_SHADER: '''\
                #version 330 core
                in vec3 v_color;
                out vec3 color;
                void main(){
                    color = v_color;
                }
                '''
            }
        log.debug('creating the shader program')
        program_id = gl.glCreateProgram()
        try:
            shader_ids = []
            for shader_type, shader_src in shaders.items():
                shader_id = gl.glCreateShader(shader_type)
                gl.glShaderSource(shader_id, shader_src)

                log.debug(f'compiling the {shader_type} shader')
                gl.glCompileShader(shader_id)

                # check if compilation was successful
                result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
                info_log_len = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
                if info_log_len:
                    logmsg = gl.glGetShaderInfoLog(shader_id)
                    log.error(logmsg)
                    sys.exit(10)

                gl.glAttachShader(program_id, shader_id)
                shader_ids.append(shader_id)

            log.debug('linking shader program')
            gl.glLinkProgram(program_id)

            # check if linking was successful
            result = gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS)
            info_log_len = gl.glGetProgramiv(program_id, gl.GL_INFO_LOG_LENGTH)
            if info_log_len:
                logmsg = gl.glGetProgramInfoLog(program_id)
                log.error(logmsg)
                sys.exit(11)

            log.debug('installing shader program into rendering state')
            gl.glUseProgram(program_id)
            yield
        finally:
            log.debug('cleaning up shader program')
            for shader_id in shader_ids:
                gl.glDetachShader(program_id, shader_id)
                gl.glDeleteShader(shader_id)
            gl.glUseProgram(0)
            gl.glDeleteProgram(program_id)


    def main_loop(self,window):
            gl.glClearColor(self.bgcolor[0],self.bgcolor[1],self.bgcolor[2],1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
            i=0
            while i< len(self.vertex_data):
                # gl.glLineWidth()
                gl.glDrawArrays(gl.GL_LINES, i, 2)
                i=i+2

            glfw.swap_buffers(window)
            glfw.poll_events()

    def main(self):
        with self.create_main_window() as window:
            while (
            glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
            not glfw.window_should_close(window)
            ):
                with self.create_vertex_buffer():
                    with self.load_shaders():
                        self.main_loop(window)

    def inputoutput(self):
        x = threading.Thread(target=self.main, args=())
        x.start()


class Turtle:


    def init(self,xpos,ypos,theta):
        self.xpos=(xpos-250)/250
        self.ypos=(ypos-250)/250
        self.theta=theta
        self.pendown=False
        self.colors=[1,1,1,
                    1,1,1]
        self.linewidth=0.5
        self.bgcolor=[0,0,0]

        self.drawer= pyopenGL(self.bgcolor)
        self.drawer.inputoutput()

        # create_main_window()

        # print("Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))
    
    def Right(self, angle):
        self.theta=self.theta-angle
        self.theta=self.theta%360
        print("Angle change in right , Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))
    
    def Left(self, angle):
        self.theta=self.theta+angle
        self.theta=self.theta%360
        print("Angle change in left , Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))

    def ResetPosition(self):
        self.xpos=0
        self.ypos=0
        self.theta=0
        print("POsition resetted, Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))

    def Forward(self,distance):
        oldx=self.xpos
        oldy=self.ypos
        # print( "angle in degree = "+str(self.theta))
        angle=math.radians(self.theta)
        directionx=round(math.cos(angle),4)
        directiony=round(math.sin(angle),4)
        # print("directionx :- "+str((distance*directionx)/250))
        # print("directiony :- "+str((distance*directiony)/250))
        newx=oldx+((distance*directionx)/250)
        newy=oldy+((distance*directiony)/250)
        self.xpos=newx
        self.ypos=newy
        vertex_data=[oldx,oldy,0,
                    newx,newy,0]
        bgcolor=self.bgcolor
        colors=self.colors
        linewidth=self.linewidth

        if(self.pendown==True):
            print("sending data for printing :")
            print(*vertex_data)
            print(*colors)
            self.drawer.drawline(vertex_data,colors)

        print("Forward ,Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))

        # main(vertex_data,bgcolor,colors,linewidth)
    
    def Backward(self,distance):
        oldx=self.xpos
        oldy=self.ypos
        # print( "angle in degree = "+str(self.theta))
        angle=math.radians(self.theta)
        directionx=round(math.cos(angle),4)
        directiony=round(math.sin(angle),4)
        # print("directionx :- "+str((distance*directionx)/250))
        # print("directiony :- "+str((distance*directiony)/250))
        newx=oldx-((distance*directionx)/250)
        newy=oldy-((distance*directiony)/250)
        self.xpos=newx
        self.ypos=newy
        vertex_data=[oldx,oldy,0,
                    newx,newy,0]
        bgcolor=self.bgcolor
        colors=self.colors
        linewidth=self.linewidth
        if(self.pendown==True):
                    self.drawer.drawline(vertex_data,colors)

        print("Backward ,Turtle's Position :- X : "+ str(self.xpos) +" Y : "+ str(self.ypos)+" Theta : "+str(self.theta))


    def PenDown(self,yes_no):
        if yes_no==True:
            self.pendown=True
            print("PenDown")
        if yes_no==False:
            self.pendown=False


    def LineWidth(self,width):
        self.linewidth=width/10
        self.drawer.LineWidth(self.linewidth)
        print("New Line width :- "+str(self.linewidth))
    
    def LineColor(self,r,g,b):
        self.colors=[r,g,b,
                        r,g,b]
        # self.drawer.LineColor(r,g,b)
        
        print("New Line Color :-" +str(r)+str(g)+str(b))

    def BGColor(self,r,g,b):
        self.bgcolor=[r,g,b]
        self.drawer.BGColor(r,g,b)

        print("New BG Color :- "+str(r)+str(g)+str(b))

    def ClearScreen(self):
        self.drawer.ClearScreen()
        print("Clearing screen")


if __name__ == '__main__':
    t1=Turtle()
    t1.init(250,250,0)
    t1.BGColor(0,0,0)

    # t1.LineColor(0.5,0.5,0.1)     #Program:1
    # t1.PenDown(True)
    # t1.LineColor(1,1,1)
    # t1.PenDown(False)
    # t1.Forward(50)
    # t1.Left(90)
    # t1.PenDown(True)
    # t1.Forward(50)
    # t1.Left(90)
    # t1.Forward(100)
    # t1.Left(90)
    # t1.Forward(100)
    # t1.Left(90)
    # t1.Forward(100)
    # t1.Left(90)
    # t1.Forward(50)
    # print("In the end of program ")               #endprogram
    
    # t1.PenDown(True)        #Program: 2
    # t1.LineColor(1,0,0)
    # for i in range(15):
    #     t1.Forward(100)
    #     t1.Right(144)
    #     time.sleep(1)

    # t1.ResetPosition()
    # t1.ClearScreen()          #endprogram

    

    colors=[(1,0,0),(1,0,1),(0,0,1),(0,1,0),(1,0.5,0),(1,1,0)]        #Program :3
    t1.PenDown(True)
    for x in range(180):      
        color=(colors[x%6])            #complex program copied from GeeksforGeeks https://www.geeksforgeeks.org/turtle-programming-python/
        t1.LineColor(color[0],color[1],color[2])
        t1.LineWidth(x/40+1)
        t1.Forward(x)
        t1.Left(59)
        time.sleep(1)         #endprogram


    

