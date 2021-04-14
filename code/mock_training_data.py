import csv
import os
import pandas as pd

from files import FileManage
from generate_mock_values import MockValues


class MockData:
    def __init__(self,
                 folder_name='folder', 
                 directory=os.getcwd(),  
                 create_folder=False, 
                 rows=100, 
                 columns=100):
        '''
        Initializes the MockData class

        Inputs:
            f (str): the name of the mockdata file
            rows, columns (int): the desired number of rows and columns 

        '''
        self.rows = rows
        self.columns = columns
        self.create_folder = create_folder

        self.manage = FileManage(destination=directory, 
                                 is_create_folder=create_folder,
                                 folder=folder_name)

        self.file = self.manage.file_name
        self.additional_layer_file = self.manage.additional_layer
        self.directory = self.manage.path

    
    def generate_data(self, index='gene_callers_id'):
        '''
        Creates a csv file and uses the helper functions to input the data and
        export it into the desired path

        Inputs:
            directory (str): directory path
            folderName (str): preferred name for folder
            index (str): preferred index
        '''
        #creates the column names
        layers = [index] + ['Core']
        metagenomes = [index] + ['metagenome_%d' %(i) for i in range(self.columns)] 

        coverage_values = []
        additional_layers = []
        #generates the rows of randomized data 
        for j in range(self.rows):
            gene_name = 'gene__%d' %(j)
            # creates the list of randomized data
            p = MockValues(self.columns)
            coverage_values.append([gene_name] + p.values)
            # stores the classified variable alongside the gene's
            additional_layers.append([gene_name] + [p.classifier])

        with open(self.file, 'w') as f:
            write = csv.writer(f, delimiter=',')
            # writes out the name of the columns and gene's coverage values
            write.writerow(metagenomes)
            write.writerows(coverage_values)
        
        # writes additional layer file for anvi'o
        with open(self.additional_layer_file, 'w') as f:
            write = csv.writer(f, delimiter='\t')
            write.writerow(layers)
            write.writerows(additional_layers)

        self.manage.move_file()

    

   