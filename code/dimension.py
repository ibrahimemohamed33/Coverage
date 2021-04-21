import numpy as np
import pandas as pd
import sys

from coverage import Coverage
from sklearn import manifold


valid_path_methods = ["auto", "D", "FW"]

class Embedding:
    def __init__(self, 
                n_neighbors, 
                directory, 
                dimension=3,
                path='auto',
                train=True,
                file_included_in_directory=False,
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

        self.coverage = Coverage(
            directory=directory,
            norm=norm,
            sort=sort,
            filter=_filter,
            coverage_values_file=file_name,
            file_included_in_directory=file_included_in_directory,
            index=index,
            mock=mock,
            rows=rows,
            columns=columns,
            train=train,
            export_file=False,
            create_folder=False,
            folder_name=folder_name,
            separator=separator
            )


        self.dataframe = self.coverage.dataframe
        self.data = self.coverage.coverage_values
        self.classifers = self.coverage.classified_values
        
        self.is_path_OK(path)
        self.embedded_data = self.embed(
                n_neighbors, 
                num_components=dimension, 
                path_method=path, 
                mock=mock
            )
        
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
    def adjust_num_components(self, num_components):
        '''
        Finds the interval [min_num_components, max_num_components] for which
        num_components lie in. From there, the function creates an inclusion map
        from num_components into max_num_components
        '''
        min_num_components, step = 10, 20
        max_num_components = min_num_components + step
        while num_components > max_num_components or num_components < min_num_components:
            if max_num_components > 150:
                break
            min_num_components += step
            max_num_components += step

        self.inclusion_map(num_components, max_num_components)
        return max_num_components

  
    def inclusion_map(self, dimension, num_components):
        if dimension < num_components:
            for i in range(dimension + 1, num_components - dimension + 1):
                    metagenome_name = 'metagenome__%d' %(i)
                    self.dataframe[metagenome_name] = 0

    
    def inclusion(self, num_components):
        '''
        Maps d-dimensional space into n-dimensional by appending 0's to the 
        remaining (n-d)-values
        '''
        __, dimension = self.dataframe.shape
        num_components = self.adjust_num_components(num_components)
        if dimension < num_components:
            if dimension < 10:
                raise ValueError(
                    """While we would ideally perform the algorithm
                       on any dataset, the sad truth is that your dimension size 
                       '%d' is too small"""
                       %(dimension)
                    )
            elif dimension > 150:
                raise ValueError(
                    """While we would ideally perform the algorithm
                       on any dataset, the sad truth is that your dimension size 
                       '%d' is too large"""
                       %(dimension)
                    )
            else:
                self.inclusion_map(dimension, num_components)
            
    
    def embed(self, n_neighbors, num_components, path_method, mock):
        '''
        Embeds d-dimensional data into N-dimensional data, where N <= d
        and N is the number of components
        '''
        # checks if the dataframe's size is large enough for an embedding
        self.inclusion(num_components)

        embedding = manifold.Isomap(
                n_neighbors=n_neighbors,
                n_components=num_components,
                path_method=path_method
            )
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