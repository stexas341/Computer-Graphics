import numpy as np
import Elements.pyECSS.math_utilities as util

 
def get_rotation_matrix(axe,angle):
    if axe == 'x':
            return util.rotate((1,0,0),angle)
    elif axe == 'y':
            return util.rotate((0,1,0),angle)
    elif axe == 'z':
            return util.rotate((0,0,1),angle)

def modelpoints4513(L, t, A, theta, s):
    translation_matrix = util.translate(t[0],t[1],t[2])
    scale_matrix = util.scale(s[0],s[1],s[2])
    i=0
    transformed_points = []
    L_array = np.array(L)
    homoL = np.c_[L_array, np.ones(L_array.shape[0])]
    for axe in A:
        rotation_matrix = get_rotation_matrix(axe,theta[i])
        i+=1
   
        for point in homoL:
            #scaled_point = np.dot(scale_matrix, point)
            #rotated_point = np.dot(rotation_matrix, scaled_point)
            #translated_point = np.dot(translation_matrix, rotated_point)
            #transformed_points.append(translated_point[:3])

            translated_point = np.dot(translation_matrix, point)
            rotated_point = np.dot(rotation_matrix, translated_point)
            scaled_point = np.dot(scale_matrix, rotated_point)
            transformed_points.append(scaled_point[:3])      
    return transformed_points

#eisodos
L = [np.array([3, 1, 2]), np.array([1, 2, 5])]
t = np.array([2, 2, 4])
A = ['y','x']  
theta = [90,45] 
s = np.array([3, 3, 3])

transformed_points = modelpoints4513(L, t, A, theta, s)
print(transformed_points)  
 
 

