import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mock_training_data import MockData

class Coverage:
    def __init__(self, 
                directory=os.getcwd(), 
                norm=True,
                sort=False, 
                filter=0,
                coverage_values_file='Untitled.txt',
                file_included_in_directory=False,
                index='gene_callers_id', 
                separator=',', 
                mock=False, 
                train=True,
                export_file=True,
                create_folder=False,
                folder_name='folder',
                rows=100, 
                columns=100):
        '''
        Initializes the Coverage class

        Inputs:
            directory (str): the desired directory of your data

            norm (bool): whether values within a metagenome sample should be normalized, where the 
                         norm is defined as a_i/(∑ a_j)

            sort (bool): whether the coverage values should be sorted by column

            filter (int): whether some samples should be filtered out

            coverage_values_file (str): the heart of the file that stores all the necessary data including
            the dataset's coverage values. If mock is True, then this variable is
            just a placeholder for the mock data's file name. 

            file_included_in_directory (bool): whether the directory includes the name of your coverage_values_file
                                               If so, then the Coverage class will parse the string.
                                 
            index (str): the preferred column name to index the dataset

            separator (str): the separator when reading the Pandas Dataframe. If mock is True, then
                             the exported mock data files are already tab-separated, Otherwise,
                             if mock is False, it's important you input the format of your files

            train (bool): whether the inputted data is training data. If so, it should contain
                          the classified values for each gene.
            
            export_file (bool): whether the cleaned up dataframe should be exported into your inputted
                                directory for Anvi'o. If both export_file and create_folder is False,
                                in addition to mock being set to False, then you most likely only need 
                                the dataframe so these files will be deleted.
            
            folder_name (str): the name of the folder for which to place your mock data. If mock is False,
                               then this variable would not be used.
            
            rows, columns (int): the number of rows and columns for the mock data. If mock is False,
                               then these variables would not be used.


        '''

        if mock:
            self.separator = separator
            _directory, _coverage, _classified = self.create_mock_data(
                            train=train, 
                            directory=directory, 
                            rows=rows, 
                            columns=columns, 
                            create_folder=create_folder, 
                            folder_name=folder_name, 
                            index=index,
                            file_included_in_directory=file_included_in_directory,
                            coverage_values_file=coverage_values_file
                        )

            self.directory = _directory
            self.coverage_values_file = _coverage
            self.classified_values_file = _classified
            
        else:
            self.separator = separator
            self.directory, self.coverage_values_file = self.parse_directory(
                        directory=directory, 
                        file_included_in_directory=file_included_in_directory, 
                        coverage_values_file=coverage_values_file
                    )
            
        self.dataframe = self.load_dataframe(
                            norm=norm,
                            sort=sort,
                            index=index,
                            create_folder=create_folder,
                            export_file=export_file,
                            file_included_in_directory=file_included_in_directory,
                            mock=mock
                        )

        if filter > 0:
            self.dataframe = self.filter_samples(filter)

        self.coverage_values, self.classified_values = self.extract_values(train)
        self.export(export_file=export_file, train=train)
    
    def parse_directory(self, directory, coverage_values_file, 
                    file_included_in_directory):
        '''
        Parses directory and extracts the file path and file
        '''

        if file_included_in_directory:
            _file = os.path.split(directory)[-1]
            _directory = os.path.split(directory)[-2]
        else:
            _file = coverage_values_file
            _directory = directory

        return _directory, _file


    def delete_files(self, create_folder, export_file):
        '''
        Deletes the text files containing all the data so that self.dataframe
        can be read, as opposed to storing any superfluous data files. This 
        is particularly helpful when inputting the dataframe into a manifold
        learning algorithm
        '''
        D = lambda string: os.path.join(self.directory, string)
        coverage_file_path = D(self.coverage_values_file)
        classified_values_file_path = D(self.classified_values_file)

        #makes sure files are in the path so they can be deleted
        if not os.path.exists(classified_values_file_path):
            raise Exception(
                """It appears that the file '%s' that stores each gene's 
                classified values for your dataset is not in your directory '%s'
                """ %(self.classified_values_file, self.directory)
                )
        
        if not os.path.exists(coverage_file_path):
            raise Exception(
                """It appears that the file '%s' that stores your dataset's 
                coverage values is not in your directory '%s'
                """ %(self.coverage_values_file, self.directory)
                )

        if not create_folder and not export_file:
            os.remove(classified_values_file_path)
            os.remove(coverage_file_path)
            print(
                "Your files '%s' and '%s' were deleted successfully" 
                %(self.coverage_values_file, self.classified_values_file)
            )


    def load_dataframe(self, norm, sort,  index, create_folder, export_file,
                       file_included_in_directory, mock=False):
        '''
        Loads the dataframe and includes coverage values of genes within samples
        Inputs:
            index (str): the preferred column that indexes the dataframe
        '''
        # refactors the joined path into a nice lambda function
        D = lambda string: os.path.join(self.directory, string)
        # checks if the inputted directory contains a file
        path = D(self.coverage_values_file)
        df = pd.read_csv(
                r"" + path, sep=self.separator, engine='python'
            )
        df = df.set_index(index)
        if norm:
            df = df/df.sum()
        if sort:
            df = df.sort_values(by=list(df.columns), axis=0)
        # deletes generated files if user only wants to extract the dataframe
        if mock:
            self.delete_files(create_folder, export_file)
        return df
    

    def filter_samples(self, filter=0):
        '''
        Filters samples in a pandas dataframe based on filter value

        Input:
            filter (float): preferred filter value
            output (bool): whether the filtered dataframe should be outputted
        '''
        criteria = (self.dataframe.median() >= filter)
        return self.dataframe[criteria.index[criteria]]

    def extract_values(self, train):
        # ensures there are some classification values when loading a personal dataset

        f = lambda dataframe: dataframe.to_numpy()
        if train:
            try:
                _classified_values = f(self.dataframe['Classification'])
                _coverage_values = f(self.dataframe.drop('Classification', axis=1))
                return _coverage_values, _classified_values

            except Exception as e:
                KeyError(
                """ Unfortunately, your dataframe does not contain the necessary
                dataframe column '%s.' Since this is your training data, you
                need to redefine your column that contains the classified
                values to the column '%s'. Otherwise, your dataframe won't be
                classified. """ %(e, e)
            )

        else:
            _classified_values = 0
            _coverage_values = f(self.dataframe)
            if _coverage_values == None:
                print("Fix 1")
            elif _classified_values == None:
                print("Fix 2")
            else:
                print("Try the other")
            return _coverage_values, _classified_values


    def create_mock_data(self, train, directory, rows, columns, coverage_values_file, 
                        create_folder, folder_name, index, file_included_in_directory):
        
        _directory, _ = self.parse_directory(
                        directory=directory, 
                        file_included_in_directory=file_included_in_directory, 
                        coverage_values_file=coverage_values_file
                    )

        if not train:
                raise Exception(
                """It appears that you meant to generate mock data with the 
                purpose of testing it against the algorithm. Unfortunately, 
                the mock data was created with the intention of training the
                algorithm, not to test it whatsoever"""
                ) 

        else:
            F = MockData(
                directory=_directory, 
                rows=rows, 
                columns=columns, 
                create_folder=create_folder,
                folder_name=folder_name
            )
            F.generate_data(index=index)

        return F.directory, F.coverage_values_file, F.classified_values_file



    def export(self, export_file, train):
        '''
        Exports the dataframe into a tab-separated .txt file for anvi'o
        to generate a newick-tree file, which, in turn, leads to a clustered
        dendrogram

        Inputs:
            export_directory (str): desired directory

        '''
        D = lambda string: os.path.join(self.directory, string)
        # exports the dataframe
        if export_file:
            t = self.dataframe.transpose()
            t.columns = 'gene_' + t.columns.astype(str)
            df = t.transpose()
            df.to_csv(D(self.coverage_values_file), sep='\t')

        # exports the additional layer file for anvi'o
        if self.classified_values_file is not None:
            f = pd.read_csv(D(self.classified_values_file), sep='\t')
            f.to_csv(D(self.classified_values_file), sep='\t', index=False)
