import os
import sys

import coverage
import dimension
import manual
import train as training 

from sklearn import manifold


epsilon = coverage.epsilon

class Compare:
    '''
    Class compares the classification of the embedded data and
    the classification of the original data. This may involve changing up
    the algorithms that allow for a lower dimensional embedding of the datasets
    '''

    def __init__(self, 
                n_neighbors,
                directory,
                path='auto',
                train=True,
                file_included_in_directory=False,
                mock=False,
                file_name='Untitled.csv', 
                index='gene_callers_id',
                create_folder=False, 
                export_file=True,
                folder_name='folder',
                separator=None, 
                norm=True, 
                _filter=coverage.epsilon, 
                rows=100, 
                columns=100,
                tree_file='tree.txt'):


        self.embedding = dimension.Embedding(directory=directory,
                                    n_neighbors=n_neighbors,
                                    norm=norm,
                                    _filter=_filter,
                                    file_name=file_name,
                                    file_included_in_directory=file_included_in_directory,
                                    index=index,
                                    mock=mock,
                                    rows=rows,
                                    columns=columns,
                                    train=train,
                                    export_file=True,
                                    create_folder=False,
                                    folder_name=folder_name,
                                    separator=separator)  
                                    
        self.dataframe = self.embedding.dataframe
        self.embedded_dataframe = self.embedding.embedded_dataframe

        self.coverage_training = training.Train(directory=directory, 
                                                coverage_values_file=self.embedding.coverage_values_file,
                                                classified_values_file=self.embedding.classified_values_file,
                                                tree_file='tree.txt',
                                                title="Regular Data")
        
        self.embedded_training = training.Train(directory=directory,
                                                coverage_values_file=self.embedding.embedded_coverage_values_file,
                                                classified_values_file=self.embedding.embedded_classified_values_file,
                                                tree_file='tree1.txt',
                                                title="Embedded Data",
                                                override=True)

        
     
        


