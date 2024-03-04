import numpy as np
import math
import Elements.pyECSS.math_utilities as util
from Elements.pyECSS.Entity import Entity
from Elements.pyGLV.GUI.Viewer import  RenderGLStateSystem,  ImGUIecssDecorator
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyECSS.Component import BasicTransform,  Camera, RenderMesh
from Elements.pyECSS.System import  TransformSystem, CameraSystem
from Elements.utils.terrain import generateTerrain
import Elements.utils.normals as norm

from Elements.pyECSS.Event import Event
from OpenGL.GL import GL_LINES

import OpenGL.GL as gl
from Elements.utils.Shortcuts import displayGUI_text
example_description = \
 "."

#Light
Lposition = util.vec(2.0, 5.5, 2.0) 
Lambientcolor = util.vec(1.0, 1.0, 1.0) 
Lambientstr = 0.2 
LviewPos = util.vec(2.5, 2.8, 5.0) 
Lcolor = util.vec(1.0,1.0,1.0)
Lintensity = 0.8
#Material
Mshininess = 0.2 
Mcolor = util.vec(0.8, 0.0, 0.8)

winWidth = 1200
winHeight = 800
scene = Scene()    

# Scenegraph with Entities, Components
rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.identity()))

eye = util.vec(1, 0.54, 1.0)
target = util.vec(0.02, 0.14, 0.217)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 1.0, 10.0)   
m = np.linalg.inv(projMat @ view)


entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(m, "orthoCam","Camera","500"))

pyramid = scene.world.createEntity(Entity(name="pyramid"))
scene.world.addEntityChild(rootEntity, pyramid)
transpyramid = scene.world.addComponent(pyramid, BasicTransform(name="transpyramid",  trs=util.identity()))
meshpyramid = scene.world.addComponent(pyramid, RenderMesh(name="meshpyramid"))

#Colored Axes
vertexAxes = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1.5, 0.0, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 1.5, 0.0, 1.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 1.5, 1.0]
],dtype=np.float32) 
colorAxes = np.array([
    [1.0, 0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0],
    [0.0, 0.0, 1.0, 1.0]
], dtype=np.float32)

vertexpyramid = np.array([

        [-0.5, 0.5, 0.5, 1.0],
        [0.5, 0.5, 0.5, 1.0],
        [0.5, 0.5, -0.5, 1.0],
        [-0.5, 0.5, -0.5, 1.0], 
        [0.0, 1.0, 0.0, 1.0]
],dtype=np.float32) 

colourpyramid = np.array([
       
        [0.5, 0.0, 1.0, 1.0], 
        [0.5, 0.0, 1.0, 1.0], 
        [0.5, 0.0, 1.0, 1.0], 
        [0.5, 0.0, 1.0, 1.0],  
        [0.5, 0.0, 1.0, 1.0], 
       
 ], dtype=np.float32)

#index arrays for above vertex Arrays
index = np.array((0,1,2), np.uint32) #simple triangle
indexAxes = np.array((0,1,2,3,4,5), np.uint32) #3 simple colored Axes as R,G,B lines


indexpyramid = np.array((
    0,1,2,
    0,2,3,
    0,1,4,
    1,2,4,
    2,3,4,
    3,0,4), np.uint32) 

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())



vertices, indices, colors, normals = norm.generateSmoothNormalsMesh(vertexpyramid , indexpyramid, colourpyramid)

meshpyramid.vertex_attributes.append(vertices)
meshpyramid.vertex_attributes.append(colors)
meshpyramid.vertex_attributes.append(normals)
meshpyramid.vertex_index.append(indices)

vArray4 = scene.world.addComponent(pyramid, VertexArray())
#shaderDec4 = scene.world.addComponent(pyramid, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))
shaderDec4 = scene.world.addComponent(pyramid, ShaderGLDecorator(Shader(vertex_source = Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG)))

