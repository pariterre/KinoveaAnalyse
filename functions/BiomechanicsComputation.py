import numpy as np
from numpy import linalg


def compute_com_i(data, winter_table):
    com_i = {}
    for (k, m) in winter_table.items():
        prox = data[m[0]]
        dist = data[m[1]]
        com_i[k] = np.reshape(prox + m[3] * (dist - prox), (prox.shape[0], 1, prox.shape[1]))
    return com_i


def compute_com(data, winter_table):
    com_i = compute_com_i(data, winter_table)
    com = np.ndarray((2, 1, data[list(data.keys())[0]].shape[1]))
    com[:, :] = 0
    for (k, m) in com_i.items():
        com += winter_table[k][5] * m * winter_table[k][2]
    return com


def derivative(data, time):
    new_data = np.ndarray(data.shape)
    new_data[:] = np.nan
    new_data[:, :, 1:-1] = (data[:, :, 2:] - data[:, :, 0:-2]) / (time[2:] - time[0:-2])
    return new_data


def compute_grf(com_ddot, masse):
    return com_ddot * masse


def compute_angles(data, segments):
    # dot(P1-O, P2-O) / (norm(P1) * norm(P2))

    angles = {}
    for (n, s) in segments.items():
        v1 = data[s[0]] - data[s[2]]
        v2 = data[s[1]] - data[s[2]]

        dot = np.einsum('ij,ij->j', v1, v2)
        denom = linalg.norm(v1, axis=0) * linalg.norm(v2, axis=0)
        angles[n] = np.arccos(dot / denom)

    return angles
