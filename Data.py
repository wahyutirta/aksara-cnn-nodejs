import numpy as np
import cv2
import os
import math
from tqdm import tqdm
from einops import rearrange, reduce, repeat
from skimage.feature import greycomatrix, greycoprops
import matplotlib.pyplot as plt 
import pickle

class Data:
    def __init__(self, workPath, imagePath):
        self.dataPath = os.path.join(workPath[0],imagePath) #image path
        self.imagePath = imagePath
        
    """
        DOKUMENTASI 
        
    """    
    @staticmethod
    def unison_shuffled_copies_4( a , b, c):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p] , c[p]
    
    @staticmethod
    def unison_shuffled_copies_2( a , b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]
    
    def loadLabel(self):
        """
        DOKUMENTASI 
        
        """
        arr_Namelabel = []
        self.count = 0
        for i, (dirpath, dirnames, filenames) in tqdm(enumerate(os.walk(self.imagePath)), desc= "Loading Image Data"):
            #print('{} {} {}'.format(repr(dirpath), repr(dirnames), repr(filenames)))
            #print(i)
            if dirpath is not self.imagePath:
                dirpath_components = dirpath.split("/")
                listImageTrain = []
                listLabelTrain = []
                listImageTest = []
                listLabelTest = []
                testFName = []
                trainFName = []
                semantic_label = dirpath_components[-1]
                
                _, label = os.path.split(semantic_label)

                #print("\nProcessing {}, {}".format(semantic_label,i))
                arr_Namelabel.append(label)
        labelArray = np.array(arr_Namelabel)
        return labelArray
    
    def load(self,trainRatio=0.8,testRatio=0.2):
        
        """
        DOKUMENTASI 
        
        """
        
        temp_mod = math.ceil(trainRatio/testRatio)
        #arr_img = []
        #arr_label = []
        arr_Namelabel = []
        self.count = 0
        for i, (dirpath, dirnames, filenames) in tqdm(enumerate(os.walk(self.imagePath)), desc= "Loading Image Data"):
            #print('{} {} {}'.format(repr(dirpath), repr(dirnames), repr(filenames)))
            #print(i)
            if dirpath is not self.imagePath:
                dirpath_components = dirpath.split("/")
                listImageTrain = []
                listLabelTrain = []
                listImageTest = []
                listLabelTest = []
                testFName = []
                trainFName = []
                semantic_label = dirpath_components[-1]
                
                _, label = os.path.split(semantic_label)

                #print("\nProcessing {}, {}".format(semantic_label,i))
                arr_Namelabel.append(label)
                self.count = 0
                train = 0
                test = 0

                for f in filenames:
                    #load images
                    file_path = os.path.join(dirpath, f)
                    #print(file_path)
                    img = cv2.imread(file_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.resize(img, (32,32), interpolation = cv2.INTER_AREA)
                    thresh, bw = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
                    

                    swap = 255 * (bw==0).astype(int)
                    #print(swap)
                    #break
                    swap = swap.reshape((1,32,32))
                    ##img = rearrange(swap, ' h w c ->  c h w ')

                    #arr_label.append(i-1)
                    # if mod append to test
                    names = semantic_label.split("\\")
                    #print(str(names[-1]))
                    if self.count % temp_mod == 0:
                        
                        listImageTest.append(swap)
                        listLabelTest.append(names[-1])
                        testFName.append(f)
                        test+= 1
                    # if not mod append to train
                    else:
                        listImageTrain.append(swap)
                        listLabelTrain.append(names[-1])
                        trainFName.append(f)
                        
                        train+= 1
                        
                    self.count+=1
                #print("blaaaaaaaaa"+ str(len(listImageTest)))
                arrayImageTest = np.array(listImageTest, dtype='float64') /255
                arrayImageTrain = np.array(listImageTrain, dtype='float64') /255
                #print(np.array(arr_img).shape)
                arrayLabelTest = np.array(listLabelTest)
                arrayLabelTrain = np.array(listLabelTrain)
                
                arrayFNameTest = np.array(testFName)
                arrayFNameTrain = np.array(trainFName)
                
                self.labelName = np.array(arr_Namelabel)
                self.jum_kelas = len(self.labelName)

                if not hasattr(self, 'testSet'):
                    self.trainSet = arrayImageTrain
                    self.trainLabel = arrayLabelTrain
                    self.testSet = arrayImageTest
                    self.testLabel = arrayLabelTest
                    
                    self.arrayFNameTrain = arrayFNameTrain
                    self.arrayFNameTest = arrayFNameTest
                else:
                    self.trainSet = np.concatenate((self.trainSet, arrayImageTrain), axis = 0)
                    self.trainLabel = np.concatenate((self.trainLabel, arrayLabelTrain), axis = 0)
                    self.testSet = np.concatenate((self.testSet, arrayImageTest), axis = 0)
                    self.testLabel = np.concatenate((self.testLabel, arrayLabelTest), axis = 0)
                    self.arrayFNameTest = np.concatenate((self.arrayFNameTest, arrayFNameTest), axis = 0)
                    self.arrayFNameTrain = np.concatenate((self.arrayFNameTrain, arrayFNameTrain), axis = 0)

        #print(self.arrayFNameTest)
        #self.trainSet, self.trainLabel, self.arrayFNameTrain = self.unison_shuffled_copies_4(self.trainSet, self.trainLabel, self.arrayFNameTrain)
        #self.testSet, self.testLabel, self.arrayFNameTest  = self.unison_shuffled_copies_4(self.testSet, self.testLabel, self.arrayFNameTest)
        #print(self.arrayFNameTest)
        return self.trainSet, self.trainLabel, self.testSet, self.testLabel
    

#mainPath = os.path.dirname(os.path.abspath(__file__)) #file path main.py
#workPath = os.path.split(mainPath) #path working folder (whole file project)
#imagePath = "data_jepun"
#data = Data(workPath,imagePath)
#trainSet, trainLabel, testSet, testLabel = data.load(trainRatio=0.8,testRatio=0.2)

#print("ts",trainSet.shape)
#print("tl",trainLabel.shape)
#print("tts",testSet.shape)
#print("ttl",testLabel.shape)



mainPath = os.path.dirname(os.path.abspath(__file__)) #file path main.py
workPath = os.path.split(mainPath) #path working folder (whole file project)
imagePath = "datasetAksara"
data = Data(workPath,imagePath)
trainSet, trainLabelSet, testSet, testLabelSet = data.load(trainRatio=0.8,testRatio=0.2)
test1 = trainSet[0]

with open('x-train.pickle', 'wb') as handle:
    pickle.dump(trainSet, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('y-train.pickle', 'wb') as handle:
    pickle.dump(trainLabelSet, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('x-test.pickle', 'wb') as handle:
    pickle.dump(testSet, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('y-test.pickle', 'wb') as handle:
    pickle.dump(testLabelSet, handle, protocol=pickle.HIGHEST_PROTOCOL)

#trainSet, trainLabelSet = data.unison_shuffled_copies_2(trainSet, trainLabelSet)

for x in range(0, 1500, 100):
    plt.imshow(trainSet[x,0,:,:])
    print(trainLabelSet[x])
    plt.show()

img = trainSet[100]





