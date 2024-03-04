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

def getNormals4513(vertices, flag):
    normals = []

    for i in range(4):
        ab = (vertices[i + 1][0] - vertices[i][0], vertices[i + 1][1] - vertices[i][1], vertices[i + 1][2] - vertices[i][2])
        ad = (vertices[i + 3][0] - vertices[i][0], vertices[i + 3][1] - vertices[i][1], vertices[i + 3][2] - vertices[i][2])
        ae = (0.0, 0.0, 0.0)
        if flag == 1:
            ae = (vertices[i - 4][0] - vertices[i][0], vertices[i - 4][1] - vertices[i][1], vertices[i - 4][2] - vertices[i][2])
        else:
            ae = (vertices[-1][0] - vertices[i][0], vertices[-1][1] - vertices[i][1], vertices[-1][2] - vertices[i][2])
        normals.append([-1 * (ab[0] + ad[0] + ae[0]), -1 * (ab[1] + ad[1] + ae[1]), -1 * (ab[2] + ad[2] + ae[2]), 1.0])

    if flag == 0:
        total_normal = [0.0, 0.0, 0.0, 1.0]
        for i in range(len(vertices) - 1):
            ab = (vertices[i][0] - vertices[-1][0], vertices[i][1] - vertices[-1][1], vertices[i][2] - vertices[-1][2])
            ac = (vertices[i + 1][0] - vertices[-1][0], vertices[i + 1][1] - vertices[-1][1], vertices[i + 1][2] - vertices[-1][2])
            if i == 3:
                ab = (vertices[i][0] - vertices[-1][0], vertices[i][1] - vertices[-1][1], vertices[i][2] - vertices[-1][2])
                ac = (vertices[0][0] - vertices[-1][0], vertices[0][1] - vertices[-1][1], vertices[0][2] - vertices[-1][2])
            cross_product = np.cross(ac, ab)
            total_normal[0] += cross_product[0]
            total_normal[1] += cross_product[1]
            total_normal[2] += cross_product[2]
        normals.append([-total_normal[0], -total_normal[1], -total_normal[2], 1.0])

    return normals