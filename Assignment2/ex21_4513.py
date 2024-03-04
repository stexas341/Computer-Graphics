import numpy as np

import Elements.pyECSS.math_utilities as util
from Elements.pyECSS.Entity import Entity
from Elements.pyGLV.GUI.Viewer import  RenderGLStateSystem,  ImGUIecssDecorator
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyECSS.Component import BasicTransform,  Camera, RenderMesh
from Elements.pyECSS.System import  TransformSystem, CameraSystem
from Elements.utils.terrain import generateTerrain
from Elements.utils.normals import Convert

from Elements.pyECSS.System import  TransformSystem, CameraSystem
from Elements.pyECSS.Entity import Entity
from Elements.pyECSS.Component import BasicTransform,  RenderMesh
from Elements.pyECSS.Event import Event
from OpenGL.GL import GL_LINES

import OpenGL.GL as gl

winWidth = 1200
winHeight = 800

Cubes = []

class Object:
    
    def __init__(self, node, trans, mesh):
        self.node = node
        self.trans = trans
        self.mesh = mesh
    
    def setshader(self, value):
        self.shader = value
        
def addEntity(name_node, name_trans, name_mesh):
    cube = scene.world.createEntity(Entity(name=name_node))
    scene.world.addEntityChild(rootEntity, cube)
    transcube = scene.world.addComponent(cube, BasicTransform(name=name_trans, trs=util.identity()))
    mesh4 = scene.world.addComponent(cube, RenderMesh(name=name_mesh))
    
    obj = Object(cube, transcube, mesh4)
    return obj

scene = Scene()    

# Scenegraph with Entities, Components
rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.identity()))


eye = util.vec(2.5, 2.5, 2.5)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 1.0, 10.0)   
m = np.linalg.inv(projMat @ view)
# projMat = util.ortho(-10.0, 10.0, -10.0, 10.0, -1.0, 10.0)  
# projMat = util.perspective(90.0, 1.33, 0.1, 100)  
# projMat = util.perspective(50.0, winWidth/winHeight, 0.01, 100.0)   


entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(m, "orthoCam","Camera","500"))

for i in range(1,82):
    Cubes.append(addEntity("cube_{}".format(i), "transcube_{}".format(i), "mesh4_{}".format(i)))


axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))


#Colored Axes
vertexAxes = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0]
],dtype=np.float32) 
colorAxes = np.array([
    [1.0, 0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0],
    [0.0, 0.0, 1.0, 1.0]
], dtype=np.float32)

#Simple Cube
vertexCube1 = np.array([
    [-0.65, -0.55, 0.55, 1.0], 
    [-0.65, 0.55, 0.55, 1.0],  
    [0.65, 0.55, 0.55, 1.0],
    [0.65, -0.55, 0.55, 1.0],  
    [-0.65, -0.55, -0.55, 1.0],
    [-0.65, 0.55, -0.55, 1.0], 
    [0.65, 0.55, -0.55, 1.0],  
    [0.65, -0.55, -0.55, 1.0],  
    
    [-0.55, -0.66, 0.55, 1.0], 
    [-0.55, 0.66, 0.55, 1.0],  
    [0.55, 0.66, 0.55, 1.0],   
    [0.55, -0.66, 0.55, 1.0],  
    [-0.55, -0.66, -0.55, 1.0],
    [-0.55, 0.66, -0.55, 1.0], 
    [0.55, 0.66, -0.55, 1.0],  
    [0.55, -0.66, -0.55, 1.0],  
    
    [-0.55, -0.55, 0.66, 1.0], 
    [-0.55, 0.55, 0.66, 1.0],  
    [0.55, 0.55, 0.66, 1.0],   
    [0.55, -0.55, 0.66, 1.0],  
    [-0.55, -0.55, -0.66, 1.0],
    [-0.55, 0.55, -0.66, 1.0], 
    [0.55, 0.55, -0.66, 1.0],  
    [0.55, -0.55, -0.66, 1.0] 
],dtype=np.float32) 

