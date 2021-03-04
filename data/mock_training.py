import os
import csv
import random

from numpy.random import uniform
from shutil import move 

class MockData:
    def __init__(self, f='Untitled.csv', rows=100, columns=100):
        '''
        Initializes the MockData class

        Inputs:
            f (str): the name of the mockdata file
            rows, columns (int): the desired number of rows and columns 

        '''
        self.file = f
        self.rows = rows
        self.columns = columns


    def _export(self, directory=None, folder_name='folder'):
        '''
        Helper function that moves one file to folder_name and puts
        the associated training data there. 
        Inputs:
            directory (str): directory path
            folderName (str): preferred name for folder
        '''
        if directory is None:
            directory = os.getcwd()
        new_path = os.path.join(os.path.normpath(directory), folder_name)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        move(self.file, new_path)


    def generate_data(self, directory=None, index= 'gene_callers_id', 
                      folder_name='folder'):
        '''
        Creates a csv file and uses the helper functions to input the data and
        export it into the desired path

        Inputs:
            directory (str): directory path
            folderName (str): preferred name for folder
            index (str): preferred index
        '''
        #creates the column names
        metagenomes = ['metagenome_%d' %(i) for i in range(self.columns)]
        metagenomes.insert(0, index)
        #generates the rows of randomized data 
        coverage_values = []
        for j in range(self.rows):
            gene_name = 'gene__%d' %(j)
            coverage = list(uniform(0, 1, self.columns))
            coverage.insert(0, gene_name)
            coverage_values.append(coverage)

        with open(self.file, 'w', ) as f:
            write = csv.writer(f, delimiter=',')
            # writes out the name of the columns and gene's coverage values
            write.writerow(metagenomes)
            write.writerows(coverage_values)

        self._export(directory, folder_name)

   