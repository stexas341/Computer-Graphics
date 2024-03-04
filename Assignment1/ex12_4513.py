# pylint: disable=import-error
import math
import numpy as np
import random
import Elements.pyECSS.math_utilities as util
from Elements.pyECSS.Entity import Entity
from Elements.pyECSS.Component import RenderMesh
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.utils.helper_function import displayGUI_text
example_description = \
"." 

winWidth = 1024
winHeight = 768

scene = Scene()

rootEntity = scene.world.createEntity(Entity(name="RooT"))

entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)

node4 = scene.world.createEntity(Entity(name="node4"))
scene.world.addEntityChild(rootEntity, node4)
mesh4 = scene.world.addComponent(node4, RenderMesh(name="mesh4"))

axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))

def generatepolygon4513(n):
    if n < 3:
        print("Ο n πρέπει να είναι τουλάχιστον 3")
        return
    pointsArray = []
    angle = 360.0 / n
    angle = math.radians(angle)
    sum = math.radians(0)

    for i in range(n):
        sum += angle
        x = math.cos(sum)
        y = math.sin(sum)
        pointsArray.append([x, y, 0.0, 1.0])
        i=i+1

    
    indexPolygon = []
    for p in range(1, n):
        indexPolygon.extend([p, p + 1,0])

    # Close the polygon
    indexPolygon.extend([0, n - 1, 0])


    colorpointsArray = []
    for _ in range(n):  # Use "_" instead of "j" as it's not used
        x = random.random()
        y = random.random()
        z = random.random()

        # Check if x, y, or z is equal to 1.0
        if x == 1.0:
            y = 0.0
            z = 0.0
        elif y == 1.0:
            x = 0.0
            z = 0.0
        elif z == 1.0:
            x = 0.0
            y = 0.0

        colorpointsArray.append([x, y, z, 1])

    mesh4.vertex_attributes.append(pointsArray) 
    mesh4.vertex_attributes.append(colorpointsArray)
    mesh4.vertex_index.append(indexPolygon)
    vArray4 = scene.world.addComponent(node4, VertexArray())


model = util.translate(0.0,0.0,0.5)@util.scale(3)
eye = util.vec(1.0, 1.0, 1.0)
target = util.vec(0,0.0,0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)

# projMat = util.perspective(120.0, 1.33, 0.1, 100.0)
projMat = util.ortho(-10.0, 10.0, -10.0, 10.0, -10, 10.0)

mvpMat =  projMat @ view @ model

shaderDec4 = scene.world.addComponent(node4, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))
shaderDec4.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)
    
# Systems
initUpdate = scene.world.createSystem(InitGLShaderSystem())
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())

generatepolygon4513(3)


scene.world.print()


running = True
# MAIN RENDERING LOOP
scene.init(imgui=True, windowWidth = winWidth, windowHeight = winHeight, windowTitle = "A Cube Scene via ECSS")

# pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
# needs an active GL context
scene.world.traverse_visit(initUpdate, scene.world.root)

while running:
    running = scene.render()
    displayGUI_text(example_description)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.render_post()
    
scene.shutdown()






