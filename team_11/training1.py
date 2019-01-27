import pandas
import csv
import numpy as np
import pickle
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

names = ['pt0x', 'pt0y', 'pt1x', 'pt1y','pageId','type']
dataset = pandas.read_csv(r'/Users/kim-li/Documents/CityU-Hackathon-2019/all_Training/1/1_form.csv', names=names)
#dataset = dataset.apply(lambda x: pandas.to_numeric(x,errors='ignore'))
dataset.dropna(inplace=True)
names2 = ['pt0x', 'pt0y', 'pt1x', 'pt1y','pageId']
testset = pandas.read_csv(r'/Users/kim-li/Documents/CityU-Hackathon-2019/Testing/67/67_form.csv',names = names2)
array2 = testset.values
X2 = array2[:,0:5]

array = dataset.values
X = array[:,0:5]
Y = array[:,5]
validation_size = 0.2
seed = 7
scoring = 'accuracy'
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

models = []
models.append(('LR', LogisticRegression(solver='liblinear',multi_class = 'auto')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma = 'scale')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    msg = "%s: %.6f (%.6f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

# Make predictions on validation dataset
cart = DecisionTreeClassifier()
cart.fit(X_train, Y_train)
predictions = cart.predict(X_validation)


print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))


#pickle.dump(knn,open("model1.pkl","wb"))
cart.fit(X,Y)

predictions = cart.predict(X2).tolist()

i = 0
with open(r'/Users/kim-li/Desktop/predicted_result.txt', 'w') as f_out:
    for i in range(len(predictions)):
        f_out.write("%d\n"%predictions[i])











