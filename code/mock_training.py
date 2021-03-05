import csv
import random

from os import getcwd as working_directory
from paths import FileManage
from numpy.random import uniform, choice

class MockData:
    def __init__(self, f='Untitled.csv', folder_name='folder', 
                directory=working_directory, rows=100, columns=100):
        '''
        Initializes the MockData class

        Inputs:
            f (str): the name of the mockdata file
            rows, columns (int): the desired number of rows and columns 

        '''
        self.rows = rows
        self.columns = columns
        self.manage = FileManage(directory=directory, folder=folder_name, 
                                 file_name=f)
        self.file = self.manage.file_name
    
    def interval_generator(self):
        classifiers = ['Core', 'Accessory', 'Absent', 'Non-Specific']
        # Currently incomplete but uses Evan K.'s classification in one specific
        # sample. From there, I decided to evenly divide the distribution between 
        # the rest of the remaining classifiers
        probabilities = [0.54, .154, .153, .153]
        alpha = choice(classifiers, 1, p=probabilities)

        if alpha == 'Core':
            interval = (0.6, 1.0)
        elif alpha == 'Accessory':
            interval = (0.2, 0.6)
        elif alpha == 'Absent':
            interval = (0.0, 0.2)
        else:
            interval = (0.0, 1.0)

        return interval
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
        metagenomes = ['metagenome_%d' %(i) for i in range(self.columns)]
        metagenomes.insert(0, index)
        #generates the rows of randomized data 
        coverage_values = []
        for j in range(self.rows):
            gene_name = 'gene__%d' %(j)
            a, b = self.interval_generator()
            coverage = list(uniform(a, b, self.columns))
            coverage.insert(0, gene_name)
            coverage_values.append(coverage)

        with open(self.file, 'w') as f:
            write = csv.writer(f, delimiter=',')
            # writes out the name of the columns and gene's coverage values
            write.writerow(metagenomes)
            write.writerows(coverage_values)

        self.manage.move_file()

   