colorCube1 = np.array([
    [1.0, 0.0, 0.0, 1.0], 
    [1.0, 0.0, 0.0, 1.0], 
    [1.0, 0.0, 0.0, 1.0], 
    [1.0, 0.0, 0.0, 1.0], 
    [1.0, 1.0, 0.0, 1.0], 
    [1.0, 1.0, 1.0, 1.0], 
    [0.0, 0.0, 1.0, 1.0], 
    [0.0, 0.0, 1.0, 1.0], 
    
    [1.0, 1.0, 0.0, 1.0], 
    [1.0, 1.0, 1.0, 1.0], 
    [0.0, 0.0, 1.0, 1.0], 
    [0.0, 0.0, 1.0, 1.0], 
    [1.0, 0.60, 0.0, 1.0], 
    [1.0, 0.60, 0.0, 1.0], 
    [1.0, 1.0, 1.0, 1.0], 
    [1.0, 1.0, 0.0, 1.0], 
    
    [0.0, 1.0, 0.0, 1.0], 
    [0.0, 1.0, 0.0, 1.0], 
    [1.0, 1.0, 1.0, 1.0], 
    [1.0, 1.0, 0.0, 1.0], 
    [0.0, 1.0, 0.0, 1.0], 
    [0.0, 1.0, 0.0, 1.0], 
    [1.0, 0.60, 0.0, 1.0], 
    [1.0, 0.60, 0.0, 1.0], 
], dtype=np.float32)

#index arrays for above vertex Arrays
index = np.array((0,1,2), np.uint32) 
indexAxes = np.array((0,1,2,3,4,5), np.uint32) 
indexCube = np.array((1,0,3, 1,3,2, 
                  10,11,7, 10,7,6,      
                  19,8,4, 19,4,15,      
                  14,5,9, 14,9,18,      
                  12,13,22, 12,22,23,      
                  21,20,16, 21,16,17), np.uint32) #rhombus out of two triangles

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

for minicube in Cubes:
    minicube.mesh.vertex_attributes.append(vertexCube1)
    minicube.mesh.vertex_attributes.append(colorCube1)
    minicube.mesh.vertex_index.append(indexCube)
    vArray4 = scene.world.addComponent(minicube.node, VertexArray())
    minicube.setshader(scene.world.addComponent(minicube.node, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG))))

# Generate terrain
vertexTerrain, indexTerrain, colorTerrain= generateTerrain(size=4,N=20)
# Add terrain
terrain = scene.world.createEntity(Entity(name="terrain"))
scene.world.addEntityChild(rootEntity, terrain)
terrain_trans = scene.world.addComponent(terrain, BasicTransform(name="terrain_trans", trs=util.identity()))
terrain_mesh = scene.world.addComponent(terrain, RenderMesh(name="terrain_mesh"))
terrain_mesh.vertex_attributes.append(vertexTerrain) 
terrain_mesh.vertex_attributes.append(colorTerrain)
terrain_mesh.vertex_index.append(indexTerrain)
terrain_vArray = scene.world.addComponent(terrain, VertexArray(primitive=GL_LINES))
terrain_shader = scene.world.addComponent(terrain, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))


