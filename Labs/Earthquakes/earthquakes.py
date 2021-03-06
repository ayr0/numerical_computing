import numpy as np
import os
import math
import matplotlib.cm as cm
import matplotlib.pylab as plt
from scipy import linalg as la

def getEpicenters(filename):
    infile = open(filename, 'r')
    data = infile.readlines()
    T = len(data)
    epicentersAngles = np.zeros((T, 2))
    epicentersEuclidean = np.zeros((T, 3))
    for i in xrange(T):
        substring1 = data[i][20:26]
        substring2 = data[i][26:33]
        epicentersAngles[i,:] = np.array([90. - float(substring1[0:5])*.001, float(substring2[0:6])*.001])
        if substring1[5] == 'S':
            epicentersAngles[i,0] = 180 - epicentersAngles[i,0]
        if substring2[6] == 'W':
            epicentersAngles[i,1] *= -1.
    return epicentersAngles

def getAllData(directory):
    filenames = os.listdir(directory)
    T = len(filenames)
    epicentersAngles = getEpicenters(directory + filenames[0])
    for i in xrange(1, T):
        temp = getEpicenters(directory + filenames[i])
        epicentersAngles = np.append(epicentersAngles, temp, 0)
    return epicentersAngles

def anglesToEuclidean(angles):
    T = angles.shape[0]
    euclidean = np.zeros((T, 3))
    for i in xrange(T):
        euclidean[i,:] = np.array([np.sin(math.radians(angles[i,0]))*np.cos(math.radians(angles[i,1])),
                                   np.sin(math.radians(angles[i,0]))*np.sin(math.radians(angles[i,1])), 
                                   np.cos(math.radians(angles[i,0]))])
    return euclidean

def euclideanToAngles(euclidean):
    T = euclidean.shape[0]
    angles = np.zeros((T, 2))
    for i in xrange(T):
        angles[i,:] = np.array([math.degrees(math.acos(euclidean[i,2])),
                                math.degrees(math.atan2(euclidean[i,1], euclidean[i,0]))])
    return angles

def anglesToLL(angles):
    T = angles.shape[0]
    LL = np.zeros((T, 2))
    LL[:,0] = angles[:,1]
    LL[:,1] = -1 * (angles[:,0] - 90)
    return LL

def angleDistance(angle1,angle2):
    return math.acos(angle1.dot(angle2)/(la.norm(angle1)*la.norm(angle2)))
