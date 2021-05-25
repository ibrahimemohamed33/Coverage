import numpy as np
import pandas as pd
import pickle

from dimension import Embedding
import training

from coverage import epsilon
from sklearn.ensemble import RandomForestClassifier



class Classifier:
    def __init__(self, 
                max_depth,
                directory, 
                tree_file_name='tree.txt',
                title='Embedded Values',
                already_classified=False,
                n_neighbors=100, 
                train=True,
                n_estimators=10,
                file_included_in_directory=False,
                file_name='Untitled.csv', 
                reduce=False,
                path='auto',
                dimension=3,
                mock=False,
                index='gene_callers_id',
                create_folder=False, 
                folder_name='folder',
                separator=None, 
                norm=True, 
                _filter=epsilon, 
                rows=100, 
                columns=100):

        self.algorithm_filename = 'metagenome-centric_classifier_algorithm.sav'
        self.train = train
        self.n_estimators = n_estimators
        self.max_depth = max_depth

        self.embedded = Embedding(n_neighbors, 
                                directory, 
                                path=path,
                                reduced_dimension=dimension,
                                train=train,
                                mock=mock,
                                file_name=file_name, 
                                index=index,
                                create_folder=create_folder, 
                                folder_name=folder_name,
                                separator=separator, 
                                norm=norm, 
                                _filter=_filter, 
                                rows=rows, 
                                columns=columns, 
                                tree_file='tree.txt')

        self.directory = self.embedded.directory
        self.dataframe = self.embedded.embedded_dataframe
        self.X = self.embedded.coverage_values

        if train:
            self.train_data(tree_file_name, title)

        self.fit_data()

    def train_data(self, tree_file_name, title):
        '''
        Allows user to manually train the data
        '''
        directory=self.embedded.directory
        coverage_values_file=self.embedded.embedded_coverage_values_file
        classified_values_file=self.embedded.embedded_classified_values_file

        training_data = training.Train(directory=directory,
                                       coverage_values_file=coverage_values_file, 
                                       classified_values_file=classified_values_file, 
                                       tree_file=tree_file_name, 
                                       title=title)
        
        self.X = training_data.coverage_values
        self.y = training_data.classified_values
    

    def save_model(self):
        '''
        Saves model to a binary file using pickle
        '''
        with open(self.algorithm_filename, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self):
        '''
        Loads model to a binary file using pickle
        '''
        with open(self.algorithm_filename, 'wb') as f:
            return pickle.load(open(self.algorithm_filename, 'wb'))

    def fit_data(self):
        '''
        Performs the random forest classifier
        '''

        # checks if random forest classifier has already been created 
        try:
            self.model = self.load_model()
        except EOFError:
            self.model = RandomForestClassifier(n_estimators=self.n_estimators,
                                                max_depth=self.max_depth)            
        if self.train:
            self.model.fit(self.X, self.y)
        else:
            self.model.apply(self.X)
        
        self.save_model()