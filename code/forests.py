import numpy as np
import pandas as pd
import joblib

from coverage import epsilon
from sklearn.ensemble import RandomForestClassifier
from dimension import Embedding


class Classifier:
    def __init__(self, 
                max_depth,
                directory, 
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
            self.y = self.embedded.classified_values
    
  
        self.fit_data()
        self.save_model()

    def fit_data(self):
        '''
        Performs the random forest classifier
        '''
        
        self.model = RandomForestClassifier(n_estimators=self.n_estimators,
                                            max_depth=self.max_depth)
                                            
        if self.train:
            self.model.fit(self.X, self.y)
        else:
            self.model.apply(self.X)

    def save_model(self):
        joblib.dump(self.model, os.path.join(self.directory, 'model.dat'))
