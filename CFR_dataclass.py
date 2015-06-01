'''
Created on 2015. 6. 1.

@author: cimple
'''
import numpy as np

class CFR_charData:
    def __init__(self, charName, CVlist):
        self.charName = charName        
        self.CVlist = CVlist
        self.numCV = len(self.CVlist)
        self.ROE = None
        self.numROE = 0      
    
    def addROE(self, cvValList):
        if len(self.CVlist) != len(cvValList): 
            print 'ERROR : length of the input CV values is different from the lentg of CV list'
            return
        if self.ROE == None:
            self.ROE = np.array(cvValList)
        else:
            self.ROE = np.vstack((self.ROE, cvValList))
        self.numROE = int(self.ROE.shape[0])
          
    
class CFR_animData:
    def __init__(self, charName, CVlist, animDataList, frameList):
        self.charName = charName        
        self.CVlist = CVlist
        self.numCV = len(self.CVlist)
        self.animDataList = np.array(animDataList)
        self.numFrames = len(frameList)
        self.frameList = frameList

class CFR_trainData:
    def __init__(self, srcCharName, tgtCharName, rbfTrain):
        self.srcCharName = srcCharName
        self.tgtCharName = tgtCharName
        self.rbfTrain = rbfTrain
        self.weightMat = rbfTrain.rbfn.weightMat