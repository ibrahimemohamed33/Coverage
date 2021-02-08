import os
import shutil
import csv
import numpy as np
from random import randint, uniform 


def _export(file, directory=None, folderName='folder'):
    '''
    Helper function that moves one file to a new folder named 'folder' and puts
    the associated training data there. 
    Inputs:
        file (str): name of file
        directory (str): directory path
        folderName (str): preferred name for folder
    '''

    if not directory:
        directory = os.getcwd()
    newPath = os.path.join(directory, folderName)
    if not os.path.isdir(newPath):
        os.mkdir(newPath)

    shutil.move(file, newPath)

def _rows_and_columns(rows=1, columns=1):
    '''
    Helper function that creates the columns of the training data and then 
    uses numpy's random, uniform distribution to calculate the coverage values
    for a dummy gene. 

    Inputs: 
        rows, columns (int): the desired number of rows and columns
    '''

    metagenomes = ['metagenome_%d' %(i) for i in range(columns)]
    # Separates the columns into a readable .csv file
    metagenomes.insert(0, None)

    # List of lists that contain each gene's associated coverage value 
    coverage_values = []
    for j in range(rows):
        gene_name = 'gene__%d' %(j)
        coverage = list(np.random.uniform(0,1,columns))
        coverage.insert(0, gene_name)
        coverage_values.append(coverage)
    
    return metagenomes, coverage_values

def generate_data(rows=1, columns=1, file='untitled.csv', directory=None, 
                  folderName='folder'):

    '''
    Creates a csv file and uses the helper functions to input the data and
    export it into the desired path

    Inputs:
        rows, columns (int): the desired number of rows and columns
        file (str): name of file
        directory (str): directory path
        folderName (str): preferred name for folder
    Outputs:
        data (csv file): a csv file that contains mock data of a gene's coverage
                        values
    '''

    metagenomes, coverage_values = _rows_and_columns(rows, columns)
    with open(file, 'w', ) as f:
        write = csv.writer(f, delimiter=',')
        # writes out the name of the columns and the gene's coverage values
        write.writerow(metagenomes)
        write.writerows(coverage_values)

    _export(file, directory, folderName)
  