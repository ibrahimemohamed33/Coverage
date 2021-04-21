import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from dimension import Embedding


class Classifier:
    def __init__(self, 
                max_depth,
                n_neighbors, 
                directory, 
                n_estimators=10,
                reduce=False,
                path='auto',
                dimension=3,
                mock=False,
                file_name='Untitled.csv', 
                index='gene_callers_id',
                create_folder=False, 
                folder_name='folder',
                separator=None, 
                norm=True, 
                sort=False, 
                _filter=0, 
                is_filtered=False,
                rows=100, 
                columns=100):

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.reduced = Embedding(n_neighbors, 
                                directory, 
                                path=path,
                                dimension=dimension,
                                mock=mock,
                                file_name=file_name, 
                                index=index,
                                create_folder=create_folder, 
                                folder_name=folder_name,
                                separator=separator, 
                                norm=norm, 
                                sort=sort, 
                                _filter=_filter, 
                                is_filtered=is_filtered,
                                rows=rows, 
                                columns=columns)
        
        if reduce:
            self.dataframe = self.reduced.embedded_dataframe
            self.X = self.reduced.embedded_data
        else:
            self.dataframe = self.reduced.dataframe
            self.X, self.y = self.reduced.data, self.reduced.classifers

    def fit_data(self, train):
        '''
        Performs the random forest classifier
        '''
        
        self.F = RandomForestClassifier(n_estimators=self.n_estimators,
                                        max_depth=self.max_depth)
        if train:
            self.F.fit(self.X, self.y)
        else:
            self.F.apply(self.X)


    # def test_accuracy(self, train):
    #     if train:
    #         X_train, X_test, y_train, y_test = train_test_split(
    #                                                 self.X, 
    #                                                 self.y, 
    #                                                 test_size=0.33, 
    #                                                 random_state=42
    #                                             )
        
            



