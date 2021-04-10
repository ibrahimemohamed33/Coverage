import numpy as np
import pandas as pd

from coverage import Coverage
from sklearn import manifold

valid_path_methods = ["auto", "D", "FW"]

class Reduction:
    def __init__(self, 
                n_neighbors, 
                directory, 
                path=None,
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
        '''
        Class attempts to simplify the high-dimensional coverage values
        into lower dimension using the Isomap algorithm
        '''

        self.n_neighbors = n_neighbors
        self.mock = mock
        self.num_components = dimension
        self.path_method = 'auto' if path is None else path

        self.coverage = Coverage(directory=directory,
                                mock=mock,
                                file_name=file_name,
                                export=False,
                                index=index,
                                folder_name=folder_name,
                                separator=separator,
                                norm=norm,
                                sort=sort,
                                filter=_filter,
                                rows=rows,
                                columns=columns)

        if is_filtered:                                
            self.dataframe = self.coverage.filtered_sample
        else:
            self.dataframe = self.coverage.dataframe
        
        self.reduced_data = self.embed()
    
    def inclusion(self):
        '''
        Maps d-dimensional space into N-dimensional by appending 0's to the 
        remaining N-d values
        '''

        dimension, _ = self.dataframe.shape
        if dimension < self.num_components:
            delta = self.num_components - dimension + 1
            for i in range(dimension + 1, delta):
                metagenome_name = 'metagenome__%d' %(i)
                self.dataframe[metagenome_name] = 0
  
    
    def embed(self):
        '''
        Embeds d-dimensional data into N-dimensional data, where N <= d
        and N is the number of components
        '''

        self.inclusion()
        embedding = manifold.Isomap(n_neighbors=self.n_neighbors,
                                    n_components=self.num_components,
                                    path_method=self.path_method)
        if self.mock:
            t = embedding.fit_transform(self.dataframe[1:])
        else:
            t = embedding.fit(self.dataframe[1:])
        
        return t

        
    





    

