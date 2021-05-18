import os
import sys

import coverage
import dimension
import manual
import training 

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
                coverage_tree_file='tree.txt',
                embedding_tree_file='tree1.txt'):


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
                                    separator=separator,
                                    manifold_method='ISOMAP')  
        self.embedding1 = dimension.Embedding(directory=directory,
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
                                    separator=separator,
                                    manifold_method='MDS',
                                    count=1)  

        self.embedding2 = dimension.Embedding(directory=directory,
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
                                    separator=separator,
                                    manifold_method='LLE',
                                    count=2)

  
          
                                    
        # self.dataframe = self.embedding.dataframe
        # self.embedded_dataframe = self.embedding.embedded_dataframe

        self.coverage_training = training.Train(directory=directory, 
                                                coverage_values_file=self.embedding.coverage_values_file,
                                                classified_values_file=self.embedding.classified_values_file,
                                                tree_file=coverage_tree_file,
                                                title="Regular Data Without Any Dimensional Reduction",
                                                export=False)
        
        self.embedded_training = training.Train(directory=directory,
                                                coverage_values_file=self.embedding.embedded_coverage_values_file,
                                                classified_values_file=self.embedding.embedded_classified_values_file,
                                                tree_file=embedding_tree_file,
                                                title="Embedded Data Using an Isomap Reduction",
                                                override=True,
                                                export=False)

        self.embedded_training1 = training.Train(directory=directory,
                                                coverage_values_file=self.embedding1.embedded_coverage_values_file,
                                                classified_values_file=self.embedding1.embedded_classified_values_file,
                                                tree_file=embedding_tree_file,
                                                title="Embedded Data Using Multidimensional Scaling",
                                                override=True,
                                                export=False)
        self.embedded_training2 = training.Train(directory=directory,
                                                coverage_values_file=self.embedding2.embedded_coverage_values_file,
                                                classified_values_file=self.embedding2.embedded_classified_values_file,
                                                tree_file=embedding_tree_file,
                                                title="Embedded Data Using Non-Hessian Locally Linear Embedding",
                                                override=True,
                                                export=False)

       

