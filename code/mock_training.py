import csv
import os

from os import getcwd as working_directory
from paths import FileManage
from numpy.random import uniform, choice
from values import MockValues as MV

class MockData:
    def __init__(self, folder_name='folder', directory=working_directory,  
                 rows=100, columns=100):
        '''
        Initializes the MockData class

        Inputs:
            f (str): the name of the mockdata file
            rows, columns (int): the desired number of rows and columns 

        '''
        self.rows = rows
        self.columns = columns
        self.manage = FileManage(directory=directory, folder=folder_name)
        self.file = self.manage.file_name
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
        metagenomes = [index] + ['metagenome_%d' %(i) for i in range(self.columns)] + ['Core']
        #generates the rows of randomized data 
        coverage_values = []
        for j in range(self.rows):
            gene_name = 'gene__%d' %(j)
            p = MV(self.columns)
            coverage = [gene_name] + p.values + [p.classifier]
            coverage_values.append(coverage)

        with open(self.file, 'w') as f:
            write = csv.writer(f, delimiter=',')
            # writes out the name of the columns and gene's coverage values
            write.writerow(metagenomes)
            write.writerows(coverage_values)
            
        self.manage.move_file()

   