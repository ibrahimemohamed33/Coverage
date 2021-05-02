import numpy as np
import pandas as pd

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
                sort=False, 
                _filter=0, 
                is_filtered=False,
                rows=100, 
                columns=100):
        
        self.train = train
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.reduced = Embedding(n_neighbors, 
                                directory, 
                                path=path,
                                dimension=dimension,
                                train=train,
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
            self.X = self.reduced.embedded_vectors
        else:
            self.dataframe = self.reduced.dataframe
            self.X, self.y = self.reduced.data, self.reduced.classifers

    def fit_data(self):
        '''
        Performs the random forest classifier
        '''
        
        self.F = RandomForestClassifier(n_estimators=self.n_estimators,
                                        max_depth=self.max_depth)
        if self.train:
            self.F.fit(self.X, self.y)
        else:
            self.F.apply(self.X)





