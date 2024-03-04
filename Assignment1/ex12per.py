import random
from statistics import mode
from turtle import width
# import unittesτ

import math
import numpy as np

import Elements.pyECSS.math_utilities as util
from Elements.pyECSS.Entity import Entity
from Elements.pyECSS.Component import RenderMesh
from Elements.pyGLV.GL.Scene import Scene
from Elements.pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from Elements.pyGLV.GL.VertexArray import VertexArray
from Elements.utils.helper_function import displayGUI_text

from Elements.pyECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from Elements.pyECSS.ECSSManager import ECSSManager


from OpenGL.GL import GL_LINES

import OpenGL.GL as gl


def generatepolygon(n):
    if(n > 2):
            
        scene = Scene()    

       
        # Scenegraph with Entities, Components
        rootEntity = scene.world.createEntity(Entity(name="RooT"))

        entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
        scene.world.addEntityChild(rootEntity, entityCam1)

        node4 = scene.world.createEntity(Entity(name="node4"))
        scene.world.addEntityChild(rootEntity, node4)
        mesh4 = scene.world.addComponent(node4, RenderMesh(name="mesh4"))


        axes = scene.world.createEntity(Entity(name="axes"))
        scene.world.addEntityChild(rootEntity, axes)
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

        #index arrays for above vertex Arrays
        index = np.array((0,1,2), np.uint32) #simple triangle 
        indexAxes = np.array((0,1,2,3,4,5), np.uint32) #3 simple colored Axes as R,G,B lines
        indexPolygon = []

        # Systems
        transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
        camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
        renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
        initUpdate = scene.world.createSystem(InitGLShaderSystem())

        model = util.translate(0.0,0.0,0.0)
        eye = util.vec(0, 1.0, 2.5)
        target = util.vec(0.0, 0.0, 0.0)
        up = util.vec(0.0, 1.0, 0.0)
        view = util.lookat(eye, target, up)

        # projMat = util.ortho(-10.0, 10.0, -10.0, 10.0, -1.0, 10.0)      
        projMat = util.perspective(90.0, 1.33, 0.1, 100)
        
        
        pointsArray = []
        i=0
        theta = 360.0/n;
        theta = math.radians(theta)
        sum = 0;
        sum = math.radians(sum)
        
        for i in range (n) :
            sum = sum + theta 
            x = round(math.cos(sum), 2)
            y = round(math.sin(sum), 2)
            pointsArray.append([x, y, 0.0, 1.0])
            #print(pointsArray)
            i = i + 1

        p = 1
        while(p < n) :
            indexPolygon.append(0)
            indexPolygon.append(p)
            p = p + 1
            indexPolygon.append(p)
            if (p == n) : 
                indexPolygon.append(0)
                indexPolygon.append(p)
                p = 1
                indexPolygon.append(p)
                #print(indexPolygon)
                break
        #print(pointsArray)
        j=0
        colorpointsArray = []
        for j in range(n) :
            x = round(random.random(), 0)
            if (x == 1.0) :
                y = 0.0
                z = round(random.random(), 0)
                colorpointsArray.append([x, y, z, 1])
                j = j + 1
                continue
            
            y = round(random.random(), 0)
            if (y == 1.0) :
                x = round(random.random(), 0)
                z = 0.0
                colorpointsArray.append([x, y, z, 1])
                j = j + 1
                continue
            
            z = round(random.random(), 0)
            if (z == 1.0) :
                x = 0.0
                y = round(random.random(), 0)
                colorpointsArray.append([x, y, z, 1])
                j = j + 1
                continue

        mesh4.vertex_attributes.append(pointsArray) 
        mesh4.vertex_attributes.append(colorpointsArray)
        mesh4.vertex_index.append(indexPolygon)
        vArray4 = scene.world.addComponent(node4, VertexArray())
        
        shaderDec4 = scene.world.addComponent(node4, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

        # Generate terrain
        from pyGLV.GL.terrain import generateTerrain
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

        showaxes = True
        ## ADD AXES TO THIS MESH - START##
        if showaxes :
            axes = scene.world.createEntity(Entity(name="axes"))
            scene.world.addEntityChild(rootEntity, axes)
            axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
            axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))
            axes_mesh.vertex_attributes.append(vertexAxes) 
            axes_mesh.vertex_attributes.append(colorAxes)
            axes_mesh.vertex_index.append(indexAxes)
            axes_vArray = scene.world.addComponent(axes, VertexArray(primitive=GL_LINES)) # note the primitive change
            axes_shader = scene.world.addComponent(axes, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))

        running = True
        # MAIN RENDERING LOOP
        scene.init(imgui=True, windowWidth = 1024, windowHeight = 768, windowTitle = "pyglGA test_renderTriangle_shader")

        # pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
        # needs an active GL context

        scene.world.traverse_visit(initUpdate, scene.world.root)

        eManager = scene.world.eventManager
        gWindow = scene.renderWindow
        gGUI = scene.gContext
        renderGLEventActuator = RenderGLStateSystem()
        eManager._subscribers['OnUpdateCamera'] = gWindow 
        eManager._actuators['OnUpdateCamera'] = renderGLEventActuator
        eManager._subscribers['OnUpdateWireframe'] = gWindow
        eManager._actuators['OnUpdateWireframe'] = renderGLEventActuator


        gWindow._myCamera = view
        mvpMat =  projMat @ view @ model 

        while running:
            running = scene.render(running)
            scene.world.traverse_visit(renderUpdate, scene.world.root)
            view = gWindow._myCamera 
            mvpMat =  projMat @ view @ model
            shaderDec4.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)
            axes_shader.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)
            scene.render_post()
            
        scene.shutdown()
        
    else : 
        print("n must be greater than 2")  
    return

num = input("Give me a number greater than 2 : ")
generatepolygon(int(num))