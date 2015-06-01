'''
Created on 2015. 6. 1.

@author: cimple
'''
import maya.cmds as mc
import sys
sys.path.append('C:/Users/cimple/Documents/GitHub/CFR')

import CFR_dataclass
reload(CFR_dataclass)
from CFR_dataclass import *

import CFR_training
reload(CFR_training)
from CFR_training import *

import CFR_running
reload(CFR_running)
from CFR_running import *

class CFR_mayaInterface:
    def __init__(self):
        None
    
    def addROEfile(self, charName, CVlist, ROE, fileName):
        import os.path        
        if (os.path.isfile(fileName)==True):
            f = open(fileName)
            import pickle
            charData = pickle.load(f)
            if charData.charName != charName :
                print 'Error : Adding to different character ROE file! charData.charName : ', charData.charName, ' Input character name: ', charName 
                return
            if charData.CVlist != CVlist :
                print 'Error : Adding to different CV list! charData.CV list and input CVlist is different.'
                return
            charData.addROE(ROE)
            f.close()
            f = open(fileName, 'w')
            pickle.dump(charData, f)
            f.close()
        else:
            charData = CFR_charData(charName, CVlist)
            charData.addROE(ROE)
            f = open(fileName, 'w')
            import pickle
            pickle.dump(charData, f)
            f.close()        
    
    def createAnimFile(self, charName, CVlist, animDataList, frameList, fileName):
        srcAnimData = CFR_animData(charName, CVlist, animDataList, frameList)        
        #writing file
        f = open(fileName, 'w')
        import pickle
        pickle.dump(srcAnimData, f)
        f.close()
    
    def createAnim(self, charName, CVlist, frameList, fileName):        
        animDataList = []
        for frame in frameList:
            tmpValList = []
            for cv in CVlist :
                tmpValList.append(mc.getAttr(cv, t=frame))
            animDataList.append(tmpValList)
        self.createAnimFile(charName, CVlist, animDataList, frameList, fileName)
    
    def importAnimFromFile(self, charName, fileName):
        f = open(fileName)
        import pickle
        animData = pickle.load(f)
        
        if animData.charName != charName :
            print 'Error : Character name is different! Data character name : ', animData.charName, ' Input character name : ', charName
            return
        
        for dataIdx, CVdata in enumerate(animData.animDataList):
            mc.currentTime(animData.frameList[dataIdx])
            for cvIdx, CV in enumerate(animData.CVlist) :
                mc.setAttr(CV, CVdata[cvIdx])
                mc.setKeyframe(CV)
        f.close()
    
    def createTrainingFile(self, srcFileName, tgtFileName, trainingFileName):
        import pickle
        srcFile = open(srcFileName)
        tgtFile = open(tgtFileName)
        srcCharData = pickle.load(srcFile)
        tgtCharData = pickle.load(tgtFile)
        
        rbfTrain = RBFtrain()
        rbfTrain.RBFtraining(srcCharData.ROE, tgtCharData.ROE)
        trainData = CFR_trainData(srcCharData.charName, tgtCharData.charName, rbfTrain)
        
        trainFile = open(trainingFileName, 'w')
        pickle.dump(trainData, trainFile)
        
        srcFile.close()
        tgtFile.close()
        trainFile.close()
    
    def createFinalResult(self, srcAnimFileName, tgtCharDataFileName, trainDataFileName, resultAnimFileName):
        import pickle
        srcAnimFile = open(srcAnimFileName)
        srcAnimData = pickle.load(srcAnimFile)
        tgtCharFile = open(tgtCharDataFileName)
        tgtCharData = pickle.load(tgtCharFile)                
        trainDataFile = open(trainDataFileName)
        trainData = pickle.load(trainDataFile)
        
        cfrr = CFRRun()
        resultAnimDataList = cfrr.CFR_running(srcAnimData, tgtCharData, trainData)        
        resultAnimData = CFR_animData(tgtCharData.charName, tgtCharData.CVlist, resultAnimDataList, srcAnimData.frameList)
        
        resultAnimFile = open(resultAnimFileName, 'w')
        pickle.dump(resultAnimData, resultAnimFile)
        
        srcAnimFile.close()
        tgtCharFile.close()
        trainDataFile.close()
        resultAnimFile.close()    