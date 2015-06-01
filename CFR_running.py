'''
Created on 2015. 6. 1.

@author: cimple
'''

import numpy as np

class CFRRun:
    def __init__(self):
        self.basisType = 'GAUSSIAN'
        
    def dist(self, a, b) :
        d1 = 0.0
        d2 = 0.0
        dim = a.shape[0]
        for i in range(dim) :
            d1 = a[i] - b[i]
            d2 += (d1*d1)
        return d2 
    
    def basisFunc(self, i, x2) :
        if self.basisType == 'HARDY' :
            return (x2 + self.minDist[i])**0.5
        elif self.basisType == 'GAUSSIAN' :
            return np.exp(-x2*0.1*0.1)
        elif self.basisType == 'LINEAR' :
            return abs((x2)**0.5)            
        else :
            print "Wrong basis type!!"
            return;
    
    def RBF_interpolate(self, srcInput, trainData, numTargetCV):
        rSrcInput = np.zeros(trainData.rbfTrain.rbfn.numInput)
        for i in range(len(rSrcInput)) :
            rSrcInput[i] = self.basisFunc(i, self.dist(srcInput, trainData.rbfTrain.rbfn.inputMat[i]))
        resultMat = np.dot(rSrcInput, trainData.weightMat)
        result = np.zeros(numTargetCV)        
        for i in range(numTargetCV) :            
            result[i] = resultMat[i]        
        return result
    
    def CFR_running(self, srcAnimData, tgtCharData, trainData):
        numTargetCV = tgtCharData.numCV
        resultAnimDataList = []
        for i in range(len(srcAnimData.animDataList)):
            out = self.RBF_interpolate(srcAnimData.animDataList[i], trainData, numTargetCV)
            resultAnimDataList.append(out)
        return resultAnimDataList
        