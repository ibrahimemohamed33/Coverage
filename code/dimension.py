import os

import numpy as np
import pandas as pd
import shutil

from manual import AdjustClassification 
from coverage import Coverage
from sklearn import manifold


valid_path_methods = ["auto", "D", "FW"]

def adjust_columns(dataframe, mock):
    t = dataframe.transpose()
    t.columns = t.columns.astype(str)
    return t.transpose()


class Embedding:
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
                sort=False, 
                _filter=0, 
                is_filtered=False,
                rows=100, 
                columns=100,
                tree_file='tree.txt'):
        '''
        Class attempts to embed high-dimensional coverage values
        into lower dimension using the Isomap algorithm
        '''
        self.train = train
        self.tree_file = tree_file

        self.directory = directory
        self.folder_name = folder_name

        self.coverage = Coverage(directory=directory,
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
                                export_file=True,
                                create_folder=False,
                                folder_name=folder_name,
                                separator=separator)       

        self.dataframe = self.coverage.coverage_values_dataframe
        self.coverage_values_file = self.coverage.coverage_values_file
        self.classified_values_file = self.coverage.classified_values_file_name
        

        _, self.dimension = self.dataframe.shape
        self.num_components = self.projected_number_of_components()        
        self.is_path_OK(path)

        self.embedded_vectors = self.embed(
                n_neighbors, 
                path_method=path, 
                mock=mock
            )
        
        self.embedded_dataframe = self.embed_into_dataframe()
        self.export(export_file, mock)
    
    def is_path_OK(self, path):
        '''
        Raises errors for invalid inputs
        '''

        if path not in valid_path_methods:
            raise Exception(
                """Your path method '%s' is not a valid method for the isomapping.
                What you should do instead is set your path to the keywords
                'auto' or 'D'. This will likely fix the issue
                """ 
                %(path)
            )
    

    def projected_number_of_components(self):
        '''
        Finds the interval [min_num_components, max_num_components] for which
        num_components lie in. From there, the function creates an inclusion map
        from num_components into max_num_components
        '''
        min_num_components, step = 10, 20
        max_num_components = min_num_components + step
        while self.dimension > max_num_components or self.dimension < min_num_components:
            if max_num_components > 150:
                break
            min_num_components += step
            max_num_components += step

        delta = lambda y: abs(self.dimension - y)
        # determines whether to round down or up 
        if delta(min_num_components) < delta(max_num_components):
            return min_num_components
        else:
            return max_num_components

  
    def inclusion_map(self):
        self.is_dimension_OK()
        if self.dimension < self.num_components:
            for i in range(self.dimension + 1, self.num_components + 1):
                metagenome_name = 'metagenome__%d' %(i)
                self.dataframe[metagenome_name] = 0

    def is_dimension_OK(self):
        if self.dimension < 10:
            raise ValueError(
                """While we would ideally perform the algorithm on any dataset, 
                the sad truth is that your dimension size '%d' is too small
                """
                %(self.dimension)
            )
            
        if self.dimension > 150:
            raise ValueError(
                """While we would ideally perform the algorithm on any dataset, 
                the sad truth is that your dimension size '%d' is too small
                """
                %(self.dimension)
            )

    
    def embed(self, n_neighbors, path_method, mock):
        '''
        Embeds d-dimensional data into n-dimensional data, where n <= d
        and n represents the number of components
        '''
        self.inclusion_map()
        embedding = manifold.Isomap(
                n_neighbors=n_neighbors,
                n_components=self.num_components,
                path_method=path_method
            )
        if mock:
            t = embedding.fit_transform(self.dataframe[:])
        else:
            fit = embedding.fit(self.dataframe[:])
            t = fit.transform(self.dataframe[:])

        return t
    
    def adjusted_indices(self):
        reduced_indices = [
            'gene__reduced_%d' %(i) for i in self.dataframe.index
        ]
        
        index_name = 'Reduced_' + self.dataframe.index.name

        return index_name, reduced_indices

        

    def embed_into_dataframe(self):
        '''
        Turns embedded data into dataframe
        '''

        index_name, reduced_indices = self.adjusted_indices()
        _, dimension = self.embedded_vectors.shape
        labels = ["Reduced__Column__%d" %(i) for i in range(dimension)]

        df = pd.DataFrame(
                data=self.embedded_vectors, columns=labels
            )

        df[index_name] = reduced_indices
        df = df.set_index(index_name)

        return df
    
    def export(self, export_file, mock):
        '''
        Exports the embededd dataframe into a file containing coverage values
        for manual classification
        '''
        
        self.embedded_coverage_values_file = 'embedded_' + self.coverage_values_file
        # exports dataframe
        if export_file:
            if os.path.exists(os.path.join(os.path.abspath(self.directory), self.embedded_coverage_values_file)):
                os.remove(os.path.join(os.path.abspath(self.directory), self.embedded_coverage_values_file))
            df = adjust_columns(self.embedded_dataframe, mock)
            df.to_csv(self.embedded_coverage_values_file , sep='\t')
            shutil.move(self.embedded_coverage_values_file , os.path.abspath(self.directory))

    
    def is_tree_file_OK(self):
        if not os.path.exists(os.path.join(self.directory, self.tree_file)):
            raise FileNotFoundError(
                """You did not go through the anvio interface to create a newick
                tree format. If you did, then you probably did not name your 
                tree_file parameter the same name as '%s', which can be a 
                problem. Worst case scenario, you restart the process and look
                at the necessary documentation at INSERT_LINK to create the 
                newick tree
                """
                %(self.tree_file)
            )

    def adjusted_dataframe_and_classification(self):
        '''
        Adjusts training data so that the coverage values are clustered, 
        using anvio clustering algorithm, and the dataframe is sorted 
        Overall, this eases the process of manually inputting the data
        '''
        if self.train:
            self.is_tree_file_OK()

            self.F = AdjustClassification(
                                    tree_file=self.tree_file, 
                                    directory=self.directory,
                                    coverage_values_file=self.embedded_coverage_values_file,
                                    classified_values_file=self.classified_values_file)
            
            self.embedded_dataframe = self.F.dataframe

    def export_classifier(self):
        self.F.export_classifier(self.classified_values_file)

    def convert_data(self):
        '''
        Using the sorted data and manually classified values, this adjusts the
        embedded data before it is used to train the model
        '''
        self.adjusted_dataframe_and_classification()
        convert = lambda dataframe: dataframe.to_numpy()
        self.coverage_values = convert(self.embedded_dataframe)
        if self.classified_values_dataframe is not None:
            self.classified_values = convert(self.classified_values_dataframe)  
    
