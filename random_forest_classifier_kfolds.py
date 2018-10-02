# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 18:21:39 2018

@author: naroairiarte
"""

from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RandomizedSearchCV



def rf_classifier_V4(path_to_data, split_number):
    """
    This function reads the needed data to  get the arguments which are going to be passed to the random forest
    classifier.
    :param path_to_data: Is a string containing the path where the .txt data is stored.
    """
    clf_list = []
    train_accuracy_list = []
    test_accuracy_list = []
    clf_accuracy_quartet = []
    confusion_matrix_list = []
    df = pd.read_table(path_to_data)
    features_index = df.columns[15:-2]
    features_dataframe = df.loc[:, features_index]
    classes_dataframe = df.loc[:, ['PROD']]
    features_dataframe['PROD'] = classes_dataframe.iloc[:, 0].values
    cross_val = StratifiedKFold(n_splits=split_number)
    index_iterator = cross_val.split(features_dataframe, classes_dataframe)
    clf = RandomForestClassifier(bootstrap=False, class_weight=None, criterion='gini',
                                 max_depth=200, max_features='auto', max_leaf_nodes=None,
                                 min_impurity_decrease=0.0, min_impurity_split=None,
                                 min_samples_leaf=2, min_samples_split=10,
                                 min_weight_fraction_leaf=0.0, n_estimators=2000, n_jobs=-1,
                                 oob_score=False, random_state=None, verbose=0,
                                 warm_start=False)

    for train_index, test_index in index_iterator:
        X_train, X_test = np.array(features_dataframe)[train_index], np.array(features_dataframe)[test_index]
        y_train, y_test = np.array(classes_dataframe)[train_index], np.array(classes_dataframe)[test_index]
        clf.fit(X_train, y_train.ravel())
        clf_list.append(clf)
        y_train_pred = clf.predict(X_train)
        train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel())*100
        train_accuracy_list.append(train_accuracy)
        y_test_pred = clf.predict(X_test)
        test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel())*100

        confusion_matrix = pd.crosstab(y_test.ravel(), y_test_pred.ravel(), rownames=['Actual Cultives'],
                                       colnames=['Predicted Cultives'])
        test_accuracy_list.append(test_accuracy)
        clf_accuracy_quartet.append([train_accuracy, test_accuracy, clf, confusion_matrix])
        print('The train accuracy for the classifier is: ' + str(train_accuracy))
        print('The test accuracy for the classifier is: ' + str(test_accuracy))
    old_max_acc = clf_accuracy_quartet[0][1]  #en la segunda posicion se guardan los accuracy de test
    pos = 0 #Porque la primera posicion es la del accuracy que pongo arriba, simplemente por llevar un orden
    cf_matrix = clf_accuracy_quartet[0][3]
    for i in range(len(clf_accuracy_quartet)): # Para saltarnos el primero que ya lo tenemos en cuenta
        max_acc = clf_accuracy_quartet[i][1]
        if (max_acc > old_max_acc):
            pos = i #El clasificador mejor estara en esta posicion
            old_max_acc = max_acc
            cf_matrix = clf_accuracy_quartet[i][3]
    final_clf = clf_accuracy_quartet[pos][2] #Que es donde se guardan los clf
    print('The chosen clf is: ' + str(final_clf))
    print('En la posicion: ' + str(pos))
    print('Con accuracy en train de: ' + str(clf_accuracy_quartet[pos][0]))
    print('Con accuracy en test de: '+ str(clf_accuracy_quartet[pos][1]))
    print('Su matriz de confusion es: ')
    print(cf_matrix)

    cf_matrix.to_csv(r'/home/naroairirarte/Desktop/confusion_matrix_fin.txt', header=True, index=True, sep=' ', mode='a')


rf_classifier_V4('/home/naroairirarte/Desktop/Declaraciones2016/Declaraciones2016_NDVI_ComI.txt', 25)

