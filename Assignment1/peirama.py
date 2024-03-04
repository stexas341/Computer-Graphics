import numpy as np

def modelpoints4513(L, t, A, theta, s):
    # Ορίζουμε τις πίνακες μετασχηματισμού για την κλιμάκωση
    scale_matrix = np.eye(3)
    scale_matrix[A] = s

    # Περιστροφή γύρω από τον άξονα A και γωνία θ
    radian_theta = np.radians(theta)
    rotation_matrix = np.eye(3)
    if A == 0:
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(radian_theta), -np.sin(radian_theta)],
            [0, np.sin(radian_theta), np.cos(radian_theta)]
        ])
    elif A == 1:
        rotation_matrix = np.array([
            [np.cos(radian_theta), 0, np.sin(radian_theta)],
            [0, 1, 0],
            [-np.sin(radian_theta), 0, np.cos(radian_theta)]
        ])
    elif A == 2:
        rotation_matrix = np.array([
            [np.cos(radian_theta), -np.sin(radian_theta), 0],
            [np.sin(radian_theta), np.cos(radian_theta), 0],
            [0, 0, 1]
        ])

    # Εφαρμόζουμε τους μετασχηματισμούς σε κάθε σημείο
    transformed_points = []
    for point in L:
        scaled_point = np.dot(scale_matrix, point)
        rotated_point = np.dot(rotation_matrix, scaled_point)
        translated_point = rotated_point + t
        transformed_points.append(translated_point)

    return transformed_points

# Παράδειγμα χρήσης
L = [np.array([3, 1, 2]), np.array([1, 2, 5])]
t = np.array([2, 2, 4])
A = 1  # Π.χ., για άξονα x
theta = 90  # Γωνία περιστροφής σε μοίρες
s = np.array([3, 3, 3])  # Συντελεστές κλιμάκωσης

transformed_points = modelpoints4513(L, t, A, theta, s)
print(transformed_points)