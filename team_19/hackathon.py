
import parsing
import string
import numpy as np
from keras.models import Sequential , load_model
from keras.layers import Dense, Activation
import keras.utils as u
import random
import matplotlib.pyplot as plt

modname = "Audit_Period_model.h5"
folder = 5
filecount = 128
entType = "Audit Period"

#build words list
#


misses = -1
#build training set
#

def testmodel(m):
    model = m

    words = parsing.getwordlist()
    pps = parsing.pagenums("Training"+"/"+str(folder) +"/"+str(folder) + "_tagged.json",entType)
    print(pps)
    ys = []
    xs = []
    for i in range(filecount):

        x = parsing.caseinputs(words,"Training"+"/"+str(folder)+"/hocr/"+str(folder)+"-"+str(i)+".hocr")
        for q in x:
            xs.append(q)

        if(i in pps):
            ys.append(1)
        else:
            ys.append(0)

    xs = np.array(xs).reshape(int(len(xs)/len(words)),len(words))
    ys = np.array(ys).reshape(len(ys),1)

    print(xs)
    preds = model.predict_classes(xs, verbose=0)
    print("page\tpredicted\tcorrect")
    tocheck = []
    for i in range(len(preds)):
        print(str(i) + "\t" + str(preds[i]) + "\t" + str(ys[i]) )
        if(preds[i]>.5):
            tocheck.append(i)

    print(tocheck)

def testmodelforpositive(m):
    model=m
    tosearch = []
    words = parsing.getwordlist()
    for i in range(1,60):
        if i not in parsing.C.missingfolders:
            r = parsing.pagenums("Training"+"/"+str(i)+"/"+str(i)+"_tagged.json",entType)
            tosearch.append((i,r))

    xs = []
    ys = []
    for i in tosearch:
        for ii in i[1]:
            x = parsing.caseinputs(words,"Training"+"/"+str(i[0])+"/hocr/"+str(i[0])+"-"+str(ii)+".hocr")
            for q in x:
                xs.append(q)
            ys.append(1)
    
    xs = np.array(xs).reshape(int(len(xs)/len(words)),len(words))
    ys = np.array(ys).reshape(len(ys),1)

    preds = model.predict_classes(xs, verbose=0)
    print("page\tpredicted\tcorrect")
    tocheck = []
    for i in range(len(preds)):
        print(str(i) + "\t" + str(preds[i]) + "\t" + str(ys[i]) )
        if(preds[i]>.5):
            tocheck.append(i)

    print(tocheck)


def trainmodel():
    dataset = parsing.loaddata("dataset")
    data = np.array(dataset[0])

    labels = np.array(dataset[1]).reshape(data.shape[0],1)


    testrows = [];
    num = 10
    posindex = []
    for i in range(data.shape[0]):
        if(labels[i][0]==1):
            posindex.append(i)
    for i in range(50):
        index = random.randint(0,len(posindex)-1)
        testrows.append(posindex[index])

    for i in range(50):
        index = random.randint(0,data.shape[0]-1)
        testrows.append(index)



    print(data.shape)
    print(labels.shape)


    model = Sequential([
        Dense(16,input_shape=(data.shape[1],),activation='relu'),
        Dense(8,activation='sigmoid'),
        Dense(1,activation='sigmoid'),
        ])

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    hist = model.fit(data, labels, epochs=500, batch_size=256)

    lossdata = hist.history['loss']
    
    testdata = []
    testresult = []
    count = 0
    for test in testrows:
        x = data[test]
        for i in x:
            testdata.append(i)
            count+=1
        testresult.append(labels[test])

    testdata = np.array(testdata).reshape(100,data.shape[1])

    preds = model.predict_classes(testdata, verbose=0)
    #print("predicted\tcorrect")
    correct=0
    for i in range(100):
        #print(str(preds[i][0])+'\t\t'+str(testresult[i][0]))
        if((float(preds[i][0])>.5) & (float(testresult[i][0]) > .5 )):
            correct+=1
        elif((float(preds[i][0])<.5) & (float(testresult[i][0]) < .5 ) ):
            correct+=1
    model.save(modname)
    print("lost data:",misses)
    print("correct 50/50:",correct/100)


    testdata = []
    testresult = []
    for test in posindex:
        x = data[test]
        for i in x:
            testdata.append(i)
            count+=1
        testresult.append(labels[test])
    testdata = np.array(testdata).reshape(len(posindex),data.shape[1])

    preds = model.predict_classes(testdata, verbose=0)
    #print("predicted\tcorrect")
    correct=0
    for i in range(len(posindex)):
        #print(str(preds[i][0])+'\t\t'+str(testresult[i][0]))
        if((float(preds[i][0])>.5) & (float(testresult[i][0]) > .5 )):
            correct+=1
        elif((float(preds[i][0])<.5) & (float(testresult[i][0]) < .5 ) ):
            correct+=1
    model.save(modname)
    print("correct %truetrue:",correct/len(posindex))


    testdata = []
    testresult = []
    for k in range(1000):
        test = random.randint(0,data.shape[0]-1)
        x = data[test]
        for i in x:
            testdata.append(i)
            count+=1
        testresult.append(labels[test])
    testdata = np.array(testdata).reshape(1000,data.shape[1])

    preds = model.predict_classes(testdata, verbose=0)
    #print("predicted\tcorrect")
    correct=0
    for i in range(len(posindex)):
        #print(str(preds[i][0])+'\t\t'+str(testresult[i][0]))
        if((float(preds[i][0])>.5) & (float(testresult[i][0]) > .5 )):
            correct+=1
        elif((float(preds[i][0])<.5) & (float(testresult[i][0]) < .5 ) ):
            correct+=1
    model.save(modname)
    print("correct %random:",correct/len(posindex))


    #print(lossdata)
    #plt.plot(lossdata)
    #plt.show()
    #testmodel(model)
    #testmodelforpositive(model)
    





