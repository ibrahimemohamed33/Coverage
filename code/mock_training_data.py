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
        self.working_directory = directory

        self.manage = FileManage(
            destination=directory, 
            create_folder=create_folder,
            folder=folder_name
            )

        self.coverage_values_file = self.manage.coverage_values_file_name
        # self.classified_values_file = self.manage.classified_values_file_name
        self.directory = self.manage.path
        self.generate_data()


    def generate_data(self, index='gene_callers_id'):
        '''
        Creates a csv file and uses the helper functions to input the data and
        export it into the desired path

        Inputs:
            directory (str): directory path
            folderName (str): preferred name for folder
            index (str): preferred index
        '''
        os.chdir(self.directory)
        #creates the column names
        classification_label = ['Classification']
        
        metagenome_labels = [index] + [
            'metagenome_%d' %(i) for i in range(self.columns)
        ] + classification_label

        coverage_values = []
        #generates the rows of randomized data 
        for j in range(self.rows):
            gene_name = 'gene__%d' %(j)
            # creates the list of randomized data
            p = MockValues(self.columns)
            coverage_values.append([gene_name] + p.values + [p.classifier])

        # writes out column's name in addition to the gene's coverage values
        with open(self.coverage_values_file, 'w') as f:
            write = csv.writer(f, delimiter=',')
            write.writerow(metagenome_labels)
            write.writerows(coverage_values)