vertexTerrain, indexTerrain, colorTerrain= generateTerrain(size=4,N=20)
# Add terrain
terrain = scene.world.createEntity(Entity(name="terrain"))
scene.world.addEntityChild(rootEntity, terrain)
terrain_trans = scene.world.addComponent(terrain, BasicTransform(name="terrain_trans", trs=util.translate(0.0, 0.001, 0.0)))
terrain_mesh = scene.world.addComponent(terrain, RenderMesh(name="terrain_mesh"))
terrain_mesh.vertex_attributes.append(vertexTerrain) 
terrain_mesh.vertex_attributes.append(colorTerrain)
terrain_mesh.vertex_index.append(indexTerrain)
terrain_vArray = scene.world.addComponent(terrain, VertexArray(primitive=GL_LINES))
terrain_shader = scene.world.addComponent(terrain, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))


## ADD AXES ##
axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.translate(0.0, 0.001, 0.0))) 
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))
axes_mesh.vertex_attributes.append(vertexAxes) 
axes_mesh.vertex_attributes.append(colorAxes)
axes_mesh.vertex_index.append(indexAxes)
axes_vArray = scene.world.addComponent(axes, VertexArray(primitive=gl.GL_LINES)) 


axes_shader = scene.world.addComponent(axes, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))



running = True
# MAIN RENDERING LOOP
scene.init(imgui=True, windowWidth = winWidth, windowHeight = winHeight, windowTitle = "22", openGLversion = 4, customImGUIdecorator = ImGUIecssDecorator)

scene.world.traverse_visit(initUpdate, scene.world.root)

################### EVENT MANAGER ###################

eManager = scene.world.eventManager
gWindow = scene.renderWindow
gGUI = scene.gContext

renderGLEventActuator = RenderGLStateSystem()

eManager._subscribers['OnUpdateWireframe'] = gWindow
eManager._actuators['OnUpdateWireframe'] = renderGLEventActuator
eManager._subscribers['OnUpdateCamera'] = gWindow 
eManager._actuators['OnUpdateCamera'] = renderGLEventActuator

eye = util.vec(2.5, 2.5, 2.5)
target = util.vec(0.0, 0.0, 0.0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)
projMat = util.perspective(50.0, 1.0, 1.0, 10.0) 
#projMat = util.perspective(50.0, winWidth/winHeight, 0.01, 100.0) 

gWindow._myCamera = view 

model_terrain_axes = util.translate(0.0,0.0,0.0)
model_pyramid = util.scale(0.8) @ util.translate(0.0,-0.5,0.0)


flag = 0
while running:
    running = scene.render()
    displayGUI_text(example_description)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.world.traverse_visit_pre_camera(camUpdate, orthoCam)
    scene.world.traverse_visit(camUpdate, scene.world.root)
    view =gWindow._myCamera # updates view via the imgui
    
    if model_pyramid[1][1] < 5 and flag == 0:
        model_pyramid = util.scale(math.sqrt(1/1.01), 1.01, math.sqrt(1/1.01)) @ model_pyramid
        if model_pyramid[1][1] >5.0001:
            flag = 1
    elif flag == 1:
        model_pyramid = util.scale(math.sqrt(1/0.99), 0.99, math.sqrt(1/0.99)) @ model_pyramid
        if model_pyramid[1][1] <= 1.9999:
            flag = 0

    if flag == 0 and model_pyramid[1][1] == 2:
        break
        
    mvp_pyramid = projMat @ view @ model_pyramid


    mvp_terrain = projMat @ view @ terrain_trans.trs
    mvp_axes = projMat @ view @ axes_trans.trs
    axes_shader.setUniformVariable(key='modelViewProj', value = mvp_axes, mat4=True)

    terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain, mat4=True)
    shaderDec4.setUniformVariable(key='modelViewProj', value=mvp_pyramid, mat4=True)
    shaderDec4.setUniformVariable(key='model',value=model_pyramid,mat4=True)
    shaderDec4.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
    shaderDec4.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
    shaderDec4.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
    shaderDec4.setUniformVariable(key='lightPos',value=Lposition,float3=True)
    shaderDec4.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
    shaderDec4.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
    shaderDec4.setUniformVariable(key='shininess',value=Mshininess,float1=True)
    shaderDec4.setUniformVariable(key='matColor',value=Mcolor,float3=True)

    scene.render_post()
    
scene.shutdown()
