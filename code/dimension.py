import numpy as np
import pandas as pd

from coverage import Coverage
from sklearn import manifold
from sklearn.ensemble import RandomForestClassifier

valid_path_methods = ["auto", "D", "FW"]

class Reduction:
    def __init__(self, 
                n_neighbors, 
                directory, 
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
        '''
        Class attempts to embed high-dimensional coverage values
        into lower dimension using the Isomap algorithm
        '''

        self.coverage = Coverage(directory=directory,
                                mock=mock,
                                file_name=file_name,
                                export_file=False,
                                create_folder=False,
                                index=index,
                                folder_name=folder_name,
                                separator=separator,
                                norm=norm,
                                sort=sort,
                                filter=_filter,
                                rows=rows,
                                columns=columns)


        self.dataframe = self.coverage.dataframe
        
        self.is_path_OK(path)
        self.embedded_data = self.embed(n_neighbors, 
                                        num_components=dimension, 
                                        path_method=path, 
                                        mock=mock)
        
        self.embedded_dataframe = self.embed_into_dataframe()
    
    def is_path_OK(self, path):
        '''
        Raises errors for invalid in`puts
        '''

        if path not in valid_path_methods:
            raise Exception("It appears that your path method '%s' is not a"
                            " a valid path. Try setting your path to 'auto' or"
                            " 'D'" 
                            %(path))
    
    def inclusion(self, num_components):
        '''
        Maps d-dimensional space into n-dimensional by appending 0's to the 
        remaining (n-d)-values
        '''
        n = num_components
        __, d = self.dataframe.shape
        if d < n:
            for i in range(d + 1, n - d + 1):
                metagenome_name = 'metagenome__%d' %(i)
                self.dataframe[metagenome_name] = 0
  
    
    def embed(self, n_neighbors, num_components, path_method, mock):
        '''
        Embeds d-dimensional data into N-dimensional data, where N <= d
        and N is the number of components
        '''
        # checks if the dataframe's size is large enough for an embedding
        self.inclusion(num_components)

        embedding = manifold.Isomap(n_neighbors=n_neighbors,
                                    n_components=num_components,
                                    path_method=path_method)
        if mock:
            t = embedding.fit_transform(self.dataframe[1:])
        else:
            t = embedding.fit(self.dataframe[1:])
            t.transform(self.dataframe[1:])
        
        return t

    def embed_into_dataframe(self):
        '''
        Turns embedded data into dataframe
        '''

        _, dimension = self.embedded_data.shape
        columns = ["Reduced__Columns__%d" %(i) for i in range(dimension)]
        df = pd.DataFrame(data=self.embedded_data, columns=columns)
        return df


class Classifier:
    def __init__(self, 
                n_estimators,
                max_depth,
                n_neighbors, 
                directory, 
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
        self.reduced = Reduction(n_neighbors, 
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
        else:
            self.dataframe = self.reduced.dataframe

    def learn(self):
        RandomForestClassifier(n_estimators=self.n_estimators,
                               max_depth=self.max_depth)
        return None 


