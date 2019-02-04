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



def rf_classifier_V3(path_to_data, split_number):
    """
    This function reads the needed data to  get the arguments which are going to be passed to the random forest
    classifier.
    :param path_to_data: Is a string containing the path where the .txt data is stored.
    """
    df = pd.read_table(path_to_data)
    features_index = df.columns[15:-2]
    features_dataframe = df.loc[:, features_index]
    classes_dataframe = df.loc[:, ['PROD']]
    features_dataframe['PROD'] = classes_dataframe.iloc[:, 0].values
    features_dataframe['is_train'] = np.random.uniform(0, 1, len(features_dataframe)) <= .65
    train, test = features_dataframe[features_dataframe['is_train'] == True], features_dataframe[
        features_dataframe['is_train'] == False]
    ####
    column_length = len(features_dataframe.columns)
    features_length = column_length - 2
    features = features_dataframe.iloc[:, :features_length]
    y_train = train.iloc[:, -2]
    features_index = features.columns[:]
    X_train = train[features_index]
    X_test  = test[features_index]
    y_test = test.iloc[:, -2]
    ######
    #TODO: seria buena idea cambiar algun parametro, como por ejemplo el n_stimators, a mas de 100
    clf = RandomForestClassifier()
    random_grid = _create_hyperparameter_finetuning_grid()
    clf_random = RandomizedSearchCV(estimator=clf, param_distributions=random_grid,
                                    scoring='accuracy', n_iter=100,
                                    cv=StratifiedKFold(n_splits=split_number),
                                    verbose=2, random_state=42, n_jobs=-1)
    #clf_random = RandomizedSearchCV(estimator=clf, param_distributions=random_grid,
    #                               scoring='accuracy', n_iter=100,
    #                                cv=split_number,
    #                                verbose=2, random_state=42, n_jobs=-1)
    clf_random.fit(X_train, y_train)

    ######
    y_train_pred = clf_random.predict(X_train)
    y_test_pred = clf_random.predict(X_test)
    train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
    test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
    print('The train accuracy for the classifier is: ' + str(train_accuracy))
    print('The test accuracy for the classifier is: ' + str(test_accuracy))
    #####

    confusion_matrix = pd.crosstab(y_test.ravel(), y_test_pred.ravel(), rownames=['Actual Cultives'],
                                   colnames=['Predicted Cultives'])

    print('The chosen clf is: ' + str(clf_random.best_estimator_))
    print('This is the confusion matrix: ')
    print(confusion_matrix)
    # TODO: meter todos los porcentajes etc en un csv que será el entregable, esto se hace desde el programa que llama a este
    confusion_matrix.to_csv(r'/home/naroairirarte/Desktop/confusion_matrix_fin.txt', header=True, index=True, sep=' ', mode='a')
    test_accuracy_file = open("test_accuracy.txt", "w")
    test_accuracy_file.write("Test accuracy: %s" % test_accuracy)
    test_accuracy_file.close()
    train_accuracy_file = open("test_accuracy.txt", "w")
    train_accuracy_file.write("Train accuracy: %s" % train_accuracy)
    train_accuracy_file.close()



def _create_hyperparameter_finetuning_grid():
    # The grid of the parameters which will bi finetunned is prepared:
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start=100, stop=2000, num=10)]
    # Number of features to consider at every split
    max_features = ['sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_features': max_features,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}
    return random_grid


rf_classifier_V3('/home/naroairirarte/Desktop/Declaraciones2016/Declaraciones2016_NDVI_ComV.txt', 10)
