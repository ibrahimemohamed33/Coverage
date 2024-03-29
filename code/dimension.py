import os

import numpy as np
import pandas as pd
import shutil


from coverage import Coverage, epsilon
from sklearn import manifold


valid_path_methods = ["auto", "D", "FW"]
valid_manifold_methods =  ['ISOMAP', 'LLE', 'MDS']

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
                _filter=epsilon, 
                rows=100, 
                columns=100,
                manifold_method='ISOMAP'):
        '''
        Class attempts to embed high-dimensional coverage values
        into lower dimension using the Isomap algorithm
        '''

        self.train = train
        self.directory = directory
        self.folder_name = folder_name

        self.coverage = Coverage(directory=directory,
                                norm=norm,
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

        if mock:
            self.coverage_values_file = self.coverage.coverage_values_file
        else:
            self.coverage_values_file = 'new_' + self.coverage.coverage_values_file

        self.classified_values_file = self.coverage.classified_values_file_name

        _, self.dimension = self.dataframe.shape
        self.num_components = self.projected_number_of_components()        
        self.is_path_OK(path)

        self.embedded_vectors = self.embed(n_neighbors, 
                                          path_method=path, 
                                          mock=mock,
                                          manifold_method=manifold_method,
                                          train=train)
        
        self.embed_into_dataframe()
        self.export(export_file=export_file, mock=mock)
    
    def is_path_OK(self, path):
        '''
        Raises errors for invalid inputs
        '''

        if path not in valid_path_methods:
            raise ValueError(
                """Your path method '%s' is not a valid method for the isomapping.
                What you should do instead is set your path to the keywords
                'auto' or 'D'. This will likely fix the issue
                """ 
                %(path)
            )
    def is_manifold_OK(self, manifold_method):
        if manifold_method not in valid_manifold_methods:
            raise ValueError(
                """ It appears your manifold_method '%s' is not a valid manifold
                method, please choose one from the list of valid_manifolds below:
                '%s' """
                %(manifold_method, ''.join(valid_manifold_methods))
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
    
    def extract_manifold(self, manifold_method, n_neighbors, path_method):
        self.is_manifold_OK(manifold_method)
        if manifold_method == 'LLE':
            self.embedding = manifold.LocallyLinearEmbedding(n_components=self.num_components,
                                                            n_neighbors=n_neighbors)

        elif manifold_method == 'MDS':
            self.embedding = manifold.MDS(n_components=self.num_components, 
                                          n_jobs=2,
                                          eps=epsilon)

        else:
            self.embedding = manifold.Isomap(n_neighbors=n_neighbors,
                                            n_components=self.num_components,
                                            path_method=path_method)
    

    def embed(self, n_neighbors, path_method, mock, manifold_method, train):
        '''
        Embeds d-dimensional data into n-dimensional data, where n <= d
        and n represents the number of components
        '''

        if self.num_components == self.dimension:
            return self.dataframe.to_numpy()
        
        else:
            self.inclusion_map()
            self.extract_manifold(manifold_method, n_neighbors, path_method)
            
            if mock or train:
                t = self.embedding.fit_transform(self.dataframe[:])
            else:
                fit = self.embedding.fit(self.dataframe[:])
                t = fit.transform(self.dataframe[:])

            return t
    
    def adjusted_indices(self):
        reduced_indices = [
            'gene__%d' %(i) for i in self.dataframe.index
        ]
        
        index_name = self.dataframe.index.name

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
        df = df - df.min().min()

        self.embedded_dataframe = df
    
    def export(self, export_file, mock):
        '''
        Exports the embededd dataframe into a file containing coverage values
        for manual classification
        '''
        
        # defines the new files for which the data will be written in
        J = lambda string: 'embedded' + '_' + string
        self.embedded_coverage_values_file = J(self.coverage_values_file)
        self.embedded_classified_values_file = J(self.classified_values_file)

        classified_directory = os.path.join(self.directory, self.classified_values_file)
        

        # copies content within classification values for the classification 
        # of the embedded dataframe
        shutil.copyfile(classified_directory, self.embedded_classified_values_file)

        # exports dataframe
        self.coverage_values = self.embedded_dataframe.to_numpy()

        abs_path = lambda path: os.path.abspath(self.directory)
        if export_file:
            # removes any previous copies from directory  
            if os.path.exists(os.path.join(abs_path(self.directory), self.embedded_coverage_values_file)):
                os.remove(os.path.join(abs_path(self.directory), self.embedded_coverage_values_file))

            if os.path.exists(os.path.join(abs_path(self.directory), self.embedded_classified_values_file)):
                os.remove(os.path.join(abs_path(self.directory), self.embedded_classified_values_file))

            
            # uses helper function to adjust the dataframe's columns for anvio
            df = adjust_columns(self.embedded_dataframe, mock)
            df.to_csv(self.embedded_coverage_values_file , sep='\t')

            # moves the files to the new directory
            shutil.move(self.embedded_coverage_values_file, os.path.abspath(self.directory))
            shutil.move(self.embedded_classified_values_file, os.path.abspath(self.directory))