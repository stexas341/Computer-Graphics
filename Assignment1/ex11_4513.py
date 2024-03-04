import numpy as np

def modelpoints4513(L, t, A, theta, s):
    translation_matrix = np.array([
        [1, 0, 0, t[0]],
        [0, 1, 0, t[1]],
        [0, 0, 1, t[2]],
        [0, 0, 0, 1]
    ])

    scale_matrix = np.array([
        [s[0], 0, 0, 0],
        [0, s[1], 0, 0],
        [0, 0, s[2], 0],
        [0, 0, 0, 1]
    ])
    radian_theta = np.radians(theta)
    if A == 'x':
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, np.cos(radian_theta), -np.sin(radian_theta), 0],
            [0, np.sin(radian_theta), np.cos(radian_theta), 0],
            [0, 0, 0, 1]
        ])
    elif A == 'y':
        rotation_matrix = np.array([
            [np.cos(radian_theta), 0, np.sin(radian_theta), 0],
            [0, 1, 0, 0],
            [-np.sin(radian_theta), 0, np.cos(radian_theta), 0],
            [0, 0, 0, 1]
        ])
    elif A == 'z':
        rotation_matrix = np.array([
            [np.cos(radian_theta), -np.sin(radian_theta), 0, 0],
            [np.sin(radian_theta), np.cos(radian_theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])


    transformed_points = []
    L_array = np.array(L)
    homoL = np.c_[L_array, np.ones(L_array.shape[0])]
    for point in homoL:
        scaled_point = np.dot(scale_matrix, point)
        rotated_point = np.dot(rotation_matrix, scaled_point)
        translated_point = np.dot(translation_matrix, rotated_point)
        transformed_points.append(translated_point[:3])


        #translated_point = np.dot(translation_matrix, point)
        #rotated_point = np.dot(rotation_matrix, translated_point)
        #scaled_point = np.dot(scale_matrix, rotated_point)
        #transformed_points.append(scaled_point[:3])
    return transformed_points

#eisodos
L = [np.array([3, 1, 2]), np.array([1, 2, 5])]
t = np.array([2, 2, 4])
A = 'y'  # Π.χ., για άξονα y
theta = 90  # Γωνία περιστροφής σε μοίρες
s = np.array([3, 3, 3])  # Συντελεστές κλιμάκωσης

transformed_points = modelpoints4513(L, t, A, theta, s)
print(transformed_points)