## ADD AXES ##
axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))
axes_mesh.vertex_attributes.append(vertexAxes) 
axes_mesh.vertex_attributes.append(colorAxes)
axes_mesh.vertex_index.append(indexAxes)
axes_vArray = scene.world.addComponent(axes, VertexArray(primitive=GL_LINES)) 
axes_shader = scene.world.addComponent(axes, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

running = True
# MAIN RENDERING LOOP
scene.init(imgui=True, windowWidth = winWidth, windowHeight = winHeight, windowTitle = "21", openGLversion = 4, customImGUIdecorator = ImGUIecssDecorator)


scene.world.traverse_visit(initUpdate, scene.world.root)


eManager = scene.world.eventManager
gWindow = scene.renderWindow
gGUI = scene.gContext

renderGLEventActuator = RenderGLStateSystem()

eManager._subscribers['OnUpdateWireframe'] = gWindow
eManager._actuators['OnUpdateWireframe'] = renderGLEventActuator
eManager._subscribers['OnUpdateCamera'] = gWindow 
eManager._actuators['OnUpdateCamera'] = renderGLEventActuator


eye = util.vec(4.2, 2.0, 4.2)
target = util.vec(0.0, 1.2, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)

projMat = util.perspective(50.0, 1.0, 1.0, 10.0)

gWindow._myCamera = view 

class points:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
ArrayOfPoints = [
    points(-1.0,1.0,0.0),
    points(0.0,1.0,0.0),
    points(1.0,1.0,0.0),
    points(-1.0,0.0,0.0),
    points(0.0,0.0,0.0),
    points(1.0,0.0,0.0),
    points(-1.0,-1.0,0.0),
    points(0.0,-1.0,0.0),
    points(1.0,-1.0,0.0),
    points(-1.0,1.0,1.0),
    points(0.0,1.0,1.0),
    points(1.0,1.0,1.0),
    points(-1.0,0.0,1.0),
    points(0.0,0.0,1.0),
    points(1.0,0.0,1.0),
    points(-1.0,-1.0,1.0),
    points(0.0,-1.0,1.0),
    points(1.0,-1.0,1.0),
    points(-1.0,1.0,-1.0),
    points(0.0,1.0,-1.0),
    points(1.0,1.0,-1.0),
    points(-1.0,0.0,-1.0),
    points(0.0,0.0,-1.0),
    points(1.0,0.0,-1.0),
    points(-1.0,-1.0,-1.0),
    points(0.0,-1.0,-1.0),
    points(1.0,-1.0,-1.0)
]

cubeap = []


for i in range(len(ArrayOfPoints)):
    cubeap.append(util.scale(0.3) @ util.translate(ArrayOfPoints[i].x, ArrayOfPoints[i].y, ArrayOfPoints[i].z) @ util.translate(0.0, 0.0, 5.0))

for i in range(len(ArrayOfPoints)):
    cubeap.append(util.scale(0.3) @ util.translate(ArrayOfPoints[i].x, ArrayOfPoints[i].y, ArrayOfPoints[i].z) @ util.translate(5.0, 0.0, 0.0))

for i in range(len(ArrayOfPoints)):
    cubeap.append(util.scale(0.3) @ util.translate(ArrayOfPoints[i].x, ArrayOfPoints[i].y, ArrayOfPoints[i].z) @ util.translate(0.0, 5.0, 0.0))

Mvp_Cubes = [0] * 81
model_terrain_axes = util.translate(0.0,0.0,0.0)
while running:
    running = scene.render()
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    view =  gWindow._myCamera 
    
    for i in range(0, 9):
        cubeap[i] = util.rotate((0, 0, 1), 0.5) @ cubeap[i]

    for i in range(9, 18):
        cubeap[i] = util.rotate((0, 0, 1), -0.5) @ cubeap[i]

    for i in range(18, 27):
        cubeap[i] = util.rotate((0, 0, 1), 1.5) @ cubeap[i]

    i = 27
    while i < 52:
        cubeap[i] = util.rotate((1, 0, 0), 1) @ cubeap[i]
        i += 3

    i = 28
    while i < 53:
        cubeap[i] = util.rotate((1, 0, 0), -1) @ cubeap[i]
        i += 3

    i = 29
    while i < 54:
        cubeap[i] = util.rotate((1, 0, 0), 2) @ cubeap[i]
        i += 3

    i = 54
    j = 0
    while i < 75:
        cubeap[i] = util.rotate((0, 1, 0), 2) @ cubeap[i]
        i += 1
        j += 1
        if j == 3:
            i += 6
            j = 0

    i = 57
    j = 0
    while i < 78:
        cubeap[i] = util.rotate((0, 1, 0), -2) @ cubeap[i]
        i += 1
        j += 1
        if j == 3:
            i += 6
            j = 0

    i = 60
    j = 0
    while i < 81:
        cubeap[i] = util.rotate((0, 1, 0), 1) @ cubeap[i]
        i += 1
        j += 1
        if j == 3:
            i += 6
            j = 0
    for i in range(len(cubeap)):
        Mvp_Cubes[i]= projMat @ view @ cubeap[i]

    mvp_terrain_axes = projMat @ view @ model_terrain_axes
    axes_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain_axes, mat4=True)
    terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain_axes, mat4=True)
    for i in range(len(Mvp_Cubes)):
        Cubes[i].shader.setUniformVariable(key='modelViewProj', value=Mvp_Cubes[i], mat4=True)
    scene.render_post()
    
scene.shutdown()